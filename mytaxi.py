#!/usr/bin/env python3

import os
import pandas as pd
from extract import parse_bill
from download import download_mytaxi_files

ATTACHMENT_DIR = os.path.join(os.getcwd(), 'attachments')
OUTPUT_DIR = os.path.join(os.getcwd(), 'output')

def setup_directories(dirs=[]):
    for directory in dirs:
        if not os.path.exists(directory):
            os.mkdir(directory)

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
    print(f'{total_bills} bills with total cost: €{total_cost}')

def main():
    setup_directories([ATTACHMENT_DIR, OUTPUT_DIR])
    download_mytaxi_files(ATTACHMENT_DIR)
    df = pdf_to_df()
    df.to_csv(os.path.join(OUTPUT_DIR, 'mytaxi.csv'))
    print_summary(df)

if __name__== "__main__":
    main()






