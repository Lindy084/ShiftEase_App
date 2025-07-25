import streamlit as st
import datetime
import pandas as pd  # <- added for CSV export

st.set_page_config(page_title="ShiftEase", layout="wide")

# Session states
if "leave_requests" not in st.session_state:
    st.session_state.leave_requests = []

if "shift_assignments" not in st.session_state:
    st.session_state.shift_assignments = []

if "notifications" not in st.session_state:
    st.session_state.notifications = []

st.title("📅 ShiftEase: Leave & Shift Manager")

# Sidebar navigation
menu = st.sidebar.radio("Go to", ["🏠 Home", "🧑‍💼 Employee", "👨‍💼 Employer", "🔔 Notifications"])

if menu == "🏠 Home":
    st.markdown("## 👋 Welcome to ShiftEase!")
    st.write(
        """
        **ShiftEase** is a simple and efficient leave and shift management system built with Python and Streamlit.

        ### 🔍 Features:
        - Employees can easily apply for time off.
        - Employers can review leave requests and assign shifts.
        - Both parties receive clear notifications.
        - Simple UI to manage and download shift and leave records.

        ---
        """
    )

elif menu == "🧑‍💼 Employee":
    st.header("🧑‍💼 Leave Request")
    name = st.text_input("Employee Name")
    leave_date = st.date_input("Leave Date", min_value=datetime.date.today())
    reason = st.text_area("Reason for Leave")

    if st.button("Submit Leave Request"):
        request = {
            "name": name,
            "date": str(leave_date),
            "reason": reason,
            "status": "Pending"
        }
        st.session_state.leave_requests.append(request)
        message = f"🔔 Leave request submitted by {name} for {leave_date}."
        st.session_state.notifications.append(message)
        st.success("Leave request submitted!")
        st.toast(message)

elif menu == "👨‍💼 Employer":
    st.header("📋 Review & Manage Requests")

    for idx, req in enumerate(st.session_state.leave_requests):
        with st.expander(f"{req['name']} - {req['date']}"):
            st.write("Reason:", req["reason"])
            st.write("Status:", req["status"])

            if req["status"] == "Pending":
                col1, col2 = st.columns(2)
                if col1.button("✅ Approve", key=f"approve_{idx}"):
                    req["status"] = "Approved"
                    message = f"✅ Leave approved for {req['name']} on {req['date']}"
                    st.session_state.notifications.append(message)
                    st.success("Leave approved.")
                    st.toast(message)
                if col2.button("❌ Reject", key=f"reject_{idx}"):
                    req["status"] = "Rejected"
                    message = f"❌ Leave rejected for {req['name']} on {req['date']}"
                    st.session_state.notifications.append(message)
                    st.warning("Leave rejected.")
                    st.toast(message)

    st.markdown("---")
    st.header("🗓️ Assign Shifts")
    emp_name = st.text_input("Employee Name (assign)")
    shift_date = st.date_input("Shift Date", min_value=datetime.date.today())
    shift_time = st.selectbox("Shift Time", ["Morning", "Afternoon", "Night"])

    if st.button("Assign Shift"):
        shift = {
            "name": emp_name,
            "date": str(shift_date),
            "time": shift_time
        }
        st.session_state.shift_assignments.append(shift)
        message = f"🔔 Shift assigned to {emp_name} on {shift_date} ({shift_time})"
        st.session_state.notifications.append(message)
        st.success("Shift assigned!")
        st.toast(message)

    st.markdown("### 📊 All Assigned Shifts")
    if st.session_state.shift_assignments:
        st.table(st.session_state.shift_assignments)

    # ====== Added Download Buttons ======
    if st.session_state.leave_requests:
        df_requests = pd.DataFrame(st.session_state.leave_requests)
        csv_requests = df_requests.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Leave Requests CSV",
            data=csv_requests,
            file_name='leave_requests.csv',
            mime='text/csv'
        )
    if st.session_state.shift_assignments:
        df_shifts = pd.DataFrame(st.session_state.shift_assignments)
        csv_shifts = df_shifts.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Shift Assignments CSV",
            data=csv_shifts,
            file_name='assigned_shifts.csv',
            mime='text/csv'
        )

elif menu == "🔔 Notifications":
    st.header("🔔 Your Notifications")

    if st.session_state.notifications:
        for note in reversed(st.session_state.notifications):
            st.info(note)
    else:
        st.write("No new notifications.")
