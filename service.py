import os
import sys
import syslog

from daemon import daemon

from server import Server

WORKDIR = os.getcwd()

def stop():
    file = open(WORKDIR +"/createDaemon.log", "r")
    pid = int(file.read())
    os.kill(pid, 9)
    print("Stop")
    # syslog.syslog("Server has been stopped.")


def start():
    print("Start")
    syslog.syslog("Server has been started.")
    with daemon.DaemonContext():
        open(WORKDIR + "/createDaemon.log", "w").write(str(os.getpid()) + "\n")
        server = Server()


def restart():
    stop()
    start()


if len(sys.argv) != 2:
    print("Usage details: {} start/stop/restart".format(sys.argv[0]))
    sys.exit

if sys.argv[1] == "start":
    start()
elif sys.argv[1] == "stop":
    stop()
elif sys.argv[1] == "restart":
    restart()
else:
    print("Invalid argument. \nUsage details: {} start/stop/restart".format(sys.argv[0]))
