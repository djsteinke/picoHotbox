import _thread
from wlan import WLAN

jobs = []
thread_running = False
wifi = WLAN


def run_job(job=None):
    # job = [command, [args, callback]]
    # callback should be this.complete_job
    global thread_running
    print("run_job: ", "job: ", job, wifi.connected)
    if job is not None:
        jobs.append(job)

    if not thread_running and len(jobs) > 0:
        thread_running = True
        print("start new thread")
        _thread.start_new_thread(jobs[0][0], jobs[0][1])


def complete_job():
    global thread_running
    print("complete_job", jobs)
    if len(jobs) > 0:
        jobs.pop(0)
    thread_running = False
    run_job()
