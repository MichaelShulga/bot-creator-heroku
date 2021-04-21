import argparse
import os

from flask import Flask, render_template, redirect
from client_settings.bot import ResultVKClientGroup


params = argparse.ArgumentParser()
params.add_argument('--heroku', action='store_true')
args = params.parse_args()

app = Flask(__name__)

vk_bot = ResultVKClientGroup('client_settings')


@app.route("/")
def index():
    return render_template('index.html', running='Running' if vk_bot.running else 'Disabled')


@app.route("/start")
def start():
    vk_bot.start()
    return redirect("/")


@app.route("/shutdown")
def stop():
    vk_bot.shutdown()
    return redirect("/")


@app.route("/restart")
def restart():
    vk_bot.restart()
    return redirect("/")


@app.route("/vk")
def vk():
    return redirect("http://www.vk.com")


def main():
    if args.heroku:  # run on heroku service
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)
    else:  # run on my pc
        app.run(port=8085, host='127.0.0.1', debug=True, use_reloader=False)


if __name__ == '__main__':
    main()
