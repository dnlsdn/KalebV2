## Step 5 — ACS712 OUT+ → LM2596 (5V) & SZBK07 (6V) Input Power Distribution

### Objective

Distribute the **positive power line** coming from the ACS712 OUT+ terminal to the **two voltage regulators**:

- **LM2596** → 5V rail (logic: ESP32, camera, sensors, PCA9685 VCC)
- **SZBK07** → 6V rail (servos MG996R)

This step completes the *positive* side of the robot’s power architecture.

XT60 → Fuse → ACS712 IN+ → ACS712 OUT+ → LM2596 (IN+)
↳ SZBK07 (IN+)


---

### Materials

- ACS712 (already connected on IN+)
- 2× 24 AWG silicone wires (bridge wires from ACS712 OUT+)
- LM2596 buck converter (5V)
- SZBK07 buck converter (6V)
- Soldering iron + solder (for LM2596 pin IN+)
- Screwdriver (for SZBK07 terminal block)
- Heat-shrink tubing (optional for strain relief)
- Multimeter (continuity test)

---

### Safety

- Do **NOT** connect the LiPo battery at this stage.
- Ensure the ACS712 OUT+ terminal is tightened securely.
- The LM2596 pin headers must be insulated from touching metal.
- Always perform continuity tests before powering anything.

---

### Procedure

#### **1. Prepare Two 24 AWG Wires**

Cut two wires (10–12 cm each):

- Wire A → for LM2596 IN+
- Wire B → for SZBK07 IN+

Strip **5 mm** of insulation on both ends.

---

#### **2. Insert Both Wires Into ACS712 OUT+**

1. Loosen the screw terminal **OUT+** on the ACS712.
2. Insert **both 24 AWG wires in parallel** into the same hole.
3. Tighten the screw firmly.
4. Pull gently to verify they are secure.

This creates a clean “Y” power split.

---

#### **3. Connect Wire A → LM2596 IN+**

The LM2596 module in use has **male header pins**, not screw terminals.

Pin layout:

[ IN+ ] [ IN- ] [ OUT+ ] [ OUT- ]


Steps:

1. Pre-tin the **IN+** pin with a drop of solder.
2. Pre-tin the stripped tip of Wire A.
3. Place the wire against the IN+ pin.
4. Heat for 1–2 seconds until solder flows.
5. Hold still 5 seconds to solidify.

Result: a strong, vibration-resistant solder joint.

---

#### **4. Connect Wire B → SZBK07 IN+**

Your SZBK07 has a **4-terminal block**:

IN+ IN- OUT+ OUT-


Steps:

1. Loosen the **IN+** terminal screw.
2. Insert Wire B (stripped 5 mm) into the metal hole.
3. Tighten firmly.
4. Pull gently to verify retention.

This completes the positive input path for the 6V servo regulator.

---

### Electrical Testing (Critical)

Set multimeter to **continuity mode (buzzer)**.

#### **Test A — LM2596 Input**

- Red probe → XT60 positive pin  
- Black probe → LM2596 **IN+** pin  

**Expected:** 🔔 **BEEP**  
→ Positive power successfully flows from XT60 → ACS712 → LM2596.

#### **Test B — SZBK07 Input**

- Red probe → XT60 positive pin  
- Black probe → SZBK07 **IN+** terminal  

**Expected:** 🔔 **BEEP**  
→ Positive power successfully flows from XT60 → ACS712 → SZBK07.

---

### Results

- ACS712 OUT+ now cleanly splits into two regulated power rails.
- LM2596 IN+ solder joint secure and electrically verified.
- SZBK07 IN+ terminal firmly tightened.
- Both continuity tests passed successfully.
- System ready for **Step 6 — Ground (GND) Star Topology Construction**.

---

### Interpretation

This step completes the **positive distribution network** for the robot.  
All power to the logic rail (5V) and servo rail (6V) now passes through:

- The fuse (safety)  
- The ACS712 (current measurement)  

This ensures safe operation, accurate current monitoring, and consistent behavior across all modules.

---

### Acceptance Criteria

- Both 24 AWG wires firmly clamped/soldered → **Pass**
- Buzzer test from XT60+ to LM2596 IN+ → **Pass**
- Buzzer test from XT60+ to SZBK07 IN+ → **Pass**
- No short circuit across XT60 pins → **Pass**

---

![IMG_0100](https://github.com/user-attachments/assets/83e88cac-34a6-491b-b63f-3e21f0521a87)
