# Lost Ark Bot

Automated discord bot for displaying patch notes from Lost Ark.

## Requirements

- Python 3.6 and up - https://www.python.org/downloads/
- git - https://git-scm.com/download/

### How to install modules

```
for windows:
python -m pip install -r requirements.txt

for linux:
python3 -m pip install -r requirements.txt
```

### CONFIG

rename `config_example.json` to `config.json` then store your token and some other private info like this:

```
{
    "DISCORD_TOKEN":"bot-token",
    "GUILD_ID":123456789,
    "DISCORD_BOT_ID":123456789
}
```

### WEBHOOK

rename `webhook_example.cfg` to `webhook.cfg` then store your token and some other private info like this:

**IMPORTANT: NEEDED FOR APSCHEDULER TO POST AUTOMATED PATCH NOTES TO DISCORD CHANNEL**

```
[webhooks]
LOST_ARK_WEBHOOK:<webhook url>

```
