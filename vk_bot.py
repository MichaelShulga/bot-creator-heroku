import random
import threading

from apscheduler.schedulers.background import BackgroundScheduler
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


class VkGroupInitial:
    def __init__(self, group_id, token):
        # initialization
        self.id = group_id
        self.token = token
        self.vk_session = VkApi(token=token)


class VkGroupMethods(VkGroupInitial):
    def send_message(self, to_id, message):
        vk = self.vk_session.get_api()
        vk.messages.send(user_id=to_id,
                         message=message,
                         random_id=random.randint(0, 2 ** 64))


class VkGroupEventsHandler(VkGroupInitial):
    def if_new_message(self, message, from_id, event):
        pass

    def own_handler(self, event):
        pass


class VkGroupScheduler(VkGroupInitial):
    scheduler = BackgroundScheduler()

    def activate_scheduler(self):
        pass

    def shutdown_scheduler(self):
        self.scheduler.shutdown()
        self.scheduler = BackgroundScheduler()

    def pause_scheduler(self):
        self.scheduler.pause()

    def resume_scheduler(self):
        self.scheduler.resume()


class VkGroupRunning(VkGroupMethods, VkGroupScheduler, VkGroupEventsHandler):
    running = False

    def activate_listening(self):
        longpoll = VkBotLongPoll(self.vk_session, self.id)
        for event in longpoll.listen():
            print(event)
            if not self.running:
                return
            if event.type == VkBotEventType.MESSAGE_NEW:
                self.if_new_message(message=event.obj.message['text'],
                                    from_id=event.obj.message['from_id'],
                                    event=event)
            self.own_handler(event)

    def start(self):
        self.running = True
        # events listener
        listener = threading.Thread(target=self.activate_listening, name="listener", args=[], daemon=True)
        listener.start()

        # scheduler
        self.activate_scheduler()
        return True

    def shutdown(self):
        self.running = False
        self.shutdown_scheduler()
        return True

    def restart(self):
        self.shutdown()
        self.start()
        return True


class VkGroup(VkGroupRunning):
    pass


if __name__ == '__main__':
    ID = '203807582'
    TOKEN = '21b426f2c33e1a65bbc8807ab67ff4d282e026b4b79e9d4b1e33f20f7a0072e137f4e77216ce578f6432a'
    vk_group = VkGroup(ID, TOKEN)
    vk_group.start()