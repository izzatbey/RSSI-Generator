import csv
import subprocess
import time


startnist = time.time()
command = 'gcc -o "C:/Users/MHK/Documents/Folder Izzat/rssi-generator/encryption/NIST-TestALICE128" "C:/Users/MHK/Documents/Folder Izzat/rssi-generator/encryption/NIST-TestALICE128.c"'
subprocess.run(command, shell=True)

command = "C:/Users/MHK/Documents/Folder Izzat/rssi-generator/encryption/NIST-TestALICE128"
subprocess.run(command, shell=True)

indeks = []
indek = []

time.sleep(1)

with open("C:/Users/MHK/Documents/Folder Izzat/rssi-generator/encryption/sudahujinist_Alice.csv", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        indeks.append(row)
prindek = []
for i in range(0, len(indeks)):
    indek.append(int(indeks[i][0]))
    prindek.append(int(indeks[i][0]) + 1)
endnist = time.time()
print('===========~~~~~~~~~~~=========~~~~~~~~~~~~~~==============\n')
print('NIST Hasil prioritas index',prindek)
print('Waktu Proses Uji NIST : ', endnist - startnist)