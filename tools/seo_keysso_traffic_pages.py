#!/usr/bin/env python3

import pandas as pd
import argparse


# Ctr по данным исследования OverLead https://overlead.me/blog/ctr-na-vydache-yandeksa-ot-2019-goda/
def get_ctr15(pos):
    return {
        pos <= 0: 0.0,
        pos == 1: 27.42,
        pos == 2: 17.38,
        pos == 3: 10.66,
        pos == 4: 6.69,
        pos == 5: 4.97,
        pos == 6: 4.19,
        pos == 7: 4.39,
        pos == 8: 4.23,
        pos == 9: 4.41,
        pos == 10: 2.83,
        pos == 11: 1.68,
        pos == 12: 1.93,
        pos == 13: 2.52,
        pos == 14: 3.45,
        pos == 15: 3.75,
        pos > 15: 0.0
    }[True]


def get_ctr10(pos):
    return {
        pos <= 0: 0.0,
        pos == 1: 31.19,
        pos == 2: 11.20,
        pos == 3: 4.69,
        pos == 4: 3.23,
        pos == 5: 3.05,
        pos == 6: 3.86,
        pos == 7: 3.93,
        pos == 8: 2.61,
        pos == 9: 1.85,
        pos == 10: 1.32,
        pos > 10: 0.0
    }[True]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f', action='store', dest='keysso_csv', help='Keys.so CSV file')
    parser.add_argument('-o', action='store', dest='output_csv', help='Output CSV file')

    args = parser.parse_args()

    organic_keys_df = pd.read_csv(args.keysso_csv, sep=';', usecols=[0, 1, 2, 3, 4],
                                  names=['Query', 'Page', 'Position', '[Wordstat]', '[!Wordstat]'], header=0)

    organic_keys_df['Traffic10'] = organic_keys_df['[!Wordstat]'] * organic_keys_df['Position'].apply(
        lambda x: get_ctr10(x) / 100)
    organic_keys_df['Traffic15'] = organic_keys_df['[!Wordstat]'] * organic_keys_df['Position'].apply(
        lambda x: get_ctr15(x) / 100)

    organic_keys_df['QueryCount'] = 1
    organic_keys_df = organic_keys_df.drop('Position', 1)

    organic_keys_df.groupby('Page').sum().sort_values('Traffic10', ascending=False).to_csv(
        args.output_csv, sep=';', decimal=',', encoding='utf-8')
