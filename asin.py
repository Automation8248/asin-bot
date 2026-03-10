name: Daily Tier-1 Kitchen ASINs

on:
  schedule:
    # Yeh daily subah 6:00 AM UTC (Indian time ke hisaab se subah 11:30 AM) par chalega
    - cron: "0 6 * * *" 
  workflow_dispatch:      # Aapko manual 'Run workflow' ka button dega testing ke liye

jobs:
  scrape_and_send:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests beautifulsoup4

      - name: Run Scraper Bot
        env:
          # GitHub Secrets se Telegram credentials fetch karna
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: python asin.py
