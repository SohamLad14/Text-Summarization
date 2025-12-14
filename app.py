import streamlit as st
import requests


st.set_page_config(page_title = "Text Summarization")

st.title("Text Summarization App")
st.write("Enter text or upload (TXT,DOCS,PDF) to summarize")

option = st.radio("Choose Option" , ("Text" ,"Upload"))

API_URL = " http://127.0.0.1:8000"


if option == 'Text':
    user_text = st.text_area("Enter the text here")
    if st.button("Summarize Text"):
        if user_text.strip() == "":
            st.warning("Enter some text to summarize")
        else:
            response = requests.get(f"{API_URL}/summarization" ,params={"text" : user_text})
            if response.status_code == 200 :
                data =response.json()
                st.subheader("Original Text")
                st.write(data['original_text'])
                st.subheader("Summary")
                st.write(data['summary'])
            else:
                st.error("Error Summarizing the text")
else :
    upload_file = st.file_uploader("Upload a file",type=["pdf","docx", "txt"])
    if upload_file is not None:
        if st.button("Summarize File"):
            files = {"file" : (upload_file.name , upload_file ,upload_file.type)}
            response = requests.post(f"{API_URL}/read-doc/" ,files =files)
            if response.status_code == 200 :
                data = response.json()
                st.subheader("Original Text")
                st.write(data["original_text"])
                st.subheader("Summary")
                st.write(data['summary'])
            else:
                st.error(f"Error:{response.json().get('detail')}")


