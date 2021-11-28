from bs4 import BeautifulSoup
import csv
import requests

def load_abbreviations(filename):
    pass

def parse_row(row):
    return { result.attrs['data-stat']: result.string for result in row.find_all('td') }

def parse_page(abbreviation):
    url = f'https://www.pro-football-reference.com/teams/{abbreviation}/career-receiving.htm'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    rows = ( item.parent for item in soup.find_all(lambda tag: tag.has_attr('csk')) )
    return map(parse_row, rows)


if __name__ == "__main__":
    abbreviations_filename = "abbreviations.csv"
    result_filename = "results.csv"
    results = parse_page('chi')
    print(sorted(results, reverse=True, key=lambda x: int(x['rec_yds']))[0])