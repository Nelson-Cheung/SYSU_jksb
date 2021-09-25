import datetime
import getopt
import sys
import time
from utils import *

def print_help_msg():
    print("python3 sysu.py --netid=your_netid --passwd=your_password [--hour=your_hour] [--minute=your_minute]\n" \
          "e.g. python3 sysu.py --netid=NelsonCheung --passwd=ilovesysu --hour=6 --minute=30" \
          )

try:
    opts, args = getopt.getopt(sys.argv[1:], shortopts="", longopts=["help", "netid=", "passwd=", "hour=", "minute="])
except getopt.GetoptError:
    print_help_msg()
    sys.exit(-1)

hour = 10
minute = 00
netid = None
passwd = None

for opt, arg in opts:
    if opt == "--help":
        print_help_msg()
        sys.exit(0)
    elif opt == "--netid":
        netid = arg
    elif opt == "--passwd":
        passwd = arg
    elif opt == "--hour":
        try:
            hour = int(arg)
        except ValueError:
            print("wrong type for hour")
            # print_help_msg()
            sys.exit(-1)

        if hour < 0 or hour > 24:
            print("wrong type for hour")
            # print_help_msg()
            sys.exit(-1)
    elif opt == "--minute":
        try:
            minute = int(arg)
        except ValueError:
            print("wrong type for minute")
            # print_help_msg()
            sys.exit(-1)

        if minute < 0 or minute > 60:
            print("wrong type for hour")
            # print_help_msg()
            sys.exit(-1)

if netid is None or passwd is None:
    print("netid and passwd must be provided")
    print_help_msg()
    sys.exit(-1)

flag = True
day = -1

while True:
    time.sleep(1)
    now = datetime.datetime.now()

    if now.day != day:
        flag = True
        day = now.day

    if flag and (now.hour > hour or (now.hour == hour and now.minute >= minute)):
        flag = False
        do_jksb(netid, passwd)
