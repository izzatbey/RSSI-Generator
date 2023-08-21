import math
import argparse
import os
import time
import numpy as np
import csv

from comm.socket_comm import socketrecv, socketsend, init_socket

def load_data_from_csv(file_path):
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip the header
        nilaiasli = [float(row[0]) for row in csv_reader]
    return np.array(nilaiasli)

def quantize_data(data, block_size=128):
    jana_alice = [str(value) for value in data]
    nilailebih = len(jana_alice) % block_size
    jmlblok = math.floor(len(jana_alice) / block_size)
    jana_alice1 = [str(jana_alice[i]) for i in range(len(jana_alice) - nilailebih)]
    
    quantized_data = []
    for blok in range(0, jmlblok):
        tmp = jana_alice1[128 * blok:128 * (blok + 1)] if blok != 0 else jana_alice1[0:128]
        quantized_data.append(tmp)
    
    return quantized_data

def perform_quantization(quantized_data):
    hasiljana = []
    for jana_alice1 in quantized_data:
        L = [(jana_alice1[i], i) for i in range(len(jana_alice1))]
        L.sort()
        nilairss, addressing = zip(*L)
        p = len(nilairss)
        N = math.log(p, 2)
        a = 2
        M = 2 ** a if a <= N else 2
        
        bb = M
        filter = len(nilairss) % bb
        if filter != 0:
            pengurangan = len(nilairss) - filter
            nilairss1 = np.array(nilairss[:pengurangan])
        else:
            nilairss1 = np.array(nilairss)
            
        aa = int(len(nilairss1) / bb)
        x = nilairss1.reshape(bb, aa).T
        
        for i in range(bb):
            for j in range(len(x)):
                x[j][i] = 4 - i
        
        x1 = x.T
        x2 = x1.reshape(aa * bb, 1)
        bentukawal = [int(x2[i]) for i in range(len(x2))]
        
        unsort = sorted(zip(addressing, bentukawal))
        addressing, bitbit = zip(*unsort)
        
        hasil = []
        for i in range(len(bitbit)):
            if bitbit[i] == 4:
                hasil.extend([1, 0])
            elif bitbit[i] == 3:
                hasil.extend([1, 1])
            elif bitbit[i] == 2:
                hasil.extend([0, 1])
            elif bitbit[i] == 1:
                hasil.extend([0, 0])
        
        hasiljana.append(hasil)
        print("hasil kuantisasi \n", hasil)
        print("jumlah key sekarang ", len(hasil))
    
    return hasiljana

def save_quantized_data_as_csv(quantized_data, file_path):
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)  # Write the header
        
        for data in quantized_data:
            csv_writer.writerow(data)

mulai = time.time()
start_jana = time.time()

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Data quantification using Jana Multibit process.')
parser.add_argument('--datapath', required=True, help='Path to the preprocess directory')
parser.add_argument('--filename', required=True, help='filename of the preprocess')
parser.add_argument('--destination', required=True, help='Path for the result destination')
args = parser.parse_args()

data_file_path = os.path.join(args.datapath, args.filename)

preprocess_data = load_data_from_csv(data_file_path)

quantized_data = quantize_data(preprocess_data)
hasiljana = perform_quantization(quantized_data)

hasilakhir = [bit for data in hasiljana for bit in data]

hasil_file_path = os.path.join(args.destination, 'Kuantifikasi_janamultibit_node.csv') 
save_quantized_data_as_csv(hasiljana, hasil_file_path)

end_jana = time.time()
time_jana = end_jana - start_jana
kgrkuan = len(hasilakhir) * (end_jana - start_jana)

print('KGR = %f' % kgrkuan)
print('waktu komputasi kuantisasi = {} seconds'.format(end_jana - start_jana))

# socketsend(hasil_file_path, init_socket())
# socketrecv(init_socket())
print("Kuantisasi Node Berhasil")
