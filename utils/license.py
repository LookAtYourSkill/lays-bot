import datetime
import json
import random
import string


def codeGenerator(char_l: list) -> str:
    return ''.join(random.choices(char_l, k=5))


def generate():
    chars = string.ascii_uppercase + string.digits
    return f"{codeGenerator(chars)}-{codeGenerator(chars)}-{codeGenerator(chars)}"


def get_time() -> str:
    return datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


def check_date():
    with open("json/licenses.json", "r") as licenses:
        licenses = json.load(licenses)

    for license in licenses:
        if licenses[license]["duration"] == "Lifetime":
            continue
        else:
            date1 = datetime.datetime.strptime(licenses[license]["end_time"], "%d.%m.%Y %H:%M:%S")
            date2 = get_date()
            if date1 > date2:
                print(date1, date2)
                return True
            else:
                print(date1, date2)
                return False


def get_date() -> str:
    return datetime.datetime.now().strftime("%d.%m.%Y")


def set_time_calcs(license):
    with open("json/licenses.json", "r") as licenses:
        licenses = json.load(licenses)

    if licenses[license]["duration"] == "1 Day":
        time = 86400

        new_date = datetime.datetime.now() + datetime.timedelta(seconds=time)
        return new_date.strftime("%d.%m.%Y %H:%M:%S")

        # return datetime.datetime.now() + datetime.timedelta(seconds=time)

    elif licenses[license]["duration"] == "7 Days":
        time = 604800

        new_date = datetime.datetime.now() + datetime.timedelta(seconds=time)
        return new_date.strftime("%d.%m.%Y %H:%M:%S")

        # return datetime.datetime.now() + datetime.timedelta(seconds=time)

    elif licenses[license]["duration"] == "1 Month":
        time = 2628000

        new_date = datetime.datetime.now() + datetime.timedelta(seconds=time)
        return new_date.strftime("%d.%m.%Y %H:%M:%S")

        # return datetime.datetime.now() + datetime.timedelta(seconds=time)

    elif licenses[license]["duration"] == "3 Months":
        time = 7884000

        new_date = datetime.datetime.now() + datetime.timedelta(seconds=time)
        return new_date.strftime("%d.%m.%Y %H:%M:%S")

        # return datetime.datetime.now() + datetime.timedelta(seconds=time)

    elif licenses[license]["duration"] == "6 Months":
        time = 15770000

        new_date = datetime.datetime.now() + datetime.timedelta(seconds=time)
        return new_date.strftime("%d.%m.%Y %H:%M:%S")

        # return datetime.datetime.now() + datetime.timedelta(seconds=time)

    elif licenses[license]["duration"] == "1 Year":
        time = 31536000

        new_date = datetime.datetime.now() + datetime.timedelta(seconds=time)
        return new_date.strftime("%d.%m.%Y %H:%M:%S")

        # return datetime.datetime.now() + datetime.timedelta(seconds=time)

    elif licenses[license]["duration"] == "Lifetime":
        return "Lifetime"

    else:
        return time
