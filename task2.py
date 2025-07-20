import smtplib
from email.message import EmailMessage
import os

# ==== CONFIG: Your Gmail credentials ====
sender_email = ""
app_password = ""  

def send_email(receiver_email, message_content, attachment_path=None):
    msg = EmailMessage()
    msg['Subject'] = 'Test Email from Python'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content(message_content)

    
    if attachment_path:
        if os.path.isfile(attachment_path):
            try:
                with open(attachment_path, 'rb') as f:
                    file_data = f.read()
                    file_name = os.path.basename(attachment_path)
                    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)
                    print(f"📎 Attached file: {file_name}")
            except Exception as e:
                print(f"❌ Could not attach file: {e}")
        else:
            print("⚠️ File not found. Proceeding without attachment.")

    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)
            print("✅ Email sent to", receiver_email)
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


while True:
    print("\n=== New Email ===")
    to = input("Enter recipient email address: ")
    msg = input("Enter the message to send: ")
    file_path = input("Enter attachment file path (or press Enter to skip): ").strip()

    send_email(to, msg, file_path if file_path else None)

    another = input("Send another email? (y/n): ").lower()
    if another != 'y':
        print("👋 Exiting email sender.")
        break
