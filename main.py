from bs4 import BeautifulSoup
import csv
import requests
import os

def load_abbreviations(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [ (row["Team"], row["Abbreviation"]) for row in reader ]

def parse_row(row):
    return { result.attrs['data-stat']: result.string for result in row.find_all('td') }

def parse_page(abbreviation):
    url = f'https://www.pro-football-reference.com/teams/{abbreviation}/career-receiving.htm'
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    rows = ( item.parent for item in soup.find_all(lambda tag: tag.has_attr('csk')) )
    return map(parse_row, rows)


if __name__ == "__main__":
    aggregate_filename = "results.csv"
    team_filename = "player.csv"
    abbreviations_filename = "abbreviations.csv"
    abbreviations = load_abbreviations(abbreviations_filename)

    fieldnames = [ k for k in next(parse_page(abbreviations[0][1])) ]

    if not os.path.exists("data"):
        os.mkdir("data")

    with open(f'data/{aggregate_filename}', 'w+', newline='') as aggregate_writer:
        agg_writer = csv.DictWriter(aggregate_writer, fieldnames=fieldnames)
        agg_writer.writeheader()

        for (team, abbr) in abbreviations:
            if not os.path.exists(f'data/{team}'):
                os.mkdir(f'data/{team}')

            results = [ x for x in parse_page(abbr) ]

            with open(f"data/{team}/player.csv", 'w+', newline='') as csvwriter:
                writer = csv.DictWriter(csvwriter, fieldnames=fieldnames)
                writer.writeheader()

                writer.writerows(results)
                agg_writer.writerows(results)
    
    print("Program complete...")

