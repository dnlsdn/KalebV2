## STEP 1 — Pre-Alignment of MG996R Servos (0° / 90° / 180°) using Arduino UNO

### Objective

Pre-align each **MG996R** servo before mechanical installation to ensure correct joint orientation for SpotMicro.  
Using an **Arduino UNO** allows safe, isolated, single-servo calibration without powering the full servo rail or PCA9685.

Correct alignment prevents mechanical stress, reversed geometry, and servo grinding once assembled.

---

### Materials

- **Arduino UNO** + USB cable  
- **1× MG996R servo** (calibrate one at a time)  
- **3 jumper wires**  
- **Arduino IDE**  
- **Servo horn + screw**  
- (Optional) mini support/clamp for holding the servo

---

### Safety

- Power **only one servo at a time** from the UNO 5V regulator.  
- Do *not* rotate the horn manually while powered.  
- Disconnect immediately if buzzing or jitter persists.  
- Never exceed **5V** on the Arduino 5V pin.

---

### Procedure

1. Connect the servo:
   - **GND** (brown/black) → UNO **GND**
   - **VCC** (red) → UNO **5V**
   - **Signal** (yellow/orange) → UNO **D9**

2. Upload this sketch:

   ```cpp
   #include <Servo.h>

   Servo s;

   void setup() {
     s.attach(9);
     s.write(0);     // change to 0, 90, or 180
   }

   void loop() {}
   ```

3. Set the target angle:
   - `0°` → internal wrist servo  
   - `90°` → default hip/knee neutral  
   - `180°` → external wrist servo  

4. Upload the sketch → the servo moves to its reference position.

5. Install the horn:
   - align it mechanically  
   - insert the center screw  
   - tighten without preload torque

6. Repeat for all remaining MG996R servos.

---

### Results

- All servos reach **0° / 90° / 180°** smoothly.  
- Horns installed with symmetry and no residual tension.  
- Servos now have precise reference alignment before leg assembly.

---

### Interpretation

Using Arduino UNO is the safest method for initial calibration, avoiding risks associated with powering multiple servos through PCA9685 or external buck converters during early assembly.

---

### Issues Encountered & Fixes

- **Buzzing** → re-aligned horn and re-uploaded test angle.  
- **Off-center horn at 90°** → adjusted by 1–2 spline steps.  
- **Servo moving on table** → clamped or taped for stability.

---

### Acceptance Criteria

- Servo reaches reference angles without jitter → **Pass**  
- Horn installs without preload torque → **Pass**  
- Arduino 5V rail remains stable → **Pass**
