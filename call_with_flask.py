import streamlit as st
from twilio.rest import Client

account_sid = ''
auth_token = ''
twilio_number = ''


st.title(" Simple Phone Call App with Twilio")
st.markdown("Enter a phone number and make a call using a default Twilio message.")

to_number = st.text_input("Enter recipient phone number (e.g. +91XXXXXXXXXX)")

if st.button("Make Call"):
    if not to_number:
        st.warning("Please enter a phone number.")
    else:
        try:
            
            client = Client(account_sid, auth_token)

            
            call = client.calls.create(
                to=to_number,
                from_=twilio_number,
                url="http://demo.twilio.com/docs/voice.xml"
            )

            st.success(f"Call initiated successfully! Call SID: {call.sid}")
        except Exception as e:
            st.error(f" Failed to make the call: {str(e)}")
