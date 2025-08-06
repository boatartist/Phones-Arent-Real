# Phones aren't real (Robo-spy-pigeon-phone)

## About the project
Challenging my attention span and the idea of a phone in a chaotic Raspberry Pi-powered robot bird, one teenage girl's mission to build an entire phone including notes, the weather, a camera and texts, as well as less conventional features like self-balancing, text-to-speech and a custom PCB and 3D printed shell. 

The bird is powered by a Raspberry Pi Zero with a Raspberry Pi camera, a round touchscreen display, speaker, rechargeable battery, power and USB breakout boards, a USB microphone and a standard 4G modem dongle for internet and texts. It's a decidedly amateur build which pushed me to my limits as I struggled to compress a variety of incompatible libraries into the Pi's miniscule storage, teaching me about the backend of modems, image recognition algorithms, accelerometer boards and most importantly, the miracle that modern phones can fit all this and more in such as small rectangle and be so simultaneously boring and addictive.

If you're interested in the gruesome details of this project you can find my full (and insane) logbook in the Wiki of this Github page, and I've included some diagrams, progress photos and instructions below, enjoy!

## Graphics, diagrams and soooooooooo many prototypes
<img width="826" height="583" alt="wiring diagram" src="https://github.com/user-attachments/assets/787985b5-027f-4f46-8a9a-559c643953c7" />
<img width="640" height="1378" alt="2D image of custom PCB" src="https://github.com/user-attachments/assets/f0854ac4-e747-4b4c-9dbf-9e5e658a74e9" />
<img width="1778" height="996" alt="photograph of some of the main components" src="https://github.com/user-attachments/assets/d8e34e93-4b6c-4cd9-97cc-a4a8557a81c3" />
<img width="546" height="842" alt="most up-to-date photo of galah phone" src="https://github.com/user-attachments/assets/d7268a65-f361-4d0b-ac88-a67df816f009" />
<img width="980" height="1305" alt="conceptual rendering of galah in blender, with colouring" src="https://github.com/user-attachments/assets/5af330da-d4ff-4208-a96a-035719d5da5c" />
<img width="2210" height="1238" alt="literal wireframe of bird" src="https://github.com/user-attachments/assets/dcbc540f-6d61-49fd-8c51-e54040deaa0f" />
<img width="703" height="815" alt="coreflute prototype showing screen with weather displayed from API" src="https://github.com/user-attachments/assets/e6f1c7d2-f1eb-41b1-b998-68deb3d76fee" />
<img width="539" height="939" alt="3D printed pigeon prototype" src="https://github.com/user-attachments/assets/be8a2e8e-45fd-400a-9930-f673b54190eb" />
<img width="1773" height="993" alt="geared foot prototype" src="https://github.com/user-attachments/assets/26b09beb-946a-4990-8797-0cfbeaee3b19" />
<img width="1194" height="1362" alt="annotated/overlayed tape and cardboard model showing vision for bird" src="https://github.com/user-attachments/assets/f3ac3f7f-27d4-4334-a50a-6cc62f32cda4" />


