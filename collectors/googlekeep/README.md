# Google Keep Collector 

## Mapping
![Keep Text note](https://user-images.githubusercontent.com/3463702/250350631-abae8a92-2ef2-48c3-8082-0c4bc58d943a.jpg)
![Keep List note](https://user-images.githubusercontent.com/3463702/253660376-61843d5a-88c1-4d07-8404-19f8a102fc95.jpg)


## Setup
To generate an app password:

TODO
1. Follow this [guide](https://github.com/rukins/gpsoauth-java/blob/b74ebca999d0f5bd38a2eafe3c0d50be552f6385/README.md#receiving-an-authentication-token)
2. When you have the oauth_token copy that to the exchange.py file in this folder
3. Follow comments and run the file
4. The printed value goes to the password field of config.json
```
{
    "username": "YOUR_MAIL_ADDRESS",
    "password": "YOUR_MASTER_TOKEN",
    "nodeName": "Daily schedule",
    "onlyUncheckedItems": true
}
```
The "onlyUncheckedItems" field is only interesting when you work with lists. If the value is _true_, it will only display the unchecked items.