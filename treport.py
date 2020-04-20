import shelve
from settings import *
from datetime import datetime
from os import path as p
from os import makedirs
import re
from os import chdir


def generate_entire_logs():
    if USE_RECVLOG:
        text = None
        with open(RECV_PATH) as f:
            text = [i for i in f.read().split('\n')]
            text = text[2:]
            f.close()
        del text[-1]
        if not text and not USE_SENDLOG:
            return
        else:
            recv_template = ""
            with open(SKEL_RECV, mode='r') as skel_file:
                recv_template = skel_file.read()
                skel_file.close()

            timestamp = None
            for i in range(len(text)):
                recv_out = recv_template
                line = text[i].split(",")
                d = line[0].strip('"')

                #Account for the fact that dates in the log do not prepend a 0
                date_list = d.split("/")
                if len(date_list[0]) == 1:
                    date_list[0] = "0" + date_list[0]
                if len(date_list[1]) == 1:
                    date_list[1] = "0" + date_list[1]
                dfmt = date_list[0] + date_list[1] + date_list[2]

                #get the time as a plain string
                t = line[1].strip('"')[:-3]
                t12 = t + line[1][-4:-1]
                tfmt = t.replace(":", "")

                stamp = dfmt + "_" + tfmt + line[1][-3:-1]
                dt = datetime.strptime(stamp, "%m%d%Y_%I%M%S%p")
                year = str(dt.year)
                month = str(dt.month)
                day = str(dt.day)
                date_path = RECV_OUT_FOLDER + year + "/" + month + "/" + day + "/"
                date_path_fmt = Path(date_path)
                if not p.exists(date_path_fmt):
                    makedirs(date_path_fmt)

                dt = datetime.strptime(stamp, "%m%d%Y_%I%M%S%p")

                recv_out = recv_out.replace("$date", d)
                recv_out = recv_out.replace("$time", t12)
                caller = "UNKNOWN"
                an = re.sub(r'\W+', '', line[2])
                if an != "":
                    caller = an
                recv_out = recv_out.replace("$remote_number", caller)
                recv_out = recv_out.replace("$pages", line[4])
                recv_out = recv_out.replace("$line", line[7])
                recv_out = recv_out.replace("$result", line[5])
                recv_out = recv_out.replace("$details", line[6])
                recv_out = recv_out.replace("$title", line[5])

                name = year + month + day + "_" + dt.strftime("%I%M%S") + line[1][-3:-1] + ".html"

                filepath = Path(str(date_path_fmt) + "/" + name)
                file = open(filepath, "w")
                f = file.write(recv_out)
                file.close()

                if i == len(text) - 1:
                    timestamp = dt
            if timestamp is not None:
                db = shelve.open(RUNTIME_SETTINGS)
                db["last_recv_time"] = timestamp.strftime("%Y%m%d_%I%M%S%p")
                db.close()

    if USE_SENDLOG:
        text = None
        with open(SEND_PATH) as f:
            text = [i for i in f.read().split('\n')]
            text = text[2:]
            f.close()
        del text[-1]
        if not text:
            return
        else:
            send_template = ""
            with open(SKEL_SEND, mode='r') as skel_file:
                send_template = skel_file.read()
                skel_file.close()

            timestamp = None
            for i in range(len(text)):
                send_out = send_template
                line = text[i].split(",")
                d = line[0].strip('"')

                #Account for the fact that dates in the log do not prepend a 0
                date_list = d.split("/")
                if len(date_list[0]) == 1:
                    date_list[0] = "0" + date_list[0]
                if len(date_list[1]) == 1:
                    date_list[1] = "0" + date_list[1]
                dfmt = date_list[0] + date_list[1] + date_list[2]

                # Get the time as a plain string
                t = line[1].strip('"')[:-3]
                t12 = t + line[1][-4:-1]
                tfmt = t.replace(":", "")
                stamp = dfmt + "_" + tfmt + line[1][-3:-1]

                dt = datetime.strptime(stamp, "%m%d%Y_%I%M%S%p")
                year = str(dt.year)
                month = str(dt.month)
                day = str(dt.day)
                date_path = SEND_OUT_FOLDER + year + "/" + month + "/" + day + "/"

                date_path_fmt = Path(date_path)
                if not p.exists(date_path_fmt):
                    makedirs(date_path_fmt)

                send_out = send_out.replace("$date", d)
                send_out = send_out.replace("$time", t12)
                caller = "UNKNOWN"
                an = re.sub(r'\W+', '', line[5])
                if an != "":
                    caller = an
                send_out = send_out.replace("$remote_number", caller)
                send_out = send_out.replace("$foo@foo.com", line[2])
                send_out = send_out.replace("$pages", line[10])
                send_out = send_out.replace("$line", line[13])
                send_out = send_out.replace("$result", line[11])
                send_out = send_out.replace("$details", line[12])
                send_out = send_out.replace("$title", line[11])
                name = year + month + day + "_" + dt.strftime("%I%M%S") + line[1][-3:-1] + ".html"

                filepath = Path(str(date_path_fmt) + "/" + name)
                file = open(filepath, "w")
                f = file.write(send_out)
                file.close()

                if i == len(text) - 1:
                    timestamp = dt

            if timestamp is not None:
                db = shelve.open(RUNTIME_SETTINGS)
                db["last_send_time"] = timestamp.strftime("%Y%m%d_%I%M%S%p")
                db.close()


