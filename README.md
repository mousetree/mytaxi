# MyTaxi Scraper

A tool to scrape mytaxi / FreeNow receipts.

## How it works

This tool will download all emails from Gmail that have the label `mytaxi` and are from the current year. The label must be created separately in Gmail using a saved filter. Recommended is `((mytaxi OR freenow) has:attachment)`

## Getting started

Create a `.env` file in the root directory with the following contents:

    GMAIL_USERNAME=yourname@gmail.com
    GMAIL_APP_PASSWORD=yourapppassword

Then run the following

    pipenv install --dev
    pipenv shell
    python -m mytaxi