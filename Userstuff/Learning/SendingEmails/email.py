from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from string import Template
from pathlib import Path
import smtplib

temp = Template(Path("template.html").read_text()) # makes a thing which allows you te send html


message = MIMEMultipart()
message["from"] = "Mosh Hamedani"
message["to"] = "testuser@codewithmosh"
#message.attach(MIMEImage(Path("name.png").read_bytes())) - attaches images,
#bytes IS required
body = temp.substitute({"name": "john"})
message["subject"] = "Test br chil"
message.attach(MIMEText(body , "html")) #attaches script

with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:  #port and host can be different
    smtp.ehlo() #establishes communication between the server
    smtp.starttls()
    smtp.login("testuser@codewithmosh.com", "todayskyisNOTblue1234")
    smtp.send_message(message)
    print('send')