def update_recv_log(db_time):
    text = None
    update_time = None
    with open(RECV_PATH) as f:
        text = [i for i in f.read().split('\n')]
        text = text[2:]
        f.close()
    if not text:
        return
    del text[-1]

    r = 0
    txt_lst = None
    if len(text) >= UPDATE_SCAN_LENGTH:
        r = UPDATE_SCAN_LENGTH
        txt_lst = text[-UPDATE_SCAN_LENGTH:]
        s = len(text) - UPDATE_SCAN_LENGTH
    else:
        r = len(text)
        text_lst = text

    recv_template = ""
    with open(SKEL_RECV, mode='r') as skel_file:
        recv_template = skel_file.read()
        skel_file.close()

    for i in range(r):
        recv_out = recv_template
        line = txt_lst[i].split(",")
        d = line[0].strip('"')

        # Account for the fact that dates in the log do not prepend a 0
        date_list = d.split("/")
        if len(date_list[0]) == 1:
            date_list[0] = "0" + date_list[0]
        if len(date_list[1]) == 1:
            date_list[1] = "0" + date_list[1]
        dfmt = date_list[0] + date_list[1] + date_list[2]

        # get the time as a plain string
        t = line[1].strip('"')[:-3]
        # get am or pm
        nd = line[1][-3:-1]
        t12 = t + line[1][-4:-1]
        tfmt = t.replace(":", "")

        # the timestamp in string format
        stamp = dfmt + "_" + tfmt + nd

        dt = datetime.strptime(stamp, "%m%d%Y_%I%M%S%p")
        year = str(dt.year)
        month = str(dt.month)
        day = str(dt.day)
        hour = dt.hour
        minute = dt.minute
        second = dt.second

        if db_time < dt:
            update_time = dt
            date_path = RECV_OUT_FOLDER + year + "/" + month + "/" + day + "/"
            date_path_fmt = Path(date_path)
            if not p.exists(date_path_fmt):
                makedirs(date_path_fmt)

            dt = datetime.strptime(stamp, "%m%d%Y_%I%M%S%p")

            recv_out = recv_out.replace("$date", d)
            recv_out = recv_out.replace("$time", t12)
            caller = "UNKNOWN"
            an = re.sub(r'\W+', '', line[2])
            if an != "":
                caller = an
            recv_out = recv_out.replace("$remote_number", caller)
            recv_out = recv_out.replace("$pages", line[4])
            recv_out = recv_out.replace("$line", line[7])
            recv_out = recv_out.replace("$result", line[5])
            recv_out = recv_out.replace("$details", line[6])
            recv_out = recv_out.replace("$title", line[5])

            name = year + month + day + "_" + dt.strftime("%I%M%S") + line[1][-3:-1] + ".html"

            filepath = Path(str(date_path_fmt) + "/" + name)
            file = open(filepath, "w")
            f = file.write(recv_out)
            file.close()

    return update_time

