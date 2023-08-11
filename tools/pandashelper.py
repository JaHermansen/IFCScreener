import os
from pathlib import Path
import pandas as pd
import xlsxwriter


CLASS = "Class"
LEVEL = "Level"

def filter_dataframe_per_class(dataframe, class_name):
    return dataframe[dataframe["Class"] == class_name].dropna(axis=1, how="all")

def get_total(dataframe):
    count = dataframe[CLASS].value_counts().sum()
    return count

def get_qsets_columns(dataframe, *software_types):
    qset_columns = set()
    [qset_columns.add(column.split(".", 1)[0]) for column in dataframe.columns if any(software_type in column for software_type in software_types)]
    return list(qset_columns) if qset_columns else None


def get_quantities(frame, quantity_set):
    columns = []
    [columns.append(column.split(".", 1)[1]) for column in frame.columns if quantity_set in column]
    columns.append("Count")
    return columns

def download_csv(file_name, dataframe):
    file_name = file_name.replace('.ifc', '.csv')
    dataframe.to_csv(f'./downloads/{file_name}')


def download_excel(file_name, dataframe):
        

    file_name = file_name.replace('.ifc', '.xlsx')

    # Getting user's home directory and appending 'Downloads'
    dir_name = str(Path.home() / "Downloads")

    # If directory does not exist, create it
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    writer = pd.ExcelWriter(os.path.join(dir_name, file_name), engine="xlsxwriter") 

    for object_class in dataframe[CLASS].unique():
        df_class = dataframe[dataframe[CLASS] == object_class].dropna(axis=1, how="all")

        df_class.to_excel(writer, sheet_name=object_class, index=False)
        worksheet = writer.sheets[object_class]  # pull worksheet object

        for idx, col in enumerate(df_class):  # loop through all columns
            series = df_class[col]
            if "PAA" in col:
                format = writer.book.add_format({'bg_color': '#ADD8E6'}) 
                # Create the cell range for the column
                cell_range = xlsxwriter.utility.xl_range(1, idx, len(series), idx)
                worksheet.conditional_format(cell_range, {'type': 'no_blanks', 'format': format})

    writer.close()
