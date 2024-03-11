import streamlit as st
from cryptography.fernet import Fernet
import pandas as pd
import os
import base64

# Initialize session state variables
if 'encryption_keys' not in st.session_state:
    st.session_state['encryption_keys'] = {}

# Directory for encrypted files
encrypted_files_dir = 'encrypted_files'
if not os.path.exists(encrypted_files_dir):
    os.makedirs(encrypted_files_dir)

# Path to the Excel log file
log_file_path = 'upload_log.xlsx'

def encrypt_file(file_content):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(file_content)
    return encrypted_data, key

def save_encrypted_file(encrypted_data, file_name):
    file_path = os.path.join(encrypted_files_dir, file_name + '.enc')
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)
    return file_path

def save_log_to_excel(username, file_name, key):
    new_row = pd.DataFrame([[username, file_name, key.decode()]], columns=['Username', 'Filename', 'Encryption Key'])
    if os.path.exists(log_file_path):
        df = pd.read_excel(log_file_path)
        df = pd.concat([df, new_row], ignore_index=True)
    else:
        df = new_row
    df.to_excel(log_file_path, index=False)

    
def load_user_files(username):
    if os.path.exists(log_file_path):
        df = pd.read_excel(log_file_path)
        return df[df['Username'] == username]['Filename'].tolist()
    return []

def get_encryption_key(username, filename):
    if os.path.exists(log_file_path):
        df = pd.read_excel(log_file_path)
        user_file = df[(df['Username'] == username) & (df['Filename'] == filename)]
        if not user_file.empty:
            return user_file.iloc[0]['Encryption Key']
    return None

def download_button(object_to_download, download_filename, button_text):
    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download).decode()
    except AttributeError:
        b64 = base64.b64encode(object_to_download.encode()).decode()

    download_link = f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">Click to download {button_text}</a>'
    st.markdown(download_link, unsafe_allow_html=True)

def app_upload():
    st.header("Upload a File")
    username = st.text_input("Enter your name", key="username")
    uploaded_file = st.file_uploader("Choose a file", key="uploaded_file")
    if st.button("Upload"):
        if uploaded_file is not None and username:
            file_content = uploaded_file.getvalue()
            encrypted_data, key = encrypt_file(file_content)
            encrypted_file_path = save_encrypted_file(encrypted_data, uploaded_file.name)
            save_log_to_excel(username, uploaded_file.name, key)
            st.session_state['encryption_keys'][username + uploaded_file.name] = key
            st.success("File encrypted and uploaded successfully!")

def app_download():
    st.header("Download a File")
    username = st.text_input("Enter the uploader's name", key="down_username")
    if username:
        user_files = load_user_files(username)
        selected_file = st.selectbox("Select a file to download", user_files, key="file_selection")
        if st.button("Download"):
            key = get_encryption_key(username, selected_file)
            if key:
                cipher_suite = Fernet(key.encode())
                file_path = os.path.join(encrypted_files_dir, selected_file + '.enc')
                with open(file_path, 'rb') as file:
                    encrypted_data = file.read()
                decrypted_data = cipher_suite.decrypt(encrypted_data)
                download_button(decrypted_data, selected_file, "this file")
            else:
                st.error("File not found or encryption key missing.")

# Streamlit page setup
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Choose the page", ["Upload Page", "Download Page"])

if app_mode == "Upload Page":
    app_upload()
elif app_mode == "Download Page":
    app_download()
