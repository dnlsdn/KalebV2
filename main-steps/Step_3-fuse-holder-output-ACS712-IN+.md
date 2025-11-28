## Step 3 — Fuse Holder Output → ACS712 IN+ (Current Sensor Input Integration)

### Objective

Connect the **output of the inline fuse holder** to the **ACS712 current sensor IN+ terminal** using a safe and reliable method.  
This completes the first half of the robot’s main power chain:

XT60 → Fuse 10A → Fuse Holder → ACS712 (IN+) → (Next step: LM2596 & SZBK07)


Due to the thickness of the high-current wire (14 AWG), the ACS712 input terminal requires a thinner bridge wire. In this step, a **24 AWG silicone wire** is used as a safe, industry-standard adapter.

---

### Materials

- **Fuse Holder output wire** (14 AWG)
- **24 AWG silicone wire** (bridge wire)
- **ACS712 30A module** (screw terminals IN+ and OUT+)
- **Soldering iron + 60/40 solder**
- **Heat-shrink tubing**
- **Multimeter (continuity mode)**

---

### Safety

- Do NOT connect the LiPo battery at this stage.  
- Ensure all solder joints have cooled before touching.  
- Keep exposed wires away from metallic or conductive surfaces.  
- Check mechanically that the ACS712 terminal screws are tight.

---

### Procedure

#### **1. Prepare the Bridge Wire (24 AWG)**

Because the ACS712 terminal cannot accept thick 14 AWG wire, a 24 AWG bridge wire is used.

Steps:

1. Strip **4–5 mm** of insulation from both the 14 AWG wire and the 24 AWG wire.  
2. Pre-tin both wire ends with a thin coat of solder.  
3. Slide heat-shrink tubing onto the 14 AWG wire.

---

#### **2. Solder the 14 AWG → 24 AWG Bridge**

1. Align the pre-tinned ends tip-to-tip.  
2. Heat with the soldering iron until the solder melts and the two wires fuse.  
3. Add a minimal amount of solder for strength.  
4. Allow **5–10 seconds** for the joint to cool.  
5. Cover the joint with heat-shrink tubing and shrink it.

Result: a clean, compact, vibration-proof electrical bridge.

---

#### **3. Insert the 24 AWG Wire Into ACS712 IN+**

1. Loosen the screw terminal labeled **IN+** or **IP+**.  
2. Insert 5 mm of bare 24 AWG copper into the hole.  
3. Tighten the screw firmly.  
4. Pull slightly to verify the wire cannot be removed.

This completes the XT60 → Fuse → ACS712 path.

---

### Electrical Testing

Testing must be performed **before moving forward**.

Set the multimeter to continuity mode (buzzer symbol).

#### **Test 1 — Continuity (Should Beep)**

- Red probe → **XT60 + (positive) pin**  
- Black probe → **ACS712 IN+ terminal** (screw or metal pad)

**Expected:** the multimeter **beeps**  
→ This confirms the entire chain is electrically connected.

#### **Test 2 — No Short (Should NOT Beep)**  
(Performed earlier, but repeated here if needed)

- Red probe → **XT60 + pin**  
- Black probe → **XT60 – pin**

**Expected:** **NO beep**  
→ Confirms no accidental short circuit.

---

### Results

- The fuse holder output is now safely adapted to the ACS712 IN+ terminal.  
- The 24 AWG bridge wire is cleanly soldered and insulated.  
- The ACS712 terminal firmly grips the bridge wire.  
- All continuity tests passed.  
- The power chain is now ready for the next step: **ACS712 OUT+ → Voltage Regulators (LM2596 & SZBK07)**.

---

### Interpretation

This step completes the **input side** of the current monitoring system.  
The ACS712 will now accurately sense total current drawn by:

- servo rail (6V),  
- logic rail (5V),  
- and all attached sensors.

Using a 24 AWG bridge is standard practice in robotics and FPV drones when connecting thick battery wires to small measurement modules.

---

### Issues Encountered & Fixes

- **14 AWG wire too thick for ACS712 terminal** → solved using 24 AWG bridge.  
- **Wire not entering terminal** → ensured correct stripping length (4–5 mm).  
- **Weak solder joint** → reflowed with more heat for a shiny, solid finish.

---

### Acceptance Criteria

- 24 AWG firmly clamped in ACS712 IN+ → **Pass**  
- Bridge joint insulated and strain-free → **Pass**  
- XT60 → Fuse → ACS712 IN+ continuity beep → **Pass**  
- No short circuit across XT60 pins → **Pass**

---

![IMG_0098](https://github.com/user-attachments/assets/f00fb287-8899-427d-8963-bd328806e07d)
