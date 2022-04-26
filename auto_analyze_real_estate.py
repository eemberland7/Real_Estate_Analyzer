# PLEASE HAVE A BACKUP BEFORE CHANGING THE ORIGINAL REPOSITORY!
# READ COMMENT FOR EVERY CHANGE CAREFULLY!

import requests
from bs4 import BeautifulSoup
import re

# Use class to contain functions. I am assuming Line 10 ---> 20 are independent
# from each other. And does not clash with other calculations in the program.
# If other calculations depend on statements & variables from Line 10 ---> 20
# please ignore the class Finn_Kode.
class Finn_Kode:
    
    def find_code():
        # Inputs for å finne annonse og avgjøre forventet inntekt
        finn_kode = input('Skriv inn Finn-Kode her: ') # Most functions should start with small caps.
        url = f"https://www.finn.no/realestate/homes/ad.html?finnkode={Finn_Kode}"
        r = requests.get(url)
        if != r.ok: # != and not or is not means the same. Usually seen it does this way.
            print("Ugyldig Finn-kode.")
            quit()
        soup = BeautifulSoup(r.content, 'html.parser')
        Leieinntekt = input('Forventet leieinntekt for objektet (kr): ')
        Forventet_Rente = input("Skriv inn forventet rente på lån (%): ")
        Andre_Utgifter = input('Andre mnd. utgifter i kr, skriv 0 hvis det ikke er noen: ')
        

while True:
    
    Finn_Kode.find_code() # The Finn Code, categorized in a class and placed in a function.

    # Avansert prosess for å fjerne tekst og konvertere totalpris til et tall:
    try:
        Totalpris_Raw = soup.find('dt', text= "Totalpris").find_next_sibling('dd').text.strip()
        Totalpris_Split = [int(s) for s in Totalpris_Raw.split() if s.isdigit()]
        Totalpris_Str = [str(int) for int in Totalpris_Split]
        Totalpris_Join = ",".join(Totalpris_Str)
        Totalpris = int(re.sub(",", "", Totalpris_Join))
    except AttributeError:
        Totalpris = input('Totalpris ikke funnet, oppgi verdi manuelt (kr): ')
        
    # Avansert prosess for å fjerne tekst og konvertere felleskostnader til et tall:
    try:
        Felleskost_Raw = soup.find('dt', text="Felleskost/mnd.").find_next_sibling('dd').text.strip()
        Felleskost_Split = [int(s) for s in Felleskost_Raw.split() if s.isdigit()]
        Felleskost_Str = [str(int) for int in Felleskost_Split]
        Felleskost_Join = ",".join(Felleskost_Str)
        Felleskost = int(re.sub(",", "", Felleskost_Join))
    except AttributeError:
        Felleskost = input('Felleskostnader ikke funnet, oppgi verdi manuelt (kr): ')

    # Avansert prosess for å fjerne tekst og konvertere kommunale avgifter til et tall:
    try:
        Komm_Avg_Raw = soup.find('dt', text="Kommunale avg.").find_next_sibling('dd').text.strip()
        Komm_Avg_Split = [int(s) for s in Komm_Avg_Raw.split() if s.isdigit()]
        Komm_Avg_Str = [str(int) for int in Komm_Avg_Split]
        Komm_Avg_Join = ",".join(Komm_Avg_Str)
        Komm_Avg = int(re.sub(",", "", Komm_Avg_Join))
    except AttributeError:
        Komm_Avg = input('Kommunale avgifter ikke funnet, oppgi verdi manuelt (kr): ')

    # Utregningen
    try:
        Forsikringer = 100
        Est_Vedlikehold = 500
        Ledighet_1Mnd = int(Leieinntekt)/12
        Loan = int(Totalpris)*0.825
        Anno_Renter = int(Loan)*int(Forventet_Rente)/100
        Mnd_Renter = int(Anno_Renter)/12
        Mnd_Komm_Avg = int(Komm_Avg)/12
        Tot_Utgifter = int(Forsikringer)+int(Est_Vedlikehold)+int(Ledighet_1Mnd)+int(Mnd_Renter)+int(Mnd_Komm_Avg)+int(Felleskost)+int(Andre_Utgifter)
        Inntekt_Pre_Tax = int(Leieinntekt)-int(Tot_Utgifter)
        Inntekt_Post_Tax = int(Inntekt_Pre_Tax)*0.78
        Egenkap = int(Totalpris)-int(Loan)
        Avkastning = round(((int(Inntekt_Post_Tax)*12)/int(Egenkap))*100, 2)

        # Kode for å skrive ut forventet avkastning:
        print(f'\nForventet årlig avkastning er ca. {Avkastning}%.\n')
    except ValueError:
        print(f"{ValueError}: Et av dine inputs er ikke et tall, prøv igjen med bare tall.\n")


# Videreutvikling, mulighet for å formattere et excel-ark med detaljene:
# input('Vil du ha opplysningene inn i et excel-ark? (Ja/Nei): ')
