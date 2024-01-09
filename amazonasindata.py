# import pandas as pd

# file_path = r'E:/codeaza/sheetdata/sheetsfolder/ARG Enterprise Cost Data Needed 8-28-23.xlsx'
# df = pd.read_excel(file_path)
# asin_column_index = None
# for idx, header in enumerate(df.columns):
#     if 'Asin' in str(header):
#         asin_column_index = idx
#         break
# if asin_column_index is not None:
#     selected_column = df.iloc[:, asin_column_index]
#     print(selected_column)
# else:
#     print("No column with 'Asin' header found in the file.")



# # # Check if 'asin' column exists in the DataFrame
# # if 'Asin' not in df.columns:
# #     print("Column 'asin' not found in the DataFrame.")
# #     exit()

# # asin_values = df['Asin'].tolist()

# # for asin in asin_values:
# #     print(asin)
import os
import pandas as pd
def process_file(file_name):
    # File from where we get ASIN
    file_path_with_asin = os.path.join(os.getcwd(), 'data_dir', file_name)
    # read ASIN as DataFeame
    read_asin_file = pd.read_excel(file_path_with_asin)
    # Read The Asin Coloumn To get All ASIN Which is going to be search in the next Sheet
    asin_to_be_search = read_asin_file['Asin']
    # Path for all order files
    all_order_files_path = os.path.join(os.getcwd(), 'data_dir', 'ordersheets')
    # Empety DataFrame
    all_order_data = []
    # all_order_data = pd.DataFrame(columns=['ASIN', "Cost/ASIN"])
    # Read Every Order File one by one
    for file_name in os.listdir(all_order_files_path):
        if file_name.endswith('.xlsx'):
            sheet_name = '2023 Orders'
            read_order_df = pd.read_excel(os.path.join(all_order_files_path, file_name), sheet_name=sheet_name)
            append_data = read_order_df[['ASIN', "Cost/ASIN"]]
            all_order_data.append(append_data)
    combined_order_df = pd.concat(all_order_data, ignore_index=True)
    try:
        for asin in asin_to_be_search.unique():
            matching_rows = combined_order_df[combined_order_df['ASIN'] == asin]
            if not matching_rows.empty:
                max_value = matching_rows['Cost/ASIN'].max()
                # update ASIN File DataFrame
                read_asin_file.loc[read_asin_file['Asin'] == asin, 'Cost'] = max_value
                # Update NaN With ASIN NOT Exist In Order File
                read_asin_file['Cost'].fillna("no sales were found", inplace=True)
                print(f'[+] {len(matching_rows)} rows found for {asin} and the MAX value: {max_value}')
        print(read_asin_file)
        # Save file with updated costs
        read_asin_file.to_excel(file_path_with_asin, index=False)
    except Exception as e:
        print(e)
