import streamlit as st
from twilio.rest import Client

account_sid = ''
auth_token = ''
twilio_number = 
# 🔗 Your TwiML Bin URL (created in Twilio console)
twiml_url = "https://handler.twilio.com/twiml/EHb27e3497be81db8bf3da826fe5781590" # replace with your actual TwiML URL

st.title(" Twilio Call from Streamlit (No ngrok)")

to_number = st.text_input("Enter recipient phone number (e.g. +91XXXXXXXXXX)")

if st.button("Make Call"):
    if not to_number.startswith("+"):
        st.error(" Phone number must start with '+' and include country code.")
    else:
        try:
            client = Client(account_sid, auth_token)
            call = client.calls.create(
                to=to_number,
                from_=twilio_number,
                url=twiml_url
            )
            st.success(f" Call initiated successfully! SID: {call.sid}")
        except Exception as e:
            st.error(f"Failed to make call: {e}")
