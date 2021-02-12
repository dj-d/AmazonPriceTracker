![SonarQube](https://github.com/dj-d/AmazonPriceTracker/workflows/SonarQube/badge.svg)

# AmazonPriceTracker
Telegram bot to check the price change of products on Amazon and CamelCamelCamel

## Setup
In the credential.json replace "__*YOUR_BOT_TOKEN*__" with the token of your bot.

```json
{
  "TOKEN": "YOUR_BOT_TOKEN"
}
```

## Usage
The bot can be launched via Python command or via Docker

### Command Line
Enter the project folder and run the following commands

```
python3 bot.py
```

### Docker

#### Automated
For Linux users, to automate the steps, you can use the script __*build_and_run.sh*__.

#### Manual
Enter the project folder and run the following commands

```bash
docker build -t amazon_price_tracker .
docker run -d --name=amazon_price_tracker -it amazon_price_tracker
```

## Link

Telegram Bot: _[AmazonPriceTracker](https://t.me/djd_apt_bot)_

## Support
