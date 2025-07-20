from flask import Flask, request, Response
from twilio.rest import Client
from pyngrok import ngrok


account_sid = ''
auth_token = ''
twilio_number = ''  
to_number = '+91XXXXXXXXXX'     


custom_message = "Hello! This is Nitin's custom call from Python using Twilio and Flask. Have a great day!"


app = Flask(__name__)

@app.route("/voice", methods=['GET', 'POST'])
def voice():
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice">{custom_message}</Say>
</Response>"""
    return Response(twiml, mimetype='text/xml')


def start_call():
   
    public_url = ngrok.connect(5000)
    print(f"Public URL: {public_url}")


    client = Client(account_sid, auth_token)
    call = client.calls.create(
        to=to_number,
        from_=twilio_number,
        url=f"{public_url}/voice"
    )
    print(f"📞 Call initiated. SID: {call.sid}")

if __name__ == "__main__":
    import threading
    threading.Thread(target=start_call).start()
    app.run()
