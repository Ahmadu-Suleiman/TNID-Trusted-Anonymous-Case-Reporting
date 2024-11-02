import streamlit as st
from tnid_api import verify_phone_number
from db_config import add_report, get_reports
import uuid
from datetime import datetime

# Define navigation state
if 'view' not in st.session_state:
    st.session_state.view = 'home'

# Helper function to navigate between screens
def navigate_to(view_name):
    st.session_state.view = view_name
    st.rerun()  # Refresh the app to load the new screen

# Home Screen - Submit Report
def home_screen():
    st.title("AnonymiTNID - Anonymous Community Reporting")
    st.subheader("Empowering Communities Through Anonymous and Verified Reporting")

    # Introduction
    st.markdown("""
        AnonymiTNID is a secure, anonymous platform that empowers individuals to report local issues or injustices. 
        Using TNID verification, AnonymiTNID ensures that each report is credible while keeping user identities anonymous.
    """)

    # Verification Section
    st.header("Step 1: Verify Your Identity Anonymously")
    phone_number = st.text_input("Enter your phone number for verification (TNID-verified for credibility, not stored)")

    if st.button("Verify Phone Number"):
        if phone_number:
            verified = verify_phone_number(phone_number)
            if verified:
                st.success("Phone number verified successfully. Your identity remains anonymous.")
                user_id = str(uuid.uuid4())  # Create unique anonymous user ID
                st.session_state['user_id'] = user_id  # Store user ID in session
            else:
                st.error("Verification failed. Please try a valid phone number.")

    # Report Submission Section
    if 'user_id' in st.session_state:
        st.header("Step 2: Submit an Anonymous Report")
        category = st.selectbox("Choose a Report Category", ["Corruption", "Safety", "Crime", "Environmental Hazard", "Other"])
        details = st.text_area("Describe the issue in detail")

        if st.button("Submit Report"):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            add_report(st.session_state['user_id'], category, details)
            st.success("Thank you! Your report has been submitted anonymously.")
            st.info(f"Submitted on {timestamp}")

    # Button to navigate to all cases screen
    st.button("View All Uploaded Cases", on_click=lambda: navigate_to('all_cases'))

# All Cases Screen
def all_cases_screen():
    st.title("All Uploaded Cases")

    # Fetch and display all reports
    reports = get_reports()
    if reports:
        for report in reports:
            st.write(f"**Category**: {report[2]}")
            st.write(f"**Details**: {report[3]}")
            st.write(f"**Submitted on**: {report[4]}")
            st.write(f"**Status**: {report[5]}")
            st.write("---")
    else:
        st.write("No reports available at the moment.")

    # Button to return to the home screen
    st.button("Return to Home", on_click=lambda: navigate_to('home'))

# Main application logic
if st.session_state.view == 'home':
    home_screen()
elif st.session_state.view == 'all_cases':
    all_cases_screen()
