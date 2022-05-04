import requests
from bs4 import BeautifulSoup
import re


def finn_code():                                            # Finn-code, found in the real estate ad
    finn_code.var = input('Skriv inn Finn-Kode her: ')


def get_url():                                              # Using requests to get URL, scraping with BeautifulSoup
    url = f"https://www.finn.no/realestate/homes/ad.html?finnkode={finn_code.var}"
    r = requests.get(url)
    if not r.ok:                                            # Validating Finn-code, if invalid it will print a message and start over
        print("\nUgyldig Finn-Kode.\n")
        finn_code()
        get_url()
    get_url.var = BeautifulSoup(r.content, 'html.parser')


def rent():                                                 # Function for containing variable; expected rental income
    rent.var = input('Forventet leieinntekt for objektet (kr): ')


def interest():                                             # Function for containing variable; expected annual interest rate
    interest.var = input("Forventet rente på lån (%): ")


def oth_costs():                                            # Function for containing variable; other known monthly costs
    oth_costs.var = input('Andre mnd. utgifter, skriv 0 hvis det ikke er noen (kr): ')


def total_price():                                          # Scraping website for total price and converting the string to an integer
    try:
        totalpris_raw = get_url.var.find('dt', text="Totalpris").find_next_sibling('dd').text.strip()
        totalpris_split = [int(x) for x in totalpris_raw.split() if x.isdigit()]
        totalpris_str = [str(x) for x in totalpris_split]
        totalpris_str = [str(x).zfill(3) for x in totalpris_str]
        totalpris_join = ",".join(totalpris_str)
        total_price.var = int(re.sub(",", "", totalpris_join))
    except AttributeError:                                  # If data is not found, the program will ask you to type it in manually
        total_price.var = input('Totalpris ikke funnet, oppgi verdi manuelt (kr): ')


def shared_costs():                                         # Scraping website for monthly shared costs, converting str to int
    try:
        felleskost_raw = get_url.var.find('dt', text="Felleskost/mnd.").find_next_sibling('dd').text.strip()
        felleskost_split = [int(x) for x in felleskost_raw.split() if x.isdigit()]
        felleskost_str = [str(x) for x in felleskost_split]
        felleskost_str = [str(x).zfill(3) for x in felleskost_str]
        felleskost_join = ",".join(felleskost_str)
        shared_costs.var = int(re.sub(",", "", felleskost_join))
    except AttributeError:                                  # If data is not found, the program will ask you to type it in manually
        shared_costs.var = input('Felleskostnader ikke funnet, oppgi verdi manuelt (kr): ')


def municipal_taxes():                                      # Scraping website for annual municipal taxes, converting str to int
    try:
        komm_avg_raw = get_url.var.find('dt', text="Kommunale avg.").find_next_sibling('dd').text.strip()
        komm_avg_split = [int(x) for x in komm_avg_raw.split() if x.isdigit()]
        komm_avg_str = [str(x) for x in komm_avg_split]
        komm_avg_str = [str(x).zfill(3) for x in komm_avg_str]
        komm_avg_join = ",".join(komm_avg_str)
        municipal_taxes.var = int(re.sub(",", "", komm_avg_join))
    except AttributeError:                                  # If data is not found, the program will ask you to type it in manually
        municipal_taxes.var = input('Kommunale avgifter ikke funnet, oppgi verdi manuelt (kr): ')


def fees():                                                 # Scraping website for purchase taxes when buying real estate, converting str to int
    try:
        fees_raw = get_url.var.find('dt', text="Omkostninger").find_next_sibling('dd').text.strip()
        fees_split = [int(x) for x in fees_raw.split() if x.isdigit()]
        fees_str = [str(x) for x in fees_split]
        fees_str = [str(x).zfill(3) for x in fees_str]
        fees_join = ",".join(fees_str)
        fees.var = int(re.sub(",", "", fees_join))
    except AttributeError:                                  # If data is not found, the program will ask you to type it in manually
        fees.var = input('Omkostninger ikke funnet, oppgi verdi manuelt (kr): ')


def calculation():                                          # Using collected data to calculate annual ROI and monthly cash flow
    s = shared_costs.var
    o = oth_costs.var
    try:
        ens = 100                                           # Ensurance
        maint = 500                                         # Maintenance
        vac = int(rent.var) / 12                            # Vacancy, excpectation is 1 month per year
        loan = int(total_price.var) * 0.85                  # Loan with 15% equity
        apr = int(loan) * int(interest.var) / 100           # Annual Percentage Rate (interest)
        mpr = int(apr) / 12                                 # Monthly Percentage Rate (interest)
        mun_tax_monthly = int(municipal_taxes.var) / 12
        tot_costs = int(ens) + int(maint) + int(vac) + int(mpr) + int(mun_tax_monthly) + int(s) + int(o)
        income_pre_tax = int(rent.var) - int(tot_costs)
        income_post_tax = int(income_pre_tax) * 0.78
        equity = int(total_price.var) + int(fees.var) - int(loan)
        avkastning = ((int(income_post_tax) * 12) / int(equity)) * 100

        print(f'\nForventet årlig avkastning er ca. {round(avkastning, 2)}%.\n'
              f'Du vil sitte igjen med ca. {round(income_post_tax)}kr pr mnd.\n')
    except ValueError:                                      # If an input is not a number, it will show a message (and start over; while True)
        print(f"\n{ValueError}: Et av dine inputs er ikke et tall, prøv igjen med bare tall.\n")


def main():                                                 # Main function, runs all functions in the right order to transfer required variables
    finn_code()
    get_url()
    rent()
    interest()
    oth_costs()
    total_price()
    shared_costs()
    municipal_taxes()
    fees()
    calculation()


if __name__ == "__main__":
    while True:
        main()


# Further development, possibility to format excel-sheets with the required info:
# excel = input('Vil du ha opplysningene inn i et excel-ark? (Ja/Nei): ')
# if excel.lower() == "ja" or "y" or "j":
#     pass
# else:
#     main()
