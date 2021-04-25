import json
import os


class Client:
    def __init__(self, package):
        self.path = os.path.join(package, "additional.json")

    def settings(self):
        with open(self.path) as additional:
            return json.load(additional)

    def update_settings(self, settings):
        with open(self.path, 'w') as additional:
            json.dump(settings, additional)

    def set_running(self, flag):
        settings = self.settings()
        settings['running'] = flag
        self.update_settings(settings)

    def running(self):
        return self.settings()['running']

    def add_error(self, error):
        settings = self.settings()
        settings["errors"].append(error)
        self.update_settings(settings)

    def clean_errors(self):
        settings = self.settings()
        settings["errors"] = []
        self.update_settings(settings)


if __name__ == '__main__':
    client = Client('client_settings')
    a, b, c = client.settings().values()
    client.set_running(True)
    print(client.settings())