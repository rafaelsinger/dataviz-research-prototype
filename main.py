import streamlit as st
from init import query_db
from helpers import get_pdf_path
import os
# to do: file uploader

st.title('Research Paper Search Engine')

prompt = st.text_input('Enter a prompt')
num_results = st.slider('Number of results', min_value=1, max_value=9, value=3)

with st.spinner("Querying database"):
    if prompt != "":
        paper_ids = query_db(prompt, num_results)
        for i, id in enumerate(reversed(paper_ids)):
            st.write(f"{i+1}. {id}")
            pdf_file_path = get_pdf_path(id)
            if os.path.exists(pdf_file_path):
                with open(pdf_file_path, "rb") as f:
                    pdf_data = f.read()
                
                st.download_button(
                    label="Download PDF",
                    data=pdf_data,
                    file_name=f"{id}",
                    mime="application/pdf"
                )
            else:
                st.warning("PDF with that title does not exist.")
