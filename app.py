
import os
from datetime import timezone
from io import BytesIO

import boto3
import streamlit as st
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# --------------------------------------------------
# 1. CONFIGURATION
# --------------------------------------------------

load_dotenv()

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
REGION = os.getenv("AWS_DEFAULT_REGION")

st.set_page_config(
    page_title="CloudVault | Storage Manager",
    page_icon="☁️",
    layout="wide"
)

# --------------------------------------------------
# 2. AWS CONNECTION
# --------------------------------------------------

@st.cache_resource
def get_s3_client():
    return boto3.client("s3", region_name=REGION)


try:
    s3 = get_s3_client()
except Exception as e:
    st.error(f"Could not initialize AWS connection: {e}")
    st.stop()

if not BUCKET_NAME or not REGION:
    st.error("Missing S3_BUCKET_NAME or AWS_DEFAULT_REGION in .env")
    st.stop()


# --------------------------------------------------
# 3. HELPER FUNCTIONS
# --------------------------------------------------

def get_files():
    """Retrieve all objects from the S3 bucket."""
    paginator = s3.get_paginator("list_objects_v2")
    files = []

    for page in paginator.paginate(Bucket=BUCKET_NAME):
        files.extend(page.get("Contents", []))

    return files

def get_all_versions():
    """Retrieve all versions of objects stored in S3."""

    paginator = s3.get_paginator("list_object_versions")
    records = []

    for page in paginator.paginate(Bucket=BUCKET_NAME):

        for version in page.get("Versions", []):
            version["RecordType"] = "Version"
            records.append(version)

        for marker in page.get("DeleteMarkers", []):
            marker["RecordType"] = "DeleteMarker"
            records.append(marker)

    return records


def restore_version(key, version_id):
    """Restore an older version of an S3 object."""

    s3.copy_object(
        Bucket=BUCKET_NAME,
        Key=key,
        CopySource={
            "Bucket": BUCKET_NAME,
            "Key": key,
            "VersionId": version_id
        }
    )



def format_size(size):
    """Convert bytes into readable file sizes."""
    if size < 1024:
        return f"{size} B"
    if size < 1024 ** 2:
        return f"{size / 1024:.2f} KB"
    if size < 1024 ** 3:
        return f"{size / (1024 ** 2):.2f} MB"
    return f"{size / (1024 ** 3):.2f} GB"


def upload_file(uploaded_file):
    
    def get_all_versions():
        """Retrieve object versions and delete markers from S3."""
        paginator = s3.get_paginator("list_object_versions")
        records = []

        for page in paginator.paginate(Bucket=BUCKET_NAME):
            for version in page.get("Versions", []):
                version["RecordType"] = "Version"
                records.append(version)

            for marker in page.get("DeleteMarkers", []):
                marker["RecordType"] = "DeleteMarker"
                records.append(marker)

        return records


    def restore_version(key, version_id):
        """Restore an older object version as the current version."""
        s3.copy_object(
            Bucket=BUCKET_NAME,
            Key=key,
            CopySource={
                "Bucket": BUCKET_NAME,
                "Key": key,
                "VersionId": version_id
            }
        )

    """Upload a file to Amazon S3."""
    s3.upload_fileobj(
        uploaded_file,
        BUCKET_NAME,
        uploaded_file.name,
        ExtraArgs={
            "ContentType": uploaded_file.type or "application/octet-stream"
        }
    )


# --------------------------------------------------
# 4. SIDEBAR
# --------------------------------------------------

st.sidebar.title("☁️ CloudVault")
st.sidebar.caption("Secure Cloud Storage Manager")

page = st.sidebar.radio(
    "Navigation",
    [
    "Dashboard",
    "Upload Files",
    "File Manager",
    "Version History",
    "About Project"
    ]
)

st.sidebar.divider()
st.sidebar.caption("AWS Region")
st.sidebar.code(REGION)
st.sidebar.caption("Connected S3 Bucket")
st.sidebar.code(BUCKET_NAME)


# --------------------------------------------------
# 5. DASHBOARD
# --------------------------------------------------

if page == "Dashboard":

    st.title("Cloud Storage Dashboard")
    st.write("Manage your files securely using Amazon S3.")

    try:
        files = get_files()

        total_files = len(files)
        total_size = sum(file["Size"] for file in files)

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Files", total_files)
        col2.metric("Storage Used", format_size(total_size))
        col3.metric("Cloud Provider", "AWS S3")

        st.divider()
        st.subheader("Recent Files")

        recent_files = sorted(
            files,
            key=lambda x: x["LastModified"],
            reverse=True
        )[:5]

        if recent_files:
            for file in recent_files:
                col1, col2 = st.columns([3, 1])

                col1.write(f"📄 {file['Key']}")
                col2.write(format_size(file["Size"]))
        else:
            st.info("Your cloud storage is currently empty.")

    except ClientError as e:
        st.error(f"AWS error: {e.response['Error']['Message']}")


