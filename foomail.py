from imapclient import IMAPClient
from email.utils import parseaddr
import time
import email
import re
import os

host = os.environ['IMAP_HOST']
username = os.environ['IMAP_USERNAME']
password = os.environ['IMAP_PASSWORD']
name_regex = re.compile(r'%s' % username, re.IGNORECASE)
today = time.strftime('%d-%B-%Y', time.gmtime())
flags = ['SINCE %s UNANSWERED' % today]
ssl = True

client = IMAPClient(host, use_uid=True, ssl=ssl)
client.login(username, password)

# Select from inbox
select_info = client.select_folder('INBOX')

# Message filter
messages = client.search(flags)

# BODY.PEEK doesn't set SEEN flag (keeps messages unread)
response = client.fetch(messages, ['BODY.PEEK[]'])
for msgid, data in response.iteritems():
    msg = email.message_from_string(data['BODY[]'])
    from_user = parseaddr(msg['from'])
    
    # Responses that include the sender will always have the UNANSWERED flag (it seems).
    # This check will keep replied messages that included the sender from being reported
    # as unanswered.
    match = name_regex.findall(msg['from'])
    if match:
        pass
    else:
        print "Message from %s sent on %s is unanswered!" % (from_user, msg['Date'])

client.logout()
