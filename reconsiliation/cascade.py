import time
import argparse
import csv
import math
import os

def read_csv_to_list(filename):
    data = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Assume each row contains only one column of data
            data.append(float(row[0]))
    return data

parser = argparse.ArgumentParser(description='Data reconciliation using cascade.')
parser.add_argument('--alice', required=True, help='Path to Alice quantification CSV file')
parser.add_argument('--bob', required=True, help='Path to Bob quantification CSV file')
parser.add_argument('--destination', required=True, help='Directory to save the result Excel file')
args = parser.parse_args()

start = time.time()

calice = read_csv_to_list(args.alice)
cbob = read_csv_to_list(args.bob)

errkuan = [i + 1 for i in range(len(calice)) if calice[i] != cbob[i]]
kdrkuan = len(errkuan) / len(calice)
print("KDR Kuantisasi ALICE - BOB = %.2f%%" % (kdrkuan * 100))

aslicalice=calice.copy()
aslibob=cbob.copy()
bital=[]
bitar=[]
bitbl=[]
bitbr=[]
bagi=math.ceil(len(calice)/2)
batas=math.ceil(bagi/2)
pjg=int(len(calice))

bital=[1,1]
y=0
u=[]
g=1
bataserror=6
maks=bataserror*8
step=0
letakerror=[]
simpan=[]
while (bataserror>0):
    del bital[:]
    del bitbl[:]
    del bitar[:]
    del bitbr[:]
    paral=0
    parbl=0
    parar=0
    parbr=0
    if step>(maks):
        print('\nLooping terlalu banyak, program otomatis berhenti, tidak dapat menemukan error lagi, hanya dapat koreksi %d error'%len(letakerror))
        break
    else:
        print('\n-Step %d'%step)
    if(y==0):
        x=0
        kiri1=0
        kiri2=bagi
        kanan1=bagi
        kanan2=pjg

    ### KIRI ###
    for i in range (kiri1,kiri2):
        bital.append(calice[i])
        bitbl.append(cbob[i])
        paral=int(paral)^int(calice[i])
        parbl=int(parbl)^int(cbob[i])

    ### KANAN ###
    for i in range (kanan1,kanan2):
        bitar.append(calice[i])
        bitbr.append(cbob[i])
        parar=int(parar)^int(calice[i])
        parbr=int(parbr)^int(cbob[i])
    c=[]
    if u==1:
        c=2
    elif u==2:
        c=1
    hasil=[]
    print('x=',x)
    y=y+1
    if (paral!=parbl or c==1):
        if(x==0):
            tengah=math.ceil(len(bital)/2)
            kiri1=0
            kiri2=tengah
            kanan1=kiri2
            kanan2=kanan1+math.floor(len(bital)/2)
            x=1
            g=1

        elif(x==1):
            tengah=math.ceil(len(bital)/2)
            kiri1=kiri1
            kiri2=kiri1+tengah
            kanan1=kiri2
            kanan2=kanan1+math.floor(len(bital)/2)
            x=1
            hasil=kiri2
            u=[]

        elif(x==2):
            tengah=math.ceil(len(bital)/2)
            kiri1=kiri1 #asline kanan1
            kiri2=kiri1+tengah
            kanan1=kiri2
            kanan2=kanan1+math.floor(len(bital)/2)
            x=1
            hasil=kiri2
            u=[]
        print ("Error ada di bagian kiri maka blok kiri dibagi")
        
    elif (parar!=parbr or c==2):
        if(x==0):
            ujung=(len(bitar))
            tengah=math.ceil(len(bitar)/2)
            kiri1=bagi
            kiri2=kiri1+tengah
            kanan1=kiri2
            kanan2=kiri1+ujung
            x=2
            g=2

        elif(x==1):
            ujung=(len(bitar))
            tengah=math.ceil(len(bitar)/2)
            kiri1=kanan1
            kiri2=kiri1+tengah
            kanan1=kiri2
            kanan2=kanan1+math.floor(len(bitar)/2)
            x=2
            hasil=kiri2
            u=[]

        elif(x==2):
            tengah=math.ceil(len(bitar)/2)
            kiri1=kanan1
            kiri2=kiri1+tengah
            kanan1=kiri2
            kanan2=kanan1+math.floor(len(bitar)/2)
            x=2
            hasil=kiri2
            u=[]
        print ("Error ada di bagian kanan maka blok kanan dibagi")
    
    elif(paral==parbl and parar==parbr):        
        if g==1:
            y=0
            u=g
            print('Hasil ex-or sama, maka pilih lawan (blok sebelumnya: kiri) = sekarang kanan')
        elif g==2:
            y=0
            u=g
            print('Hasil ex-or sama, maka pilih lawan (blok sebelumnya: kanan) = sekarang kiri')
        else:
            print('there is something wrong\n')
    
    print('Len bital: %d'%len(bital))
    print('g: %d'%(g))
    
    #Simpan letak error per 1 koreksi
    if(len(bital)==1):
        y=0
        if(paral==parbl and parar==parbr):
            break
        else:
            #del calice[hasil-1]
            #hasil=hasil+1
            if (calice[hasil-1]==1):
                calice[hasil-1]=0
            else:
                calice[hasil-1]=1
        letakerror.append(hasil)
        bataserror=bataserror-1
##        print('Error ke %d di bit ke-%d'%(len(letakerror),hasil))
        
    step=step+1

for i in range(0,len(letakerror)):
        del calice[letakerror[i]]
        del cbob[letakerror[i]]   

##print('\nBatas koreksi sudah habis')
print ("\n+++++++OUTPUT CASCADE PROTOCOL+++++++")
##print("ALICE \t BOB")
#for i in range (0, len(calice)):
    #print (" %d \t %d" %(calice[i],cbob[i]))
print('Ada %d error, terletak di bit ke'%len(letakerror),letakerror) 
output_file = os.path.join(args.destination, 'CascadeAlice.csv')

with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    for value in calice:
        writer.writerow([float(value)])

end = time.time()

print(f"Length of calice: {len(calice)}")
print(f"Number of errors detected: {len(letakerror)}")
kdrcas = len(letakerror) / len(calice) * 100  # As a percentage
print(f"KDR CASCADE ALICE - BOB = {kdrcas:.2f}%")
print(f'Computation time for Error Checking with Cascade = {end - start} seconds')