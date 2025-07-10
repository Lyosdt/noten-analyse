from bs4 import BeautifulSoup
import requests

url = "https://cis.nordakademie.de/mein-profil/mein-postfach/leistungsuebersicht"

cookies = {
    'fe_typo_user_cae070b': '6f8f44dfe13c5721edce5829dcb5c3f4.8ed18122f2bd9b3a9c9378c3c073885ed1396ad87593b365645dea7b3b56a312',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
    'Referer': 'https://cis.nordakademie.de/',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=0, i',
}

response = requests.get(url, cookies=cookies, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")

    modules = []

    # Table finden
    table = soup.find('table')

    if table:
        # Alle Zeilen in der Tabelle finden
        rows = table.tbody.find_all('tr')

        for row in rows:
            module = {'ModulID':'', 'Modulname':'','ECTS':0,'Professor':''}
            

            # Überprüfen, ob die Zeile das gewünschte 'data-label' enthält
            data_cell = row.find('td', {'data-label': 'Modulnummer:'})
            if data_cell:
                module['ModulID'] =  data_cell.text.strip() # Nur den Text innerhalb der Zelle drucken

            # Überprüfen, ob die Zeile das gewünschte 'data-label' enthält
            data_cell = row.find('td', {'data-label': 'Bezeichnung:'})
            if data_cell:
                module['Modulname'] =  data_cell.text.strip() # Nur den Text innerhalb der Zelle drucken

            # Überprüfen, ob die Zeile das gewünschte 'data-label' enthält
            data_cell = row.find('td', {'data-label': 'Credits:'})
            if data_cell:
                module['ECTS'] =  data_cell.text.strip() # Nur den Text innerhalb der Zelle drucken
            
            modules.append(module)

    for m in modules:
        print(m)

else:
    print("Fehler beim Abrufen der Seite:", response.status_code)
