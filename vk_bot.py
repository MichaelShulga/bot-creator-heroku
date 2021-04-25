import random

import vk_api
from vk_api.vk_api import VkApiGroup
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from client import Client

import gevent

from apscheduler.schedulers.background import BackgroundScheduler


class VkGroupInitial:
    def __init__(self, client_settings_package):
        # initialization
        self.client = Client(client_settings_package)

        settings = self.client.settings()
        self.id = settings["id"]
        self.token = settings["token"]

        self.vk_session = VkApiGroup(token=self.token)


class VkGroupMethods(VkGroupInitial):
    def send_message(self, to_id, message):
        vk = self.vk_session.get_api()
        vk.messages.send(user_id=to_id,
                         message=message,
                         random_id=random.randint(0, 2 ** 64))

    def wall_post(self, message):
        vk = self.vk_session.get_api()
        vk.wall.post(message=message, owner_id=f"-{self.id}")


class VkGroupEventsHandler(VkGroupInitial):
    def message_new(self, message, from_id, event):
        pass

    def group_join(self, from_id, event):
        pass

    def message_typing_state(self, from_id, event):
        pass

    def group_leave(self, from_id, event):
        pass

    def own_handler(self, event):
        pass


class BackgroundFunction:
    greenlet = None

    def start(self, func):
        self.greenlet = gevent.spawn(func)

    def shutdown(self):
        self.greenlet.kill()


class VkGroupRunning(VkGroupMethods, VkGroupEventsHandler):
    listener = BackgroundFunction()
    scheduler = BackgroundScheduler()

    def __init__(self, client_settings_package):
        super().__init__(client_settings_package)
        settings = self.client.settings()
        running = settings["running"]
        if running:
            self.start()

    def activate_listening(self):
        longpoll = VkBotLongPoll(self.vk_session, self.id)
        for event in longpoll.listen():
            print(event)
            if event.type == VkBotEventType.MESSAGE_NEW:
                self.message_new(message=event.obj.message['text'],
                                 from_id=event.obj.message['from_id'],
                                 event=event)
            if event.type == VkBotEventType.MESSAGE_TYPING_STATE:
                self.message_typing_state(from_id=event.obj.from_id,
                                          event=event)
            if event.type == VkBotEventType.GROUP_JOIN:
                self.group_join(from_id=event.obj.user_id,
                                event=event)
            if event.type == VkBotEventType.GROUP_LEAVE:
                self.group_leave(from_id=event.obj.user_id,
                                 event=event)
            self.own_handler(event)

    def activate_listening_ignore_errors(self):
        try:
            self.activate_listening()
        except Exception as e:
            self.client.add_error(str(e))
            self.activate_listening_ignore_errors()

    def activate_scheduler(self):
        pass

    def start(self):
        self.client.set_running(True)
        self.client.clean_errors()

        # events listener
        self.listener.start(self.activate_listening_ignore_errors)

        # scheduler
        self.activate_scheduler()
        self.scheduler.start()
        return True

    def shutdown(self):
        self.client.set_running(False)

        # events listener
        self.listener.shutdown()

        # scheduler
        self.scheduler.shutdown()
        self.scheduler = BackgroundScheduler()
        return True

    def restart(self):
        self.shutdown()
        self.start()
        return True


class VkGroup(VkGroupRunning):
    pass
