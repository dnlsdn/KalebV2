## Step 2 — XT60 Positive Lead → Fuse Holder Integration (Power Safety Line)

### Objective

Integrate the **XT60 positive lead** with the **ATC/ATO fuse holder** to create a protected high-current power line for the SpotMicro robot.  
This step establishes the first part of the main power chain:

LiPo 2S → XT60 → 10A Fuse → ACS712 → Regulators (5V / 6V)


Correct installation of the inline fuse ensures that the robot, servo lines, and regulators remain protected against short circuits or overload events.

---

### Materials

For this step:

- **XT60 Male connector** (pre-wired, 14AWG silicone wire)
- **ATC/ATO Inline Fuse Holder** (pre-wired loop type)
- **ATC 10A Fuse**
- **Silicone 14–16 AWG wire** (already included in holder)
- **Soldering iron (60–80W)**
- **Sn60Pb40 or Sn63Pb37 solder with flux core**
- **Heat-shrink tubing (Ø 3–5 mm)**
- **Multimeter (continuity mode)**

---

### Safety

- **Do NOT connect the LiPo** during this step.  
- Ensure the XT60 metal contacts do NOT touch conductive surfaces.  
- Work on a non-conductive mat (as shown in the build).  
- Allow solder joints to cool completely before testing.  
- Install the fuse **before** continuity testing.

---

### Procedure

#### **1. Prepare the Fuse Holder**

1. Take the pre-wired ATC/ATO fuse holder loop.  
2. Cut the loop exactly in half to create two independent wire ends.  
3. Insert the **10A fuse** into the fuse holder and close the cap.

This converts the holder into a ready inline component.

---

#### **2. Prepare the XT60 Positive Lead**

1. Identify the **red 14AWG wire** from the XT60 connector.  
2. Strip **5–6 mm** of insulation from its exposed end.  
3. Slide **2–3 cm of heat-shrink tubing** onto the XT60 wire (do NOT forget this).

---

#### **3. Pre-Tin Both Wires**

Pre-tinning improves soldering quality, especially on thick silicone cables.

1. Slightly open the strands of both wires (XT60 red and fuse-holder red).  
2. Heat the copper directly with the iron.  
3. Apply solder to the opposite side until the wire turns **fully silver** and becomes rigid.

Result: both wires become pre-tinned and mechanically stable.

---

#### **4. Solder the XT60 → Fuse Holder Joint**

1. Align the two pre-tinned wire ends **tip-to-tip**.  
2. Hold the wires with a “third hand” or pliers.  
3. Heat the junction with the iron until the tin liquefies.  
4. Add a small amount of solder to merge the two parts.  
5. Hold still for at least **5–10 seconds** while it cools.

A correct joint should be:

- smooth  
- silver and shiny  
- rigid  
- free of cracks or bumps

---

#### **5. Heat-Shrink Insulation**

1. Slide the heat-shrink tubing over the solder joint.  
2. Shrink it with hot air or indirect heat from the soldering iron.  
3. Confirm that no bare metal is visible.

This creates a vibration-proof and insulated connection.

---

### Electrical Testing

Both tests must be performed **with the fuse installed**.

#### **Test 1 — Continuity**

- Multimeter → continuity mode (buzzer symbol)
- Red probe → **XT60 + (positive) pin**
- Black probe → **free end of fuse holder wire**

**Expected:** multimeter should **beep**  
→ This confirms a complete electrical path from XT60 → solder → fuse holder → fuse → output.

#### **Test 2 — Short Circuit Check**

- Red probe → **XT60 + pin**
- Black probe → **XT60 – pin**

**Expected:** **NO beep**  
→ Confirms there is no accidental short between positive and ground.

---

### Results

- The XT60 red lead is correctly and permanently joined to the fuse holder.  
- The solder joint is solid, insulated, and mechanically secure.  
- Electrical continuity validated (fuse included).  
- No short detected between XT60 + and – pins.  
- The power safety line is now ready for integration with the **ACS712 current sensor**.

---

### Interpretation

This step completes the **high-current protection segment** of the robot’s power architecture.  
The fuse now ensures the following:

- Servos cannot draw excessive current without tripping protection  
- A wiring fault or regulator failure will blow the fuse, protecting the LiPo  
- The robot’s entire 6V and 5V rails are shielded from catastrophic damage

This foundation is mandatory before proceeding to current sensing and voltage regulation.

---

### Issues Encountered & Fixes

- **Cold solder joint** → reheated until shiny and fused uniformly.  
- **Heat-shrink forgotten** → re-soldered joint after sliding tubing in place.  
- **No continuity** → fuse was not inserted; re-tested successfully afterward.

---

### Acceptance Criteria

- Inline fuse holder installed between XT60 + and downstream power rail → **Pass**  
- 10A fuse inserted and functioning → **Pass**  
- Solder joint meets mechanical and electrical standards → **Pass**  
- Multimeter tests passed with correct beep/no-beep behavior → **Pass**

---

![IMG_0096](https://github.com/user-attachments/assets/a593a477-dca3-4998-a890-f0809bd0f338)
