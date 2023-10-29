import streamlit as st
import requests

# Define the Flask API base URL
API_BASE_URL = "https://c2ed-103-141-117-152.ngrok-free.app"

st.title("PDF File Management")

# Upload a PDF file
st.header("Upload PDF")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
if uploaded_file is not None:
    response = requests.post(f"{API_BASE_URL}/upload", files={"pdf": uploaded_file})
    if response.status_code == 200:
        st.write("File uploaded successfully")
    else:
        st.write(f"Upload failed with status code {response.status_code}")

# List available PDFs
st.header("List of Available PDFs")
pdf_list_response = requests.get(f"{API_BASE_URL}/listpdf")
if pdf_list_response.status_code == 200:
    pdf_list = pdf_list_response.json().get("pdfs", [])
    for pdf in pdf_list:
        st.write(pdf)
else:
    st.write(f"Failed to retrieve PDF list with status code {pdf_list_response.status_code}")

# Download a PDF
st.header("Download PDF")
try:
    selected_pdf = st.selectbox("Select a PDF to download", pdf_list)
    if st.button("Download"):
        if selected_pdf:
            response = requests.get(f"{API_BASE_URL}/download/{selected_pdf}")
            if response.status_code == 200:
                with open(selected_pdf, 'wb') as f:
                    f.write(response.content)
                st.success(f"Downloaded {selected_pdf}")
            else:
                st.write(f"Download failed with status code {response.status_code}")

    # Provide a link to download the file
    if selected_pdf:
        st.markdown(f"**[Download {selected_pdf}](./{selected_pdf})**")
except:
    print("\n\n\n\n<CHECK SERVER STATUS>")

