import time
import csv
import math
import xlrd

import numpy as np
import argparse
import os
from reconsiliation.reed_solomon import ReedSolomon

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Data reconsiliation using Reed Solomon.')
parser.add_argument('--datapath', required=True, help='Path to the quantification directory')
parser.add_argument('--destination', required=True, help='Path for the result destination')
args = parser.parse_args()

start3=time.time()
fooRS = ReedSolomon()
namafile2 = os.path.join(args.datapath, 'Kuantifikasi_Node.csv')
RSSI3 = []

with open(namafile2) as f:
    dataalice = csv.reader(f)
    for row in dataalice:
        RSSI3.append(row)
        
RSSI3 = np.array(RSSI3)
rss_node = []
rss_node1 = []
for i in range(len(RSSI3)):
    rss_node.append(int(RSSI3[i][0]))
nilailebih = (len(rss_node) % 6)
jmlblok = math.floor(len(rss_node)/6)
for i in range(0, (len(rss_node)-nilailebih)):
    rss_node1.append(int(rss_node[i]))
rss_node = []
for blok in range(0, jmlblok):
    tmp = []
    if blok == 0:
        tmp.extend(rss_node1[0:6])
    else:
        tmp.extend(rss_node1[6*blok:6*(blok+1)])
    rss_node.append(tmp)
    np.savetxt(os.path.join(args.destination,'Split_Hasil_Kuan_Node.csv'), rss_node, delimiter=',', fmt='%i')
bit=[]
hasil=[]
bit1=[]
decods=[]
with open(os.path.join(args.destination,'Split_Hasil_Kuan_Node.csv'), 'r') as source:
    reader = csv.reader(source)
    for line in reader:
        bit.append(line)
        tMesg=line
        tSize = 25
        # encode the message
        tCode = fooRS.RSEncode(tMesg, tSize)
        hasil.append(tCode)
        np.savetxt(os.path.join(args.destination,'Encoding_Node.csv'), hasil, delimiter=',', fmt='%i')
#ubah data ke dalam bentuk bit
bita=[]
with open(os.path.join(args.destination,'Encoding_Node.csv'), 'r') as source:
        reader = csv.reader(source)
        for line1 in reader:
                bita.append(line1)
bitb = np.array(bita)
rssa=[]
for i in range (len(bita)):
        for j in range(31):
                rssa.append(int(bitb[i][j]))     

A=rssa
#print("\n banyak rss alice:")
#print(len(A))
rata=np.mean(A)
#print("\nProses Perhitungan rata-rata:")
#print(rata)

bit_node=[]
for j in range(len(A)):
        if A[j]<=rata:
              bit_node.append(0)
        else:
                bit_node.append(1)
np.savetxt(os.path.join(args.destination,'Bit_Encoding_Node.csv'), bit_node, delimiter=',', fmt='%i')
file = os.path.join(args.destination,'Bit_Encoding_Node.csv')
rssb = []
with open(file) as f:
        datanode = csv.reader(f)
        for row in datanode:
                rssb.append(row)
rssb = np.array(rssb)
rssc = []
rssd = []
for i in range(len(rssb)):
        rssc.append(int(rssb[i][0]))
nilailebih1 = (len(rssc)%31)
jmlhblok = math.floor(len(rssc)/31)
for i in range(0, (len(rssc)-nilailebih1)):
        rssd.append(int(rssc[i]))
rssc = []
for blok in range(0, jmlhblok):
        tmp = []
        if blok == 0:
                tmp.extend(rssd[0:31])
        else:
                tmp.extend(rssd[31*blok:31*(blok+1)])
        rssc.append(tmp)
#print(rssc)
np.savetxt(os.path.join(args.destination,'Split_Bit_Encoding_Node.csv'), rssc, delimiter=',', fmt='%i')

workbook = xlrd.open_workbook(os.path.join(args.destination, 'Blok_Yang_Dihapus.xls'), on_demand = True)
worksheet = workbook.sheet_by_name('hapusblok')
first_row = [] # Header
for col in range(0,worksheet.ncols):
    first_row.append( worksheet.cell_value(0,col) )
    # transform the workbook to a list of dictionnaries
hapusbchbob=[]
for row in range(1, worksheet.nrows):
    elm = {}
    for col in range(1):
        elm=worksheet.cell_value(row,col)
    hapusbchbob.append(int(elm-1))
#print(hapusbchbob)
hapusbchbob.sort(reverse=True)
for i in range(0,len(hapusbchbob)):
	a = int(hapusbchbob[i])
	del bita[a]

with open(os.path.join(args.destination, 'Node_After_Hapus_Blok.csv'), 'w',newline='') as fp:
    a=csv.writer(fp,delimiter=',')
    a.writerows(bita)
F=[]
with open(os.path.join(args.destination, 'Node_After_Hapus_Blok.csv'), 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        F.append(row)
G=[]
with open(os.path.join(args.destination, 'Gateway_After_Hapus_Blok.csv'), 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        G.append(row)
data_hasil=[]
for i in range(len(F)):
        for j in range(len(F[i])):
                if F[i][j]!=G[i][j]:
                       data_hasil.append(F[i][j])
                else:
                        data_hasil.append(G[i][j])
with open(os.path.join(args.destination, 'Hasil_Node_After_Hapus_Blok.csv'), 'w',newline='') as f:
    writer=csv.writer(f)
    writer.writerows([[row] for row in data_hasil])
namafile2 = os.path.join(args.destination, 'Hasil_Node_After_Hapus_Blok.csv'   )            
RSSI = []
with open(namafile2) as f:
    dataalice = csv.reader(f)
    for row in dataalice:
        RSSI.append(row)
RSSI = np.array(RSSI)
rss_node = []
rss_node1 = []
for i in range(len(RSSI)):
    rss_node.append(int(RSSI[i][0]))
nilailebih = (len(rss_node) % 31)
jmlblok = math.floor(len(rss_node)/31)
for i in range(0, (len(rss_node)-nilailebih)):
    rss_node1.append(int(rss_node[i]))                       
decods = []
tSize = 25
for blok in range(0, jmlblok):
    tmp = []
    if blok == 0:
        tmp.extend(rss_node1[0:31])
    else:
        tmp.extend(rss_node1[31*blok:31*(blok+1)])
    rss_node.append(tmp)
    tMesg1 = fooRS.RSDecode(tmp, tSize)
    decods.append(tMesg1)
    np.savetxt(os.path.join(args.destination, 'Decoding_Node.csv'), decods, delimiter=',', fmt='%i')
bit2 = []
with open(os.path.join(args.destination, 'Decoding_Node.csv'), 'r') as source:
    reader1 = csv.reader(source)
    for line1 in reader1:
        bit2.append(line1)
bit2 = np.array(bit2)
rss3 = []
for i in range(len(bit2)):
    for j in range(6):
        rss3.append(int(bit2[i][j]))
rss4 = []
for k in range(len(rss3)):
        if rss3[k] == 48:
                rss4.append(0)
        elif rss3[k] == 49:
                rss4.append(1)
        else:
                rss4.append(rss3[k])
np.savetxt(os.path.join(args.destination, 'Decoding_Node_Tanpa_Parity.csv'), rss4, delimiter=',', fmt='%i')

end3=time.time()
waktu_RS = end3-start3
print('-------------------')
print('Error Correction Berhasil')
print('-------------------')