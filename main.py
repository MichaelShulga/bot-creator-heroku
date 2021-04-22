from gevent import monkey;monkey.patch_all()
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import argparse
import os

from flask import Flask, render_template, redirect, request
from client_settings.bot import ResultVKClientGroup

params = argparse.ArgumentParser()
params.add_argument('--heroku', action='store_true')
args = params.parse_args()

app = Flask(__name__)

vk_bot = ResultVKClientGroup('client_settings')

scheduler = BackgroundScheduler()


@app.route("/")
def index():
    alive_start, alive_stop = '', ''
    if scheduler.state == 1:  # keep alive scheduler is running
        alive_start = 'disabled'
    else:
        alive_stop = 'disabled'
    return render_template('index.html', running='Running' if vk_bot.client.running() else 'Disabled',
                           additional=vk_bot.client.settings(), alive_start=alive_start, alive_stop=alive_stop)


@app.route("/start")
def start():
    vk_bot.start()
    return redirect("/")


@app.route("/shutdown")
def stop():
    vk_bot.shutdown()
    url = f'{request.host_url}/stay_alive_heroku/0'
    requests.get(url)
    return redirect("/")


@app.route("/restart")
def restart():
    vk_bot.restart()
    return redirect("/")


@app.route("/none")
def none():
    return ''


@app.route("/stay_alive_heroku/<int:flag>")
def stay_alive_heroku(flag):
    if flag:
        url = f'{request.host_url}/none'
        if scheduler.state == 0:  # not started
            scheduler.add_job(lambda: requests.get(url), 'interval', minutes=14)
            scheduler.start()
            return redirect("/")
        elif scheduler.state == 2:  # paused
            scheduler.resume()
            return redirect("/")
    else:
        if scheduler.state == 1:  # running
            scheduler.pause()
            return redirect("/")
    return "Something went wrong"


def main():
    if args.heroku:  # run on heroku service
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)
    else:  # run on my pc
        app.run(port=8085, host='127.0.0.1', debug=True, use_reloader=False)


if __name__ == '__main__':
    main()
