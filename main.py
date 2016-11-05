import webapp2
from google.appengine.ext import db
from telegramcore import *

from models import User
from constants import *
from shadow import TOKEN, ADMIN_ID, BOT_ID

def get_user(uid):
    key = db.Key.from_path('User', str(uid))
    user = db.get(key)
    if user == None:
        user = User(key_name=str(uid), first_name='-')
        user.put()
    return user

def user_exists(uid):
    key = db.Key.from_path('User', str(uid))
    user = db.get(key)
    return user != None

def update_profile(uid, uname, fname, lname):
    existing_user = get_user(uid)
    if existing_user:
        existing_user.username = uname
        existing_user.first_name = fname
        existing_user.last_name = lname
        existing_user.update_last_received()
        #existing_user.put()
        return existing_user
    else:
        user = User(key_name=str(uid), username=uname, first_name=fname, last_name=lname)
        user.put()
        return user

class BibleCoachPage(webapp2.RequestHandler):
    def handle_message(self, msg):
        msg_chat = msg.get('chat')
        msg_from = msg.get('from')
        mid = msg.get("message_id")
        actual_group_name = ""

        if msg_chat.get('type') == 'private':
            uid = msg_from.get('id')
            first_name = msg_from.get('first_name')
            last_name = msg_from.get('last_name')
            username = msg_from.get('username')
        else:
            uid = msg_chat.get('id')
            first_name = msg_chat.get('title')
            last_name = None
            username = None
            actual_group_name = msg_chat.get('title').encode('utf-8', 'ignore').strip()

        user = update_profile(uid, uname=username, fname=first_name, lname=last_name)

        actual_id = msg_from.get('id')
        name = first_name.encode('utf-8', 'ignore').strip()
        actual_username = msg_from.get('username')
        if actual_username:
            actual_username = actual_username.encode('utf-8', 'ignore').strip()
        actual_name = msg_from.get('first_name').encode('utf-8', 'ignore').strip()
        actual_last_name = msg_from.get('last_name')
        if actual_last_name:
            actual_last_name = actual_last_name.encode('utf-8', 'ignore').strip()
        text = msg.get('text')

        if text:
            text = text.encode('utf-8', 'ignore')

        def get_from_string():
            name_string = actual_name
            if actual_last_name:
                name_string += ' ' + actual_last_name
            if actual_username:
                name_string += ' @' + actual_username
            return name_string

        msg_reply = msg.get('reply_to_message')
        logging.debug("msg reply: {}".format(msg_reply))

        if msg_reply and str(msg_reply.get('from').get('id')) == str(BOT_ID):
            #if hes replying to our message
            return

        if user.last_sent is None or text == '/start':
            if user.last_sent is None:
                logging.info(LOG_TYPE_START_NEW)
                new_user = True
            else:
                logging.info(LOG_TYPE_START_EXISTING)
                new_user = False

            if user.is_group():
                response = WELCOME_GROUP.format(name)
            else:
                response = WELCOME_USER.format(name)

            send_message(user, response)

            send_typing(uid)
            response = WELCOME_MESSAGE

            send_message(user, response, markdown=True, disable_web_page_preview=True)

            if new_user:
                if user.is_group():
                    new_alert = 'New group: "{}" via user: {}'.format(name, get_from_string())
                else:
                    new_alert = 'New user: ' + get_from_string()
                send_message(ADMIN_ID, new_alert)

            return

        logging.info(LOG_TYPE_COMMAND + text)

        cmd = text.lower().strip()
        short_cmd = ''.join(cmd.split())

        def is_command_equals(word):
            flexi_pattern = ('/{}@biblecoachbot'.format(word), '@@biblecoachbot/{}'.format(word))
            return cmd == '/' + word or short_cmd.startswith(flexi_pattern)

        if is_command_equals('hello'):
            send_typing(uid)
            response = WELCOME_MESSAGE
            send_message(user, response, markdown=True, disable_web_page_preview=True)

        elif is_command_equals('help'):
            response = "help meee"

            send_message(user, response, disable_web_page_preview=True)

        else:
            logging.info(LOG_UNRECOGNISED)
            if user.is_group() and '@@biblecoachbot' not in cmd:
                return

            response = UNRECOGNISED_COMMAND.format(actual_name)
            send_message(user, response)

    def handle_inline_query(self, inline_query):
        return

    def handle_callback_query(self, callback_query):
        qid = callback_query.get('id')
        data = callback_query.get('data')

        from_user = callback_query.get('from')
        chat = callback_query.get("message").get("chat")

        if chat.get('type') == 'private':
            uid = str(from_user.get('id'))
            first_name = from_user.get('first_name')
            last_name = from_user.get('last_name')
            username = from_user.get('username')
            actual_name =first_name.encode('utf-8', 'ignore').strip()
        else:
            uid = str(chat.get('id'))
            first_name = chat.get('title')
            last_name = None
            username = None
            actual_name = from_user.get('first_name').encode('utf-8', 'ignore').strip()

        user = update_profile(uid, fname=first_name, lname=last_name, uname=username)
        imid = callback_query.get('inline_message_id')

        if not imid:
            chat_id = callback_query.get('message').get('chat').get('id')
            mid = callback_query.get('message').get('message_id')
        else:
            raise Exception("Callback message was too long and was not logged.")

        return

    def answer_callback_query(self, qid, status):
        payload = {'method': 'answerCallbackQuery', 'callback_query_id': qid, 'text': status}
        output = json.dumps(payload)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(output)
        logging.info('Answered callback query!')
        logging.debug(output)

    def post(self):
        data = json.loads(self.request.body)
        logging.debug(self.request.body)

        if data.get('message'):
            logging.info('Processing incoming message')
            self.handle_message(data.get('message'))
        elif data.get('callback_query'):
            logging.info('Processing incoming callback query')
            self.handle_callback_query(data.get('callback_query'))
        elif data.inline_query:
            logging.info('Processing incoming inline query')
            self.handle_inline_query(data.inline_query)

        else:
            logging.info(LOG_TYPE_NON_MESSAGE)
            return

class MessagePage(webapp2.RequestHandler):
    def post(self):
        params = json.loads(self.request.body)
        msg_type = params.get('msg_type')
        data = params.get('data')
        uid = str(json.loads(data).get('chat_id'))
        user = get_user(uid)

        try:
            result = telegram_post(data, 4)
        except urlfetch_errors.Error as e:
            logging.warning(LOG_ERROR_SENDING.format(msg_type, uid, user.get_description(), str(e)))
            logging.debug(data)
            self.abort(502)

        response = json.loads(result.content)

        if handle_response(response, user, uid, msg_type) == False:
            logging.debug(data)
            self.abort(502)

class DefaultPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('#Hack - Bible coaching bot running in the background :)')

app = webapp2.WSGIApplication([
    ('/', DefaultPage),
    ('/bot' + TOKEN, BibleCoachPage),
    ('/message', MessagePage)
], debug=True)
