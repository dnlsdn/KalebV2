## Step 5 — Ground Star Topology (GND) Construction

### Objective

Create a **single, unified ground reference** for the entire robot using a WAGO connector as the **Punto Stella GND** (“Ground Star Point”).

This ensures that:

- all power modules share the same electrical ground  
- all logic modules (ESP32, PCA9685, MPU6050, sensors) have a stable reference  
- noise from servos does **not** interfere with the logic  
- current measurements from ACS712 remain accurate  
- the system is protected from floating grounds and dangerous voltage offsets  

This is one of the most critical wiring steps in the SpotMicro.

---

### Materials

- WAGO 5-pole connector (star topology hub)
- XT60 connector (battery)
- SZBK07 buck converter (6V for servos)
- LM2596 buck converter (5V for logic)
- ACS712 current sensor (with 3 logic pins)
- 24 AWG silicone wire (black)
- Soldering iron + solder (for LM2596 GND pin)
- Multimeter (continuity test)

---

### Safety

- **Do NOT connect the LiPo battery yet.**
- Double-check each ground wire before inserting into WAGO.
- No exposed copper should be visible outside the WAGO.
- Always verify continuity after each sub-step.
- Incorrect grounds can cause brownouts, servo resets, or destroyed modules.

---

### Procedure

The Ground Star Point is built gradually using four micro-steps:

- **G1:** XT60 Negative → WAGO  
- **G2:** SZBK07 IN− → WAGO  
- **G3:** LM2596 IN− → WAGO  
- **G4:** ACS712 GND (logic pin) → WAGO  

Each step includes a continuity check.

---

## **G1 — XT60 Negative → WAGO (Ground Root)**

1. Strip 8–10 mm of the XT60 **black wire**.  
2. Open one WAGO slot and insert the wire fully.  
3. Close the lever and pull gently to confirm retention.

**Test:**  
- Red probe → XT60 negative metal  
- Black probe → same wire (before WAGO)  
→ **BEEP** (expected)

**Result:** Established the root ground for the entire robot.

---

## **G2 — SZBK07 IN− → WAGO**

1. Prepare a 10–12 cm AWG24 black wire.  
2. Strip 5 mm and insert into SZBK07 **IN−** terminal.  
3. Strip 8–10 mm on the other end and insert into a second WAGO slot.

**Test:**  
- Red probe → XT60 negative  
- Black probe → metal part of SZBK07 IN−  
→ **BEEP**

**Result:** Servo regulator now shares the same stable ground.

---

## **G3 — LM2596 IN− → WAGO**

1. Strip and pre-tin a short AWG24 black wire.  
2. Solder the wire to **LM2596 IN−** pin.  
3. Insert the other end into the WAGO third slot.

**Test:**  
- Red probe → XT60 negative  
- Black probe → LM2596 IN−  
→ **BEEP**

**Result:** Logic regulator (5V rail) now shares the same ground.

---

## **G4 — ACS712 GND (logic pin) → WAGO**

1. Locate the **GND pin** among the three logic pins:

[VCC] [OUT] [GND]
↑ this one

2. Strip + pre-tin an AWG24 black wire.  
3. Solder to the ACS712 **GND** pin.  
4. Insert the other end into the WAGO fourth slot.

**Test:**  
- Red probe → XT60 negative  
- Black probe → ACS712 GND pin  
→ **BEEP**

**Result:** Current sensor logic reference aligned with the system ground.

---

### Results

- All ground paths (battery, 6V regulator, 5V regulator, sensors) converge into a **single star point**.  
- The system ground is now stable, clean, and electrically correct.  
- ACS712 will provide accurate readings thanks to shared reference.  
- LM2596 and SZBK07 regulators now operate with a safe common reference.  
- Robot ready for **Step 7 — GND distribution to logic modules (ESP32, PCA9685, sensors, ESP32-CAM)**.

---

### Interpretation

This step ensures electrical safety and signal stability across the entire robot:  
servo noise cannot corrupt sensor readings, and voltage references remain coherent.

A star ground is **mandatory** for multi-rail systems like SpotMicro.

---

### Acceptance Criteria

- XT60 negative locked into WAGO → **Pass**  
- SZBK07 IN− locked → **Pass**  
- LM2596 IN− soldered + locked → **Pass**  
- ACS712 GND soldered + locked → **Pass**  
- All continuity tests beep → **Pass**  
- No shorts across XT60 (+/−) → **Pass**

System ready for next steps.

---

![IMG_0102](https://github.com/user-attachments/assets/d24fb1ea-6873-4613-9735-118674f8a2dc)

