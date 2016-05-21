import Skype4Py
import schedule
from datetime import datetime, timedelta, time


class CodeTimeBot(object):

    def __init__(self):
        self.skype = Skype4Py.Skype(Events=self)
        self.skype.Attach()
        self.missed_chats = []
        self.code_time_reply = "Auto-responder: I am coding until 2pm and trying not to be disturbed. I will check Skype then. " \
                               "If urgent *and* important -- use your judgement and escalate to my mobile."

    def update_missed_chats(self):
        for chat in self.skype.RecentChats:
            if chat.Type is Skype4Py.chatTypeDialog \
                    and (datetime.now() - chat.ActivityDatetime) < timedelta(1) and chat not in self.missed_chats:
                self.missed_chats.append(chat)
                self.skype.SendMessage(chat.DialogPartner, self.code_time_reply)

    def get_missed_chats(self):
        return self.missed_chats


def code_time():
    bot = CodeTimeBot()
    is_code_time = True

    while is_code_time:
        bot.update_missed_chats()
        time.sleep(1.0)
        now = datetime.now()
        if now.time() > time(13, 00):
            is_code_time = False

if __name__ == "__main__":
    schedule.every().wednesday.at("9:00").do(code_time)
    schedule.every().friday.at("9:00").do(code_time)
