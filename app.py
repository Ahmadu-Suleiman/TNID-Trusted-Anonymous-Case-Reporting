import streamlit as st
from tnid_api import verify_phone_number
from db_config import add_report, get_reports
import uuid

st.title("Trusted Anonymous Reporting Platform")

# Verification and Reporting Section
st.subheader("Submit a Report")

phone_number = st.text_input("Enter your phone number for verification (only for credibility, not saved)")
if st.button("Verify Phone Number"):
    if phone_number:
        verified = verify_phone_number(phone_number)
        if verified:
            st.success("Phone number verified. You can submit a report anonymously.")
            user_id = str(uuid.uuid4())  # Generate a unique, anonymous user ID
            st.session_state['user_id'] = user_id  # Store the user ID in session state
        else:
            st.error("Verification failed. Please try again.")

if 'user_id' in st.session_state:
    category = st.selectbox("Category", ["Corruption", "Safety", "Crime", "Other"])
    details = st.text_area("Describe the issue")
    if st.button("Submit Report"):
        add_report(st.session_state['user_id'], category, details)
        st.success("Report submitted anonymously.")

# Display Pending Reports (For Moderators)
# st.subheader("Pending Reports")
# if st.checkbox("Show pending reports"):
#     reports = get_reports()
#     for report in reports:
#         st.write(f"Category: {report[2]}, Details: {report[3]}, Timestamp: {report[4]}")
#         if st.button("Mark as Resolved", key=report[0]):
#             update_report_status(report[0], "Resolved")
#             st.success("Report marked as resolved.")
