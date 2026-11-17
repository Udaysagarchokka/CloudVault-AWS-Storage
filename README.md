
# ☁️ CloudVault – AWS Cloud Storage Manager

A Python-based cloud file storage and management application
built using Amazon Web Services (AWS), Boto3 and Streamlit.

CloudVault allows users to securely upload, view, download,
delete and recover files stored in Amazon S3.

## 🚀 Features

- Upload files to Amazon S3.
- View and manage stored files.
- Download files from cloud storage.
- Delete stored objects.
- Monitor storage usage.
- View previous file versions.
- Restore older file versions.
- Private S3 bucket with public access blocked.
- IAM-based access control.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application programming |
| Streamlit | Web interface |
| Amazon S3 | Cloud object storage |
| Boto3 | AWS Python SDK |
| AWS IAM | Identity and access management |
| S3 Versioning | File version history and recovery |
| Git | Version control |
| GitHub | Source code hosting |

## 🏗️ Architecture

```text
       User
        |
        v
  Streamlit Dashboard
        |
        v
    Python Application
        |
        v
       Boto3
        |
        v
   AWS IAM Authentication
        |
        v
     Amazon S3
        |
        v
  Cloud File Storage
  + Version History
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Udaysagarchokka/CloudVault-AWS-Storage.git
cd CloudVault-AWS-Storage
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure AWS credentials

Create a `.env` file in the project root.

Add your own AWS configuration:

```env
AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
AWS_DEFAULT_REGION=ap-southeast-2
S3_BUCKET_NAME=YOUR_BUCKET_NAME
```

Never upload `.env` or AWS credentials to GitHub.

### 5. Run the application

```bash
python -m streamlit run app.py
```

Open:

http://localhost:8501

## 🔐 Security

- S3 Block Public Access is enabled.
- AWS access is controlled using IAM permissions.
- Credentials are stored locally in environment variables.
- Server-side encryption is enabled on the S3 bucket.
- S3 Versioning supports recovery of previous object versions.

## ☁️ AWS Services Used

**Amazon S3:** Stores files as cloud objects.

**AWS IAM:** Controls application permissions.

**S3 Versioning:** Maintains multiple versions of uploaded objects.

## 🎯 Project Objective

To develop a practical cloud storage management
application demonstrating cloud computing fundamentals,
AWS object storage, cloud security, Python integration
and file recovery.

## 👨‍💻 Author

Uday Sagar Chokka

GitHub:
https://github.com/Udaysagarchokka

## 📌 Project Status

Developed as a cloud computing portfolio project
for learning and demonstrating AWS fundamentals.
