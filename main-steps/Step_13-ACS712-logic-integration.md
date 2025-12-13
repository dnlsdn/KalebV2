# Step 13 — ACS712 Logic Integration (Current Measurement)

## Objective

Integrate the **logic side of the ACS712 30A current sensor** into the Spot Micro ESP32 electronics in order to:

- power the ACS712 internal circuitry
- provide a stable ground reference
- route the analog current signal to the ESP32 ADC
- complete the battery monitoring subsystem (current + voltage)

After this step, the ESP32 is able to **measure battery current in real time**.

---

## Hardware Involved

- ACS712 30A current sensor module
- ESP32 DevKitC
- WAGO Ground Star hub
- WAGO 5V Logic hub (with expansion bridge)
- Dupont cables (female–male, female–bare)
- Multimeter (continuity / resistance mode)

---

## ACS712 Pinout (Logic Side)

VCC OUT GND

- **VCC** → logic power (5V)
- **OUT** → analog current signal
- **GND** → common ground reference

---

## 13.1 — ACS712 GND → Ground Star Point

### Procedure

The ACS712 **logic GND pin** was already connected to the **Ground Star WAGO** during the ground topology construction phase.

This ensures that:
- ACS712
- ESP32
- LM2596
- SZBK07
- all sensors

share the same electrical reference.

### Test

- XT60 negative ↔ ACS712 GND → **BEEP**

### Result

Ground reference for the ACS712 logic is stable and correct.

---

## 13.2 — ACS712 OUT → ESP32 GPIO34 (ADC1_CH6)

### Purpose

Route the analog output of the ACS712 to a suitable ESP32 ADC input.

### Selected ESP32 Pin

- **GPIO34**
  - ADC1 channel
  - input-only
  - ideal for analog sensors

### Procedure

1. A **female–male Dupont cable** was used.
2. Female end → ACS712 **OUT** pin.
3. Male end → ESP32 **GPIO34**.

### Tests

- ACS712 OUT ↔ ESP32 GPIO34 → **BEEP**
- OUT ↛ GND → **NO BEEP**
- OUT ↛ 5V → **NO BEEP**

### Result

The current signal path is correctly routed and electrically isolated.

---

## 13.3 — ACS712 VCC → 5V Logic Rail

### Purpose

Power the ACS712 internal circuitry using the regulated **5V logic rail**.

### Procedure

1. A cable was connected from ACS712 **VCC**.
2. The cable was inserted into the **WAGO 5V LOGIC hub**.
3. Due to limited space, a **WAGO expansion bridge** was used to extend the 5V rail.

Initial continuity issues were traced to **insufficient exposed conductor** in the cable.
After stripping additional insulation, proper metal contact was achieved.

### Tests

- WAGO 5V ↔ ACS712 VCC → **BEEP**
- VCC ↛ GND → **NO BEEP**
- OUT ↛ 5V → **NO BEEP**
- OUT ↛ GND → **NO BEEP**

### Result

The ACS712 is now correctly powered and electrically safe.

---

## Final Results — Step 13

After completing this step:

- ACS712 logic side is fully powered
- Ground reference is shared with the entire system
- Current signal is connected to ESP32 GPIO34
- No shorts detected between power, ground, and signal
- Battery current measurement is now available in software

---

## Acceptance Criteria

| Check | Status |
|------|--------|
| ACS712 GND → Ground Star | ✅ Pass |
| ACS712 VCC → 5V Logic | ✅ Pass |
| ACS712 OUT → GPIO34 | ✅ Pass |
| OUT isolated from GND | ✅ Pass |
| OUT isolated from 5V | ✅ Pass |
| No unintended shorts | ✅ Pass |

---

## System Status

The **battery monitoring subsystem is now complete**:

- Voltage → GPIO36 (SP)
- Current → GPIO34 (ACS712)

The robot is ready for:
- software ADC calibration
- low-voltage protection
- current monitoring
- next hardware steps (servo power relay, PCA9685 V+, WS2812, etc.)

---

![IMG_0218](https://github.com/user-attachments/assets/de3eeeb9-0aa5-4105-bd59-dc38b7ae94b5)
