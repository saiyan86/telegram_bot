import time
import telegram
import telegram.ext
import logging
from telegram.ext import MessageHandler, Filters
from threading import Thread, Lock

TOKEN = "554910904:AAG7PsCUMMQ_RCf983C5fdN__gGwgQGujnc"

CMD_START_FLAG = "start"
CMD_RULE_FLAG = "rule"

CMD_CLEAN_URL_FLAG = "cleanurl"
CMD_CLEAN_NONTEXT_FLAG = "cleannontext"

# Message queues can hold up to 1000 messages
MSG_QUEUE_LIMIT = 1000

msg_url_queue = []
mutex_msg_url_queue = Lock()

msg_photo_queue = []
mutex_msg_photo_queue = Lock()

msg_video_queue = []
mutex_msg_video_queue = Lock()

msg_doc_queue = []
mutex_msg_doc_queue = Lock()

class CmdHandler():
    def __init__(self):
        self.init_cmd_start_handler()
        self.init_cmd_rule_handler()
        self.init_cmd_clean_url_handler()
        self.init_cmd_clean_nontext_handler()
        
    def init_cmd_start_handler(self):
        self.cmd_start_handler = telegram.ext.CommandHandler(CMD_START_FLAG, self.cmd_start)

    def get_cmd_start_handler(self):
        return self.cmd_start_handler
    
    def cmd_start(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

    def init_cmd_rule_handler(self):
        self.cmd_rule_handler = telegram.ext.CommandHandler(CMD_RULE_FLAG, self.cmd_rule)

    def get_cmd_rule_handler(self):
        return self.cmd_rule_handler
        
    def cmd_rule(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Rule: 1.xxx 2.xxx 3.xxx")

    def init_cmd_clean_url_handler(self):
        self.cmd_clean_url_handler = telegram.ext.CommandHandler(CMD_CLEAN_URL_FLAG, self.cmd_clean_url)

    def get_cmd_clean_url_handler(self):
        return self.cmd_clean_url_handler
    
    def cmd_clean_url(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Cleaning all URLs.")

        with mutex_msg_url_queue:
            while len(msg_url_queue) > 0:
                try:
                    msg_url = msg_url_queue.pop(0)
                    bot.delete_message(
                        chat_id=msg_url.chat_id,
                        message_id=msg_url.message_id,
                        timeout=None
                    )
                except telegram.TelegramError:
                    print telegram.TelegramError

        bot.send_message(chat_id=update.message.chat_id, text="URLs cleaned.")

    def init_cmd_clean_nontext_handler(self):
        self.cmd_clean_nontext_handler = telegram.ext.CommandHandler(CMD_CLEAN_NONTEXT_FLAG, self.cmd_clean_nontext)

    def get_cmd_clean_nontext_handler(self):
        return self.cmd_clean_nontext_handler
    
    def cmd_clean_nontext(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Cleaning non-text messages.")

        with mutex_msg_photo_queue:
            while len(msg_photo_queue) > 0:
                try:
                    msg_photo = msg_photo_queue.pop(0)
                    bot.delete_message(
                        chat_id=msg_photo.chat_id,
                        message_id=msg_photo.message_id,
                        timeout=None
                    )
                except telegram.TelegramError:
                    print telegram.TelegramError

        with mutex_msg_video_queue:
            while len(msg_video_queue) > 0:
                try:
                    msg_video = msg_video_queue.pop(0)
                    bot.delete_message(
                        chat_id=msg_video.chat_id,
                        message_id=msg_video.message_id,
                        timeout=None
                    )
                except telegram.TelegramError:
                    print telegram.TelegramError

        with mutex_msg_doc_queue:
            while len(msg_doc_queue) > 0:
                try:
                    msg_doc = msg_doc_queue.pop(0)
                    bot.delete_message(
                        chat_id=msg_doc.chat_id,
                        message_id=msg_doc.message_id,
                        timeout=None
                    )
                except telegram.TelegramError:
                    print telegram.TelegramError

        bot.send_message(chat_id=update.message.chat_id, text="Non-text cleaned.")

class MsgHandler():
    def __init__(self):
        self.init_url_handler()
        self.init_photo_handler()
        self.init_video_handler()
        self.init_doc_handler()
        self.init_all_special_handler()

    def init_url_handler(self):
        self.url_handler = MessageHandler(
            (Filters.text &
             (Filters.entity(telegram.MessageEntity.URL) |
              (Filters.entity(telegram.MessageEntity.TEXT_LINK)))),
            self.msg_url
        )

    def get_url_handler(self):
        return self.url_handler

    def msg_url(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="This is an URL!")

        with mutex_msg_url_queue:
            msg_url_queue.append(update.message)

    def init_photo_handler(self):
        self.photo_handler = MessageHandler(
            Filters.photo,
           self.msg_photo
        )

    def get_photo_handler(self):
        return self.photo_handler
    
    def msg_photo(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="This is a photo!")

        with mutex_msg_photo_queue:
            msg_photo_queue.append(update.message)

    def init_video_handler(self):
        self.video_handler = MessageHandler(
            Filters.video,
           self.msg_video
        )

    def get_video_handler(self):
        return self.video_handler
    
    def msg_video(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="This is a video!")  

        with mutex_msg_video_queue:
            msg_video_queue.append(update.message)

    def init_doc_handler(self):
        self.doc_handler = MessageHandler(
            Filters.document,
           self.msg_doc
        )

    def get_doc_handler(self):
        return self.doc_handler
    
    def msg_doc(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="This is a document!")

        with mutex_msg_doc_queue:
            msg_doc_queue.append(update.message)

    # Handler for all messages expect for normal text.
    def init_all_special_handler(self):
        self.all_special_handler = MessageHandler(
            Filters.video |
            Filters.photo |
            Filters.document |
            (Filters.text &
            (Filters.entity(telegram.MessageEntity.URL) |
            (Filters.entity(telegram.MessageEntity.TEXT_LINK)))),
            self.msg_all_special
        )

    def get_all_special_handler(self):
        return self.all_special_handler

    def msg_all_special(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="This is a special message! Not normal text!")        
    
def main():
    updater = telegram.ext.Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    cmd_handler = CmdHandler()
    dispatcher.add_handler(cmd_handler.get_cmd_start_handler())
    dispatcher.add_handler(cmd_handler.get_cmd_rule_handler())
    dispatcher.add_handler(cmd_handler.get_cmd_clean_url_handler())
    dispatcher.add_handler(cmd_handler.get_cmd_clean_nontext_handler())

    msg_handler = MsgHandler()
    dispatcher.add_handler(msg_handler.get_url_handler())
    dispatcher.add_handler(msg_handler.get_photo_handler())
    
    updater.start_polling()
    
if __name__ == "__main__":
    main()
