# Current Power & Wiring Connections

The wiring as it physically is, not as it is meant to end up. The power path was measured on
2026-07-31 in session 2; the I2C bus was built and verified on 2026-08-14 in session 4; the 6V servo
rail was built and measured on 2026-08-27 in session 5; the relay was removed on 2026-09-19 in
session 6; the bus bars were replaced by WAGOs on 2026-11-01 in session 20. Everything marked not wired
is planned but does not exist yet.

All grounds go to three WAGO 221-415 chained together, the ground star: **A** takes every heavy ground,
**B** and **C** the logic ones. All 5V logic goes to a fourth, **D**. The 3.3V logic and the two I2C lines
pass through the PCA9685's two 6-pin headers, which are joined pin for pin on the board.

**Session 20 found two errors in this file.** The LM2596's and the SZBK07's OUT− were listed on the black
bus bar as "Verified"; neither has a wire. Every row below was re-checked wire by wire while the bars came
out.

---

## Power path

| From | To | State |
|---|---|---|
| LiPo 2S negative | WAGO A | Verified, session 20 |
| LiPo 2S positive | 10A fuse | Verified, 7.55V after the fuse |
| Fuse output | ACS712 terminal | Verified |
| ACS712 terminal | LM2596 IN+ and SZBK07 IN+, split with a WAGO | Verified |
| SZBK07 IN− | WAGO A | Verified, session 20 |
| LM2596 IN− | WAGO B | Verified, session 20 |

AWG14 on the whole power path.

---

## LM2596 — 5V logic step-down

| Pin | Connected to | State |
|---|---|---|
| OUT+ | WAGO D | Verified, 4.95V at WAGO D under the logic load, session 20 |
| OUT− | **no wire** | Found in session 20. Input and output share ground on this module, so the logic return comes back through IN− |

Trimmed to 5.00V with no load in session 1. It reads 4.98V once the logic is drawing current, which
is normal and was left alone.

---

## SZBK07 — 6V servo step-down

| Pin | Connected to | State |
|---|---|---|
| OUT+ | Servo rail WAGO, AWG14 | Verified, 6.01V at the servo rail WAGO with the pack connected, session 20 |
| OUT− | **no wire** | Found in session 20. Input and output share ground, so the servo return comes back through IN− |

**The two metal side bars of this module are electrically live**, at the same potential as the
positive input, so around 7.5V with the pack connected. They are the heatsink and the power
transistor tab is bolted to them. Verified: they beep against the positive input and stay silent
against ground.

Nothing at ground potential may touch them, no metal tool near them while powered, and the module
cannot be mounted on a conductive surface. Its mounting screws are live.

---

## Servo rail — PCA9685

Built in session 5, relay removed in session 6. **The rail is live whenever the pack is connected**:
there is no relay and no software control of the servo power, as in Leika.

| From | To | State |
|---|---|---|
| SZBK07 OUT+ | Servo rail WAGO 221-412, AWG14 | Verified |
| Servo rail WAGO | PCA9685 V+, green screw terminal, **AWG16** | Verified, 6.0V with the pack connected |
| PCA9685 GND, green screw terminal | WAGO A, **AWG16** | Verified, session 20 |

**The relay is gone.** Its IN pin was the base of a PNP transistor with its emitter on VCC, so it
stayed open only above about 4.2V, which no ESP32 pin reaches (3.1V measured driven high). This is
the blue low-level-trigger variant of the module; the reference projects use a KY-019 / HW-482, which
has an NPN input and is driven directly at 3.3V. Session 5 has the measurements. In session 6 the two
power wires that met at its COM and NO screws were joined in a WAGO 221-412, stripped to 11mm and
tug-tested, and the module left the bench with its three Dupont.

**AWG16 and not AWG14 to the PCA9685, by necessity.** Its green 2-pole terminal is a 3.5mm block
rated to 1.5mm²; AWG14 at 2.08mm² does not fit it by design. The narrowest point of this path is not
the wire but the PCA9685's own V+ traces, which are on the backlog to be reinforced with solder.

**The ground return is AWG16 from the screw terminal**, added in session 5 in place of a Dupont sized
for logic current.

**No external capacitor.** This PCA9685 carries a **1000µF 10V** on the servo rail already, verified
by continuity. A spare 1000µF 16V is in the drawer, to be fitted on the SZBK07 output if the rail
ever collapses on peaks.

Verified in session 6, no servo attached:

| Measurement | Reading |
|---|---|
| PCA9685 V+ ↔ black bus bar, pack connected | 6.0V |
| PCA9685 V+ ↔ black bus bar, XT60 unplugged | 0V, over a few seconds |
| SZBK07 OUT+ ↔ PCA9685 V+, continuity | yes |
| PCA9685 V+ ↔ black bus bar, continuity | no, after the capacitor's charging beep |

---

## ESP32 — replaced in session 17

The board was lost in session 16 (`main-steps/16-resets.md`). The replacement, an ESP-WROOM-32 with a
CP2102 and 30 pins, went on in session 17 with the same five Duponts:

