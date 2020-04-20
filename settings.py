from pathlib import Path
APP_NAME = "TReport"
APP_AUTHOR = "TReport"
ROOT_DRIVE = "c:"
#The name of the user this script is going to run as in task scheduler, as labeled under C:\Users
USER = "Administrator.lan"
USE_RECVLOG = True
USE_SENDLOG = True
PWD = Path(ROOT_DRIVE + "/scripts/TReport/")
LOG_PATH = "/Program Files (x86)/GFI/FaxMaker/logs"
RECV_LOG = "/rcvlog.fmlogger.txt"
SEND_LOG = "/sendlog.fmlogger.txt"
RECV_PATH = Path(ROOT_DRIVE + LOG_PATH + RECV_LOG)
SEND_PATH = Path(ROOT_DRIVE + LOG_PATH + SEND_LOG)
SKEL_SEND = Path("./skel_send.html")
SKEL_RECV = Path("./skel_recv.html")
RUNTIME_DIR = Path("c:/Users/" + USER + "/AppData/Roaming/" + APP_AUTHOR + "/" + APP_NAME)
RUNTIME_SETTINGS = "C:\\Users\\" + USER + "\\AppData\\Roaming\\" + APP_AUTHOR + "\\" + APP_NAME + "\\" + "settings.db"
# adjust this value to the number of faxes you get/send per scheduled task interval
UPDATE_SCAN_LENGTH = 255
SEND_OUT_FOLDER = "s:/transmission_reports/sent/"
RECV_OUT_FOLDER = "s:/transmission_reports/received/"