## Original introduction from May 16, 2024
Hello! Welcome to my Robot-spy-pigeon-phone-assistant-project (renamed to Phones aren't real)! This is an idea I've had in my head for ages, and I really want to document one of my procrastination projects properly, so I'm just going to put everything I do onto this github, then procrastinate on my procrastination by fixing it later.

So, robot phones. I think I was unreasonably influenced by Amy McCulloch's Jinxed series, which is a pretty good YA series in its own right. Basically the premise is that everyone has an animal-looking robot that does everything their phone used to do, and also is like a pet and friend and assistant, and idk I just think that's pretty cool. I would just make that but it'd kinda feel like plagiarism or something, which brings me to my second influence: Birds aren't real. I assume everyone has heard of this pseudo conspiracy, which is just hilarious and very much something my generation would make up in response to actual conspiracy theorists. Essentially, all birds were hunted down and killed by the US government/CIA in the 50s and 60s and replaced with spy drones that are tracking us, ooh scary. Finally: ornithopters. You know drones? They're like that but cooler, because they flap their wings. I'm not an aeronautical engineer (I'm just a highschooler actually), but I do have a very hyper plane loving little brother, so there's that

With these ideas in mind I have a bunch of features I want to implement at some point but may never, best explained through a series of tiny sketches:

<img width="2134" height="1408" alt="image" src="https://github.com/user-attachments/assets/8f0dcd99-3214-425d-8dd3-1497e35dc37c" />
<img width="2149" height="1420" alt="image" src="https://github.com/user-attachments/assets/46a5d839-bbd1-4f6b-8d51-1ae6545386bb" />

Look at the little cyborg pigeon!!!❤️❤️❤️❤️ I'm so proud of my non-existent drawing skills. If you can't read my handwriting (valid, I can't either), here's some of the highlights:

cute little perch
holds a little pencil
camera (or is it a death laser?)
touchscreen
eyes follow you around
full 360° vision, head rotates
foot clamps/jointed toes (taking inspiration from nerdforge's prosthetic finger but it defaults to contracted so it doesn't fall off the perch)
Bits that move (perched edition): feet lift and flap, head rotates = 3 servos, optional bonus: balance body by tilting
also some sound effects/comments ie. eeeee, creeeeak, ring ring..., unknown phone number...


## Assembly Instructions
Components:
- Raspberry Pi Zero 2 W
- Waveshare Round 1.28inch Touch LCD
- 3.7V 2000mAh LiPo battery
- Telstra LTE 4GX usb modem
- Raspberry Pi camera
- Raspberry Pi camera cable for Pi Zero
- SD card with Raspbian OS for Pi Zero
- USB microphone
- Adafruit Mini USB 4-Port Hub
- Adafruit PowerBoost 500 Charger board
- ADXL345 Accelerometer
- 3 x 9g micro servos
- Mini HDMI to HDMI adapter
- solderable USB sockets
- custom PCB HAT (TBC)
- small speaker/piezo buzzer
- BC557 transistor (for audio amplification)
- 10uF electrolytic capacitor
- 150 ohm resistor
- 270 ohm resistor
- 33 nF ceramic capacitor
- male and female header pins (lots idk how many)

Also possibly needed:
- hdmi cable
- usb mouse and keyboard
- monitor
- micro-usb power source for charging
- soldering equipment
- optional led or sensor for eye

Next up, software settings:
- Raspbian OS for Pi Zero 2 W
- connect to home wifi
- connect to modem by going to `192.168.0.1`
- raspberry pi configuration enable SPI, I2C, set timezone and locale
- alsamixer confirm microphone connection
- open config.txt with `sudo nano /boot/firmware/config.txt` and add `dtoverlay=audremap,pin=13,func=4` to the bottom, as well as `dtoverlay=i2c-gpio,bus=4,i2c_gpio_delay_us=1,i2c_gpio_sda=23,i2c_gpio_scl=24` where spi is enabled, then save and close
- install all python modules with `sudo apt install python3-xyz`, where xyz is the name of each package, (pip is broken in newer versions of raspbian so we need to do it one at a time)
- install espeak with `sudo apt install -y espeak`
- install vosk (stt) with `pip3 install vosk --break-system-packages` (yes it's a bit sketchy but it didnt' work with python3)
- install picamera `sudo apt-get install python3-picamera2 python3-picamera2` (change this in the code, picamera is outdated we need the new version)
- download all the code and put it on the desktop; command line: `wget https://github.com/boatartist/Robo-spy-pigeon-phone/raw/refs/heads/main/galah.zip`
- check all path names are right by running code on the command line `python3 /home/pi/Desktop/galah/bird.py` (or whatever the file is called)
- run the code and make any changes you need to, there may be compatibility errors
- (change the gpio pin for the speaker power from gpio 24 to gpio 12)
- right click on the audio icon in the top right of the screen, increase the volume, in device profiles turn off hdmi audio and check that av jack is enabled in stereo.
- edit `/home/pi/etc/rc.local` and add the line `sudo python3 /home/pi/Desktop/galah/bird.py &`, which should make your code run on startup but in the background so that if it crashes you can still use the raspberry pi
