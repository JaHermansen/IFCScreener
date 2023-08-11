import streamlit as st
import ifcopenshell
from PIL import Image
from tools import ifchelper
from tools import graph_maker
import datetime

# Page icon
icon = Image.open('Images/paa1.png')

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



def get_project_coordinates(ifc_file):
    project = ifc_file.by_type("IfcSite")[0]

    if hasattr(project, "RefLatitude") and hasattr(project, "RefLongitude"):
        latitude_x, latitude_y, latitude_z, _ = project.RefLatitude
        longitude_x, longitude_y, longitude_z, _ = project.RefLongitude

        # Return the x, y, and z coordinates
        return longitude_x, longitude_y, longitude_z, latitude_x, latitude_y, latitude_z

    # Return None if the coordinates are not found
    return None


def count_ifc_products(ifc_file):
    project = ifc_file


    # Find all IfcProduct entities
    products = project.by_type("IfcProduct")

    # Count the number of products
    count = len(products)

    return count

def get_file_creation_date(ifc_file_path):
    ifc_file = ifc_file_path
    owner_history = ifc_file.by_type("IfcOwnerHistory")[0]
    creation_date = owner_history.CreationDate

    # Convert Unix timestamp to datetime object
    date_time = datetime.datetime.fromtimestamp(creation_date)

    # Format the datetime object as a readable date string
    formatted_date = date_time.strftime("%Y-%m-%d ")

    return formatted_date
def main():
    if "file_name" not in st.session_state:
        st.session_state["file_name"] = ""

    st.set_page_config(
        layout="wide",
        page_title="IFC Screener",
        page_icon=icon,
    )
    st.markdown("<h1 style='color: #006095;'>IFC Screener</h1>", unsafe_allow_html=True)

    st.markdown("### Click on Browse File in the Side Bar to start")

    st.markdown("""---""")
    
    uploaded_file = st.sidebar.file_uploader("Choose a file", key="uploaded_file", on_change=callback_upload)
    if st.sidebar.button("Remove File"):
        remove_uploaded_file()

    if "is_file_uploaded" in st.session_state and st.session_state["is_file_uploaded"]:
        st.sidebar.success("Project successfully loaded")
        #st.sidebar.write("You may now reload a new file")
    if st.session_state["file_name"] != "":

            col1, col2 = st.columns(2)

            if st.session_state.get("ifc_file") is None:
                st.warning("No file provided. Please upload a file.")
            else:
                with col1:
                    st.markdown("##### Project resume")
                    st.write("IFC schema: " + "".join(str(item) for item in st.session_state["ifc_file"].schema))
                    st.write(f"Project name: {get_project_name()}")
                    creation_date = get_file_creation_date(st.session_state["ifc_file"])
                    st.write("Creation Date: " + str(creation_date))
                    #coordinates = get_project_coordinates(st.session_state["ifc_file"])
                    #if coordinates:
                    #    longitude_x, longitude_y, longitude_z, latitude_x, latitude_y, latitude_z = coordinates
                     #   st.write("##### Project coordinates")
                      #  st.write("Latitude: " + str(latitude_x) + "° " + str(latitude_y) + "' " + str(latitude_z) + "''")
                       # st.write("Longitude: " + str(longitude_x) + "° " + str(longitude_y) + "' " + str(longitude_z) + "''")
                    product_count = count_ifc_products(st.session_state["ifc_file"])
                    st.write("##### IfcProducts")
                    st.write("IfcProducts entities: " + str(product_count))


                with col2:
                    st.markdown("#### IfcProduct distribution")
                    graph = graph_maker.get_elements_graph(st.session_state["ifc_file"])
                    st.write(graph)

if __name__ == "__main__":
    main()
