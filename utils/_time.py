import copy
import datetime
import json


def get_time() -> str:
    # time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    return datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")  # datetime.datetime.timestamp(time)


def remove_expired_timers():
    with open("json/timer.json", "r") as timer_info:
        timers = json.load(timer_info)

    # create a copy from the json
    timer_copy = copy.copy(timers)

    # loop through the timers
    for timer in timer_copy:
        # check if the timer is expired
        if timer_copy[timer]["end_time"] is True:
            # remove the license
            del timers[timer]
            # save the new json
            with open("json/timer.json", "w") as dumpfile:
                json.dump(timers, dumpfile, indent=4, default=str)
            continue


def set_end_time(time):
    end_date = datetime.datetime.now() + datetime.timedelta(seconds=time)
    return end_date.strftime("%d.%m.%Y %H:%M:%S")

    # return datetime.datetime.now() + datetime.timedelta(seconds=time)
