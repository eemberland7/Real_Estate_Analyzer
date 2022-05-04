import requests
from bs4 import BeautifulSoup
import re


def finn_code():
    finn_code.var = input('Skriv inn Finn-Kode her: ')


def get_url():
    url = f"https://www.finn.no/realestate/homes/ad.html?finnkode={finn_code.var}"
    r = requests.get(url)
    if not r.ok:
        print("\nUgyldig Finn-Kode.\n")
        finn_code()
        get_url()
    get_url.var = BeautifulSoup(r.content, 'html.parser')


def rent():
    rent.var = input('Forventet leieinntekt for objektet (kr): ')


def interest():
    interest.var = input("Forventet rente på lån (%): ")


def oth_costs():
    oth_costs.var = input('Andre mnd. utgifter, skriv 0 hvis det ikke er noen (kr): ')


def total_price():
    try:
        totalpris_raw = get_url.var.find('dt', text="Totalpris").find_next_sibling('dd').text.strip()
        totalpris_split = [int(x) for x in totalpris_raw.split() if x.isdigit()]
        totalpris_str = [str(x) for x in totalpris_split]
        totalpris_str = [str(x).zfill(3) for x in totalpris_str]
        totalpris_join = ",".join(totalpris_str)
        total_price.var = int(re.sub(",", "", totalpris_join))
    except AttributeError:
        total_price.var = input('Totalpris ikke funnet, oppgi verdi manuelt (kr): ')


def shared_costs():
    try:
        felleskost_raw = get_url.var.find('dt', text="Felleskost/mnd.").find_next_sibling('dd').text.strip()
        felleskost_split = [int(x) for x in felleskost_raw.split() if x.isdigit()]
        felleskost_str = [str(x) for x in felleskost_split]
        felleskost_str = [str(x).zfill(3) for x in felleskost_str]
        felleskost_join = ",".join(felleskost_str)
        shared_costs.var = int(re.sub(",", "", felleskost_join))
    except AttributeError:
        shared_costs.var = input('Felleskostnader ikke funnet, oppgi verdi manuelt (kr): ')


def municipal_taxes():
    try:
        komm_avg_raw = get_url.var.find('dt', text="Kommunale avg.").find_next_sibling('dd').text.strip()
        komm_avg_split = [int(x) for x in komm_avg_raw.split() if x.isdigit()]
        komm_avg_str = [str(x) for x in komm_avg_split]
        komm_avg_str = [str(x).zfill(3) for x in komm_avg_str]
        komm_avg_join = ",".join(komm_avg_str)
        municipal_taxes.var = int(re.sub(",", "", komm_avg_join))
    except AttributeError:
        municipal_taxes.var = input('Kommunale avgifter ikke funnet, oppgi verdi manuelt (kr): ')


def fees():
    try:
        fees_raw = get_url.var.find('dt', text="Omkostninger").find_next_sibling('dd').text.strip()
        fees_split = [int(x) for x in fees_raw.split() if x.isdigit()]
        fees_str = [str(x) for x in fees_split]
        fees_str = [str(x).zfill(3) for x in fees_str]
        fees_join = ",".join(fees_str)
        fees.var = int(re.sub(",", "", fees_join))
    except AttributeError:
        fees.var = input('Omkostninger ikke funnet, oppgi verdi manuelt (kr): ')


def calculation():
    s = shared_costs.var
    o = oth_costs.var
    try:
        ens = 100                                           # Ensurance
        maint = 500                                         # Maintenance
        vac = int(rent.var) / 12                            # Vacancy
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
    except ValueError:
        print(f"\n{ValueError}: Et av dine inputs er ikke et tall, prøv igjen med bare tall.\n")


def main():
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
