# Step 11.2 — Servo Relay Power Control (FULL Integration Report)

## Objective

Integrate the **5V relay module** that controls servo power delivery from the 6V regulator (SZBK07) to the PCA9685 servo rail.  
This relay allows the ESP32 to **enable/disable all servos in software**, preventing brownouts during boot and ensuring safe startup conditions.

This step covered:

- Relay **GND** connection to the Ground Star Point  
- Relay **VCC** connection to the 5V Logic Rail  
- Relay **IN** connection to ESP32 GPIO5  
- Full electrical validation through continuity tests

---

# R1 — Relay GND → Ground Star Point

### Procedure

1. A dupont **female–to–bare wire** was prepared (one end cut and stripped).
2. The female terminal was connected to the relay’s **GND** pin.
3. The stripped AWG24 wire was inserted into an **expanded WAGO GND hub**.
4. Mechanical retention was verified.

### Test (T1)

- XT60 negative ↔ relay GND → **BEEP**

### Result

Relay now shares the system-wide ground reference with:
- ESP32  
- PCA9685  
- MPU6050  
- LM2596  
- SZBK07  
- ACS712  

Ground integrity confirmed.

---

# R2 — Relay VCC → 5V Logic Rail (LM2596 Output → WAGO 5V)

### Procedure

1. A dupont **female–female** cable was used.
2. One end connected to the relay **VCC** pin.
3. The opposite end connected to the **WAGO 5V Logic hub**.

### Test (T2)

- Relay VCC ↔ WAGO 5V → **BEEP**

### Result

Relay coil receives a clean, regulated **5.00V** from the LM2596.  
This ensures reliable triggering and no false activations.

---

# R3 — Relay IN → ESP32 GPIO5

### Purpose

This connection allows software control.  
The relay module is **LOW LEVEL TRIGGER**, meaning:

- GPIO5 = LOW → relay ACTIVE → servos ON  
- GPIO5 = HIGH → relay INACTIVE → servos OFF  

### Procedure

1. A **dupont female–female** cable was used.
2. One female end connected to the relay **IN** pin.
3. The other female end connected to **GPIO5** on the ESP32.

### Tests

#### **T3 — Cable Continuity**
- Relay IN ↔ GPIO5 → **BEEP**  
Confirms electrical continuity of the control line.

#### **T4 — Isolation Check**
- IN ↔ relay GND → **NO BEEP**  
- IN ↔ relay VCC → **NO BEEP**

Ensures no unintended shorts.

### Result

The relay is now fully controllable from the ESP32 with a stable signal.

---

# Final Results (Step 11 Completed)

| Component | Status |
|----------|--------|
| Relay GND integrated into Ground Star | **OK** |
| Relay VCC powered from 5V Logic Rail | **OK** |
| Relay control (IN) connected to GPIO5 | **OK** |
| No shorts on relay control circuitry | **OK** |
| System ready to switch servo power safely | **OK** |

---

## Interpretation

The relay module is now fully installed in the power architecture.  
When the ESP32 boots or resets, servo power will remain **disabled**, preventing:

- sudden servo movement  
- high current spikes  
- PCA9685 bus brownouts  

Software can now safely enable servo power *after* system initialization.

---

![IMG_0165](https://github.com/user-attachments/assets/bc1fa498-f5d6-4188-965a-5fac1193939d)