def update_send_log(db_time):
    text = None
    update_time = None
    with open(SEND_PATH) as f:
        text = [i for i in f.read().split('\n')]
        text = text[2:]
        f.close()
    if not text:
        return
    del text[-1]

    r = 0
    txt_lst = None
    if len(text) >= UPDATE_SCAN_LENGTH:
        r = UPDATE_SCAN_LENGTH
        txt_lst = text[-UPDATE_SCAN_LENGTH:]
    else:
        txt_lst = text
        r = len(txt_lst)

    send_template = ""
    with open(SKEL_SEND, mode='r') as skel_file:
        send_template = skel_file.read()
        skel_file.close()

    for i in range(r):
        send_out = send_template
        line = txt_lst[i].split(",")
        d = line[0].strip('"')

        # Account for the fact that dates in the log do not prepend a 0
        date_list = d.split("/")
        if len(date_list[0]) == 1:
            date_list[0] = "0" + date_list[0]
        if len(date_list[1]) == 1:
            date_list[1] = "0" + date_list[1]
        dfmt = date_list[0] + date_list[1] + date_list[2]

        # Get the time as a plain string
        t = line[1].strip('"')[:-3]
        # get am or pm
        nd = line[1][-3:-1]
        t12 = t + line[1][-4:-1]
        tfmt = t.replace(":", "")

        #the timestamp in string format
        stamp = dfmt + "_" + tfmt + line[1][-3:-1]
        dt = datetime.strptime(stamp, "%m%d%Y_%I%M%S%p")
        
        year = str(dt.year)
        month = str(dt.month)
        day = str(dt.day)
        hour = dt.hour
        minute = dt.minute
        second = dt.second

        if db_time < dt:
            update_time = dt
            date_path = SEND_OUT_FOLDER + year + "/" + month + "/" + day + "/"
            date_path_fmt = Path(date_path)
            if not p.exists(date_path_fmt):
                makedirs(date_path_fmt)

            send_out = send_out.replace("$date", d)
            send_out = send_out.replace("$time", t12)
            caller = "UNKNOWN"
            an = re.sub(r'\W+', '', line[5])
            if an != "":
                caller = an
            send_out = send_out.replace("$remote_number", caller)
            send_out = send_out.replace("$foo@foo.com", line[2])
            send_out = send_out.replace("$pages", line[10])
            send_out = send_out.replace("$line", line[13])
            send_out = send_out.replace("$result", line[11])
            send_out = send_out.replace("$details", line[12])
            send_out = send_out.replace("$title", line[11])
            name = year + month + day + "_" + dt.strftime("%I%M%S") + line[1][-3:-1] + ".html"

            filepath = Path(str(date_path_fmt) + "/" + name)
            file = open(filepath, "w")
            f = file.write(send_out)
            file.close()

    return update_time

if __name__ == "__main__":
    chdir(PWD)
    if not p.exists(RUNTIME_DIR):
        makedirs(RUNTIME_DIR)

        with shelve.open(RUNTIME_SETTINGS) as db:
            db["Init"] = True
            db["last_recv_time"] = None
            db["last_send_time"] = None
            db.close()

    last_recv_time = None
    last_send_time = None
    with shelve.open(RUNTIME_SETTINGS) as db:
        last_recv_time = db["last_recv_time"]
        last_send_time = db["last_send_time"]
        if last_recv_time:
            last_recv_time = datetime.strptime(db["last_recv_time"], "%Y%m%d_%I%M%S%p")
        if last_send_time:
            last_send_time = datetime.strptime(db["last_send_time"], "%Y%m%d_%I%M%S%p")
        db.close()

    if last_recv_time is None and USE_RECVLOG:
        generate_entire_logs()
        exit(0)
    elif last_send_time is None and USE_SENDLOG:
        generate_entire_logs()
        exit(0)

    if USE_RECVLOG and last_recv_time and type(last_recv_time) == datetime:
        dt = update_recv_log(last_recv_time)
        if dt is not None:
            stamp = dt.strftime("%Y%m%d_%I%M%S%p")
            with shelve.open(RUNTIME_SETTINGS) as db:
                db["last_recv_time"] = stamp
                db.close()
    else:
        print("recvlog stamp was not converted")

    if USE_SENDLOG and last_send_time and type(last_send_time) == datetime:
        dt = update_send_log(last_send_time)
        if dt is not None:
            stamp = dt.strftime("%Y%m%d_%I%M%S%p")
            with shelve.open(RUNTIME_SETTINGS) as db:
                db["last_send_time"] = stamp
                db.close()
    else:
        print("sendlog stamp was not converted")