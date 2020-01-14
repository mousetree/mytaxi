#!/usr/bin/env python3

from mytaxi.extract import parse_bill
from mytaxi.download import download_mytaxi_files
from datetime import datetime
from environs import Env
import os
import pandas as pd

env = Env()
env.read_env()

base_path = os.path.dirname(os.path.realpath(__file__))
CURRENT_YEAR = datetime.now().year
SEARCH_YEAR = env.str('SEARCH_YEAR', CURRENT_YEAR)
ATTACHMENT_DIR = os.path.join(base_path, '..', 'attachments', SEARCH_YEAR)
OUTPUT_DIR = os.path.join(base_path, '..', 'output')

def setup_directories(dirs=[]):
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)

def pdf_to_df():
    bills = []
    for filename in os.listdir(ATTACHMENT_DIR):
        if filename.endswith(".pdf"):
            filepath = os.path.join(ATTACHMENT_DIR, filename)
            metadata = parse_bill(filepath)
            metadata['filename'] = filename
            bills.append(metadata)
    df = pd.DataFrame.from_records(bills)
    return df

def print_summary(df):
    total_cost = df['price'].sum()
    total_bills = df.shape[0]
    print(df)
    print_banner(f'{total_bills} bills with total cost: €{total_cost:.2f}')

def print_banner(text):
    print('\n'+'-'*len(text))
    print(text)
    print('-'*len(text)+'\n')

def run():
    setup_directories([ATTACHMENT_DIR, OUTPUT_DIR])
    download_mytaxi_files(ATTACHMENT_DIR, SEARCH_YEAR)
    df = pdf_to_df()
    csv_path = os.path.join(OUTPUT_DIR, 'mytaxi.csv')
    df.to_csv(csv_path)
    print_summary(df)
    print(f'A summary of your rides can be found at: {csv_path}')

if __name__== "__main__":
    run()






