from playwright.sync_api import sync_playwright, Playwright
import re

USERNAME = "20063"
PASSWORD = "m.Kp58zX3/qS"

modules = []
pruefungen = []

def run(playwright: Playwright):
    chromium = playwright.chromium
    browser = chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://cis.nordakademie.de/mein-profil/mein-postfach/leistungsuebersicht")
    page.get_by_placeholder('Benutzername:').fill(USERNAME)
    page.get_by_placeholder('Passwort:').fill(PASSWORD)
    page.locator("input[value=Anmelden]").click()
    page.goto("https://cis.nordakademie.de/mein-profil/mein-postfach/leistungsuebersicht")
    table = page.locator("div#curricular")

    for row in table.locator("tr").all():
        if row.locator("td[data-label='Modulnummer:']").count() > 0:
            module = {'ModulID':'', 'Modulname':'','ECTS':0,'Professor':''}
            pruefung = {'ModulID':'','Pruefungsdatum':'','Noteneingabedatum':'','Note':'','Bestanden':'', 'AnzahlKlausuren':'', 'Anzahl1.0': '',
                        'Anzahl1.3': '',
                        'Anzahl1.7': '',
                        'Anzahl2.0': '',
                        'Anzahl2.3': '',
                        'Anzahl2.7': '',
                        'Anzahl3.0': '',
                        'Anzahl3.3': '',
                        'Anzahl3.7': '',
                        'Anzahl4.0': '',
                        'Anzahl5.0': ''}

            module["ModulID"] = row.locator("td[data-label='Modulnummer:']").inner_html()
            module["Modulname"] = row.locator("td[data-label='Bezeichnung:']").inner_html()
            module["ECTS"] = row.locator("td[data-label='Credits:']").inner_html()

            pruefung["ModulID"] = row.locator("td[data-label='Modulnummer:']").inner_html()
            note = row.locator("td[data-label='Note:']").inner_html().strip()
            pruefung["Note"] = note if note != '' and note !='bestanden' else ''
            if note != '':
                if note == "bestanden":
                    pruefung["Bestanden"] = True
                else:
                    pruefung["Bestanden"] = True if float(note.replace(',','.')) < 5.0 else False
            pruefung["Pruefungsdatum"] = row.locator("td[data-label='Prüfungsdatum:']").inner_html()
            pruefung["Noteneingabedatum"] = row.locator("td[data-label='Noteneingabedatum:']").inner_html()

            if row.get_by_title("Verteilung").count() > 0:
                noten = []


                row.get_by_title("Verteilung").click()
                page.wait_for_load_state('load')

                verteilung = page.locator("tbody").first

                for col in verteilung.locator("td").all():
                    if col.inner_html() == "Anzahl":
                        continue
                    noten.append(int(col.inner_html()))

                pruefung['Anzahl1.0'] = noten[0]
                pruefung['Anzahl1.3'] = noten[1]
                pruefung['Anzahl1.7'] = noten[2]
                pruefung['Anzahl2.0'] = noten[3]
                pruefung['Anzahl2.3'] = noten[4]
                pruefung['Anzahl2.7'] = noten[5]
                pruefung['Anzahl3.0'] = noten[6]
                pruefung['Anzahl3.3'] = noten[7]
                pruefung['Anzahl3.7'] = noten[8]
                pruefung['Anzahl4.0'] = noten[9]
                pruefung['Anzahl5.0'] = noten[10]

                pruefung['AnzahlKlausuren'] = sum(noten)


                page.go_back()
            pruefungen.append(pruefung)
            modules.append(module)

            

    browser.close()
    

with sync_playwright() as playwright:
    run(playwright)
    
for module in modules:
        print(module)

for pruefung in pruefungen:
     print(pruefung)