import os
import pandas as pd

def mergeFiles(type_of_district, ad_type):
# Specify the folder path
    folder_path = os.getcwd() + '/results/' + ad_type + '/' + type_of_district

    # List to store all dataframes
    all_dataframes = []

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.xlsx') or filename.endswith('.xls'):
            file_path = os.path.join(folder_path, filename)
            df = pd.read_excel(file_path)
            all_dataframes.append(df)

    # Concatenate all dataframes
    merged_df = pd.concat(all_dataframes, ignore_index=True)

    # Write the merged dataframe to a new Excel file
    merged_df.to_excel(folder_path + '.xlsx', index=False)

    print("All Excel files have been merged into 'merged_file.xlsx'")