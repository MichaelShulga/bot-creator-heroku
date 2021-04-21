import random

from apscheduler.schedulers.background import BackgroundScheduler
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from client import Client

import gevent


class VkGroupInitial:
    def __init__(self, client_settings_package):
        # initialization
        self.client = Client(client_settings_package)

        settings = self.client.settings()
        self.id = settings["id"]
        self.token = settings["token"]

        self.vk_session = VkApi(token=self.token)


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


class BackgroundFunction:
    greenlet = None

    def start(self, func):
        self.greenlet = gevent.spawn(func)

    def shutdown(self):
        self.greenlet.kill()


class VkGroupRunning(VkGroupMethods, VkGroupScheduler, VkGroupEventsHandler):
    background_listener = BackgroundFunction()

    def __init__(self, client_settings_package):
        super().__init__(client_settings_package)
        settings = self.client.settings()
        running = settings["running"]
        if running:
            self.start()

    def activate_listening(self):
        longpoll = VkBotLongPoll(self.vk_session, self.id)
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                self.if_new_message(message=event.obj.message['text'],
                                    from_id=event.obj.message['from_id'],
                                    event=event)
            self.own_handler(event)

    def start(self):
        self.client.set_running(True)

        # events listener
        self.background_listener.start(self.activate_listening)

        # scheduler
        self.activate_scheduler()
        return True

    def shutdown(self):
        self.client.set_running(False)

        # events listener
        self.background_listener.shutdown()

        # scheduler
        self.shutdown_scheduler()
        return True

    def restart(self):
        self.shutdown()
        self.start()
        return True


class VkGroup(VkGroupRunning):
    pass
