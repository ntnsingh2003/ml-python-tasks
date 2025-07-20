import streamlit as st
import os
from datetime import datetime
from PIL import Image, ImageDraw
import pywhatkit
import smtplib
from email.message import EmailMessage
from twilio.rest import Client
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import requests

# 🔥 Stylish Background
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #141e30, #243b55);
        color: white;
    }
    h1, h2, h3, label, .stTextInput > div > div > input, .stTextArea > div > textarea {
        color: white !important;
    }
    .stButton > button {
        background-color: #f63366;
        color: white;
        border-radius: 8px;
        padding: 0.6em 1em;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #ff5c8d;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Menu
st.sidebar.title("🛠️ Multi-Automation Toolkit")
task = st.sidebar.selectbox("Select Task", [
    "📲 WhatsApp", "📧 Email", "📞 Call", "📩 SMS",
    "🔍 Google Search", "🖼️ Image Art", "🌐 Site Downloader"
])

# 📲 WhatsApp Message
if task == "📲 WhatsApp":
    st.title("📲 Send WhatsApp Message")
    phone = st.text_input("Enter WhatsApp number (with +91)")
    msg = st.text_area("Enter your message")
    send_now = st.checkbox("Send instantly?")
    if st.button("🚀 Send Message"):
        try:
            if send_now:
                pywhatkit.sendwhatmsg_instantly(phone, msg, wait_time=15, tab_close=True)
            else:
                now = datetime.now()
                pywhatkit.sendwhatmsg(phone, msg, now.hour, now.minute + 2)
            st.success("✅ Message sent/scheduled")
        except Exception as e:
            st.error(f"❌ {e}")

# 📧 Email Sender
elif task == "📧 Email":
    st.title("📧 Send Email with Attachment")
    sender = st.text_input("Sender Gmail")
    app_pass = st.text_input("App Password", type="password")
    to = st.text_input("Receiver Email")
    body = st.text_area("Message")
    file = st.file_uploader("📌 Upload file (optional)")

    if st.button("📤 Send Email"):
        try:
            msg = EmailMessage()
            msg["Subject"] = "Sent via Streamlit App"
            msg["From"] = sender
            msg["To"] = to
            msg.set_content(body)

            if file:
                msg.add_attachment(file.read(), maintype='application', subtype='octet-stream', filename=file.name)

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(sender, app_pass)
                smtp.send_message(msg)
            st.success("✅ Email sent!")
        except Exception as e:
            st.error(f"❌ {e}")

# 📞 Phone Call
elif task == "📞 Call":
    st.title("📞 Make a Call with Twilio")
    sid = st.text_input("Twilio SID")
    token = st.text_input("Twilio Auth Token", type="password")
    from_number = st.text_input("Twilio Number")
    to_number = st.text_input("Recipient Number")
    twiml_url = st.text_input("TwiML Bin URL")

    if st.button("📞 Call Now"):
        try:
            client = Client(sid, token)
            call = client.calls.create(to=to_number, from_=from_number, url=twiml_url)
            st.success(f"📞 Call initiated! SID: {call.sid}")
        except Exception as e:
            st.error(f"❌ {e}")

# 📩 SMS
elif task == "📩 SMS":
    st.title("📩 Send SMS via Twilio")
    sid = st.text_input("Twilio SID")
    token = st.text_input("Auth Token", type="password")
    from_number = st.text_input("Twilio Number")
    to_number = st.text_input("Recipient Number")
    message = st.text_area("Message")

    if st.button("📤 Send SMS"):
        try:
            client = Client(sid, token)
            msg = client.messages.create(body=message, from_=from_number, to=to_number)
            st.success(f"✅ SMS sent! SID: {msg.sid}")
        except Exception as e:
            st.error(f"❌ {e}")

# 🔍 Google Search
elif task == "🔍 Google Search":
    from googlesearch import search
    st.title("🔍 Google Search")
    query = st.text_input("Search query")
    if st.button("Search"):
        try:
            results = search(query, num_results=5, advanced=True)
            for r in results:
                st.markdown(f"**{r.title}**\n\n🔗 [{r.url}]({r.url})\n\n📖 {r.description}")
        except Exception as e:
            st.error(f"❌ {e}")

# 🖼️ Generate Digital Art
elif task == "🖼️ Image Art":
    st.title("🖼️ Create Digital Art")
    text = st.text_input("Text on Image", "Hello from Python!")
    if st.button("🎨 Generate Image"):
        width, height = 800, 400
        image = Image.new("RGB", (width, height), color="white")
        draw = ImageDraw.Draw(image)
        draw.rectangle([50, 50, 200, 200], fill="skyblue", outline="black", width=3)
        draw.ellipse([300, 50, 450, 200], fill="lightgreen", outline="black", width=3)
        draw.line([500, 100, 700, 100], fill="red", width=5)
        draw.text((50, 250), text, fill="black")
        image.save("my_art.png")
        st.image("my_art.png", caption="Your Art 🎨")

# 🌐 Website Downloader
elif task == "🌐 Site Downloader":
    st.title("🌐 Download Website Content")
    input_url = st.text_input("Enter website URL (https://...)")
    if st.button("📅 Download"):
        try:
            output_dir = "downloaded_site"
            visited = set()

            def sanitize_filename(url):
                parsed = urlparse(url)
                path = parsed.path.strip("/")
                if not path or path.endswith("/"):
                    return "index.html"
                return path.replace("/", "_") + ".html"

            def save_content(url, content):
                name = sanitize_filename(url)
                path = os.path.join(output_dir, name)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "wb") as f:
                    f.write(content)

            def crawl(url):
                if url in visited:
                    return
                visited.add(url)
                try:
                    r = requests.get(url)
                    if "text/html" in r.headers.get("Content-Type", ""):
                        save_content(url, r.content)
                        soup = BeautifulSoup(r.text, "html.parser")
                        for tag in soup.find_all(["a", "img", "link", "script"]):
                            attr = "href" if tag.name in ["a", "link"] else "src"
                            file_url = tag.get(attr)
                            if file_url:
                                full_url = urljoin(url, file_url)
                                if urlparse(full_url).netloc == urlparse(url).netloc:
                                    crawl(full_url)
                    else:
                        save_content(url, r.content)
                except Exception as e:
                    st.warning(f"⚠️ Error fetching {url}: {e}")

            if not input_url.startswith("http"):
                input_url = "https://" + input_url

            crawl(input_url)
            st.success("✅ Website downloaded into 'downloaded_site/'")
        except Exception as e:
            st.error(f"❌ {e}")