import pandas as pd

def insert_data_to_excel(file_path, data_lists, sheet_name='Sheet1'):
    # Create a DataFrame from the data_lists
    data = {'Column1': data_lists[0], 'Column2': data_lists[1], 'Column3': data_lists[2]}
    df = pd.DataFrame(data)

    # Check if the file exists
    if os.path.exists(file_path):
        # Load the existing Excel file
        existing_df = pd.read_excel(file_path, sheet_name)
        
        # Append new data to the existing DataFrame

        updated_df = existing_df._append(df, ignore_index=True)

        # Write the updated DataFrame back to the Excel file
        updated_df.to_excel(file_path, index=False, sheet_name=sheet_name)

        print(f"Data appended to existing file: {file_path}")

    else:
        # Create a new Excel file
        df.to_excel(file_path, index=False, sheet_name=sheet_name)

        print(f"Data written to new file: {file_path}")


df = pd.read_excel('./Broker data.xlsx','Mumbai')
l = df['Column2']
print(len(l))
print(len(set(l)))
