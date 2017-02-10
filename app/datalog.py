import numpy as np
import datetime as dt
import pandas as pa
import time
#import ipdb
import signal
import thread
import logging
import atexit
import settings
import os

# i2c io pins
P_SCK  = 3
P_SDA  = 2
P_BAUD = 50000

# sensor data
SENSOR_BASEID  = 0x48
SENSOR_DATALEN = 2

# i2c commands for pigpio software i2c
I2C_END      = 0
I2C_START    = 2
I2C_STOP     = 3
I2C_SET_ADDR = 4
I2C_READ     = 6

if settings.settings.fridgeLogging:
    try:
        import pigpio
    except:
        logging.fatal("PIGPIO library could not be loaded, install PIGPIO to read sensor data or disable data logging in the settings!")
        exit()


class DataLogger:

    def __init__(self):
        self.ioif = None
        self.logging = True
        signal.signal(signal.SIGINT, self.cleanup)
        logging.info("Data Logger created")
        thread.start_new_thread(self.log_data, ())
        #self.log_data()

    def log_data(self):

        # pigpio
        self.ioif = pigpio.pi()

        # software i2c
        try:
            self.ioif.bb_i2c_open(P_SDA, P_SCK, P_BAUD)
        except:
            logging.error("bus already open")
            self.ioif.bb_i2c_close(P_SDA)
            self.ioif.bb_i2c_open(P_SDA, P_SCK, P_BAUD)

        logging.info("Data Logger started")

        log = 0
        data_fast = np.zeros(8)
        data_perm = np.zeros(8)
        n_fast = 1
        n_perm = 1
        while logging:
            logging.info("Data Logger logging")
            columns = list(("time", ))

            for i in range(SENSOR_BASEID, SENSOR_BASEID + 8):
                (count, data) = self.ioif.bb_i2c_zip(P_SDA, [I2C_SET_ADDR, i, I2C_START, I2C_READ, SENSOR_DATALEN, I2C_STOP, I2C_END])
                columns.append(str(i))
                if count > 1:
                    read = ((data[0] << 8) & 0xFF00) + (data[1])
                    read = read / 256.0
                    if read > 127:
                        read -= 256
                    data_fast[i-SENSOR_BASEID] += read
                    data_perm[i-SENSOR_BASEID] += read 
                else:
                    data_fast[i-SENSOR_BASEID] = np.nan
                    data_perm[i-SENSOR_BASEID] = np.nan
                time.sleep(0.05)

            infoline = np.empty((1, 9), dtype=object)

            if n_fast % 10 == 0:
                infoline[0, 1:9] = data_fast[0:8] / n_fast
                n_fast = 0
                infoline[0, 0] = dt.datetime.now()
                pdataline = pa.DataFrame.from_records(infoline, columns=columns)
                self.savetofile(False, pdataline)
                data_fast = np.zeros(8)

            if n_perm % 100 == 0:
                infoline[0, 1:9] = data_perm[0:8] / n_perm
                n_perm = 0
                infoline[0, 0] = dt.datetime.now()
                pdataline = pa.DataFrame.from_records(infoline, columns=columns)
                self.savetofile(True, pdataline)
                data_perm = np.zeros(8)

            n_fast += 1
            n_perm += 1
            

    def savetofile(self, permanent, data):

        if permanent:
            date = dt.datetime.now().strftime('%Y%m%d')
            exists = os.path.isfile('app/static/logdata_' + date + '.csv')
            with open('app/static/logdata_' + date + '.csv', 'a+') as f:
                data.to_csv(f, header=not exists, index=False)
        else:
            exists = os.path.isfile('/tmp/baroness_logdata_fast.csv')
            with open('/tmp/baroness_logdata_fast.csv', 'a+') as f:
                data.to_csv(f, header=not exists, index=False)

    def cleanup(self):
        self.logging = False
        logging.info("Data logger closed")
        self.ioif.bb_i2c_close(P_SDA)

if __name__ == "__main__":

    #for standalone mode
    print "creating datalogger"
    logger = DataLogger()
    while(1):
        time.sleep(1)
