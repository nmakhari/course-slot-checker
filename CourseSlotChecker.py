import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

print("STARTING COURSE SLOT CHECKER")

# SUBJECT, COURSE CODE, ARRAY OF EMAILS TO NOTIFY
COURSES = [
  ("PSYCH", "207", []),
  ("EARTH", "121", []),
  ("SCI", "238", [])
]
URL = "https://classes.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl"
ONLN_TARGET_TEXT = "ONLN  ONLINE    "

smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "SENDER GMAIL HERE"
sender_password = "GMAIL APP PASSWORD HERE"

while True:
  for course in COURSES:
    form_payload = {
        "level": "under",
        "sess": "1239",
        "subject": course[0],
        "cournum": course[1]
    }
    
    response = requests.post(URL, data=form_payload)
    
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
    
        # Find the table cell for the online class offering
        target_td = soup.find("td", text=ONLN_TARGET_TEXT)
    
        if target_td:
            # Find the parent row
            target_tr = target_td.find_parent("tr")
    
            if target_tr:
              # Get all cell contents for that row
              cols = [ele.text.strip() for ele in target_tr.find_all("td")]
    
              if int(cols[6]) - int(cols[7]) > 0:
                print("AVAILABLE SPOT")
                # Create an SMTP server connection
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(sender_email, sender_password)

                for receiver_email in course[2]:
                  # Construct the email message
                  msg = MIMEMultipart()
                  msg["From"] = sender_email
                  msg["To"] = receiver_email
                  msg["Subject"] = f'{course[0]} {course[1]} has an open slot.'
      
                  body = f'{course[0]} {course[1]} has an open slot.'
                  msg.attach(MIMEText(body, "plain"))
      
                  # Send the email
                  server.sendmail(sender_email, receiver_email, msg.as_string())
    
                # Close the SMTP server connection
                server.quit()
              else:
                print("NO SPOTS")
            else:
                print("The <tr> element containing the specified <td> was not found.")
                raise "NO TR"
        else:
            print("The <td> element containing the specified text was not found.")
            raise "NO TD"
    else:
        print(f"POST request failed with status code: {response.status_code}")
        raise "REQUEST FAILED"

  time.sleep(10)

  