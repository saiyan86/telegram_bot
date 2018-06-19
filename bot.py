import telegram
import telegram.ext
import logging
from telegram.ext import MessageHandler, Filters

TOKEN = "554910904:AAG7PsCUMMQ_RCf983C5fdN__gGwgQGujnc"

CMD_START_FLAG = "start"
CMD_RULE_FLAG = "rule"

class CmdHandler():
    def __init__(self):
        self.init_cmd_start_handler()
        self.init_cmd_rule_handler()
        
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
        
    def init_photo_handler(self):
        self.photo_handler = MessageHandler(
            Filters.photo,
           self.msg_photo
        )

    def get_photo_handler(self):
        return self.photo_handler
    
    def msg_photo(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="This is a photo!")

    def init_video_handler(self):
        self.video_handler = MessageHandler(
            Filters.video,
           self.msg_video
        )

    def get_video_handler(self):
        return self.video_handler
    
    def msg_video(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="This is a video!")  

    def init_doc_handler(self):
        self.doc_handler = MessageHandler(
            Filters.document,
           self.msg_doc
        )

    def get_doc_handler(self):
        return self.doc_handler
    
    def msg_doc(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="This is a document!")

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

    msg_handler = MsgHandler()
    dispatcher.add_handler(msg_handler.get_url_handler())
    dispatcher.add_handler(msg_handler.get_photo_handler())
    
    updater.start_polling()
    
if __name__ == "__main__":
    main()
