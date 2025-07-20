import streamlit as st
from twilio.rest import Client

st.title(" Send SMS using Twilio")


account_sid = ""
auth_token = ""
twilio_number = ""


to_number = st.text_input("Enter recipient's phone number (with +country code)")
message_body = st.text_area("Enter the message you want to send")


if st.button("Send SMS"):
    if not to_number or not message_body:
        st.error("Please fill in all fields.")
    else:
        try:
            client = Client(account_sid, auth_token)
            message = client.messages.create(
                body=message_body,
                from_=twilio_number,
                to=to_number
            )
            st.success(f" SMS sent! Message SID: {message.sid}")
        except Exception as e:
            st.error(f" Failed to send SMS: {e}")
