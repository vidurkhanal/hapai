import json
import smtplib
import os
from email.mime.text import MIMEText
from tokenize import Triple


def notify(message):
    try:
        message = json.loads(message)
        mp3_fid = message["mp3_fid"]
        sender_address = "test@test.com"
        receiver_add = message["username"]
        # msg = EmailMessage()
        # msg.set_content(f"mp3 file_id: {mp3_fid} is now ready!!")
        msg = MIMEText(f'mp3 file_id: {mp3_fid} is now ready!!')
        msg["Subject"] = "MP3 Download"
        msg["From"] = sender_address
        msg["To"] = receiver_add

        with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
            server.login(os.environ.get("MAILTRAP_USER"),
                         os.environ.get("MAILTRAP_PASSWORD"))
            server.sendmail(sender_address, receiver_add, msg.as_string())
            print("Email Sent...", flush=True)
    except Exception as err:
        print(err, flush=True)
        return err
