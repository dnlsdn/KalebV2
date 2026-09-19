# Current Power & Wiring Connections

The wiring as it physically is, not as it is meant to end up. The power path was measured on
2026-07-31 in session 2; the I2C bus was built and verified on 2026-08-14 in session 4; the 6V servo
rail was built and measured on 2026-08-27 in session 5; the relay was removed on 2026-09-19 in
session 6. Everything marked not wired is planned but
does not exist yet.

All grounds go to a single black bus bar, the ground star. All 5V logic goes to a single red bus
bar. The 3.3V logic and the two I2C lines are distributed with WAGO connectors, not bars.

---

## Power path

| From | To | State |
|---|---|---|
| LiPo 2S negative | Black bus bar | Verified |
| LiPo 2S positive | 10A fuse | Verified, 7.55V after the fuse |
| Fuse output | ACS712 terminal | Verified |
| ACS712 terminal | LM2596 IN+ and SZBK07 IN+, split with a WAGO | Verified |
| LM2596 IN− and SZBK07 IN− | Black bus bar | Verified |

AWG14 on the whole power path.

---

## LM2596 — 5V logic step-down

| Pin | Connected to | State |
|---|---|---|
| OUT+ | Red bus bar | Verified, 4.98V under the logic load |
| OUT− | Black bus bar | Verified |

Trimmed to 5.00V with no load in session 1. It reads 4.98V once the logic is drawing current, which
is normal and was left alone.

---

## SZBK07 — 6V servo step-down

| Pin | Connected to | State |
|---|---|---|
| OUT+ | Servo rail WAGO, AWG14 | Verified, 6.0V measured at OUT+ with the pack connected |
| OUT− | Black bus bar | Verified |

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
| PCA9685 GND, green screw terminal | Black bus bar, **AWG16** | Verified |

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

## Red bus bar — 5V logic

All four verified by continuity against the bar. Seven of its twelve positions are free.

| Board | Pin |
|---|---|
| ESP32 | VIN |
| ACS712 | VCC |
| HC-SR04 #1 | VCC |
| HC-SR04 #2 | VCC |

The PCA9685 used to be on this bar and was moved to 3.3V in session 4. See below.

**This bar is live whenever the ESP32 is plugged into USB, even with the battery disconnected.**
The ESP32's VIN pin is tied to it, and USB power back-feeds out of VIN onto the bar. Measured
4.93V in session 4, so this board has no meaningful diode drop on that path. "Battery disconnected"
does not mean "nothing is powered".

---

## 3.3V — WAGO distribution

One wire from the ESP32 3V3 pin into a 5-port WAGO, two out. Two ports still free.

| Board | Pin | State |
|---|---|---|
| PCA9685 | VCC | Verified |
| MPU6050 | VCC | Verified |

**The PCA9685 is on 3.3V and not on the 5V bar for a reason.** Its SDA and SCL pull-up resistors
go to VCC — measured 9.96kΩ on both lines in session 4 — so VCC sets the idle voltage of the whole
I2C bus. With VCC at 5V, SDA and SCL would idle at 5V and sit above the ESP32's 3.6V absolute
maximum. At 3.3V the bus is clean and needs no level shifting anywhere.

---

## I2C bus — WAGO distribution

Two more WAGOs, one per line, each carrying one wire from the ESP32 and one to each board.

| Line | ESP32 pin | Boards | State |
|---|---|---|---|
| SDA | GPIO21 | PCA9685, MPU6050 | Verified |
| SCL | GPIO22 | PCA9685, MPU6050 | Verified |

Addresses confirmed by an I2C scanner in session 4: **PCA9685 at 0x40, MPU6050 at 0x68.**

**WAGO 221 connectors are specified from 0.14mm² up, and Dupont wire is around 0.08mm².** It is
below the minimum and the lever does not always grip it. One of the SDA wires was not making
contact and was caught by a continuity check before power was applied. The fix is to strip three or
four millimetres and fold the conductor back on itself before inserting, then tug-test every wire.
Any WAGO holding Dupont wire on this build has to be treated as suspect until it has been pulled on.

---

## Black bus bar — ground star

Verified by continuity against the bar: ESP32, PCA9685, ACS712, HC-SR04 #1,
HC-SR04 #2, MPU6050, and the PCA9685 OE pin.

The PCA9685's ground now arrives on **AWG16 from the green screw terminal**, not on the old Dupont,
which was removed in session 5. OE was re-checked against the bar after that rerouting and still has
continuity — OE is active-low, and if it floats high all twelve PWM outputs are disabled, which looks
exactly like a firmware bug and is not one.

**The bar has two free positions** since the relay's ground came off in session 6. The battery
voltage sensor, the OLED and the ESP32-CAM will need grounds after the robot walks; a WAGO tapped off
one free position covers them.

Verified: the red bus bar and the black bus bar are not connected to each other.

---

## Servo on the bench

| Channel | Servo | State |
|---|---|---|
| 0 | Replacement MG996R, horn off | Verified in session 7: centred at 1500µs and held; V+ 6.0V, red bar 4.98V while holding |

---

## Not wired yet

| Connection | Note |
|---|---|
| ACS712 OUT to GPIO34 | After it walks |
| Battery voltage sensor | Not mounted, after it walks |
| HC-SR04 TRIG and ECHO | After it walks, ECHO through a 1kΩ/2kΩ divider |
| Servos on PCA9685 channels 1-11 | Front left 0/1/2, front right 3/4/5, rear left 6/7/8, rear right 9/10/11. Channel 0 holds a bench test servo |

---

**Last verified:** 2026-09-19, session 7.
