from run_all_loops import run
from daemon_loops.celery import app


@app.task
def launch_loops():
    run()
