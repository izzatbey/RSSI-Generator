import csv
import time
import numpy as np
from scipy.signal import savgol_filter
import argparse
import os

# Initialization Subjects
w = 999
p = 10
RSSI=[]
RSSI2=[]
# Parse command-line arguments
parser = argparse.ArgumentParser(description='Preprocess data using savitzky golay.')
parser.add_argument('--datapath', required=True, help='Path to the datasets directory')
parser.add_argument('--destination', required=True, help='Path for the result destination')
args = parser.parse_args()
data_file_path = os.path.join(args.datapath, "data_rss_node.csv")

start1 = time.time()


with open (data_file_path) as f:
    data=csv.reader(f)
    for row in data:
        RSSI.append(row)
RSSI=np.array(RSSI)

for i in range(len(RSSI)):
    RSSI2.append(int(RSSI[i][0]))
RSSI2=np.array(RSSI2)
RSSI=RSSI2.reshape(1000)

destination_file_path = os.path.join(args.destination, 'Golay_Node.csv')
X_smooth_1 = savgol_filter(RSSI, w, polyorder = p)
np.savetxt(destination_file_path, X_smooth_1, delimiter=",", fmt='%10.5f')

end1 = time.time()
waktu_golay = end1-start1
print('------------------')
print('Preproses Berhasil')
print('------------------')
print ("Lama Eksekusi :",waktu_golay,"detik")