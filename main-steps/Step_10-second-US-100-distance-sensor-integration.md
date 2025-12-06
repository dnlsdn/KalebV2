# Step 10 — Second US-100 Distance Sensor Integration (TRIG/ECHO with Safe Voltage Divider)

## Objective

Integrate the second US-100 ultrasonic distance sensor into the robot’s logic subsystem, using:

- shared 5V logic rail  
- shared Ground Star Point  
- dedicated TRIG pin (GPIO14)  
- protected ECHO input using a 2kΩ / 1kΩ voltage divider (5V → 3.3V)

This completes both ultrasonic sensors and ensures stable obstacle detection.

---

## Materials

- US-100 ultrasonic sensor  
- 1× 2kΩ resistor  
- 1× 1kΩ resistor  
- WAGO connectors (5V, GND, divider nodes)  
- ESP32 DevKitC  
- Dupont cables  
- Multimeter (continuity + ohms)

---

# L10.1 — Power Integration (5V + GND)

### Connections

- US-100 VCC → WAGO 5V logic  
- US-100 GND → WAGO Ground Star Point (via expansion WAGO)

### Tests

- **A2 — VCC continuity:** XT60+ ↔ US100 VCC → BEEP  
- **B2 — 5V rail verified:** WAGO 5V ↔ US100 VCC → BEEP  
- **C2 — GND continuity:** XT60− ↔ US100 GND → BEEP  

### Result

Sensor receives stable 5V and ground.

---

# L10.2 — TRIG2 → GPIO14

### Connections

- US-100 TRIG → GPIO14 (ESP32) via Dupont

### Tests

- **D2 — TRIG continuity:** TRIG ↔ GPIO14 → BEEP  
- **E2 — TRIG isolation:** TRIG ↛ GND → NO BEEP  

### Result

Trigger line connected and isolated.

---

# L10.3 — ECHO2 Voltage Divider (2kΩ / 1kΩ → GPIO27)

The US100's ECHO pin outputs 5V, so a divider is required to step it down to 3.3V.

---

## Divider Architecture

ECHO2 → 2kΩ → NODE A → GPIO27
|
1kΩ
|
GND

---


- **NODE A (WAGO4):** ECHO2, GPIO27, upper leg of 2kΩ  
- **NODE B (WAGO5):** lower leg of 2kΩ + upper leg of 1kΩ  
- **GND (WAGO3):** lower leg of 1kΩ  

---

# Sub-Steps

## L10.3.1 — ECHO2 → Node A
- ECHO2 → WAGO4  
- 2kΩ (leg 1) → WAGO4  

## L10.3.2 — GPIO27 → Node A
- GPIO27 → WAGO4  

## L10.3.3 — Bridge Node A → Node B
- 2kΩ (leg 2) → WAGO5  
- 1kΩ (leg 1) → WAGO5  

## L10.3.4 — Ground Leg
- 1kΩ (leg 2) → WAGO3 (GND expansion)

---

# Final Electrical Tests

## F2 — Echo Path OK
2kΩ (Node A) ↔ ECHO2 → **BEEP**

## G2 — Node A Not Grounded
Node A ↛ GND → **NO BEEP**

## H2 — Divider Resistance
Measure between free legs of 2kΩ and 1kΩ → **≈3kΩ**

## I2 — GPIO Isolation
GPIO27 ↛ GND → **NO BEEP**

## L2-A — Node A ↛ 5V
NO BEEP

## L2-B — Node A ↛ 3.3V
NO BEEP

---

## Final Results

- Second US-100 fully integrated  
- Safe 5V → 3.3V conversion on ECHO2  
- TRIG2 isolated and functional  
- VCC and GND correctly connected  
- No short circuits detected  
- Wiring is symmetric to Sensor #1  
- System ready for relay + servo power distribution (Step 11)

---

## Acceptance Criteria

| Check | Status |
|-------|--------|
| Power rails correct | Pass |
| TRIG2 → GPIO14 OK | Pass |
| 2kΩ/1kΩ divider correct | Pass |
| All continuity tests passed | Pass |
| No shorts to 3.3V/5V/GND | Pass |
| Architecture matches sensor #1 | Pass |

---

![IMG_0158](https://github.com/user-attachments/assets/5e2ca30c-e452-4df4-be2b-5c8f9d5ea551)
