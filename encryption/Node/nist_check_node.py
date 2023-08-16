import csv
import subprocess
import time


subprocess.Popen('./NIST-Test128')

indeks=[]
indek=[]

#time.sleep(1)
with open('NISTHash1.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        indeks.append(row)
prindek=[]
for i in range(0,len(indeks)):
    indek.append(int(indeks[i][0]))
    prindek.append(int(indeks[i][0])+1)
print('NIST Hasil prioritas index',prindek)

print('-------------------')
print('Uji NIST Berhasil')
print('-------------------')