# Quantities

import streamlit as st
from tools import ifchelper
from tools import pandashelper
from tools import graph_maker
import pandas as pd
from PIL import Image
import ifcopenshell
import random
import os
from datetime import date
import re

#Page icon
icon = Image.open('paa1.png')

st.set_page_config(
    layout= "wide",
    page_title= "PAA IFC Screener",
    page_icon= icon,
)


session = st.session_state
# Get the original file name
original_file_name = st.session_state["file_name"]
# Create the updated file name with the current date
updated_file_name = original_file_name.split(".")[0] + "_updated_" + str(date.today()) + ".ifc"



def get_ifc_pandas():
    data, pset_attributes = ifchelper.get_objects_data_by_class(
        session.ifc_file,
        "IfcBuildingElement"
        )
    return ifchelper.create_pandas_dataframe(data, pset_attributes)

def get_ifc_pandas_filter(class_filter):
    data, pset_attributes = ifchelper.get_objects_data_by_class(
        session.ifc_file,
        class_filter
        )
    return ifchelper.create_pandas_dataframe(data, pset_attributes)

def explore():
    # DATA
    st.write("Data:")
    st.write(session.df)  # use df from session_state

def get_df(file):
    # get extension and read file
    extension = file.name.split('.')[1]
    if extension.upper() == 'CSV':
        df = pd.read_csv(file)
    elif extension.upper() == 'XLSX':
        df = pd.read_excel(file, engine='openpyxl')
    elif extension.upper() == 'PICKLE':
        df = pd.read_pickle(file)
    #st.write(f"Debug: {df.head()}")  # debug line
    session.df = df  # store df in session_state

def download_csv():
    pandashelper.download_csv(session.file_name, session.Dataframe)
    
def download_excel():
    pandashelper.download_excel(session.file_name,session.DataFrame)

def callback_upload():
    st.session_state["file_name"] = st.session_state["uploaded_file"].name
    st.session_state["array_buffer"] = st.session_state["uploaded_file"].getvalue()
    st.session_state["is_file_uploaded"] = True

def update_properties(bim_type_codes_selected):

    
    owner_history = session.ifc_file.by_type("IfcOwnerHistory")[0]
    products = session.ifc_file.by_type("IfcProduct")
    procs = []
    for i in products:
        if i.is_a("IfcProduct"):
            procs.append(i)

    for proc in procs:
        pset = ifcopenshell.util.element.get_psets(proc, psets_only=True)
        property_values = []
        for bim_type_code in bim_type_codes_selected:
            pset_value = None
            for pset_name, pset_values in pset.items():
                if bim_type_code in pset_name:
                    pset_value = pset_values.get("Value")
                    break
            if pset_value is not None:
                property_values.append(
                    session.ifc_file.createIfcPropertySingleValue(
                        bim_type_code, bim_type_code, session.ifc_file.create_entity("IfcText", str(pset_value)), None
                    )
                )
            else:
                property_values.append(
                    session.ifc_file.createIfcPropertySingleValue(
                        bim_type_code, bim_type_code, session.ifc_file.create_entity("IfcText", "Test"), None
                    )
                )
        property_set = session.ifc_file.createIfcPropertySet(proc.GlobalId, owner_history, "Pset_PAABIMTypeCodes", None, property_values)
        session.ifc_file.createIfcRelDefinesByProperties(proc.GlobalId, owner_history, None, None, [proc], property_set)

    # Write the modified IFC file to the Downloads folder
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    updated_file_path = os.path.join(downloads_path, updated_file_name)
    session.ifc_file.write(updated_file_path)



    ###

def execute():
    st.markdown("<h1 style='color: #006095;'>PAA Model Quantities</h1>", unsafe_allow_html=True)
    if st.session_state.get("ifc_file") is None:
        st.warning("No file provided. Please upload a file.")
    else:
        
        tab1, tab2, tab3, tab4 = st.tabs(["Dataframe Utilities", "Quantities Review", "PAA Properties", "Add External Data"])
        
        with tab1:

            
            st.header("DataFrame Review")
            st.write("Overall dataframe")
            session["DataFrame"] = get_ifc_pandas()
            st.write(session["DataFrame"])

            #st.button("Download CSV", key="download_csv", on_click=download_csv)
            st.button("Download Excel", key="download_excel", on_click=download_excel)

            st.header("Filter by class")
            classesfilter = session.DataFrame["Class"].value_counts().keys().to_list()
            class_selectorfilter = st.selectbox("Select Class", options=classesfilter or [], key="class_selector_filter")

            st.write(get_ifc_pandas_filter(class_selectorfilter))
            

            

            
        
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                st.write("Options")
                classes = session.DataFrame["Class"].value_counts().keys().to_list()
                class_selector = st.selectbox("Select Class", options=classes or [], key="class_selector")
                
                session["filtered_frame"] = pandashelper.filter_dataframe_per_class(session.DataFrame, session.class_selector)
                #st.write(session["filtered_frame"])
                session["qtos"] = pandashelper.get_qsets_columns(session["filtered_frame"])
                
                if session["qtos"] is not None:
                        qto_selector = st.selectbox("Select Quantity Set", session.qtos, key='qto_selector')
                        quantities = pandashelper.get_quantities(session.filtered_frame, session.qto_selector)
                        st.selectbox("Select Quantity", quantities, key="quantity_selector")
                        st.radio('Split per', ['Level', 'Type'], key="split_options")
                else:
                    st.warning("No quantities ~ ask your file issuer to export some")
                #st.write(session["qtos"])
            with col2:
                st.write("Graph")
                if "quantity_selector" in session:
                    if session.quantity_selector == "Count":
                        total = pandashelper.get_total(session["filtered_frame"])
                        st.write(f"The total number of {session.class_selector} is {total}")
                    else:
                        st.subheader(f'{session.class_selector} {session.quantity_selector}')
                        graph = graph_maker.load_graph(
                            session.filtered_frame,
                            session.qto_selector,
                            session.quantity_selector,
                            session.split_options,
                        )
                        st.write(graph)


        with tab3:
            st.header("PAA BIMTypeCodes")

            col1, col2 = st.columns(2)

            with col1:
                st.write("Specify BIMTypeCodes:")
                bim_type_codes = [
                    "TypeName",
                    "TypeCode",
                    "TypeNumber",
                    "TypeID",
                    "TypeCode-Description",
                    "Typetekst"
                ]
                bim_type_codes_selected = []
                for bim_type_code in bim_type_codes:
                    checkbox_state = st.checkbox(bim_type_code, value=True, key=f"checkbox_{bim_type_code}")
                    if checkbox_state:
                        bim_type_codes_selected.append(bim_type_code)
                
                st.write("Selected BIMTypeCodes:")
                st.write(pd.DataFrame({"BIMTypeCodes": bim_type_codes_selected}))



            with col2:
                st.write("Create BIMTypeCodes in file")
                execute_button = st.button("Execute Property Creation")

            if execute_button:
                update_properties(bim_type_codes_selected)
                st.success("Property creation completed successfully!")
                st.warning("Check your download folder for the updated file")
   
            st.write(session["DataFrame"])


        with tab4:
            st.header("Upload data to model")
            st.write("upload data")

            file = st.file_uploader("Upload file", type=['csv', 'xlsx', 'pickle'])
            if not file:
                st.write("Upload a .csv or .xlsx file to get started")
            else:  # only proceed if a file is uploaded
                get_df(file)
                explore()




    
execute()
