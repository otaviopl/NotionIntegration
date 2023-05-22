# Notion Bot to send email with Tasks :rocket:

:construction: __UNDER CONSTRUCTION!__ :construction:

Based on a Notion control panel, the software will fetch the tasks that must be completed in the next __N__ days and send them by email daily.

The idea is to use this API connection with Notion to automate more things, and include more information in the automated email.

## How to use

### Create a Google GMail API credentials

Visit the [website](https://developers.google.com/gmail/api/quickstart/python) to follow the tutorial and create a project on Google Cloud with proper credentials.

The Google Cloud credentials file must be in the project root folder with the name `'credentials.json'`. After the authentication, a `token.json` file will be created.

### Create your Notion credentials

Follow the [Notion guide](https://developers.notion.com/docs/authorization) and create your API credentials. Put it inside a `notion_credentials.json` file, following this format:

```py
{
    "database_id": "",
    "notion_key": ""
}
```

### Create email configurations

The software will look for some settings like source and destination email inside the 'email_config.json' file in the root folder of the project. The file must follow the following format:

```py
{
    "email_from": "<EMAIL_ADDR",
    "email_to": "<EMAIL_ADDR>",
    "display_name": "User Name"
}
```