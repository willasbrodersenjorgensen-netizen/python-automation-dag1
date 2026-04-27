    
import csv
import json
import os

# 1. Definer stien (Vi bruger den simple sti, da json_data ligger i din hovedmappe)
file_path = r'C:\Users\mormo\Desktop\Maschine Learning\automation\json_data\users.json'

# 2. Indlæs data
users = []
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        users = json.load(f)
    print(f"Succes! Indlæste {len(users)} brugere fra filen.")
except Exception as e:
    print(f"FEJL: Kunne ikke læse filen. Fejlbesked: {e}")

# 3. Find leads
gemte_leads = []

for user in users:
    # Vi henter email
    email = user.get('email', '').strip().lower()
    navn = user.get('name', 'Ukendt')
    
    print(f"Tjekker: {navn} ({email})")
    
    if email.endswith(".biz"):
        lead = {
            "Navn": navn,
            "Email": user.get('email'),
            "Firma": user.get('company', {}).get('name', 'Intet firma')
        }
        gemte_leads.append(lead)
        print(f"FUNDET: {navn}")

# 4. Gem til CSV
if gemte_leads:
    output_fil = 'mine_leads.csv'
    with open(output_fil, 'w', newline='', encoding='utf-8') as f:
        felt_navne = ["Navn", "Email", "Firma"]
        writer = csv.DictWriter(f, fieldnames=felt_navne)
        
        writer.writeheader()
        writer.writerows(gemte_leads)
    
    print(f"\n Sådan {len(gemte_leads)} leads er gemt i '{output_fil}'")
else:
    print("\n Ingen leads fundet med .biz mail. Tjek din users.json!")