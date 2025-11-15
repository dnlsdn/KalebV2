# Spot Micro ESP32 — Complete Electronics Roadmap

Version: 1.0

This roadmap describes all electronics needed to build the Spot Micro ESP32 using:

* 12× MG996R
* ESP32 DevKitC
* ESP32-CAM
* PCA9685
* MPU6050
* 2× HC-SR04
* OLED SSD1306
* WS2812 Ring
* 5V Relay
* LM2596, SZBK07
* 25V Voltage Sensor
* ACS712 30A

Contains:

* General architecture
* Dedicated ESP32 pinout
* Detailed step-by-step roadmap
* ASCII diagram

---

# 1. General Architecture

```text
         ┌──────────────────────── LiPo 2S (7.4V) ────────────────────────┐
         │                                                                │
         │                 (+)                                  (-) GND   │
         │                  │                                    │        │
         │           [ 10A Fuse ]                                │        │
         │                  │                                    │        │
         └───────────[ ACS712 30A ]───────────────┬──────────────┘
                                                  │
                                       ┌──────────┴───────────┐
                                       │                      │
                           LOGIC BRANCH (5V)       SERVO BRANCH (6V)
                                LM2596                     SZBK07
                                 5.0V                       6.0V
                                   │                          │
                             ┌─────┴─────┐             ┌──────┴──────┐
                             │           │             │             │
                        ESP32 DevKit   ESP32-CAM     5V Relay     PCA9685
                        I2C Sensors    (video)       (ON/OFF 6V)  + 12× MG996R
                        HC-SR04        Wi-Fi           │
                        WS2812 ring                    │
                        Button LED               → 6V to servos
                        Voltage sensor
                        ACS712 output → ADC
                             │
                     All grounds connected
                           (single star)
```

---

# 2. ESP32 Pinout

| Function                  | GPIO |
| ------------------------- | ---- |
| I2C SDA                   | 21   |
| I2C SCL                   | 22   |
| Servo Relay               | 5    |
| WS2812 DATA               | 23   |
| HC-SR04 #1 TRIG           | 13   |
| HC-SR04 #1 ECHO (divider) | 26   |
| HC-SR04 #2 TRIG           | 14   |
| HC-SR04 #2 ECHO (divider) | 27   |
| Button                    | 18   |
| Button LED optional       | 19   |
| Voltage sensor 25V        | 36   |
| ACS712 output             | 34   |

---

# 3. Step-by-Step Roadmap

## Phase 0 — Setup and Safety

* Non conductive surface
* LiPo disconnected
* Prepare multimeter and tools

---

## Phase 1 — Adjust LM2596 and SZBK07

* LM2596 set to 5.00V
* SZBK07 set to 6.00V

---

## Phase 2 — Fuse and ACS712

* LiPo + → 10A Fuse → IN+ ACS712
* OUT+ ACS712 → power distribution
* Use 14–16 AWG wire

---

## Phase 3 — Logic branch, servo branch, common ground

* ACS712 OUT+ → LM2596 IN+, SZBK07 IN+
* Single ground star point
* 1000µF near PCA9685

---

## Phase 4 — Relay ON/OFF for servos

* SZBK07 OUT+ → Relay COM
* Relay NO → 6V to PCA9685
* Relay IN → GPIO 5

---

## Phase 5 — ESP32 + I2C Bus

* ESP32 powered at 5V
* SDA 21, SCL 22
* PCA9685 VCC 3.3V, V+ 6V
* MPU6050 on 3.3V
* OLED on 3.3V

---

## Phase 6 — HC-SR04 (with voltage divider)

### Sensor 1

* TRIG → 13
* ECHO → divider → 26

### Sensor 2

* TRIG → 14
* ECHO → divider → 27

### Divider:

```
ECHO → 2kΩ → node → GPIO
             |
            1kΩ
             |
            GND
```

---

## Phase 7 — WS2812 Ring

* DATA → GPIO 23 with 330–500Ω resistor
* 5V + GND
* 1000µF capacitor near ring

---

## Phase 8 — ESP32-CAM

* 5V → CAM
* Common ground
* Flash using FT232RL as needed

---

## Phase 9 — PCA9685 → 12× MG996R

* Servos on channels 0–11
* Signal → PCA9685
* Red → 6V
* Black → GND
* Center all servos at 1500µs before mounting horns

---

## Phase 10 — Battery Sensors

### Voltage Sensor

* OUT → GPIO 36
* IN+ → positive after ACS712

### ACS712

* OUT → GPIO 34

---

## Phase 11 — Final Testing

* I2C scanner
* OLED test
* Relay test
* Single servo test
* HC-SR04 test
* WS2812 test
* ESP32-CAM test
* Battery test under load

---

# ASCII ESP32 Diagram

```text
                ┌─────────────────────────┐
        3V3  ───│• 3V3               VIN •│── 5V
        GND  ───│• GND               GND •│── GND
        21   ───│• SDA               23  •│── WS2812
        22   ───│• SCL               5   •│── RELAY
        13   ───│• TRIG1             14  •│── TRIG2
        26   ───│• ECHO1             27  •│── ECHO2
        18   ───│• BUTTON            19  •│── LED BUTTON
        36   ───│• VBAT SENSOR       34  •│── ACS712
                └─────────────────────────┘
```

---

# End of document
