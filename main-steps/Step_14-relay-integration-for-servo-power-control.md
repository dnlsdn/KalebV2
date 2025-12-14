# Step 14 — Relay Integration for Servo Power Control (6V Rail)

## Objective

Integrate a **5V relay module** to safely control the **6V power line** feeding the PCA9685 servo rail (V+).

This step enables:

- Software-controlled ON/OFF of all servos
- Protection of the ESP32 from servo inrush currents
- Safe startup and shutdown sequences
- Future emergency stop and power-cycling logic

At the end of this step, the servo power line is fully controllable but still safely disconnected from the servos.

---

## Materials

- Relay module (SRD-05VDC-SL-C, low-level trigger)
- ESP32 DevKitC
- SZBK07 buck converter (6V)
- PCA9685 PWM driver
- WAGO connectors (5V logic, GND star)
- Dupont cables
- 24 AWG silicone wire
- Multimeter (continuity test)

---

## Safety

- LiPo battery **disconnected at all times**
- No servos connected to PCA9685 V+
- All tests performed with multimeter and logic power only
- GND always connected before any power line

---

## Step 14.1 — Relay Logic Wiring

### Connections

- **Relay VCC → WAGO 5V LOGIC**
- **Relay GND → Ground Star (WAGO)**
- **Relay IN → ESP32 GPIO5**

### Notes

- Relay is **low-level triggered**
- GPIO LOW → relay ON
- GPIO HIGH → relay OFF

---

## Step 14.2 — Relay Logic Test (No Load)

### Observations

- Audible click when toggling relay state
- Red LED always ON (5V power present)
- Green LED changes brightness/state with relay activation

### Interpretation

- ESP32 GPIO control works correctly
- Relay logic and power are stable
- Module behavior matches low-level trigger design

---

## Step 14.3 — Relay Integration in 6V Servo Power Line

### Wiring

- **SZBK07 OUT+ (6V) → COM terminal of relay**
- **Relay NO terminal → PCA9685 V+**
- **Relay NC terminal → not used**

### Functional Meaning

- Relay OFF → no 6V reaches PCA9685 → servos OFF
- Relay ON → 6V reaches PCA9685 → servos ON

---

## Electrical Tests

### Test R1 — Relay OFF

- Red probe → SZBK07 OUT+
- Black probe → PCA9685 V+

**Result:** No continuity (no beep)  
→ Servo power correctly disconnected

### Test R2 — Relay ON

- Red probe → SZBK07 OUT+
- Black probe → PCA9685 V+

**Result:** Continuity present (beep)  
→ Servo power correctly delivered

---

## Results

- Relay correctly switches the 6V servo rail
- ESP32 fully controls servo power state
- PCA9685 V+ line is isolated when relay is OFF
- No servos connected yet (intentional and correct)
- Entire power architecture behaves as designed

---

## Interpretation

This step completes the **power safety layer** of the Spot Micro ESP32.

The robot can now:
- Boot safely without servo load
- Enable servos only when firmware is ready
- Avoid brown-outs and current spikes
- Implement emergency stop logic in software

---

## Acceptance Criteria

| Check | Status |
|------|-------|
| Relay logic control (GPIO5) | Pass |
| Relay click + LED behavior | Pass |
| 6V disconnected when OFF | Pass |
| 6V connected when ON | Pass |
| PCA9685 V+ isolated (no servos) | Pass |
| LiPo kept disconnected | Pass |

---

**System ready for servo integration or firmware testing.**

---

![IMG_0222](https://github.com/user-attachments/assets/d22656ae-ff52-4024-948d-b1e39369f301)
