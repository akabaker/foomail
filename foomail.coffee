# Description
#   <description of the scripts functionality>
#
# Dependencies:
#   "<module name>": "<module version>"
#
# Configuration:
#   LIST_OF_ENV_VARS_TO_SET
#
# Commands:
#   hubot <trigger> - <what the respond trigger does>
#   <trigger> - <what the hear trigger does>
#
# Notes:
#   <optional notes required for the script>
#
# Author:
#   <github username of the original script author>

module.exports = (robot) ->
    robot.respond /foomail/i, (msg) ->
        msg.http("http://localhost:5000/")
            .get() (err, res, body) ->
                try
                    json = JSON.parse body
                    msg.send "There are #{json.count} unanswered messages."
                    for message in json.messages
                        msg.send "Subject: #{message.subject}\n
                                  From: #{message.from}\n
                                  Date: #{message.date}\n"
                catch error
                    msg.send "No unanswered messages or messages not found"
