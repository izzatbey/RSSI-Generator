import csv
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import argparse
import os

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Preprocess data using polynomial fitting.')
parser.add_argument('--datapath', required=True, help='Path to the datasets directory')
parser.add_argument('--filename', required=True, help='filename of the datasets')
parser.add_argument('--destination', required=True, help='Path for the result destination')
args = parser.parse_args()

data_file_path = os.path.join(args.datapath, args.filename)

x = []
y = []
with open(data_file_path) as f:
    data = csv.reader(f, delimiter='\t')
    for i, row in enumerate(data):
        x.append(float(row[0]))
        y.append(i)

x = np.array(x)
y = np.array(y)

def mapping(x, a, b):  
    return a * x + b 

def mapping2(x, a, b):  
    return a * x**2 + b  

def mapping3(x, a, b):  
    return a * x**3 + b

# using the curve_fit() function
params, _ = curve_fit(mapping3, y, x)  
a, b = params[0], params[1]
y_fit3 = a * y**3 + b

# Construct full paths for the plot and CSV destination
data_plot_path = os.path.join(args.destination, 'plotCurv_GW.pdf')
data_destination_path = os.path.join(args.destination, 'curve_fitting_GW.csv')

# plotting the graph
plt.plot(x, label="y - original")  
plt.plot(y_fit3, label="y = a * x^3 + b")
plt.xlabel('y')  
plt.ylabel('x')  
plt.legend(loc='best', fancybox=True, shadow=True)  
plt.grid(True)  

# Save the plot before showing it
plt.savefig(data_plot_path)
plt.show()

# Create a CSV file
with open(data_destination_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['fit3'])
    csvwriter.writerows(zip(y_fit3))

print('------------------')
print('Preproses Berhasil')
print('------------------')