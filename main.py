from bs4 import BeautifulSoup
import csv
import requests

def load_abbreviations(filename):
    pass

def parse_page(abbreviation):
    url = f'https://www.pro-football-reference.com/teams/{abbreviation}/career-receiving.htm'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    return [ x.string for x in soup.find_all(attrs={"data-stat": "player"}) ]


if __name__ == "__main__":
    abbreviations_filename = "abbreviations.csv"
    result_filename = "results.csv"
    results = parse_page('chi')
    for result in results:
        print(result)