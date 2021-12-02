from bs4 import BeautifulSoup
import csv
from pandas.core.frame import DataFrame
import requests
import os

import pandas as pd
import matplotlib.pyplot as plt

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
    rows = ( item.parent for item in soup.find_all(attrs={'scope': 'row'}) )
    return map(parse_row, rows)

def scrape_pfr_data(aggregate_filename):
    abbreviations_filename = "abbreviations.csv"
    abbreviations = load_abbreviations(abbreviations_filename)
    fieldnames = [ k for k in next(parse_page(abbreviations[0][1])) ]
    aggregate_fieldnames = fieldnames + [ 'team' ]

    if not os.path.exists("data"):
        os.mkdir("data")
    
    with open(f'data/{aggregate_filename}', 'w+', newline='') as aggregate_writer:
        agg_writer = csv.DictWriter(aggregate_writer, fieldnames=aggregate_fieldnames)
        agg_writer.writeheader()

        for (team, abbr) in abbreviations:
            if not os.path.exists(f'data/{team}'):
                os.mkdir(f'data/{team}')

            results = [ x for x in parse_page(abbr) ]
            agg_results = [ player.copy() for player in results ]
            for player in agg_results:
                player['team'] = team

            with open(f"data/{team}/player.csv", 'w+', newline='') as csvwriter:
                writer = csv.DictWriter(csvwriter, fieldnames=fieldnames)
                writer.writeheader()

                writer.writerows(results)
                agg_writer.writerows(agg_results)

def set_dark_background():
    plt.style.use('dark_background')

def set_plt_globals(ax, limit=500):
    plt.axes(ax)
    plt.title(f'top {limit} career receiving yards for a team in nfl history')
    plt.grid(True, alpha=0.25)
    plt.xlabel("final year with team")
    plt.ylabel(range(4000, 20000, 1000))

    ax.legend()

    plt.figtext(0.01, 0.02, "h/t Pro-Football-Reference")

def get_top_players(df, limit=500):
    return df.sort_values('rec_yds', ascending=False).head(limit)


def generate_bears_graph(df : DataFrame, first_color='yellow', second_color='red'):

    set_dark_background()

    df = get_top_players(df)
    bears_top_rec_df = df.loc[df['team'] == 'Bears'].sort_values('rec_yds', ascending=False).head(1)
    bears_top_postmerger_rec_df = df.loc[(df['year_max'] >= 1970) & (df['team'] == 'Bears')].sort_values('rec_yds', ascending=False).head(1)

    ax1 = bears_top_rec_df.plot(x="year_max", y="rec_yds", s=40, kind="scatter", zorder=2, c=first_color, label="Bears career leader")
    bears_top_postmerger_rec_df.plot(x="year_max", y="rec_yds", ax=ax1, s=40, kind="scatter", zorder=2, c=second_color, label="Bears career leader post-merger (1970)")
    df.plot(x="year_max", y="rec_yds", ax=ax1, kind="scatter", s=4, c='white', zorder=1, label="_")

    set_plt_globals(ax1)

    plt.show()

def generate_top_receivers_graph(df: DataFrame, first_color='yellow', second_color='red'):
    set_dark_background()

    df = get_top_players(df)
    ax = df.iloc[[0]].plot(x="year_max", y="rec_yds", s=40, kind="scatter", zorder=2, c=first_color, label="Jerry Rice")
    df.iloc[[1]].plot(x="year_max", y="rec_yds", ax=ax, s=40, kind="scatter", zorder=2, c=second_color, label="Larry Fitzgerald")
    df.plot(x='year_max', y='rec_yds', ax=ax, kind="scatter", s=4, c='white', zorder=1, label="_")

    set_plt_globals(ax)
    plt.show()

def generate_hutson_graph(df: DataFrame, color='yellow'):
    set_dark_background()

    df = get_top_players(df)
    ax = df.loc[df['year_max'] < 1950].iloc[[0]].plot(x='year_max', y='rec_yds', s=40, kind='scatter', zorder=2, c=color, label='Don Hutson')
    df.plot(x='year_max', y='rec_yds', ax=ax, kind='scatter', s=4, c='white', zorder=1, label="_")

    set_plt_globals(ax)
    plt.show()

if __name__ == "__main__":
    aggregate_filename = "results.csv"

    if not os.path.exists(f'data/{aggregate_filename}'):
        scrape_pfr_data(aggregate_filename)

    df = pd.read_csv(f'data/{aggregate_filename}')

    generate_bears_graph(df)
    # generate_top_receivers_graph(df)
    # generate_hutson_graph(df)
    
    print("Program complete...")

