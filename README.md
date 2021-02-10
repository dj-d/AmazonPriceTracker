![SonarQube](https://github.com/dj-d/AmazonPriceTracker/workflows/SonarQube/badge.svg)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=dj-d_AmazonPriceTracker&metric=alert_status)](https://sonarcloud.io/dashboard?id=dj-d_AmazonPriceTracker)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=dj-d_AmazonPriceTracker&metric=bugs)](https://sonarcloud.io/dashboard?id=dj-d_AmazonPriceTracker)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=dj-d_AmazonPriceTracker&metric=code_smells)](https://sonarcloud.io/dashboard?id=dj-d_AmazonPriceTracker)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=dj-d_AmazonPriceTracker&metric=security_rating)](https://sonarcloud.io/dashboard?id=dj-d_AmazonPriceTracker)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=dj-d_AmazonPriceTracker&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=dj-d_AmazonPriceTracker)

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
python3 -m pip install -r requirements.txt
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

## Support
