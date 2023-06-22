
CLASS = "Class"
LEVEL = "Level"

def filter_dataframe_per_class(dataframe, class_name):
    return dataframe[dataframe["Class"] == class_name].dropna(axis=1, how="all")

def get_total(dataframe):
    count = dataframe[CLASS].value_counts().sum()
    return count

def get_qsets_columns(dataframe):
    qset_columns = set()
    [qset_columns.add(column.split(".", 1)[0]) for column in dataframe.columns if "Qto" in column]
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
    import os
    from pathlib import Path
    import pandas
    file_name = file_name.replace('.ifc', '.xlsx')

    # Getting user's home directory and appending 'Downloads'
    dir_name = str(Path.home() / "Downloads")

    # If directory does not exist, create it
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    writer = pandas.ExcelWriter(os.path.join(dir_name, file_name), engine="xlsxwriter") 
    for object_class in dataframe[CLASS].unique():
        df_class = dataframe[dataframe[CLASS] == object_class].dropna(axis=1, how="all")
        df_class.to_excel(writer, sheet_name=object_class)
    writer.close() # Use close instead of save