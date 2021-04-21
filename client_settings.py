from vk_bot import VkGroup

ID = '203807582'
TOKEN = '21b426f2c33e1a65bbc8807ab67ff4d282e026b4b79e9d4b1e33f20f7a0072e137f4e77216ce578f6432a'


class EventsHandler(VkGroup):
    def if_new_message(self, message, from_id, event):
        if message == 'Привет':
            answer = 'Ку'
        else:
            answer = 'Пошел в жопу'
        self.send_message(to_id=from_id, message=answer)

    def own_handler(self, event):
        # https://vk.com/dev/groups_events
        pass


class OwnFunctions(VkGroup):
    def send_date_to_me(self):
        message = "Проверка бота 7:30"
        self.send_message(to_id=315336001, message=message)


class SchedulerSettings(OwnFunctions):
    def activate_scheduler(self):
        self.scheduler.add_job(self.send_date_to_me, 'interval', days=1, start_date='2021-04-21 07:30:00')
        self.scheduler.start()


class ResultVKClientGroup(EventsHandler, SchedulerSettings):
    pass


def main():
    client_group = ResultVKClientGroup(ID, TOKEN)
    client_group.start()


if __name__ == '__main__':
    main()
