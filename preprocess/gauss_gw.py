import time
import csv
import xlrd
import numpy as np
import argparse
import os

parser = argparse.ArgumentParser(description='Data quantification using Gaussian process.')
parser.add_argument('--datapath', required=True, help='Path to the raw directory')
parser.add_argument('--filename', required=True, help='filename of the raw')
parser.add_argument('--destination', required=True, help='Path for the result destination')
args = parser.parse_args()

data_file_path = os.path.join(args.datapath, args.filename)

start1 = time.time()
#import data rssival_bob
data_y=[]
with open(data_file_path) as f:
    databob = csv.reader(f)
    for row in databob:
        data_y.append(row)
RSSI=[]
RSSI=np.array(data_y)
pjg_bob_sebelum = len(RSSI)

#data sequence
data_x1 = []
wb = xlrd.open_workbook('data_x.xls')
sh = wb.sheet_by_index(0)
for h in range(0,sh.nrows):
    data_x = int(sh.cell_value(rowx = h, colx = 0))
    data_x1.append(data_x)
    
data_x1 = np.asarray(data_x1,dtype='int64')
pjgdata_x1=sum(data_x1)

#####reshape RSSI
rss_bob=[]
for i in range(len(RSSI)):
    rss_bob.append(int(RSSI[i][0]))


bawah=128 #jumlah baris
samping=int(len(rss_bob)/bawah) #jumlah data yang diprocess

#-----reshape
bob=np.array(rss_bob)
rssival_bob=bob.reshape(samping,bawah).T
pjg_bob_sesudah = len(rssival_bob)

for j in range(0, 25):
    A = [len(data_x1), pjgdata_x1, sum(data_x1**2)]
    A11, A12, A13 = A
    A = [A12, A13, sum(data_x1**3)]
    A21, A22, A23 = A
    A = [A22, A23, sum(data_x1**4)]
    A31, A32, A33 = A

hasilB11=[]
for i in range(0,25):
    nilaibaris=0
    for j in range (0,128):
        nilaibaris=(nilaibaris+rssival_bob[j][i])
    hasilB11.append(nilaibaris)

hasilB21=[]
hasil_awalb21=[]
for i in range(0,25):
    nilaibaris=0
    nilaisum = 0
    hasil_awalb21=[]
    for j in range (0,128):
        nilaibaris=(data_x1[j]*rssival_bob[j][i])
        hasil_awalb21.append(nilaibaris)
        nilaisum = sum (hasil_awalb21)
    hasilB21.append(nilaisum)

hasilB31=[]
hasil_awalb31=[]
for i in range(0,25):
    nilaibaris=0
    nilaisum = 0
    hasil_awalb31=[]
    for j in range (0,128):
        nilaibaris=((data_x1[j]**2)*rssival_bob[j][i])
        hasil_awalb31.append(nilaibaris)
        nilaisum = sum (hasil_awalb31)
    hasilB31.append(nilaisum)

##======GAUSS JORDAN=============
hasilgauss = []
for i in range (0,25):
    A = np.array ([[A11, A12, A13, (hasilB11[i])],
                   [A21, A22, A23, (hasilB21[i])],
                   [A31, A32, A33, (hasilB31[i])]])
     
    #===== METODE ELIMINASI GAUSS =========#
    n=len(A)
    
    #~~~~~~proses triangularisasi~~~~~~~~~~#
    for k in range(0,n-1):

        for i in range(k+1,n):
            m=A[i][k]/A[k][k]
             
            for j in range(0,n+1):
                hasil= A[i][j] - m*A[k][j] #type data int 64 bit
                A[i][j]=hasil.astype(np.int32) #type data int 32 bit

    #~~~~~~proses substitusi-mundur~~~~~~~~#
    X = np.zeros((n,1))
    X[n-1][0]=A[n-1][n]/A[n-1][n-1]
    for j in range(n-2,-1,-1):
        S=0
        for i in range(j+1,n):
            S=S+A[j][i]*X[i][0]
            X[j][0]=(A[j][n]-S)/A[j][j]
    #======================================#
    # print ('X=',X)
    for j in range(0,128):
        y=X[0]+(X[1]*j+1)+(X[2]*(j**2))
        hasilgauss.append(int(y))

hasilgauss=np.array(hasilgauss)
hasilgauss=hasilgauss.reshape(3200,1)
np.savetxt(os.path.join(args.destination, "reg_bob1.csv"), hasilgauss, delimiter=',')
end1 = time.time()
timeGauss = end1 - start1

print('------------------')
print('Preproses Berhasil')
print("waktu komputasi = ", timeGauss)
print('------------------')