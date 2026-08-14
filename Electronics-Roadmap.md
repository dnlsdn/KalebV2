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

# 2. Firmware

**The reference project contains no firmware.** [SpotMicroESP32 by
michaelkubina](https://github.com/michaelkubina/SpotMicroESP32) is a mechanical and electrical
design; its README states the project lacks the whole programming part, and its `code/` directory
holds test sketches and links to community forks. Wiring this robot exactly as documented produces
a machine that cannot move.

The target firmware is **[Leika, by
runeharlyk](https://github.com/runeharlyk/SpotMicroESP32-Leika)**, one of the three community forks
the reference project recommends. It implements inverse kinematics and two gaits — a 12-point
Bezier trot and an 8-phase crawl — and is driven from a phone browser over WiFi, so it needs no
extra hardware. The two alternatives were rejected: Maarten Weyn's fork needs the ESP-IDF toolchain,
and Blacksheep909's Nitro-Fork needs a custom PCB and an RC transmitter.

The chassis is compatible. michaelkubina publishes the leg link geometry the forks are built
around: **L1 shoulder 10mm, L2 upper leg 60.5mm, L3 lower leg 111.1mm, L4 foot 118.5mm.**

**Toolchain.** Arduino IDE for the small test sketches — the I2C scanner, the relay test, the single
servo. PlatformIO only for Leika itself, which is a submodule project with a filesystem image and a
Svelte web app and does not build in the Arduino IDE.

---

# 3. ESP32 Pinout

Only the core pins are fixed. **The pins for the optional peripherals are deliberately left
unassigned** and get read from Leika's configuration when each one is integrated — the pinout is
dictated by the firmware that runs, not by this document.

| Function      | GPIO | Source            |
| ------------- | ---- | ----------------- |
| I2C SDA       | 21   | Same in all forks |
| I2C SCL       | 22   | Same in all forks |
| Servo relay   | 27   | michaelkubina     |
| ACS712 output | 34   | michaelkubina     |

PCA9685 I2C address: **0x40**. MPU6050: 0x68 or 0x69.

Servo channel map, from michaelkubina, in the order shoulder / upper leg / lower leg:

| Leg         | Channels |
| ----------- | -------- |
| Front left  | 0, 1, 2  |
| Front right | 3, 4, 5  |
| Rear left   | 6, 7, 8  |
| Rear right  | 9, 10, 11 |

An earlier version of this document assigned the relay to GPIO25 and the second sensor's ECHO to
GPIO27, which collides with the reference pinout. Caught in session 3, before anything was wired.

---

# 4. Step-by-Step Roadmap

Phases 0 to 5 and 9 are the path to a walking robot. **Phases 6, 7, 8 and 10 are optional
integrations and come after it walks** — the reference project marks all of those components as
optional and "not tested yet". The WS2812 ring (phase 7) is dropped from this build entirely.

Order of work is in `STATE.md`, not here. This document describes the wiring; `STATE.md` decides
what gets wired next.

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
* Relay IN → GPIO 27
* The relay module is active-low: LOW turns it on, HIGH turns it off. Before `setup()` runs the pin
  is not driven by anything, so add a 10k pull-up from that pin to 3.3V to keep the relay off
  through boot and reset. Without it the servo rail can close for a few milliseconds at power-up,
  while the PCA9685 has not been given any command yet.

---

## Phase 5 — ESP32 + I2C Bus

* ESP32 powered at 5V
* SDA 21, SCL 22
* PCA9685 VCC 3.3V, V+ 6V
* MPU6050 on 3.3V
* OLED on 3.3V

---

## Phase 6 — HC-SR04 (with voltage divider) — OPTIONAL, after it walks

Pins below are from the old invented pinout and are **not** final. Read Leika's configuration before
wiring these. The divider itself is correct and stays as described.


### Sensor 1

* TRIG → 13
* ECHO → divider → 26

### Sensor 2

* TRIG → 14
* ECHO → divider → 27

### Divider:

```
ECHO → 1kΩ → node → GPIO
             |
            2kΩ
             |
            GND
```

The series resistor is the 1kΩ and the 2kΩ goes to ground, so the node sits at 5 × 2/3 = 3.33V.
Swapping the two gives 1.67V, which is below the roughly 2.5V the ESP32 needs to read a pin as
high, and the sensor either misbehaves or never triggers.

---

## Phase 7 — WS2812 Ring — DROPPED from this build

* DATA → GPIO 23 with 330–500Ω resistor
* 5V + GND
* 1000µF capacitor near ring

---

## Phase 8 — ESP32-CAM — OPTIONAL, after it walks

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

## Phase 10 — Battery Sensors — OPTIONAL, after it walks

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
        21   ───│• SDA               27  •│── RELAY
        22   ───│• SCL               34  •│── ACS712
                └─────────────────────────┘

     Core pins only. The optional peripherals get their pins
     from Leika's configuration, when they are integrated.
```

---

# End of document
