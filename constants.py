#text
WELCOME_MESSAGE = 'HELLO FRIENDS!!! :)'
WELCOME_GROUP = 'WELCOME {}'
WELCOME_USER = 'WELCOME {}'

CMD_LIST = '/hello'
UNRECOGNISED_COMMAND = '#hack'

#log
LOG_SENT = '{} {} sent to uid {} ({})'
LOG_ENQUEUED = 'Enqueued {} to uid {} ({})'
LOG_DID_NOT_SEND = 'Did not send {} to uid {} ({}): {}'
LOG_ERROR_SENDING = 'Error sending {} to uid {} ({}):\n{}'
LOG_ERROR_DAILY = 'Error enqueueing dailies:\n'
LOG_ERROR_QUERY = 'Error querying uid {} ({}): {}'
LOG_TYPE_FEEDBACK = 'Type: Feedback\n'
LOG_TYPE_START_NEW = 'Type: Start (new user)'
LOG_TYPE_START_EXISTING = 'Type: Start (existing user)'
LOG_TYPE_NON_TEXT = 'Type: Non-text'
LOG_TYPE_NON_MESSAGE = 'Type: Non-message'
LOG_TYPE_COMMAND = 'Type: Command\n'
LOG_UNRECOGNISED = 'Unrecognised command'
LOG_USER_MIGRATED = 'User {} migrated to uid {} ({})'
LOG_USER_DELETED = 'Deleted uid {} ({})'
LOG_USER_REACHABLE = 'Uid {} ({}) is still reachable'
LOG_USER_UNREACHABLE = 'Unable to reach uid {} ({}): {}'

RECOGNISED_ERROR_PARSE = 'Bad Request: Can\'t parse message text'
RECOGNISED_ERROR_MIGRATE = 'Bad Request: group chat is migrated to a supergroup chat'
RECOGNISED_ERRORS = ('PEER_ID_INVALID',
                     'Bot was blocked by the user',
                     'Forbidden: user is deleted',
                     'Forbidden: user is deactivated',
                     'Forbidden: bot was kicked from the group chat',
                     'Forbidden: bot was kicked from the channel chat',
                     'Forbidden: bot was kicked from the supergroup chat',
                     'Forbidden: bot is not a member of the supergroup chat',
                     'Bad Request: chat not found',
                     'Bad Request: group chat was deactivated',
                     RECOGNISED_ERROR_MIGRATE)
#Config
DEFAULT_VERSION = 'ESV'