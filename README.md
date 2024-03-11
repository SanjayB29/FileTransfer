
# File Encryption and Decryption App

This application is built with Streamlit and allows users to upload files to be encrypted and stored securely. Users can also download and decrypt these files using the application. It utilizes the `cryptography` library for encryption and decryption processes and manages file and user information through a simple Excel log file.

## Features
- File encryption before upload
- Secure storage of encrypted files
- Decryption and download of files
- User-specific encryption keys managed in an Excel log

## How to Set Up and Run the Application

### Clone the Repository
To get started, clone the repository to your local machine using:
```bash
git clone https://github.com/SanjayB29/FileTransfer.git
```


### Install Dependencies
Install the necessary dependencies by running:
```bash
pip install -r requirements.txt
```

### Run the Application
Navigate to the directory containing the application files and run the application with:
```bash
streamlit run app.py
```


## How It Works
1. **Uploading and Encrypting Files**: Users can upload files through the application's upload page. The application then encrypts these files and saves them in a designated directory, along with a log entry in an Excel file containing the username, filename, and encryption key.

2. **Downloading and Decrypting Files**: Users can download and decrypt files through the application's download page. The application reads the encryption key from the Excel log, decrypts the file, and provides a download link to the user.

### Important Components
- `encrypt_file(file_content)`: Encrypts the file content using a newly generated key.
- `save_encrypted_file(encrypted_data, file_name)`: Saves the encrypted file to the filesystem.
- `save_log_to_excel(username, file_name, key)`: Logs the encryption details in an Excel file.
- `load_user_files(username)`: Loads a list of files uploaded by a specific user.
- `get_encryption_key(username, filename)`: Retrieves the encryption key for a specific file and user.

## Note
This application is intended for educational and demonstration purposes. Ensure you understand the security implications of handling encryption keys and managing file uploads and downloads in your applications.

