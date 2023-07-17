import streamlit as st
import ifcopenshell
from PIL import Image
from tools import ifchelper
from tools import graph_maker

# Page icon
icon = Image.open('paa1.png')

def callback_upload():
    st.session_state["file_name"] = st.session_state["uploaded_file"].name
    st.session_state["array_buffer"] = st.session_state["uploaded_file"].getvalue()
    st.session_state["ifc_file"] = ifcopenshell.file.from_string(st.session_state["uploaded_file"].getvalue().decode("utf-8"))
    st.session_state["is_file_uploaded"] = True

def get_project_name():
    return st.session_state.get("file_name", "")

def change_project_name():
    st.session_state["ifc_file"].by_type("IfcProject")[0].Name = st.session_state["project_name_input"]

def remove_uploaded_file():
    st.session_state["file_name"] = ""
    st.session_state["array_buffer"] = None
    st.session_state["ifc_file"] = None
    st.session_state["is_file_uploaded"] = False

def draw_model_health_ui():
    col1, col2 = st.columns(2)

    if st.session_state.get("ifc_file") is None:
        st.warning("No file provided. Please upload a file.")
    else:
        with col1:
            graph = graph_maker.get_elements_graph(st.session_state["ifc_file"])
            st.write(graph)

        with col2:
            graph = graph_maker.get_high_frequency_entities_graph(st.session_state["ifc_file"])
            st.write(graph)

def main():
    if "file_name" not in st.session_state:
        st.session_state["file_name"] = ""

    st.set_page_config(
        layout="wide",
        page_title="IFC Screener",
        page_icon=icon,
    )
    st.markdown("<h1 style='color: #006095;'>PAA IFC Screener</h1>", unsafe_allow_html=True)
    st.markdown("### Click on Browse File in the Side Bar to start")
    uploaded_file = st.sidebar.file_uploader("Choose a file", key="uploaded_file", on_change=callback_upload)
    if st.sidebar.button("Remove File"):
        remove_uploaded_file()

    if "is_file_uploaded" in st.session_state and st.session_state["is_file_uploaded"]:
        st.sidebar.success("Project successfully loaded")
        #st.sidebar.write("You may now reload a new file")
    if st.session_state["file_name"] != "":
        st.write(f'Start Exploring "{get_project_name()}"')
        st.markdown("### Model Statistics")
        draw_model_health_ui()


if __name__ == "__main__":
    main()
