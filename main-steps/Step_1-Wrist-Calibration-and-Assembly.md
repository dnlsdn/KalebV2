## STEP 1 — Wrist Servo Calibration (0° / 180°) and Mechanical Assembly

### Objective

Calibrate and mount the **four wrist servos** used in the SpotMicro robot, following the structure from the official guide by *michaelkubina*.  
This step covers:

- Setting **2 servos to 0°** and **2 servos to 180°** using Arduino code.  
- Assigning each wrist to the correct orientation:  
  - **Front Left → 0°**  
  - **Rear Left → 0°**  
  - **Front Right → 180°**  
  - **Rear Right → 180°**  
- Fully assembling the four wrist modules according to the official assembly instructions.

Correct calibration ensures symmetrical behavior and prevents misalignment during later leg assembly.

---

### Materials

From the official *Wrist* section of the guide:

- **4× MG996R Servo** (2 at 0°, 2 at 180°)
- **16× Servo rubber dampeners**
- **4× Wrist** (2 right‑handed, 2 left‑handed)
- **4× Wrist counterpiece** (2 right‑handed, 2 left‑handed)
- **4× Shoulder Joint Ball Bearing Pin**
- **4× Foot Tip**
- **24× M3 nuts**
- **16× M3×20 screws**
- **8× M3×8 screws**
- **4× M2 nuts**
- **4× M2×8 screws**
- **Arduino UNO + USB cable** (for calibration)

---

### Safety

- Calibrate **only one servo at a time** from the Arduino 5V pin.  
- Do not rotate a powered servo by hand.  
- Ensure correct left/right orientation before tightening screws.  
- Keep M3 nuts seated in their slots during assembly—they fall out easily.  
- Do not overtighten the wrist bearing pin: the wrist must rotate smoothly.

---

### Procedure

#### **1. Servo Calibration (Arduino UNO)**

Using the standard Arduino `Servo.h` library:

```cpp
#include <Servo.h>

Servo s;

void setup() {
  s.attach(9);
  s.write(0);     // change to 0 or 180 depending on the wrist
}

void loop() {}
```

Calibrate each servo according to the selected orientation:

- **Front Left  → 0°**  
- **Rear Left   → 0°**  
- **Front Right → 180°**  
- **Rear Right  → 180°**

Attach the horn only when the servo reaches the programmed position and stops moving.

---

#### **2. Foot Tip Installation**

From the guide:

- Insert **2× M3 nuts** into the wrist.
- Position the foot tip at the bottom.
- Secure using **2× M3×8 screws**.

---

#### **3. Wrist Counterpiece + Bearing Pin**

- Insert **1× M2 nut** into the wrist counterpiece.
- Pass **1× M2×8 screw** through the bearing pin.
- Tighten to secure the pin to the counterpiece.

---

#### **4. Wrist Assembly (“Wrist Sandwich”)**

- Insert **4× M3 nuts** into the wrist counterpiece.
- Insert the calibrated servo into the wrist counterpiece slot.
- Align the wrist and wrist counterpiece.  
- Close the assembly while keeping all nuts in place.
- Fasten with **4× M3×20 screws**.

Repeat the entire process for:

- Front Left Wrist  
- Rear Left Wrist  
- Front Right Wrist  
- Rear Right Wrist  

---

### Results

- All four wrist modules assembled and functional.  
- Servos are correctly aligned to **0° or 180°** based on side.  
- Foot tips securely mounted.  
- Bearing pins rotate smoothly without friction.  
- Wrist shells properly mirrored (LHS vs RHS).

---

### Interpretation

This step completes the **entire lower leg wrist section**, providing stable and symmetric wrist joints ready for later tibia and femur installation.  
Correct servo alignment here prevents significant mechanical and software issues later in the build.

---

### Issues Encountered & Fixes

- **Misaligned horn** → recalibrated servo, repositioned horn.  
- **M3 nuts falling out** → held in place with tweezers during closing.  
- **Wrist mirrored incorrectly** → laid out left/right parts before assembly.

---

### Acceptance Criteria

- All four wrists assembled identically per side → **Pass**  
- Correct servo orientation assignment (0° left, 180° right) → **Pass**  
- Bearing pins smooth and wrist structure rigid → **Pass**  
- Servos centered without jitter → **Pass**