# --------------------------------------------------
# 6. UPLOAD FILES
# --------------------------------------------------

elif page == "Upload Files":

    st.title("Upload Files")
    st.write("Select files from your computer to store in AWS S3.")

    uploaded_files = st.file_uploader(
        "Choose files",
        accept_multiple_files=True
    )

    if st.button("Upload to Cloud", type="primary"):

        if not uploaded_files:
            st.warning("Please select at least one file.")
        else:
            for file in uploaded_files:
                try:
                    with st.spinner(f"Uploading {file.name}..."):
                        upload_file(file)

                    st.success(f"Uploaded: {file.name}")

                except ClientError as e:
                    st.error(
                        f"Failed to upload {file.name}: "
                        f"{e.response['Error']['Message']}"
                    )

    st.caption("Files are stored in your private S3 bucket.")


# --------------------------------------------------
# 7. FILE MANAGER
# --------------------------------------------------

elif page == "File Manager":

    st.title("File Manager")

    try:
        files = get_files()

        if not files:
            st.info("No files available.")
        else:
            for file in files:

                key = file["Key"]

                with st.expander(f"📄 {key}"):

                    st.write("Size:", format_size(file["Size"]))

                    st.write(
                        "Last Modified:",
                        file["LastModified"].strftime(
                            "%d-%m-%Y %H:%M:%S"
                        )
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button(
                            "Download",
                            key=f"download_{key}"
                        ):
                            try:
                                response = s3.get_object(
                                    Bucket=BUCKET_NAME,
                                    Key=key
                                )

                                data = response["Body"].read()

                                st.download_button(
                                    "Save File",
                                    data=data,
                                    file_name=key.split("/")[-1],
                                    key=f"save_{key}"
                                )

                            except ClientError as e:
                                st.error(str(e))

                    with col2:
                        if st.button(
                            "Delete",
                            key=f"delete_{key}"
                        ):
                            st.session_state[
                                f"confirm_{key}"
                            ] = True

                    if st.session_state.get(f"confirm_{key}", False):
                        st.warning(
                            "Confirm deletion of this object?"
                        )

                        if st.button(
                            "Confirm Delete",
                            key=f"confirm_delete_{key}"
                        ):
                            try:
                                s3.delete_object(
                                    Bucket=BUCKET_NAME,
                                    Key=key
                                )

                                st.session_state[
                                    f"confirm_{key}"
                                ] = False

                                st.success("Object deleted.")
                                st.rerun()

                            except ClientError as e:
                                st.error(str(e))

    except ClientError as e:
        st.error(f"AWS error: {e}")


# --------------------------------------------------
# 8. PROJECT INFORMATION
# --------------------------------------------------

elif page == "About Project":

    st.title("About CloudVault")

    st.write("""
    CloudVault is a cloud-based file storage and management
    application developed using Python and Amazon Web Services.

    The application uses Amazon S3 for object storage and
    Boto3 to communicate with AWS services.
    """)

    st.subheader("Technology Stack")

    st.markdown("""
    - Python
    - Streamlit
    - Amazon S3
    - AWS IAM
    - Boto3
    - AWS server-side encryption
    - S3 Versioning
    """)

    st.subheader("Security")

    st.write("""
    The S3 bucket is configured to block public access.
    Application access is controlled using a restricted
    IAM identity and AWS credentials stored locally.
    """)

    st.success("CloudVault — Secure Cloud File Management")


# --------------------------------------------------
# 9. VERSION HISTORY AND RECOVERY
# --------------------------------------------------

elif page == "Version History":

    st.title("File Version History")
    st.write(
        "View previous versions of your files "
        "and restore older versions."
    )

    try:
        records = get_all_versions()

        if not records:
            st.info("No file versions found.")
        else:
            records.sort(
                key=lambda x: x["LastModified"],
                reverse=True
            )

            st.subheader("Stored Versions")

            for index, record in enumerate(records):

                key = record["Key"]
                version_id = record["VersionId"]
                record_type = record["RecordType"]

                with st.expander(
                    f"{key} — {record_type}"
                ):

                    st.write("Version ID:", version_id)
                    st.write(
                        "Last Modified:",
                        record["LastModified"].strftime(
                            "%d-%m-%Y %H:%M:%S"
                        )
                    )

                    if record_type == "DeleteMarker":

                        st.warning(
                            "This version represents a deletion."
                        )

                    else:

                        st.write(
                            "Size:",
                            format_size(record["Size"])
                        )

                        if st.button(
                            "Restore this version",
                            key=f"restore_{index}"
                        ):

                            try:
                                restore_version(key, version_id)

                                st.success(
                                    f"Restored: {key}"
                                )

                                st.rerun()

                            except ClientError as error:
                                st.error(
                                    error.response["Error"]["Message"]
                                )

    except ClientError as error:
        st.error(
            f"AWS version history error: "
            f"{error.response['Error']['Message']}"
        )

