# IFC Screener ![Project Name](paa1.png)


This is a Streamlit application for analyzing and manipulating IFC (Industry Foundation Classes) files. The application provides various functionalities to explore and process the data contained in IFC files.

## Getting Started

To use the application, follow the steps below:

1. Install the required dependencies mentioned in the `requirements.txt` file.
2. Run the Streamlit application using the following command:



## Dependencies

The application requires the following dependencies:

- Streamlit
- Pandas
- PIL (Python Imaging Library)
- ifcopenshell

Install the dependencies using the following command:



## Usage

1. Upload an IFC file by clicking on the "Upload file" button.
2. Once the file is uploaded, you can explore the data, review quantities, create BIMTypeCodes, and add external data using the different tabs provided.

### Tab 1: DataFrame Utilities

This tab allows you to review the overall DataFrame and filter the data by class. You can download the filtered data as an Excel file.

### Tab 2: Quantities Review

In this tab, you can select a class and review the quantities associated with it. You can choose a quantity set and a specific quantity to visualize in a graph. The graph can be split by level or type.

### Tab 3: BIMTypeCodes

This tab enables you to create BIMTypeCodes in the IFC file. You can specify the BIMTypeCodes you want to create and execute the property creation process. The updated IFC file will be available for download.

### Tab 4: Add External Data

This tab allows you to upload external data (in CSV, XLSX, or Pickle format) to associate with the IFC file. You can preview the uploaded data and add new properties to the IFC elements based on the uploaded data.

## Acknowledgements

This application is built using Streamlit, a powerful Python library for creating interactive web applications. It also utilizes other libraries such as Pandas, PIL (Python Imaging Library), and ifcopenshell for data processing and manipulation.

## Support

For any issues or questions, please create an issue on the GitHub repository or contact the project maintainer.
