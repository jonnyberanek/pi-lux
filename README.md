# 🔴 pi 🟢 lux 🔵
A WIP monorepo of sorts for an all-around system to intelligently control LED strips. Meant to be run on a raspberry pi and designed for WS2801 LEDs. 

The repo currently includes:
  - A TCP server listening to and reacting to instructions
  - A simple React app used to control the fill of the strip manually
  - An Express backend for listening to external commands and routing them to the TCP server

Planned integrations inlcude listening to f.lux for dimming as the night grows darker; Alexa skills for acessible, quick controls; and a more robust web dashboard to control settings and custom patterns!
