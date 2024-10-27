import time
import csv
import numpy as np
import math
import argparse
import os

parser = argparse.ArgumentParser(description='Data preprocessing using Kalman process.')
parser.add_argument('--datapath', required=True, help='Path to the raw directory')
parser.add_argument('--filename', required=True, help='filename of the raw data')
parser.add_argument('--destination', required=True, help='Path for the result destination')
args = parser.parse_args()

data_file_path = os.path.join(args.datapath, args.filename)

start_kalman=time.time()

sinyal=[]
with open(data_file_path) as f:
	databob = csv.reader(f)
	for row in databob:
		sinyal.append(row)
  
RSSI=[]
RSSI=np.array(sinyal)

interval=0.007
rss_bob=[]
rss_bob1=[]
for i in range(len(RSSI)):
	rss_bob.append(int(RSSI[i][0]))
nilailebih = (len(rss_bob)%64)
jmlblok= math.floor(len(rss_bob)/64)
for i in range(0,(len(rss_bob)-nilailebih)):
	rss_bob1.append(int(rss_bob[i]))
	
rss_bob=[] #mengosongkan variabel

for blok in range(0,jmlblok):
	tmp=[]
	if blok == 0:
		tmp.extend(rss_bob1[0:64])
	else:
		tmp.extend(rss_bob1[64*blok:64*(blok+1)])
	rss_bob.append(tmp)
	
# print(rss_bob)
hasilkalman=[]
for i in range(0,jmlblok):
	rssival_bob=[]
	rssival_bob=np.array(rss_bob[i])
	rssival_bob=rssival_bob.reshape(4,16).T
##	print(rssival_bob)
	a=1 	#a posteri error estimate
	h=1
	R=1		#measurement error covariance matrix (noise)
	Q=0.01	#process noise covariance
	#=====estimasi awal=======#
	xaposteriori_0=0
	paposteriori_0=1
	#=========================#
	#deklarasi variabel untuk proses kalman filter
	xapriori=[]			#estimasi priori nilai x
	residual=[]
	papriori=[]			#estimasi nilai error
	k=[]				#nilai kalman gain
	paposteriori=[]
	xaposteriori=[]

	#proses kalman filtering
	rowa1=[]
	rowa2=[]
	rowa3=[]
	rowa4=[]
	rowa5=[]
	rowa6=[]
	##coba=[]
	for m in range(0,4):
		rowa1.append(a*xaposteriori_0)					#mencari XK(TU)
		rowa2.append(rssival_bob[0][m]-h*rowa1[m])	#mencari nilai zk-Hxk
		rowa3.append(a*a*paposteriori_0+Q)				#mencari PK(TU)
		rowa4.append(rowa3[m]/(rowa3[m]/rowa3[m]+R))	#mencari kalman gain(MU)
		rowa5.append(rowa3[m]*(1-rowa4[m]))				#mencari PK(MU)
		rowa6.append(rowa1[m]+rowa4[m]*rowa2[m])		#mencari XK(MU)
	##print coba
	xapriori.append(rowa1)
	residual.append(rowa2)
	papriori.append(rowa3)
	k.append(rowa4)
	paposteriori.append(rowa5)
	xaposteriori.append(rowa6)
	for j in range(1,16):
		rowa7=[]
		rowa8=[]
		rowa9=[]
		rowa10=[]
		rowa11=[]
		rowa12=[]
		for n in range(0,4):
			rowa7.append(xaposteriori[j-1][n])
			rowa8.append(rssival_bob[j][n]-h*rowa7[n])
			rowa9.append(a*a*paposteriori[j-1][n]+Q)
			rowa10.append(rowa9[n]/(rowa9[n]+R))
			rowa11.append(rowa9[n]*(1-rowa10[n]))
			rowa12.append(rowa7[n]+rowa10[n]*rowa8[n])
		xapriori.append(rowa7)
		residual.append(rowa8)
		papriori.append(rowa9)
		k.append(rowa10)
		paposteriori.append(rowa11)
		xaposteriori.append(rowa12)
	kal=np.array(xaposteriori)
	kbob=kal.T
	kalmanbob=kbob.reshape(4*16,1)
	hasilkalman.append(kalmanbob)
kalmanakir=[]

for i in range(0,jmlblok):
	for j in range(0,64):
		kalmanakir.append(int(hasilkalman[i][j]))
np.savetxt(os.path.join(args.destination,'hasilkalmanbob.csv'),kalmanakir,delimiter=',',fmt='%s')

end_kalman=time.time()
time_kalman=end_kalman-start_kalman

print('-------------------')
print('Kuantisasi Berhasil')
print("waktu komputasi kuantisasi = ", time_kalman, "detik")
print('-------------------')
# End Preprocess