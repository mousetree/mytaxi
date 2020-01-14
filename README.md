# MyTaxi Scraper

A tool to scrape mytaxi / FreeNow receipts.

## How it works

This tool will download all emails from Gmail that have the label `mytaxi` and are from the current year. The label must be created separately in Gmail (i.e. by using a saved filter). Recommended is `((mytaxi OR freenow) has:attachment)`. The tool will output a summary of your rides and the total cost in the command line and also generate a CSV with your ride history.

## Getting started

Create a `.env` file in the root directory with the following contents:

    GMAIL_USERNAME=yourname@gmail.com
    GMAIL_APP_PASSWORD=yourapppassword

If you use 2FA then you will need to [create an app password](https://devanswers.co/create-application-specific-password-gmail/)

Then run the following:

    pipenv install --dev
    pipenv shell
    python -m mytaxi

The above requires `pipenv` to be installed.
