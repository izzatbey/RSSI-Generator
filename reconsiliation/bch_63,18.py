import os
import time


print("\nProses Error Koreksi BCH..")
startbch=time.time()
os.system('octave bch.m')

endbch=time.time()
print('waktu komputasi bch={}second'.format(endbch-startbch))