import streamlit as st
import pandas as pd
from io import BytesIO
import os

# File path for the Excel file
FILE_PATH = "student_details_10th.xlsx"

# Function to load the Excel file or create a new one
def load_excel(file_path=FILE_PATH):
    try:
        return pd.read_excel(file_path)
    except FileNotFoundError:
        # Return an empty DataFrame if the file doesn't exist
        return pd.DataFrame(columns=["Name", "Mother's Name", "Email", "Address"])

# Function to save DataFrame to Excel
def save_to_excel(df, file_path=FILE_PATH):
    try:
        temp_file = "temp_student_details_10th.xlsx"
        df.to_excel(temp_file, index=False, engine='openpyxl')
        # Replace the original file
        os.replace(temp_file, file_path)
    except PermissionError:
        st.error("The file is currently open. Please close it and try again.")

# Streamlit app
def main():
    st.title("Student Details Class 10th")

    # Initialize session state for input clearing
    if "submitted" not in st.session_state:
        st.session_state["submitted"] = False

    # Form for student details
    with st.form("student_form"):
        name = st.text_input("Student Name", value="" if st.session_state["submitted"] else "")
        mother_name = st.text_input("Mother's Name", value="" if st.session_state["submitted"] else "")
        email = st.text_input("Email (Optional)", value="" if st.session_state["submitted"] else "")
        address = st.text_area("Address", value="" if st.session_state["submitted"] else "")
        submitted = st.form_submit_button("Submit")

    if submitted:
        # Validate inputs
        if name and mother_name and address:  # Email is now optional
            # Load the existing Excel file
            df = load_excel()

            # Append new details using pd.concat
            new_data = {"Name": name, "Mother's Name": mother_name, "Email": email if email else None, "Address": address}
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)

            # Save to Excel
            save_to_excel(df)

            # Balloon animation alert using st.empty() and custom HTML/JS
            alert = st.empty()
            alert.markdown(
                """
                <div style="position: relative; text-align: center; width: 100%; padding-top: 10px;">
                    <div style="animation: floatUp 4s ease-in-out infinite; font-size: 18px; font-weight: bold; background-color: #4CAF50; color: white; border-radius: 25px; padding: 10px; width: 200px; margin: 0 auto; text-align: center;">
                        Details submitted successfully!
                    </div>
                </div>
                <style>
                    @keyframes floatUp {
                        0% { transform: translateY(0); opacity: 1; }
                        50% { transform: translateY(-30px); opacity: 0.8; }
                        100% { transform: translateY(-60px); opacity: 0.6; }
                    }
                </style>
                """, unsafe_allow_html=True
            )

            # Clear the form inputs after submission
            st.session_state["submitted"] = True
        else:
            st.error("Please fill in all the required fields (Name, Mother's Name, and Address).")
            st.session_state["submitted"] = False

    # Admin login section
    st.subheader("Admin Section")
    admin_password = "Yasmeh123#"  # Replace this with a secure password
    admin_access = False

    # Admin login form
    with st.form("admin_login"):
        password = st.text_input("Enter Admin Password", type="password")
        login = st.form_submit_button("Login")

    if login:
        if password == admin_password:
            admin_access = True
            st.success("Admin access granted.")
        else:
            st.error("Incorrect password. Access denied.")

    # Allow download only if admin is authenticated
    if admin_access:
        st.write("Welcome, Admin! You can download the Excel sheet below.")

        # Check if the Excel file exists
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, "rb") as file:
                st.download_button(
                    label="Download Excel",
                    data=file,
                    file_name="student_details_10th.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )
        else:
            st.error("No data found. Please submit some student details first.")

if __name__ == "__main__":
    main()
