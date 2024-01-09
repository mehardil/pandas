import os
import pandas as pd
import csv
import os
import datetime

def readfile_folder(): 
    """this function read all xlsx file form folder and get there Asin number and store this in list"""
    folder_path = r'E:/codeaza/sheetdata/sheetsfolder'
    file_list = os.listdir(folder_path)
    Asindata = []
    file_data = []
    for file_name in file_list:
        if file_name.endswith('.xlsx'): 
            file_path = os.path.join(folder_path, file_name)
            print(f"Reading {file_name}")
            file_data.append(file_name)
            df = pd.read_excel(file_path)
            if 'Cost' in df.columns:
                asin_values = df['Asin'].tolist()
                for asin in asin_values:
                    print(asin)
                    Asindata.append(asin)
                    
            else:
                print("INPUT FILE HAVE NO NAME")
    print("Finished reading and processing all files.")
    return Asindata ,file_data

def compare_price():
    """this function read Asin and check this in second file and get there price"""
    Asinvalue , file_data = readfile_folder()
    file_path = '2023 Year to Date Purchases By Store.xlsx'
    sheet_name = '2023 Orders'
    df = pd.read_excel(file_path ,sheet_name=sheet_name)
    column_name = "Cost/ASIN"
    column_ASIN = "ASIN"
    print(Asinvalue)
    ASINCODE = []
    PRICE = [] 
    DATE = []
    for productasin in Asinvalue:
        print(productasin , "there is value of Asin")
        search_value = productasin
        filtered_df = df[df[column_ASIN] == search_value]
        cost_values = filtered_df["Cost/ASIN"].tolist()
        print(cost_values)
        try:
            max_cost_value = max(cost_values)
            print("Maximum value:", max_cost_value)
        except:
            max_cost_value = "Missing Cost Value"
            
        ASINCODE.append(productasin)
        PRICE.append(max_cost_value)
    return ASINCODE ,PRICE

def Savedata():
    """here we save data"""
    folder_path = r'E:/codeaza/sheetdata/sheetsfolder'
    file_list = os.listdir(folder_path)
    asincode , price = compare_price()
    for file_name in file_list:
        if file_name.endswith('.xlsx'): 
            file_path = os.path.join(folder_path, file_name)
            print(f"Reading {file_name}")
            df = pd.read_excel(file_path)
            if 'Cost' in df.columns:
                for i,j in zip(asincode,price):
                    df.loc[df['Asin'] == i, 'Cost'] = j 
            else:
                print("INPUT FILE HAVE NO NAME")   
        df.to_excel(file_path, index=False)       
   
          
    
def fetch_records():
    Savedata()
fetch_records()

