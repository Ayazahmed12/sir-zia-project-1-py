import streamlit as st 
import pandas as pd
import os
from io import BytesIO
st.set_page_config(page_title="Data Sweeper", layout='wide')


# custom css
st.markdown(
    """
    <style>
    .stApp{
       background-color: black;
       color: white;
       }
       </style>
       """,
       unsafe_allow_html=True
)

# Title and description
st.title("Datasweeper Sterling Integrator By Ayaz Ahmed")
st.write("Transform Your Files between CSV and Excel formats with buil-in data cleaning and visulization creating the project for quater3!")

#File uploader

uploaded_files = st.file_uploader("upload your file(accept SCV and Excel)",type=["CSV","Excel"],accept_multiple_files=(True))

for file in uploaded_files:
    file_ext =os.path.splitext(file.name[-1].lower) ()

    if file_ext == ".SCV":
        df=pd.read_csv(file)

    elif file_ext == "xlsx":
        df=pd.read_excel(file)
    else:
        st.error(f"Unsupported file type: {file_ext}")
        continue
     #file details
    st.write("preview the head of the Dataframe")
    st.dataframe(df.head())

    #Data Cleaning Options
    st.subheader("Data cleaning options")
    if st.checkbox(f"cleaning data for {file.name}"):
        col1, col2 =st.columns(2)

        with col1:
            if st.button(f"Remove Duplicates from the file : {file.name}"):
                df.drop_duplicates(inplace=True)
                st.write("Duplicates Removed!")

        with col2:
            if st.button(f"fill missing value for {file.name}"):
                numeric_cols = df.select_dtypes(include=["number"]).columns
                df[numeric_cols] = df [numeric_cols].fillna(df[numeric_cols].mean())
                st.write("Missing values have been filled")            

        st.subheader("select colomes to keep")        
        colums = st.multiselect(f"choos colums for {file.name}", df.columns, df.colums, default=df.columns)
        df = df[colums]

        
        #Data visulization

        st.subheader("Data visulization")
        if st.checkbox(f"show visulization for[{file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:, 2])

        #Conversion Options
        st.subheader("conversion options")
        conversion_type = st.radio(f"convert{file.name} to:",["CVS" ,"Excel"], key=file.name)
        if st.button(f"convert{file.name}"):
            buffer = BytesIO()
            if conversion_type =="CVS":
                df.to.cvs(buffer, index=False)
                file_name = file.name.replace(file_ext, ".cvs")
                mime_type ="text/cvs"

            elif conversion_type == "Excel":
                df.to.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, "xlsx")
                mime_type ="application/vnd.openxmlformat-officedocument.spreadsheettml.sheet"
                buffer.seek(0)

                st.download_button(
                    label=f"Download {file.name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )

                st.success ("All files precessed successfully!")
