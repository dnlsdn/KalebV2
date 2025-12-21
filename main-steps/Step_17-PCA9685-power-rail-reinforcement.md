# Step 17 — PCA9685 Power Rail Reinforcement (V+ / GND)

## Objective

Improve the **electrical reliability and safety** of the PCA9685 servo power rail by upgrading the **V+ and GND connections** to properly handle the **high current demands** of 12× MG996R servos.

This step addresses early signs of **connector overheating** and ensures the servo rail can safely support peak loads during motion.

---

## Problem Identified

During initial power testing, the following issue was observed:

- PCA9685 **V+ and GND were connected using standard Dupont jumper wires**
- Under load, the Dupont connectors showed:
  - Increased temperature
  - Slight softening of the plastic housing
- This indicated **excessive current for the connector rating**

MG996R servos can draw **high peak currents**, especially when multiple servos move simultaneously.
Standard Dupont wiring is **not suitable** for this use case.

---

## Root Cause Analysis

- Dupont wires (≈ AWG26–28) are designed for **signal-level currents**
- Servo power rail requires:
  - High instantaneous current
  - Low resistance
  - Stable mechanical connection
- The PCA9685 board variant used features **only male header pins**, requiring an adaptation strategy

---

## Corrective Action Taken

### Power Distribution

- A **single WAGO connector** is used as the 6 V servo power distribution node
- Power path:
  - SZBK07 (6.0 V) → Relay → WAGO → PCA9685

### Cable Upgrade

- **AWG18 silicone wire** used for both:
  - V+ (6 V)
  - GND
- These wires carry the full servo current safely

### Dupont as Mechanical Interface Only

- Dupont female connectors are used **only at the PCA9685 header**
- Dupont wire length limited to **~2 cm**
- AWG18 wire is **soldered directly** to the shortened Dupont leads
- Heat-shrink tubing and strain relief applied

This ensures:
- Dupont connectors carry **negligible current**
- All high current flows through AWG18 conductors

---

## Safety Considerations

- V+ and GND upgraded **symmetrically**
- No high-current paths rely on friction-fit connectors
- Servo rail is fully controlled by the relay
- Power is never applied to servos during ESP32 boot

---

## Results

- No further heating observed on PCA9685 power connections
- Stable 6.0 V measured on V+ under load
- No voltage drop during relay activation
- Power distribution suitable for **12 MG996R servos**

---

## Interpretation

This maintenance step was **mandatory** to ensure long-term reliability.

Using Dupont wiring for servo power would have led to:
- Progressive connector degradation
- Voltage instability
- Potential damage to PCA9685 or servos

After reinforcement, the servo power rail is now:
- Electrically sound
- Mechanically robust
- Ready for full multi-servo testing

---

## Acceptance Criteria

| Check | Status |
|------|--------|
| AWG18 used for V+ and GND | Pass |
| Dupont limited to ≤ 2 cm | Pass |
| No connector heating | Pass |
| Stable 6.0 V under load | Pass |
| Relay-controlled power maintained | Pass |

---

<img width="504" height="631" alt="image" src="https://github.com/user-attachments/assets/3c5e80f6-1c5e-46cb-92de-8529854ecd31" />
