# Step 11.1 — Servo Power Switching Relay (6V Line) — Power Side Wiring

## Objective

Create the **high-current switching path** for the servo power rail using the relay module.  
This allows the ESP32 to **turn the 6V supply ON/OFF** for all 12 MG996R servos by toggling a single GPIO pin.

This step wires **only the power side** of the relay:

- SZBK07 6V output → COM (center)
- NO (normally open) → PCA9685 V+ (servo power rail)
- NC left unused

No logic wiring (VCC, GND, IN) is performed yet.

---

# Relay Terminal Identification

Using the multimeter:

- Terminals **2 ↔ 3** produced continuity → COM–NC pair  
- Terminal 1 had no continuity with the others → NO terminal  

Therefore:
Left terminal = NO
Center terminal = COM
Right terminal = NC

NC is unused for this build.

---

# Wiring Overview

SZBK07 OUT+ → COM (relay)
NO (relay) → PCA9685 V+ (6V servo rail)
NC → not used


GND is **not** switched; it remains connected in the Ground Star Point.

---

# 11.1.1 — SZBK07 OUT+ → Relay COM

### Procedure

1. Prepare AWG24 red wire (~10–12 cm).
2. Strip 5–6 mm.
3. Insert into **SZBK07 OUT+** terminal and tighten.
4. Strip the opposite end and insert into **COM (center)** terminal on relay.
5. Tighten firmly and pull to verify retention.

### Test P1 — Continuity
- SZBK07 OUT+ ↔ COM → **BEEP**  
✔ Connection verified.

---

# 11.1.2 — Relay NO → PCA9685 V+ (using Dupont adapter)

### Procedure

1. Cut a dupont **female–female** cable in half.
2. Keep the **female** side; discard or save the other.
3. Strip ~4–5 mm of wire on the cut end.
4. Insert stripped wire into **NO (left)** terminal of the relay.
5. Tighten firmly.
6. Plug the dupont **female connector** into the **PCA9685 V+** pin (servo power input).

### Test P2 — Continuity
- Relay NO ↔ PCA V+ → **BEEP**  
✔ Signal path correct.

---

# 11.1.3 — Relay Off-State Verification

### Test P3 — COM ↛ NO
- COM ↔ NO → **NO BEEP**  
✔ Relay contacts open (expected for normally-open configuration).

### Test P4 — NO ↛ GND
- NO ↔ GND → **NO BEEP**  
✔ No short to ground.

### Result

The relay is now properly inserted in series on the **positive 6V line** feeding the servos.

---

# Final Results

- Positive 6V rail routed through relay COM/NO
- PCA9685 V+ now receives power **only when relay is activated**
- No shorts detected between COM, NO, or GND
- All continuity tests successful
- System ready for **Step 11.2 — Logic-side relay wiring (VCC, GND, IN → GPIO5)**

---

# Acceptance Criteria

| Check                                         | Status |
|----------------------------------------------|--------|
| COM ↔ SZBK07 OUT+ continuity                 | Pass   |
| NO ↔ PCA V+ continuity                       | Pass   |
| COM ↛ NO with relay unpowered                | Pass   |
| NO ↛ GND                                      | Pass   |
| Wiring matches relay identification results   | Pass   |

---

![IMG_0164](https://github.com/user-attachments/assets/1cc49043-9514-4d2d-b792-b08c26589769)


