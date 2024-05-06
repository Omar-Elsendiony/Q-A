from ast import Dict
import sys

from time import sleep
import threading
from _thread import interrupt_main
import sys
from io import StringIO


class CustomThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(CustomThread, self).__init__(*args, **kwargs)
        self._stopper = threading.Event()

    def stop(self):
        self._stopper.set()

    def stopped(self):
        return self._stopper.is_set()

    def run(self):
        sleep(5)
        while not self.stopped():
            interrupt_main()


def runCode(code: str, myglobals):
    # save the old stdout that is reserved
    oldStdOUT = sys.stdout
    # get the redirected output instance
    redirectedOutput = sys.stdout = StringIO()
    oldStdERR = sys.stderr
    redirectedOutput2 = sys.stderr = StringIO()
    # result is initially empty
    result = ""
    # there is error
    isError = False
    if (myglobals.get('res')):
        del myglobals['res']
    thread = CustomThread()
    try:
        thread.start()
        exec(code, myglobals)
        result = redirectedOutput.getvalue()
    except Exception as e:
        isError = True
        result = repr(e)
    except SystemExit as s:
        isError = True
        result = redirectedOutput2.getvalue()
    except KeyboardInterrupt as k:
        isError = True
        result = "timed out"
    thread.stop()
    if (myglobals.get('testcase')):
        del myglobals['testcase']
    sys.stdout = oldStdOUT
    sys.stderr = oldStdERR

    return result, isError
