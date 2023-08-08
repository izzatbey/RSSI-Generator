import argparse
import csv
import os
import time
import numpy as np

def quantize_rssi(rssi, bb=4):
    rss = []
    for row in rssi:
        rss.append(float(row[0]))

    L = [(rss[i], i) for i in range(len(rss))]
    L = sorted(L, reverse=False)

    aa = int(len(rss) / bb)
    nilairss, address = zip(*L)
    address = np.array(address)
    address = address.reshape(bb, aa).T

    for i in range(bb):
        for j in range(len(address)):
            if i == 0:
                rss[address[j][i]] = 1
            elif i == 1:
                rss[address[j][i]] = 2
            elif i == 2:
                rss[address[j][i]] = 3
            elif i == 3:
                rss[address[j][i]] = 4

    rss[225:250] = []
    rss[449:474] = []
    rss[673:698] = []
    rss[897:922] = []

    quantized_rss = []
    for val in rss:
        if val == 4:
            quantized_rss.extend('11')
        elif val == 3:
            quantized_rss.extend('10')
        elif val == 2:
            quantized_rss.extend('00')
        elif val == 1:
            quantized_rss.extend('01')

    quantized_rss[:900] = []
    return quantized_rss

def save_quantized_rssi(file_name, quantized_rssi):
    with open(file_name, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for val in quantized_rssi:
            csvwriter.writerow([val])
            
start = time.time()

# Parsing Arguments
parser = argparse.ArgumentParser(description='Data quantification using 2-Array in Gateway.')
parser.add_argument('--datapath', required=True, help='Path to the preprocess directory')
parser.add_argument('--filename', required=True, help='filename of the preprocess')
parser.add_argument('--destination', required=True, help='Path for the result destination')
args = parser.parse_args()

data_file_path = os.path.join(args.datapath, args.filename)

with open(data_file_path) as f:
    data = csv.reader(f)
    RSSI1 = np.array(list(data))

quantized_rssi_data = quantize_rssi(RSSI1)
save_quantized_rssi(os.path.join(args.destination, "Kuantifikasi_GW.csv"), quantized_rssi_data)

end = time.time()
waktu_kuantifikasi = end - start

print("Lama Eksekusi:", waktu_kuantifikasi, "detik")
print('-------------------')
print('Kuantisasi Berhasil')
print('-------------------')