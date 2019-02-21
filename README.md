# Telegram Bot for room taking - Hosted on Amazon AWS

## Getting started
Store a 'keys' file with access tokens and secret variables.
It needs to have:

```
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=

export TELEGRAM_TOKEN=
export AWS_URL=

export CHAT_BOT=
```
Our bot was hosted on serverless Amazon AWS, so if you use Lambdas you need to specify a key id and access id key too.


Then, open a terminal on the telegram_bot folder and export secret variables with:
```
source keys
```

Then:
```
pip install -r requirements.txt -t vendored
```


Now your package is ready to be deployed on Amazon AWS:
```
serverless deploy
```

If you send /start to your Bot's chat, you will be ready to work with it.

![img](https://i.imgur.com/LQJOJhZ.png)
## Authors

* **Riccardo Basso** - *Università degli studi di Genova*
* **Davide Ponzini** - *Università degli studi di Genova*
