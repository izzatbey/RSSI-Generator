import argparse
import csv
import os
import time
import numpy as np

def load_data_from_csv(file_path):
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip the header
        nilaiasli = [float(row[0]) for row in csv_reader]
    return np.array(nilaiasli)

def quantize_data(data, rata_rata, s):
    quantized_data = []

    for value in data:
        if value < (rata_rata + (0.4 * s)):
            quantized_data.append(0)
        elif value > (rata_rata + s):
            quantized_data.append(1)
        else:
            quantized_data.append(2)

    return quantized_data

def prune_data(quantized_data):
    pruned_data = []
    error_count = 0

    for i in range(len(quantized_data)):
        if quantized_data[i] != 2 and quantized_data[i] != 2:
            pruned_data.append(quantized_data[i])
        else:
            error_count += 1

    return pruned_data, error_count

start2=time.time()

parser = argparse.ArgumentParser(description='Data quantification using Lossy Tope process.')
parser.add_argument('--datapath', required=True, help='Path to the preprocess directory')
parser.add_argument('--filename', required=True, help='filename of the preprocess')
parser.add_argument('--destination', required=True, help='Path for the result destination')
args = parser.parse_args()

data_file_path = os.path.join(args.datapath, args.filename)

preprocess_data = load_data_from_csv(data_file_path)           #menghitung standar deviasi

rata_rata = np.mean(preprocess_data)
s = np.sqrt(np.var(preprocess_data))

quantized_data = quantize_data(preprocess_data, rata_rata, s)

pruned_data, error_count = prune_data(quantized_data)

    # Save pruned data to a new CSV file
output_file_path = os.path.join(args.destination, 'KuantisasiTopeGateway.csv')
with open(output_file_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(pruned_data)
        
end2 = time.time()
timeTope = end2 - start2
print("waktu komputasi kuantisasi = ", timeTope)