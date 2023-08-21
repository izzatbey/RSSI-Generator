clc
clear all
close all
tic;%awal waktu ekseskusi

warning('off','all');
pkg load communications;
pkg load signal;
pkg load io;

m=6; 
n=2^m-1; 
k=30;

q=csvread("E:/My Code Projects/rssi_generator/datasets/Quantification/Node/Kuantifikasi_Node.csv");
p=csvread('E:/My Code Projects/rssi_generator/datasets/Quantification/Gateway/Kuantifikasi_GW.csv');
%%%%%PUNYA BOB%%%%%
qb=csvread('E:/My Code Projects/rssi_generator/datasets/Quantification/Gateway/Kuantifikasi_GW.csv');
pb=csvread("E:/My Code Projects/rssi_generator/datasets/Quantification/Node/Kuantifikasi_Node.csv");

msg=gf(q);
%msge=gf(p); 
%%%%%PUNYA BOB%%%%%%%%
msgb=gf(qb);
%msgeb=gf(pb);%merubah ke galois field

[genpoly,factors,cst,h,t] = bchpoly(n,k); %generate dan memperoleh maksimal kesalahan (t)
genpoly = fliplr(genpoly);

db=floor(length(msg)/k); 
%dbe=floor(length(msge)/k); %pembagian blok
%%%%%PUNYA BOB%%%%%%%%
dbb=floor(length(msgb)/k); 
%dbeb=floor(length(msgeb)/k);

coba=length(msg); 
cobab=length(msgb); 

fprintf('Panjang pesan Asli Alice sebanyak %d bit\n',coba)
fprintf('Panjang pesan Asli Bob sebanyak %d bit\n',cobab)

c=0;
for i=1:db %looping untuk pembagian blok dalam data
    for j=1:k
        x(i,j)=q(j+c); %data dalam 1 blok
        xx(i,j)=p(j+c);
    end
    c=c+k;
    msg1=gf(x); 
    msge1=gf(xx); %merubah menjadi gf
    code1=bchenc(msg1,n,k); %proses encoding
    codew1=bchenc(msge1,n,k);
    f=gf(code1);
    ff=gf(codew1); %hasil encoding didalam gf
    hzl=bchdeco(f,n,k); %data asli di decoder
    hsl=bchdeco(ff,n,k);
    AA=gf(hzl); %hasil decoder
    AA=transpose(AA(:,1:k));
    BB=gf(hsl);
    BB=transpose(BB(:,1:k));
    A=AA.x; %merubah gf ke bentuk array biasa
    B=BB.x;
    A=transpose(A);
    B=transpose(B);
end
%%%%%PUNYA BOB%%%%%%%%
c=0;
for i=1:dbb %looping untuk pembagian blok dalam data
    for j=1:k
        xb(i,j)=qb(j+c); %data dalam 1 blok
        xxb(i,j)=pb(j+c);
    end
    c=c+k;
    msg1b=gf(xb); 
    msge1b=gf(xxb); %merubah menjadi gf
    code1b=bchenc(msg1b,n,k); %proses encoding
    codew1b=bchenc(msge1b,n,k);
    fb=gf(code1b);
    ffb=gf(codew1b); %hasil encoding didalam gf
    hzlb=bchdeco(fb,n,k); %data asli di decoder
    hslb=bchdeco(ffb,n,k);
    AAb=gf(hzlb); %hasil decoder
    AAb=transpose(AAb(:,1:k));
    BBb=gf(hslb);
    BBb=transpose(BBb(:,1:k));
    Ab=AAb.x; %merubah gf ke bentuk array biasa
    Bb=BBb.x;
    Ab=transpose(Ab);
    Bb=transpose(Bb);
end

db=length(A);

C=[];
Benar=zeros(1,k); %untuk baris yang kurang dari y agar nilai matriks sama
if (B==A) %jika pesan asli dan pesan proses sama maka benar
    fprintf('Tidak ada error');
    C=A;
    %fprintf('Pesan setelah dikoreksi yaitu :');C
