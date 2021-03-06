import serial
import signal
from pynput.keyboard import Key, Controller
keyboard = Controller()
import time
import os

ser = serial.Serial('COM4', 9600, timeout=.1)
ser.flushInput()

def elevate():
    import ctypes, win32com.shell.shell, win32event, win32process
    outpath = r'%s\%s.out' % (os.environ["TEMP"], os.path.basename(__file__))
    if ctypes.windll.shell32.IsUserAnAdmin():
        if os.path.isfile(outpath):
            sys.stderr = sys.stdout = open(outpath, 'w', 0)
        return
    with open(outpath, 'w+', 0) as outfile:
        hProc = win32com.shell.shell.ShellExecuteEx(lpFile=sys.executable, \
            lpVerb='runas', lpParameters=' '.join(sys.argv), fMask=64, nShow=0)['hProcess']
        while True:
            hr = win32event.WaitForSingleObject(hProc, 40)
            while True:
                line = outfile.readline()
                if not line: break
                sys.stdout.write(line)
            if hr != 0x102: break
    os.remove(outpath)
    sys.stderr = ''
    sys.exit(win32process.GetExitCodeProcess(hProc))

elevate()
while True:
    try:
        if (ser.inWaiting()):
            line = ser.readline();
            line = line.decode("utf-8")
            print(line);
            keyboard.press('j')
            time.sleep(0.15)
            keyboard.release('j')
    except:
        print("Keyboard Interrupt")
        break
