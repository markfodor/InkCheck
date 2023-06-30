# InkCheck
## Background / Inspiration
```
"When you have your goals in front of you, they become a powerful compass that directs your decisions and actions.
Stay focused, stay driven, and let your goals lead the way." - Unknown

"Goals kept in your heart remain wishes forever.
Take them out, write them down, and keep them in sight as a constant reminder of what you're capable of achieving." - Les Brown
```

This repo can help you set up an e-ink board and display your Trello and/or Google Keep data so your goals can be seen every day.

## General description
This is a forked repo from [MagInkDash](https://github.com/markfodor/MagInkDash). That project was used as a base for everything here.
So if you have the opportunity, buy that guy a coffee (link on the MagInkDash README). :v:

InkCheck however differs in many aspects.
It is able to display your Google Keep and/or Trello data on an [Inkplate E-Ink Display](https://soldered.com/product/soldered-inkplate-10-9-7-e-paper-board-with-enclosure-copy/).

You can use it to display:
- your daily schedule
- your long-term goal
- a TODO list
- any text/quote you want to keep in mind

## Hardware Required
- [Inkplate 10 E-Ink Display](https://soldered.com/product/soldered-inkplate-10-9-7-e-paper-board-with-enclosure-copy/) - Used as a client to display the generated image. If you go with this it will be less hardware tinkering.
- A server, which is powerful enough to run the image generation. It could be a [Raspberry Pi](https://www.raspberrypi.org/)

## How It Works
A cron job on RPi will trigger a Python script to run every hour to fetch calendar events from Google Calendar, weather forecast from OpenWeatherMap and random factoids from OpenAI's ChatGPT. The retrieved content is then formatted into the desired layout and saved as an image. An Apache server on the RPi will then host this image such that it can be accessed by the Inkplate 10. On the Inkplate 10, the corresponding script   will then connect to the RPi server on the local network via a WiFi connection, retrieve the image and display it on the E-Ink screen. The Inkplate 10 then goes to sleep to conserve battery. The dashboard remains displayed on the E-Ink screen, because well, E-Ink...

Some features of the board: 
- **Battery Life**: As with similar battery powered devices, the biggest question is the battery life. I'm currently using a 1500mAh battery on the Inkplate 10 and based on current usage, it should last me around 3-4 months. With the 3000mAh that comes with the manufacturer assembled Inkplate 10, we could potentially be looking at 6-8 month battery life. With this crazy battery life, there are much more options available. Perhaps solar power for unlimited battery life? Or reducing the refresh interval to 15 or 30min to increase the information timeliness?
- **Telegram Bot**: Although the battery life is crazy long on the Inkplate 10, I still wish to be notified when the battery runs low. To do so, I set up a Telegram Bot and the Inkplate will trigger the bot to send me a message if the measured battery voltage falls below a specified threshold. That said, with the bot set up, there's actually much more you could do, e.g. send yourself a message when it's to expected to rain in the next hour.

## Setting Up 

1. Start by flashing [Raspberrypi OS Lite](https://www.raspberrypi.org/software/operating-systems/) to a SD/MicroSD Card. If you're using a Raspberry Pi with 32bit CPU, there are [known issues](https://forums.raspberrypi.com/viewtopic.php?t=323478) between the latest RPiOS "bullseye" release and chromium-browser, which is required to run this code. As such, I would recommend that you keep to the legacy "buster" OS if you're still running this on older RPi hardware.

2. After setting up the OS, run the following commmand in the RPi Terminal, and use the [raspi-config](https://www.raspberrypi.org/documentation/computers/configuration.html) interface to setup Wifi connection, and set the timezone to your location. You can skip this if the image is already preconfigured using the Raspberry Pi Imager.

```bash
sudo raspi-config
```
3. Run the following commands in the RPi Terminal to setup the environment to run the Python scripts and function as a web server. It'll take some time so be patient here.

```bash
sudo apt update
sudo apt-get install python3-pip
sudo apt-get install chromium-chromedriver
sudo apt-get install libopenjp2-7-dev
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
pip3 install pytz
pip3 install selenium
pip3 install Pillow
pip3 install openai  
sudo apt-get install apache2 -y  
sudo chown pi:www-data /var/www/html
sudo chmod 755 /var/www/html
```
4. Download the over the files in this repo to a folder in your PC first. 

5. In order for you to access your Google Calendar events, it's necessary to first grant the access. Follow the [instructions here](https://developers.google.com/calendar/api/quickstart/python) on your PC to get the credentials.json file from your Google API. Don't worry, take your time. I'll be waiting here.

6. Once done, copy the credentials.json file to the "gcal" folder in this project. Navigate to the "gcal" folder and run the following command on your PC. A web browser should appear, asking you to grant access to your calendar. Once done, you should see a "token.pickle" file in your "gcal" folder.

```bash
python3 quickstart.py
```

7. Copy all the files (other than the "inkplate" folder) over to your RPi using your preferred means. 

8. Run the following command in the RPi Terminal to open crontab.
```bash
crontab -e
```
9. Specifically, add the following command to crontab so that the InkCheck Python script runs on the hour, every hour.
```bash
0 * * * * cd /location/to/your/InkCheck && python3 main.py
```
10. As for the Inkplate, I'm not going to devote too much space here since there are [official resources that describe how to set it up](https://inkplate.readthedocs.io/en/latest/get-started.html). It may take some trial and error for those new to microcontroller programming but it's all worth it! Only the Arduino portion of the guide is relevant, and you'll need to be able to run *.ino scripts via Arduino IDE before proceeding. From there, run the "inkplate.ino" file from the "inkplate" folder from the Arduino IDE when connected to the Inkplate.

12. That's all! Your Dashboard should now be refreshed every hour! 

## Acknowledgements
- [Lexend Font](https://fonts.google.com/specimen/Lexend)
- [Bootstrap](https://getbootstrap.com/): Styling toolkit to customise the look of the dashboard
- [Freepik](https://www.freepik.com/): For the background image used in this dashboard