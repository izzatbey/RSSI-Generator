import csv
import time
import numpy as np
import argparse
import os

#Initialization subject
start1 = time.time()
x=[]
RSSI2=[]
degrees = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Preprocess data using polynomial fitting.')
parser.add_argument('--datapath', required=True, help='Path to the datasets directory')
parser.add_argument('--destination', required=True, help='Path for the result destination')
args = parser.parse_args()
data_file_path = os.path.join(args.datapath, "data_rss_gateway.csv") 

with open (data_file_path) as f:
    data=csv.reader(f)
    for row in data:
        x.append(row)
x=np.array(x)
for i in range(len(x)):
    RSSI2.append(int(x[i][0]))
RSSI2=np.array(RSSI2)
x=RSSI2.reshape(3000)

y =  np.linspace(0, 3000, 3000)

for deg in degrees:
    destination_file_path = os.path.join(args.destination, f'Polyfit_GW_{deg}deg.csv')
    p = np.polyfit(y, x, deg)
    np.savetxt(destination_file_path, np.polyval(p,y) ,delimiter=",", fmt='%10.5f')

end1 = time.time()
waktu_pra = end1-start1
print('------------------')
print('Preproses Berhasil')
print('------------------')
print ("Lama Eksekusi :",waktu_pra,"detik")