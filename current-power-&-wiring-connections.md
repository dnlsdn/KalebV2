# Current Power & Wiring Connections

The wiring as it physically is, not as it is meant to end up. The power path was measured on
2026-07-31 in session 2; the I2C bus was built and verified on 2026-08-14 in session 4; the 6V servo
rail was built and measured on 2026-08-27 in session 5. Everything marked not wired is planned but
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
| OUT+ | Relay COM, AWG14 | Verified, 6.0V measured at OUT+ with the pack connected |
| OUT− | Black bus bar | Verified |

**The two metal side bars of this module are electrically live**, at the same potential as the
positive input, so around 7.5V with the pack connected. They are the heatsink and the power
transistor tab is bolted to them. Verified: they beep against the positive input and stay silent
against ground.

Nothing at ground potential may touch them, no metal tool near them while powered, and the module
cannot be mounted on a conductive surface. Its mounting screws are live.

---

## Servo rail — relay and PCA9685

Built in session 5. Measured with the pack connected and USB unplugged, so these are the real
operating numbers and not USB back-feed.

| From | To | State |
|---|---|---|
| SZBK07 OUT+ | Relay COM, AWG14 | Verified, 6.0V |
| Relay NO | PCA9685 V+, green screw terminal, **AWG16** | Verified |
| PCA9685 GND, green screw terminal | Black bus bar, **AWG16** | Verified |
| Relay IN | **Nothing** — see below | Not wired |

**AWG16 and not AWG14 on the last two, by necessity.** The PCA9685's green 2-pole terminal is a
3.5mm block rated to 1.5mm²; AWG14 at 2.08mm² does not fit it. Thinning the AWG14 by cutting strands
was rejected. The run is short, the current is capped upstream by a 10A relay, and the narrowest
point of this path is not the wire at all — it is the PCA9685's own V+ traces, which are on the
backlog to be reinforced with solder.

**The ground return is new.** The PCA9685's ground previously reached the bar through a Dupont wire
sized for logic current. That Dupont was removed once the AWG16 was in. Servo return current is not
a logic-level current.

**The relay terminals were identified by measurement, not by the silkscreen**, which is not in a
language the builder reads. At rest a relay has exactly one closed contact, COM–NC, so the terminal
with continuity to nothing is NO.

**No external capacitor.** This PCA9685 carries a **1000µF 10V** on the servo rail already, verified
by continuity: positive leg to the V+ screw, negative to GND. A spare 1000µF 16V is in the drawer as
a documented remedy, to be fitted before the relay if the rail ever collapses on peaks.

Verified with the pack connected, no servo attached:

| Measurement | Reading |
|---|---|
| SZBK07 OUT+ ↔ black bus bar | 6.0V |
| PCA9685 V+ ↔ black bus bar, relay open | 0V |
| PCA9685 V+ ↔ black bus bar, relay closed by hand | 6.0V |

---

## Relay control — why it is still not wired

**GPIO27 cannot drive this module.** The IN pin is the base of a PNP transistor with its emitter on
VCC: floating it sits at 4.2V, which is 4.93V minus one base-emitter drop, and an ohmmeter finds no
resistive path between IN and VCC because there is a junction there, not a resistor. The relay stays
open only while IN is above roughly 4.2V.

An ESP32 pin never gets there — 3.3V driven high (3.1V measured), around 3.9V when high-impedance and
clamped by its own protection diode. Wired directly, the relay closed and stayed closed.

| Measurement | Reading |
|---|---|
| IN floating, module powered | 4.2V |
| IN ↔ VCC, module unpowered, ohms | open |
| IN with a 10k to ground | relay chatters on the threshold |
| GPIO27 driven high, IN disconnected | 3.1V |
| IN wired to GPIO27, sketch driving high | relay closed, node at 2.0V |

The planned 10k pull-up from GPIO27 to 3.3V was **not installed**. GPIO27 and IN are one node, so it
would have pulled the same wire in the same direction, and to a lower voltage than the module needs.

No series resistor is needed for the boot-time 4.2V on GPIO27 either: the source impedance is of the
order of kilohms, so the current into the ESP32's protection clamp is around a tenth of a milliamp,
for the length of a boot.

The fix is an NPN stage — 1k from GPIO27 to the base, 10k base to ground, collector to IN, emitter to
the black bus bar. It inverts the command and makes the safe state the natural one: transistor off,
IN left alone at 4.2V, relay open with no software involved.

---

## Red bus bar — 5V logic

All five verified by continuity against the bar.

| Board | Pin |
|---|---|
| ESP32 | VIN |
| Relay module | VCC |
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

Verified by continuity against the bar: ESP32, PCA9685, relay module, ACS712, HC-SR04 #1,
HC-SR04 #2, MPU6050, and the PCA9685 OE pin.

The PCA9685's ground now arrives on **AWG16 from the green screw terminal**, not on the old Dupont,
which was removed in session 5. OE was re-checked against the bar after that rerouting and still has
continuity — OE is active-low, and if it floats high all twelve PWM outputs are disabled, which looks
exactly like a firmware bug and is not one.

**The bar has one free position left.** The only thing still queued for it is the battery voltage
sensor, which comes after the robot walks. A WAGO tapped off the bar, or a second bar, solves it.

Verified: the red bus bar and the black bus bar are not connected to each other.

---

## Not wired yet

| Connection | Note |
|---|---|
| Relay control | Needs an NPN stage between GPIO27 and IN. Direct wiring does not work — see above |
| ACS712 OUT to GPIO34 | After it walks |
| Battery voltage sensor | Not mounted, after it walks |
| HC-SR04 TRIG and ECHO | After it walks, ECHO through a 1kΩ/2kΩ divider |
| 12 servos on PCA9685 channels 0-11 | Front left 0/1/2, front right 3/4/5, rear left 6/7/8, rear right 9/10/11 |

---

**Last verified:** 2026-08-27, session 5.
