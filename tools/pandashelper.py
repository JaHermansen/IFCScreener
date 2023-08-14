import os
from io import BytesIO
from pathlib import Path
import pandas as pd
import xlsxwriter
import streamlit as st


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
    output = BytesIO()

    workbook = xlsxwriter.Workbook(output, {'in_memory': True})

    for object_class in dataframe[CLASS].unique():
        df_class = dataframe[dataframe[CLASS] == object_class].dropna(axis=1, how="all")

        worksheet = workbook.add_worksheet(object_class)  # create worksheet with name 'object_class'

        for r_idx, row in enumerate(df_class.values):
            for c_idx, value in enumerate(row):
                worksheet.write(r_idx + 1, c_idx, value)  # +1 as headers are already written

        for idx, col in enumerate(df_class):  # loop through all columns
            series = df_class[col]
            if "PAA" in col:
                format = workbook.add_format({'bg_color': '#ADD8E6'})
                # Create the cell range for the column
                cell_range = xlsxwriter.utility.xl_range(1, idx, len(series), idx)
                worksheet.conditional_format(cell_range, {'type': 'no_blanks', 'format': format})

    # Write the column headers
    for c_idx, col_name in enumerate(df_class.columns):
        worksheet.write(0, c_idx, col_name)

    workbook.close()

    st.download_button(
        label="Download Excel workbook",
        data=output.getvalue(),
        file_name=file_name.replace('.ifc', '.xlsx'),
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

