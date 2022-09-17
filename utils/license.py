import copy
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
    # time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    return datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")  # datetime.datetime.timestamp(time)


def remove_expired_licenses():
    with open("json/licenses.json", "r") as licenses:
        licenses = json.load(licenses)

    # create a copy from the json
    license_copy = copy.copy(licenses)

    # loop through the licenses
    for license in license_copy:
        # check if duration is lifetime
        if license_copy[license]["duration"] == "Lifetime" and license_copy[license]["duration"] is None:
            # !! print(f"{license} is Lifetime | Skipped")
            continue
        else:
            # check if the license is expired
            if license_copy[license]["expired"] is True:
                # remove the license
                del licenses[license]
                # save the new json
                with open("json/licenses.json", "w") as dumpfile:
                    json.dump(licenses, dumpfile, indent=4)
                continue

# ! NOT USED
def check_date():
    with open("json/licenses.json", "r") as licenses:
        licenses = json.load(licenses)

    for license in licenses:
        if licenses[license]["duration"] == "Lifetime" and licenses[license]["duration"] is None:
            print(f"{license} is Lifetime | Skipped")
            continue
        else:
            date_1_string = str(licenses[license]["end_time"])
            date1 = datetime.datetime.strptime(date_1_string, "%d.%m.%Y %H:%M:%S")

            date_2_string = str(get_time())
            date2 = datetime.datetime.strptime(date_2_string, "%d.%m.%Y %H:%M:%S")

            if date1 > date2:
                # let it return True
                print(f"{license} is valid until {licenses[license]['end_time']}")
            elif date1 < date2:
                # let it return False
                print(f"License {license} is expired")


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
