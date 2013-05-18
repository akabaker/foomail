from email.utils import parseaddr
from imapclient import IMAPClient
import email
import time
import json
import os
import re

def login(host, username, password):
    """Login to imap server and return client IMAPClient instance"""

    client = IMAPClient(host, use_uid=True, ssl=True)
    client.login(username, password)
    return client

def get_messages(client, folder, flags):
    """
    Select a folder in the user's mailbox to search, returning messages list
    that match flags.

    Keyword arguments:
    client -- IMAPClient instance
    folder -- Folder to search for messages (default folder)
    
    Returns:
    messages -- List of messages matching flags

    """

    select_info = client.select_folder(folder)

    # Message filter
    messages = client.search(flags)
    if len(messages) == 0:
        raise ValueError
    else:
        return messages

def find_messages(client, messages, regex):
    """
    Return messages that are unanswered, excluding threads that are responded
    to by the sender.

    Keyword arguments:
    client -- IMAPClient instance
    messages -- list of messages

    """

    # BODY.PEEK doesn't set SEEN flag (keeps messages unread)
    response = client.fetch(messages, ['BODY.PEEK[]'])
    results = {'count': 0}

    for msgid, data in response.iteritems():
        msg = email.message_from_string(data['BODY[]'])
        from_user = parseaddr(msg['from'])
        
        # Responses that include the sender will always have the UNANSWERED flag (it seems).
        # This check will keep replied messages that included the sender from being reported
        # as unanswered.
        match = regex.findall(msg['from'])
        if match:
            pass
        else:
            results[msgid] = {
                'from': from_user, 
                'date': msg['Date'], 
                'subject': msg['subject']
            }
            results['count'] += 1

    return results
    client.logout()

def main():
    host = os.environ['IMAP_HOST']
    username = os.environ['IMAP_USERNAME']
    password = os.environ['IMAP_PASSWORD']
    name_regex = re.compile(r'%s' % username, re.IGNORECASE)
    today = time.strftime('%d-%B-%Y', time.gmtime())
    flags = ['SINCE %s UNANSWERED' % today]
    folder = 'INBOX'

    client = login(host, username, password)
    try:
        messages = get_messages(client, folder, flags)
        results = find_messages(client, messages, name_regex)
        print json.dumps(results, sort_keys=True, indent=4)
    except ValueError:
        print 'No messages match %s' % flags

if __name__ == '__main__':
    main()