else
    %disp('Terdapat Error');
    for y=1:db %looping blok ke 1 hingga n
        salah=find(B(y,:)~=A(y,:)); %mencari nilai yg beda antara pesan asli dan pesan setelahproses
        js=length(salah); %banyak pesan yg beda
        jb=length(k-salah); %banyak pesan yg sama
        if js==0 %jika jumlah data yg beda = 0 maka 1 blok benar semua
            %fprintf('Letak salah pada blok %d, tidak ada\n', y);
            B(y,:); %tmpilkan blok
            C=[C;B(y,:)]; %cetak blok gabung c yg bernilai matrik kosong ke B
        elseif js<=t %jika jumlah beda kurang atau sama dg maksimal error dikoreksi
            %fprintf('\n\nLetak salah pada blok %d, ada di bit ke : ', y);
            %disp(salah);
            %fprintf('Proses koreksi : \n');
             %for i=1:js %Pengulangan koreksi error dalam satu blok
                 %if B(y,salah(i))==0 %jika indeks yg berbeda ke n=0 maka ganti 1
                     %fprintf('(%d) Bit ke-%d [nol -> satu]\n',i,salah(i));
                  %   B(y,salah(i))=1;
                  %else
                     %fprintf('(%d) Bit ke-%d [satu -> nol]\n',i,salah(i)); %jika indeks yg berbeda ke n=1 maka ganti 0
                  %   B(y,salah(i))=0;
                 %end
             %end
            B(y,:); %tmpilkan blok
            C=[C;B(y,:)]; %cetak blok gabung c yg bernilai matrik kosong ke B
        else %jika jumlah perbedaan lebih besar dari t maka di hapus
            %fprintf('Jumlah error lebih dari satu, pada blok %d di bit ke',y);
            %disp(salah);
            %fprintf('Karena jumlah error lebih dari %d, maka blok %d dihapus\n',t,y);
        end
    end
end

dbb=length(Bb);

Cb=[];
Benarb=zeros(1,k); %untuk baris yang kurang dari y agar nilai matriks sama
if (Bb==Ab) %jika pesan asli dan pesan proses sama maka benar
    %disp('Tidak ada error\n');
    Cb=Ab;
    %fprintf('Pesan setelah dikoreksi yaitu :');Cb
else
    %disp('Terdapat Error');
    for yb=1:dbb %looping blok ke 1 hingga n
        salahb=find(Bb(yb,:)~=Ab(yb,:)); %mencari nilai yg beda antara pesan asli dan pesan setelahproses
        jsb=length(salahb); %banyak pesan yg beda
        jbb=length(k-salahb); %banyak pesan yg sama
        if jsb==0 %jika jumlah data yg beda = 0 maka 1 blok benar semua
            %fprintf('Letak salah pada blok %d, tidak ada\n', yb);
            Bb(yb,:); %tmpilkan blok
            Cb=[Cb;Bb(yb,:)]; %cetak blok gabung c yg bernilai matrik kosong ke B
        elseif jsb<=t %jika jumlah beda kurang atau sama dg maksimal error dikoreksi
            %fprintf('\n\nLetak salah pada blok %d, ada di bit ke : ', yb);
            %disp(salahb)
            %fprintf('Proses koreksi : \n');
            for i=1:jsb %Pengulangan koreksi error dalam satu blok
                if Bb(yb,salahb(i))==0 %jika indeks yg berbeda ke n=0 maka ganti 1
                    %fprintf('(%d) Bit ke-%d [nol -> satu]\n',i,salahb(i));
                    Bb(yb,salahb(i))=1;
                 else
                    %fprintf('(%d) Bit ke-%d [satu -> nol]\n',i,salahb(i)); %jika indeks yg berbeda ke n=1 maka ganti 0
                    Bb(yb,salahb(i))=0;
                end
            end
            Bb(yb,:); %tmpilkan blok
            Cb=[Cb;Bb(yb,:)]; %cetak blok gabung c yg bernilai matrik kosong ke B
        else %jika jumlah perbedaan lebih besar dari t maka di hapus
            %fprintf('Jumlah error lebih dari satu, pada blok %d di bit ke',yb);
            %disp(salahb)
            %fprintf('Karena jumlah error lebih dari %d, maka blok %d dihapus\n',t,yb);
        end
    end
end

[baris,kolom]=size(C);
[barisb,kolomb]=size(Cb);%ukuran matriks data

total=baris*kolom; 
totalb=barisb*kolomb;%jumlah banyak data setelah proses

u=C'; 
ub=Cb'; %ubah kolom ke baris

w=reshape(u,1,total); 
wb=reshape(ub,1,totalb);%atur ulang baris dan kolom data

ww=w'; 
wwb=wb'; %ubah 1 baris ke 1 kolom

%kj=find(ww==wwb); nn=ww(kj);
csvwrite('hasilbch_Node_O100m.csv', ww);
csvwrite('hasilbch_GW_O100m.csv', wwb);

fprintf('Panjang pesan Alice setelah dikoreksi yaitu : %d\n',total);
fprintf('Panjang pesan Bob setelah dikoreksi yaitu : %d\n',totalb);
