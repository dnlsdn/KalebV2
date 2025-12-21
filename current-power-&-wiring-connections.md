# Current Power & Wiring Connections

This document describes the **current electrical wiring state** of the robot.
It reflects the *actual connections as of now*, without assumptions or future changes.

All grounds marked as **GND star** refer to a **single common star-ground point**.

---

## SZBK07 – Servo Power Step-Down (6V)

| Pin | Connected To |
|----|-------------|
| IN− | GND star |
| IN+ | ACS712 terminal |
| OUT+ | Relay terminal |

---

## LM2596 – Logic Power Step-Down (5V)

| Pin | Connected To |
|----|-------------|
| IN− | GND star |
| OUT+ | 5V star |
| OUT− | GND star |

---

## ACS712 – Current Sensor (30A)

| Pin / Terminal | Connected To |
|---------------|-------------|
| Terminal | SZBK07 IN+ |
| Terminal | Fuse |
| GND | GND star |
| OUT | ESP32 GPIO34 |
| VCC | 5V star |

---

## Relay – 5V / 10A (Servo Power Control)

| Pin / Terminal | Connected To |
|---------------|-------------|
| Terminal | 6V star |
| Terminal | SZBK07 OUT+ |
| IN | ESP32 GPIO25 |
| GND | GND star |
| VCC | 5V star |

---

## Voltage Sensor (0–25V)

| Pin / Terminal | Connected To |
|---------------|-------------|
| Terminal | GND star |
| Terminal | 5V star |
| S | ESP32 ADC pin |
| + | 3V3 star |
| − | GND star |

---

## PCA9685 – 16-Channel PWM Servo Driver

| Pin | Connected To |
|----|-------------|
| GND | GND star |
| OE | GND star |
| SCL | ESP32 GPIO22 |
| SDA | ESP32 GPIO21 |
| VCC | 3V3 |
| V+ | null |

---

## Notes

- Servo power (V+) is **physically disconnected** when the relay is OFF  
- Logic and control electronics remain powered at 5V / 3.3V  
- All grounds are tied together using a **star grounding topology**
- This file documents the *current state only*, not final or recommended wiring

---

**Last updated:** _current working session_
