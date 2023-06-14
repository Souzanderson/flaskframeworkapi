import datetime

class Log():
    
    def __init__(self, log, type = "INFO"):
        self.log = log
        self.type = type
        self.set(log, type)

    def set(self, log, type):
        dt = datetime.datetime.now().strftime("[%d-%m-%Y %H:%M:%S] =>")
        tp = f"[{type}] => "
        print(dt, tp, log)