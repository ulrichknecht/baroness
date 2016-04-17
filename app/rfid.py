try:
    import MFRC522
except:
    print "ERROR: Need MFRC522 Library to read RFID tags, disable RFID if no reader is present!"
    exit()
import signal
import thread
import time


class RFID:

    def __init__(self, callbackf):
        self.reader = MFRC522.MFRC522()
        signal.signal(signal.SIGINT, self.stop)
        self.callback = callbackf
        self.loop = True
        thread.start_new_thread(self.read, ())

    def read(self):
        while True:
            while self.loop:
                (status, tagtype) = self.reader.MFRC522_Request(self.reader.PICC_REQIDL)
                print "RFID Status:", status 
                if status == self.reader.MI_OK:
                    (status, uid) = self.reader.MFRC522_Anticoll()
                    if status == self.reader.MI_OK:
                        uids = "0x" + "".join(format(x, '02x') for x in uid)
                        print "RFID Detect:", uids      
                        self.stop()
                        self.callback(uids)
            while not self.loop:
                time.sleep(0.1)

    def start(self):
        print "RFID reader started"
        self.loop = True

    def stop(self):
        print "RFID reader stopped"
        self.loop = False