| Wire | From | ESP32 pin |
|---|---|---|
| red | WAGO D, 5V | VIN (5V) |
| black | WAGO B | GND |
| new F-F Dupont | PCA9685 header 1, VCC | 3V3 |
| new F-F Dupont | PCA9685 header 1, SDA | D21 (GPIO21) |
| new F-F Dupont | PCA9685 header 1, SCL | D22 (GPIO22) |

Since session 20 the ESP32's 3V3, D21 and D22 go straight to the PCA9685 on female-female Duponts.

Both reds were checked by resistance before power, unpowered: red bus bar to VIN and 3.3V WAGO to 3V3
near 0 ohm. They are the only pair that can be swapped, and swapped they put 5V on the IMU.

---

## WAGO D — 5V logic

A WAGO 221-415, all five ports used. Each wire checked by continuity in session 20; 4.95V with the pack in.

| Board | Pin |
|---|---|
| LM2596 | OUT+ (the feed) |
| ESP32 | VIN |
| ACS712 | VCC |
| HC-SR04 #1 | VCC |
| HC-SR04 #2 | VCC |

**This node is live whenever the ESP32 is plugged into USB, even with the battery disconnected.**
USB power back-feeds out of the VIN pin. Measured 4.93V in session 4, so this board has no meaningful
diode drop on that path. "Battery disconnected" does not mean "nothing is powered".

---

## 3.3V and I2C — through the PCA9685

The PCA9685 has a 6-pin header on each end, GND, OE, SCL, SDA, VCC, V+, and the two are joined pin for
pin on the board: checked by continuity in session 20, all six pairs. So the board distributes 3.3V and
the I2C bus itself.

| Header | Pin | Connected to |
|---|---|---|
| 1 | VCC | ESP32 3V3 |
| 1 | SDA | ESP32 GPIO21 |
| 1 | SCL | ESP32 GPIO22 |
| 1 | OE | jumper to GND on the same header |
| 1 | GND | jumper from OE |
| 1, 2 | V+ | **nothing**: it carries the 6V servo rail |
| 2 | VCC, SDA, SCL | MPU6050 VCC, SDA, SCL |
| 2 | GND, OE | free |

Addresses: **PCA9685 at 0x40, MPU6050 at 0x68**, confirmed again on a cold power-on in session 20.

**The PCA9685 is on 3.3V and not on 5V for a reason.** Its SDA and SCL pull-up resistors go to VCC —
measured 9.96kΩ on both lines in session 4 — so VCC sets the idle voltage of the whole I2C bus. With VCC
at 5V, SDA and SCL would idle at 5V and sit above the ESP32's 3.6V absolute maximum.

**OE is active-low.** If it floats high all sixteen PWM outputs are disabled, which looks exactly like a
firmware bug and is not one. Checked in session 20: OE to GND beeps, SCL to GND does not.

---

## WAGOs A, B, C — ground star

Three WAGO 221-415 chained by two short offcuts of power wire. All the heavy grounds share A, so the
battery and servo current never crosses a link.

| WAGO | Ports |
|---|---|
| A | LiPo −, SZBK07 IN−, PCA9685 GND (AWG16), link to B, **one free** |
| B | link from A, LM2596 IN−, ESP32 GND, link to C, **one free** |
| C | link from B, MPU6050 GND, ACS712 GND, HC-SR04 #1 GND, HC-SR04 #2 GND |

Verified in session 20, unpowered: A to C and ESP32 GND to A beep; 5V, 3.3V and 6V to ground read
kilohms rising, no short. The bus bars are off the bench and kept.

**WAGO 221 connectors are specified from 0.14mm² up, and Dupont wire is around 0.08mm².** It is below
the minimum and the lever does not always grip it: in session 4 an SDA wire sat in a WAGO without
contact. Strip longer, fold the conductor back on itself before inserting, then tug-test every wire.
Any WAGO holding Dupont wire on this build has to be treated as suspect until it has been pulled on.

---

## Servos

All twelve on the PCA9685 since session 12, on michaelkubina's channel map. The robot is assembled and
sits beside the bench; the lower-leg servos reach through their extensions.

| Leg | Shoulder | Upper leg | Wrist |
|---|---|---|---|
| Front left | 0 | 1 | 2 |
| Front right | 3 | 4 | 5 |
| Rear left | 6 | 7 | 8 |
| Rear right | 9 | 10 | 11 |

Brown to GND (black row), red to V+ (middle), orange to PWM (yellow row). Verified in session 12 with
`code/channel_check`: every channel moved its own joint, none swapped, none buzzing at its mounting
angle. With all twelve holding: **PCA9685 V+ 6.0V, red bus bar 5.0V**.

---

## Not wired yet

| Connection | Note |
|---|---|
| ACS712 OUT to GPIO34 | After it walks |
| Battery voltage sensor | Not mounted, after it walks |
| HC-SR04 TRIG and ECHO | After it walks, ECHO through a 1kΩ/2kΩ divider |

---

**Last verified:** 2026-09-21, session 12.
