# Google Keep Collector 

## Mapping
![Keep Text note](https://user-images.githubusercontent.com/3463702/250350631-abae8a92-2ef2-48c3-8082-0c4bc58d943a.jpg)
![Keep List note](https://user-images.githubusercontent.com/3463702/253660376-61843d5a-88c1-4d07-8404-19f8a102fc95.jpg)


## Setup
To generate an app password:

1. Go to your [Google Account](https://myaccount.google.com/)
2. Select Security.
3. Under "Signing in to Google," select 2-Step Verification.
4. At the bottom of the page, select App passwords.
5. Enter a name that helps you remember where you’ll use the app password.
6. Select Generate.
7. Now you can copy the generated password to the config.json
```
{
    "username": "YOUR_MAIL_ADDRESS",
    "password": "YOUR_PASSWORD",
    "nodeName": "Daily schedule",
    "onlyUncheckedItems": true
}
```
The "onlyUncheckedItems" field is only interesting when you work with lists. If the value is _true_, it will only display the unchecked items.