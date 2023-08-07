from adafruit_datetime import datetime
from .logging_conf import *
import os


class Logger:
    def __init__(self, subtag):
        self.__subtag = subtag

    def d(self, msg: str = ""):
        self.__log("Debug", msg)

    def i(self, msg: str = ""):
        self.__log("Info", msg)

    def w(self, msg: str = ""):
        self.__log("Warning", msg)

    def e(self, msg: str = ""):
        self.__log("Error", msg)

    def __log(self, level: str, msg: str):
        time = self.__get_time()
        date = self.__get_date()
        pretty = f"{date['year']}-{date['month']}-{date['day']} "
        pretty += f"{time['hour']}:{time['min']}:{time['sec']} "
        pretty += f"{tag}:{self.__subtag} [{level}] {msg}"

        if level == "Debug" and debug:
            print(pretty)
            self.__file_log(pretty)
        else:
            print(pretty)
            self.__file_log(pretty)

    def __file_log(self, msg: str):
        date = self.__get_date()
        file_name = f"{date['year']}-{date['month']}-{date['day']}.log"
        try:
            if file_name in os.listdir():
                with open(file_name, "a") as f:
                    f.write(msg + "\n")
            else:
                with open(file_name, "x") as f:
                    f.write(msg + "\n")
        except:
            pass

    def __get_time(self) -> {"hour", "min", "sec"}:
        unf_time = datetime.now()
        return {
            "hour": f"0{unf_time.hour}" if (unf_time.hour < 10) else unf_time.hour,
            "min": f"0{unf_time.minute}" if (unf_time.minute < 10) else unf_time.minute,
            "sec": f"0{unf_time.second}" if (unf_time.second < 10) else unf_time.second,
        }

    def __get_date(self) -> {"year", "month", "day"}:
        unf_time = datetime.now()
        return {
            "year": f"0{unf_time.year}" if (unf_time.year < 10) else unf_time.year,
            "month": f"0{unf_time.month}" if (unf_time.month < 10) else unf_time.month,
            "day": f"0{unf_time.day}" if (unf_time.day < 10) else unf_time.day,
        }
