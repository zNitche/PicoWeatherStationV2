## PicoWeatherStationV2

Off-grid, standalone version of [PicoWeatherStation](https://github.com/zNitche/PicoWeatherStation) powered by [strawberryAPI](https://github.com/zNitche/strawberryAPI).

---

![interior](.media/pw_interior.jpg)
![exterior](.media/pw_exterior.jpg)

#### Features
- Logging temperature & humidity.
- Logging battery & pv voltage.
- Access to logged data through WiFi hotspot and web app.
- Logs visualisation using `chart.js`.

#### Setup
1. clone repo
2. clone submodules
```
git submodule update --init --recursive
```
3. set `HOTSPOT_SSID` and `HOTSPOT_PASSWORD` in `config.py`
4. set `WEATHER_LOGS_PER_HOUR` in `config.py` (default logging sensors data every 20 minutes).
5. format sd card (FAT32).
6. `chart.js` setup:
rpi pico doesn't have enough space for flashing css/js libs, get `chart.js` from cdns (`https://cdn.jsdelivr.net/npm/chart.js@4.3.0/dist/chart.umd.min.js`),
then put it on sd card `/static/libs/chart.js`.
7. flash `RPi Pico`.

#### Wiring
ToDo

#### Parts
- 1x Raspberry Pi Pico W
- 1x DHT20 temperature and humidity sensor
- 1x DS3231 I2C RTC module
- 1x MicroSD card
- 1x SPI MicroSD card reader module
- 1x Circuit board
- 1x Waterproof case
- Some gold pin connectors
- Some connecting wires
- 1x Cell holder for 2x 18650 battery
- 2x 18650 li-ion battery
- 1x Step-down Voltage Regulator - 1,0V-17V
- 1x Step-up converter 5V
- 1x Lipol charger TP4056 1S 3,7V with protection
- 2x 6V solar panel 165x135x3mm
- 1A fuse with wires
- 2x 3.3V zener diode
- 1x 4.7k resistor
- 1x 1k resistor
- 2x 10k resistor
- 3x ARK connector raster 5.0mm 2 pin
- some 3mm screws and nuts
- some 4mm screws and nuts

#### 3D printed parts
all models are provided in `freecad` project files for easier modifications.
- 1x bat_mount
- 1x case_backplate
- 2x case_bridge
- 1x case_m_top
- 1x case_th_connector
- 1x pcb_mount
- 2x pv_b_holder
- 2x pv_b_s_mount
- 1x pv_t_mount
- 2x pv_s_mount
- 2x pv_t_s_mount
- 1x th_holder
- 1x th_holder_b
- 1x th_holder_mount
