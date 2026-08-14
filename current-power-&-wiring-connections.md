# Current Power & Wiring Connections

The wiring as it physically is, not as it is meant to end up. The power path was measured on
2026-07-31 in session 2; the I2C bus was built and verified on 2026-08-14 in session 4. Everything
marked not wired is planned but does not exist yet.

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
| OUT+ | Nothing yet | 6.00V measured with no load |
| OUT− | Black bus bar | Verified |

**The two metal side bars of this module are electrically live**, at the same potential as the
positive input, so around 7.5V with the pack connected. They are the heatsink and the power
transistor tab is bolted to them. Verified: they beep against the positive input and stay silent
against ground.

Nothing at ground potential may touch them, no metal tool near them while powered, and the module
cannot be mounted on a conductive surface. Its mounting screws are live.

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

PCA9685 OE is tied to ground, which enables the PWM outputs. It does nothing yet: V+ is
disconnected and no servo is attached.

Verified: the red bus bar and the black bus bar are not connected to each other.

---

## Not wired yet

| Connection | Note |
|---|---|
| SZBK07 OUT+ to relay COM | 6V servo rail step, AWG14 |
| Relay NO to PCA9685 V+ | The servos have never been powered |
| Relay IN to ESP32 GPIO27 | Active-low module, needs a 10k pull-up to 3.3V so it stays off through boot |
| 1000µF near the PCA9685 | 6V servo rail step |
| ACS712 OUT to GPIO34 | After it walks |
| Battery voltage sensor | Not mounted, after it walks |
| HC-SR04 TRIG and ECHO | After it walks, ECHO through a 1kΩ/2kΩ divider |
| 12 servos on PCA9685 channels 0-11 | Front left 0/1/2, front right 3/4/5, rear left 6/7/8, rear right 9/10/11 |

---

**Last verified:** 2026-08-14, session 4.
