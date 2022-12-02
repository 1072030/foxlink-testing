# %%
import json
import argparse
import os
import random
import numpy as np
from datetime import datetime, timedelta

CURRENT_PATH = os.getcwd()
# %%


class CreateTime():
    def __init__(self, filename: str, start: int = 30, disconn=30, conn_time=60):
        '''
        filename        :str      json檔名
        data            :list     資料存放
        start           :int      程式執行後,過多久異常發生。default: 30 sec
        now             :datetime 現在時間
        event_start_time:datetime 異常開始時間。now+start
        disconn         :int      異常開始後，多久斷網。    default: 30 sec
        conn_time       :int      斷線後多久恢復連網(秒)。  default: 60 sec
        '''
        self.filename = filename
        self.data = []
        self.start = 30
        self.now = datetime.now()
        self.event_start_time = datetime.now() + timedelta(seconds=self.start)
        self.disconn = disconn
        self.conn_time = conn_time
        # print("now:", self.now, "\nstart:", self.start, "\nevent_start_time:", self.event_start_time,"\ndisconn:", self.disconn)

    # load test file
    def load_data(self):
        with open(f"{CURRENT_PATH}/app/scenario/{self.filename}.json", encoding="utf8") as js_file:
            self.data = json.load(js_file)
        return self.data

    # 填入異常開始時間(start time);test1,test2,test4
    def test_start_time(self):
        for i in self.data["foxlinkEvent"]:
            i["start_time"] = self.event_start_time.strftime("%Y-%m-%d %H:%M:%S")
        return self.data

    # 異常發生時間隨機產生;test3
    def random_start_time(self, break_time=300, end_time=600):
        '''
        break_time: 多久時間內機台皆發生異常(預設5分鐘)。單位:秒
        end_time: 異常發生後，過多久解除(10分鐘)  單位:秒
        '''
        break_ls = sorted([random.randint(0, break_time) for _ in range(91)], reverse=True)  # 91個時間段(0~BREAK)
        break_ls = [(self.event_start_time + timedelta(seconds=i)) for i in break_ls]  # 91個機台異常時間(現在時間往後推)

        for idx, message in enumerate(self.data["foxlinkEvent"]):
            if message["status"] == "create":
                event_id = self.data["foxlinkEvent"][idx]["event_id"]  # 取event_id
                message["start_time"] = break_ls[event_id].strftime("%Y-%m-%d %H:%M:%S")  # "填入"機台異常開始時間

            if message["status"] == "update":  # 只有48台機台有update end time(結束任務)
                message["start_time"] = break_ls[event_id].strftime("%Y-%m-%d %H:%M:%S")  # "填入"機台異常開始時間
                event_end_time = self.event_start_time + timedelta(seconds=end_time)  # 機台異常結束時間
                message["end_time"] = event_end_time.strftime("%Y-%m-%d %H:%M:%S")  # "填入"機台異常結束時間
        return self.data

    # 換班前後發生異常;test5
    def shift__start_time(self, shift_time, before_sf_bt=300, before_sf_rt=120, after_sf_bt=120):
        '''
        shift_time  : datetime ,換班時間
        before_sf_bt: int      ,換班前多久機台發生異常。          default:300 sec
        before_sf_rt: int      ,換班前多久機台18台(預先設計)完成。 default:120 sec
        after_sf_bt : int      ,換班後多久31台機台異常。          default:120 sec
        '''
        shift_time = datetime.strptime(shift_time, "%Y-%m-%d %H:%M:%S")  # convert str to datetime
        # 填入異常開始時間(start time)與結束時間(end_time)
        for message in self.data["foxlinkEvent"]:
            if message["project"] in ["D52", "N104", "X61", "D7X"]:
                message["start_time"] = (shift_time - timedelta(seconds=before_sf_bt)
                                         ).strftime("%Y-%m-%d %H:%M:%S")  # "填入"機台異常開始時間
                if message["status"] == "update":
                    message["end_time"] = (shift_time - timedelta(seconds=before_sf_rt)
                                           ).strftime("%Y-%m-%d %H:%M:%S")  # "填入"機台異常結束時間
            else:
                message["start_time"] = (shift_time + timedelta(seconds=after_sf_bt)
                                         ).strftime("%Y-%m-%d %H:%M:%S")  # "填入"機台異常開始時間
        return self.data

    # 頻繁發生異常;test6
    def freq_breakdown(self):

        event_end_time = self.event_start_time + timedelta(seconds=600)  # 反覆發生異常持續10分鐘，不能改因為event已寫好
        ls_all = []
        # 根據事先設計好的故障頻率建立event開始與結束時間list
        # frequncy 0(1)，異常開始並馬上結束(持續0秒)，過1秒後再次發生
        freq0 = np.arange(self.event_start_time, event_end_time, timedelta(seconds=1)).astype(datetime)
        for idx in range(600 * 2 * 10):
            machine_num = int(idx / (600 * 2))
            idx = idx - ((600 * 2) * machine_num)
            if idx % 2 == 0:
                time_idx = int(idx / 2)
                ls = [freq0[time_idx].strftime("%Y-%m-%d %H:%M:%S"), ""]
            else:
                time_idx = int((idx - 1) / 2)
                ls = [freq0[time_idx].strftime("%Y-%m-%d %H:%M:%S"), freq0[time_idx].strftime("%Y-%m-%d %H:%M:%S")]
            ls_all.append(ls)

        # frquncy 5,10,15,30,60,600 sec，異常開始過*秒結束，立即發生異常
        for i in [5, 10, 15, 30, 60, 600]:
            freq = np.arange(self.event_start_time, event_end_time, timedelta(seconds=i)).astype(datetime)
            freq = np.insert(freq, len(freq), event_end_time)  # insert endtime

            time_num = len(freq) - 1
            if i == 600:  # 該頻率有幾個機台
                m = 31
            else:
                m = 10
            event_num = time_num * 2 * m

            for idx in range(event_num):
                machine_num = int(idx / (time_num * 2))
                idx = idx - ((len(freq) - 1) * 2 * machine_num)

                if idx % 2 == 0:
                    time_idx = int(idx / 2)
                    ls = [freq[time_idx].strftime("%Y-%m-%d %H:%M:%S"), ""]
                else:
                    time_idx = int(idx / 2)
                    ls = [freq[time_idx].strftime("%Y-%m-%d %H:%M:%S"), freq[time_idx +
                                                                             1].strftime("%Y-%m-%d %H:%M:%S")]
                ls_all.append(ls)

        # 填入時間
        for i in range(len(ls_all)):
            self.data["foxlinkEvent"][i]["start_time"] = ls_all[i][0]
            self.data["foxlinkEvent"][i]["end_time"] = ls_all[i][1]
        return self.data

    # 異常結束後員工端操作API;test7
    def test_event_end(self, break_time):
        event_end_time = self.event_start_time + timedelta(seconds=break_time)

        for message in self.data["foxlinkEvent"]:
            message["start_time"] = self.event_start_time.strftime("%Y-%m-%d %H:%M:%S")  # "填入"機台異常開始時間

            if message["status"] == "update":
                message["end_time"] = event_end_time.strftime("%Y-%m-%d %H:%M:%S")  # "填入"機台異常結束時間
        return self.data

    # 填入斷線時間時間
    def disconnect(self):
        disconn_start_time = self.event_start_time + timedelta(seconds=self.disconn)  # 斷線開始時間
        disconn_end_time = disconn_start_time + timedelta(seconds=self.conn_time)  # 斷線結束時間
        # 填入時間並轉換格式
        network = self.data["network_status"]["server_network"][0]
        network["status"] = "disconnect"
        network["start_time"] = disconn_start_time.strftime("%Y-%m-%d %H:%M:%S")
        network["end_time"] = disconn_end_time.strftime("%Y-%m-%d %H:%M:%S")
        return self.data

    # load file
    def output_data(self):
        with open(f"{CURRENT_PATH}/app/scenario/{self.filename}.json", "w", encoding='utf8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

# %%


def main(test_filename, start=30, disconn=30, conn_time=60, shift_time="2022-10-16 22:50:00", break_time=20):
    '''
        filename        :str      json檔名
        start           :int      程式執行後,過多久異常發生。default: 30 sec
        disconn         :int      異常開始後，多久斷網。    default: 30 sec
        conn_time       :int      斷線後多久恢復連網(秒)。  default: 60 sec
        shift_time      :str      換班時間。test5使用
        break_time      :int      異常持續時間。test7 使用  default: 20 sec
    目前預設:
    1. 程式開始執行後過30秒(start)機台開始發生異常
    2. 異常發生後過30秒(disconn)斷線
    3. 斷線後過60秒(conn_time)恢復連線
    4. 使用情境5時需要調整換班時間(shift_time)，目前預設"2022-10-16 22:50:00"
    5. 使用情境5時需要調整異常持續時間(break_time)，目前預設20秒
    '''

    test_time = CreateTime(test_filename, start, disconn, conn_time)
    test_time.load_data()
    if test_filename == "testLogin":
        pass
    elif test_filename == "test1" or test_filename == "test2" or test_filename == "test4":
        test_time.test_start_time()
    elif test_filename == "test3":
        test_time.random_start_time()
    elif test_filename == "test5":
        test_time.shift__start_time(shift_time)
    elif test_filename == "test6":
        test_time.freq_breakdown()
    elif test_filename == "test7":
        test_time.test_event_end(break_time)
    test_time.disconnect()
    test_time.output_data()


# %%
# testLogin,test1,test2,test3,test4,test6 直接輸入檔名。
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filename", required=True)
parser.add_argument("-s", "--shift")
parser.add_argument("-b", "--break_time", type=int)
args = parser.parse_args()
main(test_filename=args.filename, shift_time=args.shift, break_time=args.break_time)

# test 5, 除檔名外,測試時要改換班時間
# main("test5", shift_time="2022-10-16 22:50:00")

# # test 7, 除檔名外,測試時要調整異常持續多久才會結束
# main("test7", break_time = 20)

# %%
