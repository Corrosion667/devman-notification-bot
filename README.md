# Devman notification bot

[![Maintainability](https://api.codeclimate.com/v1/badges/8af3731206254f254a6a/maintainability)](https://codeclimate.com/github/Corrosion667/devman-notification-bot/maintainability)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![linter check](https://github.com/Corrosion667/devman-notification-bot/actions/workflows/linter-check.yml/badge.svg)](https://github.com/Corrosion667/devman-notification-bot/actions/workflows/linter-check.yml)

---

## Basic information

***Devman notification bot*** send notifications via telegram about checking of works and lessons on **dvmn.org**.

<ins>Each *notification* include:</ins>  
- Lesson title;
- Link to the lesson;
- Status message about success or failure.

Bot will also send you notification if there is any problems with Devman Api.

## Running

The easiest way to run this bot is to use official ***Docker image***.  
You only need to create **.env** file and set the <ins>following environmental variables</ins> *(as in the .env(example) file)*:  

| Environmental      | Description                                           |
|--------------------|-------------------------------------------------------|
| `DEVMAN_TOKEN`     | personal student token from *dvmn.org* to use its API |       
| `TELEGRAM_TOKEN`   | bot token from @BotFather in telegram                 |      
| `TELEGRAM_CHAT_ID` | your id from @userinfobot                             |
| `USERNAME`         | your name                                             |

Run bot in container with the following command:
```bash
docker run -d --env-file .env corrosion667/devman-notification-bot
```
&nbsp;
#### *Alternative running method*

If you do not have docker, you can use this workflow:
1. clone the repository:
```bash
git clone https://github.com/Corrosion667/devman-notification-bot.git
```
2. Create **.env** file and set the <ins>environmental variables</ins> as described above.
3. Install dependencies:
```bash
make install
```
* Please take note that it requires *poetry*. If you do not have it yet, run:
```bash
make full-install
```
* So that *poetry* will also be installed into your user's environment with project dependencies.
4. Run the bot:
```bash
make run
```