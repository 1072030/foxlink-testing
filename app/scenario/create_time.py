import json
import numpy as np
from datetime import datetime, timedelta

class CreateTime():
    def __init__(self, filename: str, start=10):
        '''
        filename        :str      json檔名
        data            :list     資料存放
        start           :int      程式執行後,過多久異常發生。default: 30 sec
        now             :datetime 現在時間
        event_start_time:datetime 異常開始時間。now+start
        interval        :int      間隔時間
        '''
        self.filename = filename 
        self.data = [] 
        self.start = start 
        self.now = datetime.utcnow() 
        self.event_start_time = datetime.utcnow() + timedelta(seconds=self.start) 
        self.interval = 15

    # load test file
    def load_data(self):
        with open(f"{self.filename}.json",encoding="utf8") as js_file:
            self.data = json.load(js_file)
        return self.data

    # 填入異常開始時間(start time);
    def test_start_time(self):
        for message in self.data["foxlinkEvent"]:
            message["start_time"] = self.event_start_time.strftime("%Y-%m-%d %H:%M:%S")
        return self.data

    # 異常自動結束;
    def test_event_end(self):
        event_end_time = self.event_start_time + timedelta(seconds=self.interval)

        for message in self.data["foxlinkEvent"]:   
            message["start_time"] = self.event_start_time.strftime("%Y-%m-%d %H:%M:%S") # "填入"機台異常開始時間
            
            if message["status"] == "update": 
                message["end_time"] = event_end_time.strftime("%Y-%m-%d %H:%M:%S") # "填入"機台異常結束時間
        return self.data

    # load file
    def output_data(self):
        with open(f"{self.filename}.json", "w", encoding='utf8') as f:
            json.dump(self.data, f,ensure_ascii=False, indent=4)

def main(test_filename,start=30):
    '''
        filename        :str      json檔名
        start           :int      程式執行後,過多久異常發生。default: 30 sec
    目前預設:
    1. 程式開始執行後過10秒(start)機台開始發生異常
    '''

    test_time = CreateTime(test_filename,start)
    test_time.load_data()
    if test_filename == "Dispatch":
        test_time.test_start_time()
    elif test_filename == "AutoEnd":
        test_time.test_event_end()
    test_time.output_data()

# Dispatch, AutoEnd
main("Dispatch") 

