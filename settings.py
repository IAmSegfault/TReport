from pathlib import Path
APP_NAME = "TReport"
APP_AUTHOR = "TReport"
ROOT_DRIVE = "c:"
USER = "Administrator"
LOG_PATH = "/Program Files (x86)/GFI/FaxMaker/logs"
RECV_LOG = "/rcvlog.fmlogger.txt"
SEND_LOG = "/sendlog.fmlogger.txt"
RECV_PATH = Path(ROOT_DRIVE + LOG_PATH + RECV_LOG)
SEND_PATH = Path(ROOT_DRIVE + LOG_PATH + SEND_LOG)
SKEL_SEND = Path("./skel_send.html")
SKEL_RECV = Path("./skel_recv.html")
RUNTIME_DIR = Path("c:/Users/" + USER + "/AppData/Roaming/" + APP_AUTHOR + "/" + APP_NAME)
RUNTIME_SETTINGS = Path("c:/Users/" + USER + "/AppData/Roaming/" + APP_AUTHOR + "/" + APP_NAME + "/" + "settings.db")

LOG_TEST = Path("./rcvlog.fmlogger.txt")