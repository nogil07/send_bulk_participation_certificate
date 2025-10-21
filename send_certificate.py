import csv
import smtplib
import os
import time
import random
import ssl
from email.message import EmailMessage
from email.utils import make_msgid, formataddr

# --- Configuration ---
SENDER_NAME = "Team Prayag25"
SENDER_EMAIL = "Your mail id"
SENDER_PASSWORD = "16-digit password" # IMPORTANT: Use your 16-character Google App Password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

# --- Email Content and Sending Functions ---
def get_random_subject(event_name):
    """Returns a randomly chosen subject line for uniqueness."""
    subject_options = [
        f"Thank you for participating in {event_name}",
        f"Your {event_name} Participation Certificate",
        f"A note of thanks from the Prayag25 Team"
    ]
    return random.choice(subject_options)

def create_email_body_html(participant_name, event_name, sender_email):
    """Creates the personalized HTML body of the email."""
    return f"""<html><body><p>Hello {participant_name},</p><p>On behalf of the Prayag25 team, we wanted to extend our thanks for your active participation in the <b>{event_name}</b>. It was a pleasure to have you with us.</p><p>Please find your certificate of participation attached.</p><p></p><br><p>Best regards,<br>Team Prayag25</p></body></html>"""

def create_email_body_plain(participant_name, event_name, sender_email):
    """Creates the personalized plain text body of the email."""
    return f"Hello {participant_name},\n\nOn behalf of the Prayag25 team, we wanted to extend our thanks for your active participation in the {event_name}. It was a pleasure to have you with us.\n\nPlease find your certificate of participation attached.\n\n\n\nBest regards,\nTeam Prayag25"

def send_certificate_email(participant):
    """
    Sends a single certificate email. Returns True on success and False on failure.
    """
    try:
        msg = EmailMessage()
        msg['From'] = formataddr((SENDER_NAME, SENDER_EMAIL))
        msg['To'] = formataddr((participant['Name'], participant['Email']))
        msg['Subject'] = get_random_subject(participant['Event'])
        msg['Message-ID'] = make_msgid()
        
        msg.set_content(create_email_body_plain(participant['Name'], participant['Event'], SENDER_EMAIL))
        msg.add_alternative(create_email_body_html(participant['Name'], participant['Event'], SENDER_EMAIL), subtype='html')
        
        certificate_path = os.path.join('certificates', f"{participant['Name'].lower().replace(' ', '_')}_certificate.png")
        if not os.path.exists(certificate_path):
            print(f"ERROR: Certificate not found for {participant['Name']}. Looked for: {certificate_path}")
            return False # Indicate failure
        
        with open(certificate_path, 'rb') as f:
            msg.add_attachment(f.read(), maintype='image', subtype='png', filename=os.path.basename(certificate_path))
        
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        
        return True # Indicate success
        
    except Exception as e:
        print(f"FAILED to send email to {participant['Name']}. Error: {e}")
        return False # Indicate failure

# --- Main Program ---
if __name__ == "__main__":
    if not os.path.exists('participants.csv'):
        print("FATAL ERROR: 'participants.csv' was not found.")
        exit()
    if not os.path.exists('certificates'):
        print("FATAL ERROR: 'certificates' folder was not found.")
        exit()

    with open('participants.csv', 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        # Clean up header names just in case
        reader.fieldnames = [name.strip() for name in reader.fieldnames]
        participants = list(reader)
    
    print(f"Found {len(participants)} participants. Starting the email sending process...")
    
    results_data = [] # This list will store the results

    for i, participant in enumerate(participants):
        print("-" * 50)
        print(f"Processing participant {i+1}/{len(participants)}: {participant.get('Name')}")

        email = participant.get('Email', '').strip()
        status = ''

        # The main logic: only act if an email address is present
        if email:
            if send_certificate_email(participant):
                status = 'Sent'
                print(f"✅ Successfully sent email to {participant.get('Name')}")
            else:
                status = 'Failed' # The function already printed the reason
        else:
            status = 'Skipped - No Email'
            print("Skipping: No email address found.")

        # Add the status to the participant's data
        participant['Status'] = status
        results_data.append(participant)

        # A short, random delay between emails is good practice
        time.sleep(random.randint(2, 5))

    # --- Create the Final Report ---
    if results_data:
        # Get the headers from the first participant record and add 'Status'
        fieldnames = list(results_data[0].keys())
        
        with open('sending_report.csv', 'w', newline='', encoding='utf-8') as report_file:
            writer = csv.DictWriter(report_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results_data)
        
        print("-" * 50)
        print(f"✅ Process complete. A detailed report has been saved to 'sending_report.csv'")
    else:
        print("No participants were found to process.")