# Step 12 — Battery Voltage Sensor (0–25V) → ESP32 (SP / GPIO36)

## Objective

Integrate the **0–25V voltage sensor module** into the power architecture and connect it to the ESP32 so that the microcontroller can continuously **monitor LiPo voltage**.

This enables:

- low-voltage protection for the LiPo  
- battery status display (e.g., on OLED / serial)  
- safe shutdown or servo power cut when voltage is too low  

---

## Hardware Used

- 1× 0–25V Voltage Sensor module  
  - Input terminals: **GND, VCC**  
  - Output pins: **S, +, −**
- ESP32 DevKitC (with pin **SP = GPIO36 = ADC1_CH0**)  
- Existing WAGO hubs:
  - **WAGO GND** (Ground Star Point + expansions)
  - **WAGO 3.3V** (logic rail)
  - **WAGO ACS712 OUT+** (positive node after fuse and current sensor)
- Dupont cables (female–female, female–to-bare)  
- AWG24 silicone wires (black and red)  
- Multimeter (continuity mode)

---

## 12.2 — Powering the Voltage Sensor Module

The module has three logic pins:

S + -


For cleaner integration and safety, the sensor is powered from the **3.3V rail**, not 5V.

### 12.2.1 — Sensor “−” pin → Ground (WAGO GND)

**Wiring:**

- A dupont female–to–bare (or female–to–male) was used.
- **Female** end → connected to the **“−”** pin of the voltage sensor.
- The other end → inserted into a **WAGO GND** slot (ground star / expansion).

**Test:**

- Multimeter (continuity): XT60 negative ↔ sensor “−” pin → **BEEP**  
✅ Sensor ground successfully tied to system ground.

---

### 12.2.2 — Sensor “+” pin → 3.3V (WAGO 3.3V)

**Wiring:**

- A dupont cable was used.
- **Female** end → connected to the **“+”** pin of the sensor.
- Other end → connected to the **WAGO 3.3V hub** (fed by ESP32 3.3V).

**Test:**

- XT60 GND ↔ sensor “+” → no beep (expected).  
- WAGO 3.3V ↔ sensor “+” → continuity confirmed (direct node).

✅ The voltage sensor logic is now powered cleanly at 3.3V.

---

## 12.3 — Sensor “S” Pin → ESP32 Analog Input (SP / GPIO36)

The sensor output **S** provides a scaled analog voltage proportional to the LiPo voltage.

**Target ESP32 pin:**

- **SP** (label on board) = **GPIO36 = ADC1_CH0**

**Wiring:**

- One dupont female–to–male was used.
- **Female** → connected to sensor pin **S**.
- **Male** → connected to **SP (GPIO36)** on the ESP32.

**Tests:**

- Continuity: S ↔ SP → **BEEP**  
  - Confirms a solid electrical connection between sensor and ADC input.
- SP ↔ 3.3V → **NO BEEP**  
- SP ↔ GND → **NO BEEP**

✅ The analog signal path is valid and isolated from power rails.

---

## 12.4 — Connecting Battery Voltage to the Sensor (High-Side Nodes)

The sensor has two **screw terminals** for the measured voltage:

[ GND ] [ VCC ]


This is where the **battery voltage (through the power path)** is sampled.

### 12.4.1 — Sensor Input GND Terminal → WAGO GND

**Wiring:**

- AWG24 black wire was prepared and stripped (~5–6 mm).
- One end inserted into the **GND screw terminal** of the sensor, screw tightened firmly.
- The other end inserted into **WAGO GND** (star ground / expansion).

**Test:**

- XT60 negative ↔ sensor GND terminal → **BEEP**

✅ Sensor ground reference matches system ground.

---

### 12.4.2 — Sensor Input VCC Terminal → ACS712 OUT+ Node

The voltage sensor must “see” the battery voltage **after** the fuse and current sensor:

XT60+ → Fuse → ACS712 IN+ → ACS712 OUT+ → [ LM2596 IN+, SZBK07 IN+, Voltage Sensor VCC ]


**Wiring:**

- AWG24 red wire was stripped and inserted into the **VCC screw terminal** of the sensor; screw fully tightened.
- The other end was inserted into a **WAGO node connected to ACS712 OUT+**, which already feeds:
  - LM2596 IN+  
  - SZBK07 IN+  
  - (and now) the Voltage Sensor VCC

**Test:**

- Continuity within the node (local WAGO ↔ sensor VCC terminal) verified.  
- XT60+ ↔ sensor VCC terminal is logically connected **through fuse + ACS712**, consistent with previous power path tests.

✅ The voltage sensor is now sampling the true LiPo voltage on the main positive rail.

---

## Current Status & Notes

- The **voltage sensor** is:
  - powered by **3.3V** (logic rail)
  - referenced to **Ground Star Point**
  - reading the **battery positive rail after ACS712 OUT+**
  - feeding its analog output into **ESP32 SP / GPIO36**

- The **ACS712 logic pins (VCC, OUT, GND)** will be wired in a later step; currently, only its power path (morsetti IN/OUT) is used.

- No shorts have been detected:
  - Sensor S is not shorted to 3.3V or GND  
  - Sensor VCC and GND correctly map into the battery path nodes  

---

## Final Result (Step 12)

| Check                                                   | Status |
|---------------------------------------------------------|--------|
| Sensor “−” tied to Ground Star Point                    | ✅     |
| Sensor “+” powered from 3.3V rail                       | ✅     |
| Sensor “S” connected to ESP32 SP / GPIO36               | ✅     |
| Sensor input GND wired to battery ground node           | ✅     |
| Sensor input VCC wired to ACS712 OUT+ node              | ✅     |
| No undesired shorts to 3.3V or GND on S / VCC           | ✅     |

The system is now ready for **ADC calibration in software** (mapping raw ADC values to real LiPo voltage) and for the next step: **ACS712 logic-side wiring (VCC, GND, OUT → GPIO34)**.

---

![IMG_0166](https://github.com/user-attachments/assets/bf693eaf-90a8-4b00-9bc1-f47e07559594)
