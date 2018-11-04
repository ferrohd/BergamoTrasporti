import requests
from bs4 import BeautifulSoup
import json

def main():

    comune1 = 'A216'
    comune2 = 'A214'
    trip = 'RITORNO'

    #login(comune1, comune2)
    #search(comune1, comune2, trip)
    response = search(comune1, comune2, trip)
    parse_response(response)

def login(comune1, comune2):
    url = 'http://ro.autobus.it/ro/Login.asp'
    payload = {'ComuneA': comune1,
                'ComuneB': comune2,
                'Submit': 'Cerca',
                'user': 'Sab'}
    r = requests.get(url=url, params=payload)
    print(r.status_code)


def search(comune1, comune2, trip):
    url = 'http://ro.autobus.it/ro/asp/RicercaOrari.asp'
    payload = {'comuneArrINI': comune1,
                'comunePartINI': comune2,
                'RicercaVeloce': '1',
                'submit': 'cerca',
                'User': 'Sab'}

    data = {'MinOraPart': '07:30',
            'MaxOraPart': '23:59',
            'comunePartINI': 'A794|Bergamo',
            'comuneArrINI': 'C759|Cividate+al+Ppiano',
            'TIPOVIS': 'FERMATE',
            'CAMBIOCOMUNE': '0',
            'DesLocPart': 'Bergamo (terminal sab e autolinee)',
            'DesLocDest': 'Cividate+al+Piano+-+via+per+romano',
            'direzione': trip,
            'gg': '',
            'meseanno': '',
            'controlloEsisteFermata': '0',
            'PARTENZA': '',
            'LocPart': '111111|Bergamo (terminal sab e autolinee)|0',
            'ARRIVO': '',
            'LocDest': 'C51089|Cividate+al+Piano+-+via+per+romano|0',
            'dataViaggio': '6/11/2018',
            'OREDalSel': '23:59',
            'OREAlSel': '16:00',
            'fascia': 'libera',
            'ordine': 'NumCambi, OraPart',
            'MaxNodi': '1',
            'MinimoV': '0',
            'CERCA_' + trip: 'corse di ' + trip}

    r = requests.post(url=url, params=payload, data=data)
    print(r.status_code)
    return r.text


def parse_response(text):
    soup = BeautifulSoup(text, 'lxml')
    table = soup.find_all('table', class_='TABELLASOLUZIONICORSE')[1]
    tab_data = [[celldata.text for celldata in rowdata.find_all('td')] for rowdata in table.find_all("tr")]

    stripped_data = []
    for array in tab_data:
        stripped_data.append(([item.replace('\u00a0', ' ') for item in array]))
    with open('result.json', 'w') as f:
        json.dump(stripped_data, f)


if __name__ == "__main__":
    main()
