# Trello Collector 

## Mapping
![Trello](https://user-images.githubusercontent.com/3463702/250350632-9970813a-3a66-47c2-b825-de2e0113df19.jpg)

```
{
    "key": "YOUR_API_KEY",
    "token": "YOUR_TOKEN",
    "board": "Test board",
    "list": "Long-term Goals"
}
```

## Setup
Everything you need to do is written on the [Atlassian guide](https://developer.atlassian.com/cloud/trello/guides/rest-api/api-introduction/).

When you have your newly created app you will be able to see the corresponding **API key** -> click on the app.
![Trello app](https://user-images.githubusercontent.com/3463702/253630254-3f9e753a-4f27-49ce-baef-cd55cba5d0e2.png)

After that you just need to authorize it and get the **token**.
![Trello token](https://user-images.githubusercontent.com/3463702/253630914-5f3f9e95-e28f-4d7f-9625-3643b2f75ec5.png)

Once you have a board created on your workspace and have a list on it, you will be able to fill the config.json.