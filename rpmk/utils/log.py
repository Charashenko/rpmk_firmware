import time
import os

DEBUG = True


class Logger:
    def __init__(self, tag):
        self.__tag = tag

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
        pretty += f"{self.__tag} [{level}] {msg}"

        if level == "Debug" and DEBUG:
            print(pretty)
            # self.__file_log(pretty)
        else:
            print(pretty)
            # self.__file_log(pretty)

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
        unf_time = time.localtime()
        return {
            "hour": f"0{unf_time[3]}" if (unf_time[3] < 10) else unf_time[3],
            "min": f"0{unf_time[4]}" if (unf_time[4] < 10) else unf_time[4],
            "sec": f"0{unf_time[5]}" if (unf_time[5] < 10) else unf_time[5],
        }

    def __get_date(self) -> {"year", "month", "day"}:
        unf_date = time.localtime()
        return {
            "year": f"0{unf_date[0]}" if (unf_date[0] < 10) else unf_date[0],
            "month": f"0{unf_date[1]}" if (unf_date[1] < 10) else unf_date[1],
            "day": f"0{unf_date[2]}" if (unf_date[2] < 10) else unf_date[2],
        }
