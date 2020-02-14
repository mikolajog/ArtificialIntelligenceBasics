#!/usr/bin/env python3

import pandas as pd
import numpy as np

#wczytujemy metadata i iterujemy po nich
meta = pd.read_csv("BIRAFFE-metadata.csv", sep=";")
dataframes_list=[]

for rekord in meta.index:
    print(meta['ID'][rekord]) #to show that we have processed it
    
    if(meta['BIOSIGS'][rekord]!=meta['BIOSIGS'][rekord] or meta['PROCEDURE'][rekord] !=meta['PROCEDURE'][rekord] ):
        continue #if is Nan continue
    else:
        #each person has biosigs and procedure (EKG, GSR) in seperate CSV
        bio_csv = "BIRAFFE-biosigs/BIRAFFE-biosigs/SUB"+str(meta['ID'][rekord])+"-BioSigs.csv" 
        procedure_csv = "BIRAFFE-procedure/BIRAFFE-procedure/SUB"+str(meta['ID'][rekord])+"-Procedure.csv"  

        bio = pd.read_csv(bio_csv, sep=";")
        procedure = pd.read_csv(procedure_csv , sep=";")

        #needed for counting mean and std of values
        lista_std_ecg=[]
        lista_mean_ecg=[]
        lista_std_eda=[]
        lista_mean_eda=[] 
        
        ind=0
        
        lista_ecg=[]
        lista_eda=[]
        
        #checking biosig as timestamp must be proper for every picture (6 seconds for each picture)
        for ind1 in bio.index:
            if(bio['TIMESTAMP'][ind1] >= procedure['TIMESTAMP'][ind]):
                if(bio['TIMESTAMP'][ind1] <= procedure['TIMESTAMP'][ind] +6.0):
                    lista_ecg.append(bio['ECG'][ind1])
                    lista_eda.append(bio['EDA'][ind1])
                elif(ind<119):
                    a1=np.std(np.array(lista_ecg))
                    a2=np.mean(np.array(lista_ecg))
                    a3 = np.std(np.array(lista_eda))
                    a4=np.mean(np.array(lista_eda))
                    lista_std_ecg.append(a1)
                    lista_mean_ecg.append(a2)
                    lista_std_eda.append(a3)
                    lista_mean_eda.append(a4)

                    lista_ecg=[]
                    lista_eda=[]
                    ind=ind+1

        a1=np.std(np.array(lista_ecg))
        a2=np.mean(np.array(lista_ecg))
        a3 = np.std(np.array(lista_eda))
        a4=np.mean(np.array(lista_eda))

        lista_std_ecg.append(a1)
        lista_mean_ecg.append(a2)
        lista_std_eda.append(a3)
        lista_mean_eda.append(a4)

        lista_ecg=[]
        lista_eda=[]
        ind=ind+1
        
        new_df = procedure
        new_df.insert(8, "Mean ECG", lista_mean_ecg) 
        new_df.insert(9, "STD ECG", lista_std_ecg) 
        new_df.insert(10, "Mean EDA", lista_mean_eda) 
        new_df.insert(11, "STD EDA", lista_std_eda) 
        new_df.insert(12, "ID", meta['ID'][rekord]) 

        dataframes_list.append(new_df)

final_data=pd.concat(dataframes_list, ignore_index = True)
 
print(final_data)
    
final_data.to_csv(r'PSIProjectData.csv')
