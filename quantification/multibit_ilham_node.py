import time
import pandas as pd
import numpy as np
import argparse
import os

class Multibit:
    def __init__(self):
        self.__dataBefore = 0
        self.__pointRange = 0
        self.__resultBiner = np.zeros([2,1])
    def setDataBefore(self, dataBefore):
        self.__dataBefore  = dataBefore
    def getDataBefore(self):
        return self.__dataBefore
    def setPointRange(self, pointRange):
        self.__pointRange = pointRange
    def getPointRange(self):
        return self.__pointRange
    def baseData(self):
        if self.__pointRange >= 0.9325:
            self.__resultBiner[0][0] = 0
            self.__resultBiner[1][0] = 0
        elif self.__pointRange >= 0.875 and self.__pointRange < 0.9325:
            self.__resultBiner[0][0] = 0
            self.__resultBiner[1][0] = 0
        elif self.__pointRange >= 0.8125 and self.__pointRange < 0.875:
            self.__resultBiner[0][0] = 0
            self.__resultBiner[1][0] = 0
        elif self.__pointRange >= 0.75 and self.__pointRange < 0.8125:
            self.__resultBiner[0][0] = 1
            self.__resultBiner[1][0] = 0
        elif self.__pointRange >= 0.6875 and self.__pointRange < 0.75:
            self.__resultBiner[0][0] = 1
            self.__resultBiner[1][0] = 0
        elif self.__pointRange >= 0.625 and self.__pointRange < 0.6875:
            self.__resultBiner[0][0] = 1
            self.__resultBiner[1][0] = 0
        elif self.__pointRange >= 0.5625 and self.__pointRange < 0.625:
            self.__resultBiner[0][0] = 1
            self.__resultBiner[1][0] = 0
        elif self.__pointRange >= 0.5 and self.__pointRange < 0.5625:
            self.__resultBiner[0][0] = 1
            self.__resultBiner[1][0] = 1
        elif self.__pointRange >= 0.4375 and self.__pointRange < 0.5:
            self.__resultBiner[0][0] = 1
            self.__resultBiner[1][0] = 1
        elif self.__pointRange >= 0.375 and self.__pointRange < 0.4375:
            self.__resultBiner[0][0] = 1
            self.__resultBiner[1][0] = 1
        elif self.__pointRange >= 0.3125 and self.__pointRange < 0.375:
            self.__resultBiner[0][0] = 1
            self.__resultBiner[1][0] = 1
        elif self.__pointRange >= 0.25 and self.__pointRange < 0.3125:
            self.__resultBiner[0][0] = 0
            self.__resultBiner[1][0] = 1
        elif self.__pointRange >= 0.1875 and self.__pointRange < 0.25:
            self.__resultBiner[0][0] = 0
            self.__resultBiner[1][0] = 1
        elif self.__pointRange >= 0.125 and self.__pointRange < 0.1875:
            self.__resultBiner[0][0] = 0
            self.__resultBiner[1][0] = 1
        elif self.__pointRange >= 0.0625 and self.__pointRange < 0.125:
            self.__resultBiner[0][0] = 0
            self.__resultBiner[1][0] = 1
        elif self.__pointRange < 0.0625:
            self.__resultBiner[0][0] = 0
            self.__resultBiner[1][0] = 0

        return self.__resultBiner

parser = argparse.ArgumentParser(description='Data quantification using Multibit process.')
parser.add_argument('--datapath', required=True, help='Path to the preprocess directory')
parser.add_argument('--filename', required=True, help='filename of the preprocess')
parser.add_argument('--destination', required=True, help='Path for the result destination')
args = parser.parse_args()

data_file_path = os.path.join(args.datapath, args.filename)

start = time.time()    
dataTmp = pd.read_csv(data_file_path, sep=",", header=None)
dataTmp.columns = ['a']
maxSeq = 128
dataSetFull = [dataTmp['a'][i * maxSeq:(i + 1) * maxSeq] for i in range(25)]

arrObj = np.zeros([len(dataTmp) * 2, 1])

for seq in range(len(dataSetFull)):
    countAllData = len(dataSetFull[seq])
    if countAllData == 0:
        continue  # Skip this sequence if it has no data

    uniqueData = dataSetFull[seq].value_counts().index.tolist()
    if len(uniqueData) == 0:
        continue  # Skip if there are no unique values

    dataFreq = dataSetFull[seq].value_counts()
    final = np.zeros([len(uniqueData), 5])

    # Assign the first cumulative probability safely
    if len(uniqueData) > 0:
        final[0][3] = final[0][2]

    # Continue with the cumulative probability calculation
    for i in range(1, len(uniqueData)):
        final[i][3] = final[i - 1][3] + final[i][2]

    # Process data normally
    iterator = 0 + (seq * maxSeq)
    if iterator >= len(arrObj):
        print(f"Error: iterator {iterator} out of bounds for arrObj with size {len(arrObj)}")
        break  # Stop to avoid further issues
    for i in range(countAllData):
        for j in range(len(uniqueData)):
            if dataTmp['a'][i + (maxSeq * seq)] == final[j][0]:
                objectInitial = Multibit()
                final[j][4] = 1 - float(final[j][3])
                objectInitial.setPointRange(final[j][4])
                arrObj[iterator] = objectInitial.baseData()[0]
                arrObj[iterator + 1] = objectInitial.baseData()[1]
                iterator += 2

np.savetxt(os.path.join(args.destination, 'quan_alice1.csv'), arrObj, delimiter=';', fmt='%i')
end = time.time()
timeMultibit = end - start

print('-------------------')
print('Kuantisasi Berhasil')
print("waktu komputasi kuantisasi = ", timeMultibit)
print('-------------------')