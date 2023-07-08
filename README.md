# InkCheck
## Background / Inspiration
```
"When you have your goals in front of you, they become a powerful compass that directs your decisions and actions.
Stay focused, stay driven, and let your goals lead the way." - Unknown

"Goals kept in your heart remain wishes forever.
Take them out, write them down, and keep them in sight as a constant reminder of what you're capable of achieving." - Les Brown
```

This repo can help you set up an e-ink board and display your Trello and Google Keep data so your goals can be seen every day.

![InkCheck](https://user-images.githubusercontent.com/3463702/250285813-c93ab4b4-c946-4134-a144-b92ad8b61ca0.jpg)

### Google Keep mapping
![Keep](https://user-images.githubusercontent.com/3463702/250350631-abae8a92-2ef2-48c3-8082-0c4bc58d943a.jpg)
It also works with lists as the following Trello example shows. It is rendered the same way.

### Trello mapping
![Trello](https://user-images.githubusercontent.com/3463702/250350632-9970813a-3a66-47c2-b825-de2e0113df19.jpg)

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
A cron job on your server will trigger a Python script to run every hour (or the set interval) to fetch Google Keep and/or Trello data. The retrieved content is then formatted into the desired layout with a [Jinja](https://jinja.palletsprojects.com/) template and saved as an image. An Apache server will then host this image so that it can be accessed by the Inkplate 10. On the Inkplate 10, the corresponding script  will then connect to the server on the local network via WiFi connection, retrieve the image and display it on the E-Ink screen. The Inkplate then goes to sleep to conserve battery. The image remains displayed on the E-Ink screen.

Some features of the board: 
- **Battery Life**: As with similar battery powered devices, the biggest question is the battery life. I'm currently using a 1500mAh battery on the Inkplate 10 and based on current usage, it should last me around 3-4 months. With the 3000mAh that comes with the manufacturer assembled Inkplate 10, we could potentially be looking at 6-8 month battery life. With this crazy battery life, there are much more options available. Perhaps solar power for unlimited battery life? Or reducing the refresh interval to 15 or 30min to increase the information timeliness?
- **Telegram Bot**: Although the battery life is crazy long on the Inkplate 10, I still wish to be notified when the battery runs low. To do so, I set up a Telegram Bot and the Inkplate will trigger the bot to send me a message if the measured battery voltage falls below a specified threshold. That said, with the bot set up, there's actually much more you could do, e.g. send yourself a message when it's to expected to rain in the next hour.

## Setting Up 

1. Start by flashing [Raspberrypi OS Lite](https://www.raspberrypi.org/software/operating-systems/) to a SD/MicroSD Card. If you're using a Raspberry Pi with 32bit CPU, there are [known issues](https://forums.raspberrypi.com/viewtopic.php?t=323478) between the latest RPiOS "bullseye" release and chromium-browser, which is required to run this code. As such, I would recommend that you keep to the legacy "buster" OS if you're still running this on older RPi hardware.

2. After setting up the OS, run the following commmand in the RPi Terminal, and use the [raspi-config](https://www.raspberrypi.org/documentation/computers/configuration.html) interface to setup Wifi connection, and set the timezone to your location. You might want to enable the SSH connection as well, because it is easier to setup the config remotely.

```bash
sudo raspi-config
```
3. Run the following commands in the RPi Terminal to setup the environment to run the Python scripts and function as a web server. It'll take some time so be patient here.

```bash
sudo apt update
sudo apt-get install python3-pip
sudo apt-get install chromium-chromedriver
sudo apt-get install libopenjp2-7-dev
sudo apt install git
sudo apt-get install apache2 -y
sudo chown pi:www-data /var/www/html
sudo chmod 755 /var/www/html
```

4. Make sure that the Apache server is running. If you are on the same local network with your server, just type the IP addess of your server in the browser and it should load the default index.html.

5. Clone repository and install python dependencies. Sidenote: Some of the dependencies might dispplay warnings. No need to worry if everything works fine.
```bash
git clone https://github.com/markfodor/InkCheck
cd InkCheck
pip install -r requirements.txt
```

6. Fill the variables in the config.json.

7. Do a test run and check the logs. If everything is ok you should not see any error logs.
```bash
python3 main.py
```
This might takes a bit longer (depends on your hardware - 2-3 mins on a Raspberry Pi Zero). When it is done, you should be able to find the rendered html file (renderer/inkcheck.html) and the screenshot (output/inkcheck.png). The image should be available on your network if you check in a browser: YOUR_SERVER_IP/inkcheck.png

7. Copy all the files (other than the "inkplate" folder) over to your RPi using your preferred means. 

8. Run the following command in the RPi Terminal to open crontab.
```bash
crontab -e
```

9. Specifically, add the following command to crontab so that the InkCheck Python script runs on the hour, every hour.
```bash
0 * * * * cd /location/to/your/InkCheck && python3 main.py
```
If you want to set an other interval check out the [crontab.guru](https://crontab.guru/) site.

10. As for the Inkplate, I'm not going to devote too much space here since there are [official resources that describe how to set it up](https://inkplate.readthedocs.io/en/latest/get-started.html). It may take some trial and error for those new to microcontroller programming but it's all worth it! Only the Arduino portion of the guide is relevant, and you'll need to be able to run *.ino scripts via Arduino IDE before proceeding. From there, compile and upload the "inkplate.ino" file from the "inkplate" folder in the Arduino IDE when connected to the Inkplate. And do not forget to fill the ssid, password and imgurl fields at the top of the ino file. Oh, and the BOTtoken if you want to get notifications about the battery.
Common problems:
- Inkplate is not connected
- Inkplate is not ON - a light blue led should shine through the 3D-printed case next to the ON button.
- Wrong board selected. Tools -> Boards: Soldered Inkplate 10
- Wrong port is selected. Tools -> Port
- Inkplate is not recognized. When it is correctly connected you should see some info about the board when clicking Tools -> Get Board Info

12. That's all! Your InkCheck should now be refreshed every hour!

## Acknowledgements
- [Lexend Font](https://fonts.google.com/specimen/Lexend)
- [Jinja](https://jinja.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)

## Contribution
Feel free to fork/modify the code to your needs. If you want something to be in this repo, then just open an issue or a pull request.

Things I want to add:
- Generalize the code -> it would be easier to add a new source
- Generalize the template to handle single and double coulmns
- Portrait and landscape mode
- Docker support -> easier to setup the server
- Optional: server endpoint to kickstart the image generation so you do not need to wait for the next refresh