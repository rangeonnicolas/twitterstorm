from twitterWatch.celery import app
from trends.trendwatcher import send_request, launch_loop
import datetime as dt


@app.task
def get_twitter_trends(now=None, last_exec=None, msg=" (cron)"):
    # print("Bah yo! Task1 getTwTrends. " + msg)
    if now is None:
        now = dt.datetime.now(dt.timezone.utc)
    send_request(now, last_exec, msg=msg)


@app.task
def launch_advanced_loop():
    # print("Bah yo la grosse loop!")
    launch_loop()
