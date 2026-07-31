# Current Power & Wiring Connections

The wiring as it physically is, not as it is meant to end up. Everything marked verified was
measured on 2026-07-31 in session 2. Everything marked not wired is planned but does not exist yet.

All grounds go to a single black bus bar, the ground star. All 5V logic goes to a single red bus
bar.

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

All six verified by continuity against the bar.

| Board | Pin |
|---|---|
| ESP32 | VIN |
| PCA9685 | VCC |
| Relay module | VCC |
| ACS712 | VCC |
| HC-SR04 #1 | VCC |
| HC-SR04 #2 | VCC |

Dupont wire on all of these. Fine for the current they draw, but they hold by friction: they have
to be secured before the robot walks.

---

## Black bus bar — ground star

All six verified by continuity against the bar: ESP32, PCA9685, relay module, ACS712, HC-SR04 #1,
HC-SR04 #2.

Verified: the red bus bar and the black bus bar are not connected to each other.

---

## Not wired yet

| Connection | Note |
|---|---|
| SZBK07 OUT+ to relay COM | 6V servo rail step, AWG14 |
| Relay NO to PCA9685 V+ | The servos have never been powered |
| Relay IN to ESP32 GPIO25 | Active-low module, needs a 10k pull-up to 3.3V so it stays off through boot |
| 1000µF near the PCA9685 | 6V servo rail step |
| I2C SDA to GPIO21, SCL to GPIO22 | I2C step |
| PCA9685 OE to ground | I2C step |
| ACS712 OUT to GPIO34 | Not wired |
| Battery voltage sensor | Not mounted |
| HC-SR04 TRIG to GPIO13 and GPIO14 | Next session |
| HC-SR04 ECHO to GPIO26 and GPIO27 | Next session, through a 1kΩ/2kΩ divider |
| 12 servos on PCA9685 channels 0-11 | Last two steps of the backlog |

---

**Last verified:** 2026-07-31, session 2.
