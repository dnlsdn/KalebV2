# Step 7 — PCA9685 Ground Integration + OE Enable

## Objective

Integrate the PCA9685 fully into the robot’s power and logic system by:

- Connecting its **ground** to the central Ground Star Point (WAGO)
- Connecting its **OE (Output Enable)** pin to **GND** to permanently enable PWM output

These steps ensure stable reference levels for the PWM driver and guarantee that all PWM channels are active when the PCA9685 receives commands.

---

## Materials

- PCA9685 module
- WAGO connector (Ground Star Point)
- Dupont female–female cables
- Dupont male–female cable (for OE → WAGO)
- Multimeter (continuity mode)

---

# L3 — PCA9685 GND → Ground Star Point

### Procedure

1. Identify the PCA9685 **GND** pin on the I²C header:
VCC — GND — SCL — SDA — OE — V+
2. Connect a **female–female dupont** to the PCA9685 GND pin.  
3. Insert a **male dupont** into an available slot on the WAGO star ground.  
4. Connect the female dupont to this male pin, completing the GND path.

### Test (continuity)

- Red probe → XT60 negative  
- Black probe → PCA9685 GND  

**Expected result:** 🔔 BEEP  
The PCA9685 now shares the same reference ground as the ESP32, LM2596, SZBK07, and ACS712.

---

# L6 — PCA9685 OE → Ground Star Point (Permanent Enable)

### Purpose

The PCA9685 OE pin is *active low*.  
- **OE = LOW (0V)** → PWM outputs ENABLED  
- **OE = HIGH or floating** → PWM outputs DISABLED  

Therefore, OE must be tied to **GND** for correct operation.

### Procedure

1. Locate the **OE** pin on the PCA9685:
VCC — GND — SCL — SDA — OE — V+
↑
this pin
2. Insert a **female dupont** onto the OE pin.  
3. Insert the **male end** of a male–female dupont into the WAGO star ground.  
4. Connect the two ends.

### Test (continuity)

- Red probe → XT60 negative  
- Black probe → OE pin (touch the metal inside the dupont)

**Expected:** 🔔 BEEP  
This confirms OE is correctly pulled LOW.

---

## Final Results

- PCA9685 is fully integrated into the robot’s shared ground system  
- OE is permanently enabled, activating all PWM outputs  
- I²C communications will operate correctly due to a stable ground reference  
- Module is now ready for servo power (V+) and for I²C scanning with the ESP32  

---

## Acceptance Criteria

| Check | Status |
|-------|--------|
| PCA9685 GND → WAGO continuity | **Pass** |
| PCA9685 OE → WAGO continuity | **Pass** |
| No short circuits on PCA9685 pins | **Pass** |
| Ground path stable and shared | **Pass** |

---

![IMG_0147](https://github.com/user-attachments/assets/1b07ac79-09f7-4d4f-ad5b-b0dc8fddfcd0)
