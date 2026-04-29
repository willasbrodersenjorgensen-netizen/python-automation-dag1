    


import json
import csv
import smtplib
import gspread
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from oauth2client.service_account import ServiceAccountCredentials

# --- KONFIGURATION (Tjek disse!) ---
AFSENDER_MAIL = "willasbrodersenjorgensen@gmail.com" 
APP_KODE = "ppad ctiw znta tine" 
CREDS_FILE = r'C:\Users\mormo\Desktop\Maschine Learning\automation\json_data\creds.json'
JSON_DATA_STIG = r'C:\Users\mormo\Desktop\Maschine Learning\automation\json_data\users.json'
SHEET_NAVN = "mine leads"
SHEET_ID = '1NAEvrMHo8Mp3KofyYjdz-TjfO2mjBgsVW77jYQNyOWo'



SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def log_alle_leads_til_sheets(alle_leads):
    """Logger alle leads til Google Sheets."""
    if not alle_leads:
        return

    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID).sheet1
        
        sheet.append_rows(alle_leads, value_input_option='USER_ENTERED')
        print(f" Succes! Logget {len(alle_leads)} rækker til Google Sheets.")

    except Exception as e:
        # Håndtering af Google-hikke (503 og 200)
        error_msg = str(e)
        if "503" in error_msg:
            print(" Google har travlt (503). Prøv igen om et øjeblik.")
        elif "200" in error_msg:
            print(" Logget i Sheets (bekræftet via Response 200).")
        else:
            print(f" Sheets fejl: {e}")

def send_test_mail(navn, firma):
    """Sender en automatiseret mail via Gmail SMTP."""
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(AFSENDER_MAIL, APP_KODE)

        msg = MIMEMultipart()
        msg['From'] = AFSENDER_MAIL
        msg['To'] = AFSENDER_MAIL 
        msg['Subject'] = f"Samarbejde med {firma}?"

        indhold = f"Hej {navn},\n\nJeg har fulgt med i {firma}. Da I er en .biz-virksomhed, tænkte jeg, at vi skulle tage en snak?\n\nMvh Willas"
        msg.attach(MIMEText(indhold, 'plain'))

        server.send_message(msg)
        server.quit()
        print(f" Mail sendt vedr. {navn}")
    except Exception as e:
        print(f" Mail fejl: {e}")

def main():
    # 1. Indlæser JSON
    try:
        with open(JSON_DATA_STIG, 'r', encoding='utf-8') as f:
            users = json.load(f)
    except Exception as e:
        print(f"FEJL: Kunne ikke læse filen: {e}")
        return

    gemte_leads_dict = []
    sheets_data_liste = []
    
    # 2. Find .biz leads
    for user in users:
        email = user.get('email', '').strip().lower()
        if email.endswith(".biz"):
            navn = user.get('name', 'Ukendt')
            firma = user.get('company', {}).get('name', 'Intet firma')
            
            print(f" FUNDET: {navn} ({firma})")

            gemte_leads_dict.append({"Navn": navn, "Email": email, "Firma": firma})
            sheets_data_liste.append([navn, firma, email, "Lead Fundet"])

            send_test_mail(navn, firma)

    # 3. Log til Sheets
    if sheets_data_liste:
        log_alle_leads_til_sheets(sheets_data_liste)

    # 4. CSV Backup
    if gemte_leads_dict:
        try:
            with open('mine_leads.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["Navn", "Email", "Firma"])
                writer.writeheader()
                writer.writerows(gemte_leads_dict)
            print(" CSV backup oprettet.")
        except:
            pass

    print("\n Program færdig.")

if __name__ == "__main__":
    main()
