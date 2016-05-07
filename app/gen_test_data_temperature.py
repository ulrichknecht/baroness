import numpy as np
import datetime as dt
import pandas as pa
import ipdb
testdata = np.empty((14400, 7), dtype=object)

#ipdb.set_trace()

for n, line in enumerate(reversed(testdata)):
    a = (dt.datetime.now() - dt.timedelta(seconds=(300*n)))
    line[0] = a
    line[1] = np.sin(2.0 * np.pi *20.0 / 14400 * n) * 5 + np.sin(2.0 * np.pi * 2.0 / 14400 * n) * 1.4 + 10
    line[2] = np.sin(2.0 * np.pi *20.0 / 14400 * n) * 4 + np.sin(2.0 * np.pi * 2.0 / 14400 * n) * 1.4 + 13
    line[3] = np.sin(2.0 * np.pi *20.0 / 14400 * n) * 3 + np.sin(2.0 * np.pi * 2.0 / 14400 * n) * 1.4 + 15
    line[4] = np.sin(2.0 * np.pi *30.0 / 14400 * n) * 5 + np.sin(2.0 * np.pi * 3.5 / 14400 * n) * 1 + 10
    line[5] = np.sin(2.0 * np.pi *30.0 / 14400 * n) * 4 + np.sin(2.0 * np.pi * 3.5 / 14400 * n) * 1 + 13
    line[6] = np.sin(2.0 * np.pi *30.0 / 14400 * n) * 3 + np.sin(2.0 * np.pi * 3.5 / 14400 * n) * 1 + 15

pdata = pa.DataFrame.from_records(testdata,columns=("time","1","2","3","4","5","6"))
print pdata

pdata.to_csv("static/testdata.csv", index=False)
#np.savetxt("static/testdata.csv", testdata)

readdata = pa.read_csv("static/testdata.csv")
print readdata
