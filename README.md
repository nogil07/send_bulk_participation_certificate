# Bulk Certificate Emailer

This project is a Python script that automates the process of sending personalized certificates to a list of participants via email.

## Features

- **Bulk Emailing:** Sends emails to a large number of recipients based on a CSV file.
- **Personalization:** Each email is personalized with the participant's name and the event name.
- **Certificate Attachment:** Automatically attaches the correct certificate for each participant.
- **Reporting:** Generates a `sending_report.csv` file with the status of each email (Sent, Failed, or Skipped).
- **Error Handling:** Skips participants with no email address and logs failures.
- **Randomized Subjects:** Uses different subject lines to reduce the chance of emails being marked as spam.

## Prerequisites

- Python 3.x

The script uses standard Python libraries, so no special `pip` installations are required.

## How to Use

1.  **Configure the Script:**
    Open `send_certificate.py` and edit the configuration section at the top:
    ```python
    SENDER_NAME = "Your Name or Organization"
    SENDER_EMAIL = "your_email@gmail.com"
    SENDER_PASSWORD = "your_google_app_password" # Use a 16-character Google App Password
    ```
    **Important:** For security reasons, it is highly recommended to use a Google App Password instead of your regular Gmail password.

2.  **Prepare the Participants List:**
    Create a `participants.csv` file in the same directory. The CSV file must have the following headers: `Name`, `Email`, and `Event`.

    Example `participants.csv`:
    ```csv
    Name,Email,Event
    Jofin Joji,jofinjoji@example.com,Python Workshop
    Meera Paul,meerapaul@example.com,Data Science Webinar
    ```

3.  **Add Certificates:**
    Place the certificate files in the `certificates` directory. The certificate for each participant must be named in the format: `participant_name_certificate.png`. For example, for a participant named "Jofin Joji", the certificate should be named `jofin_joji_certificate.png`.

4.  **Run the Script:**
    Execute the script from your terminal:
    ```bash
    python send_certificate.py
    ```

## File Structure

```
.
├── certificates/
│   ├── Nogil_Binu_certificate.png  
├── participants.csv
├── send_certificate.py
└── sending_report.csv (Generated after running the script)
```

- **`send_certificate.py`**: The main script that sends the emails.
- **`participants.csv`**: The list of participants to whom certificates will be sent.
- **`certificates/`**: The directory where the certificate image files are stored.
- **`sending_report.csv`**: A report file that is generated after the script runs, containing the status of each email.

