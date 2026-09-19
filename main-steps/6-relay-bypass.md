# Session 06 — Removing the Relay

**Date:** September 19, 2026

## What I set out to do

Make the 6V servo rail usable without adding parts. Session 5 proved that the relay module cannot be
held open by an ESP32 pin, so the plan was to bypass it: join the two power wires that met at its
COM and NO screws, and let the rail follow the battery connector, exactly as Leika does.

## Why the relay went instead of being fixed

The module is the blue, low-level-trigger variant of its AliExpress listing: a PNP input stage that
stays open only above about 4.2V, which no ESP32 pin reaches. The reference projects never hit this
because they use a different module. michaelkubina and the Nitro-Fork both use a KY-019 / HW-482,
which has an NPN input, is active high, and is driven straight from a 3.3V pin.

Four ways out were on the table: an NPN stage, an LED in series with IN, buying a KY-019, or no
relay at all. The first three all keep software control of the servo power, and all three add parts,
a purchase or a firmware patch — Leika has no relay support. None of that is needed to make the robot
walk. Leika itself specifies a manual main power switch and nothing else, so this build now does the
same.

## What I actually did

Planned as a jumper between COM and NO. Changed before starting: a jumper means two wires under each
screw, an AWG14 plus a second conductor, and the module's terminal is not made to clamp that. A loose
clamp at servo current heats up.

So the relay was taken out entirely:

- Pack disconnected, fuse out, USB unplugged. **0V** between the red and black bars before starting.
- The AWG14 from SZBK07 OUT+ and the AWG16 to PCA9685 V+ were unscrewed from COM and NO.
- Both joined in a **WAGO 221-412**. Stripped to **11mm**, WAGO's length for the 221 series; the old
  strips were cut for the relay's screw terminal. Strands twisted, pushed in until the copper reached
  the back wall, levers closed, both wires tug-tested.
- The three Dupont on the relay's logic header were removed, VCC from the red bar and GND from the
  black bar, and the module left the bench.

## Continuity checks before power

| Check | Result |
|---|---|
| SZBK07 OUT+ ↔ PCA9685 V+ screw | continuity — the WAGO conducts |
| PCA9685 V+ ↔ black bus bar | no continuity, after the short beep of the 1000µF charging |
| Servo headers on the PCA9685 | nothing connected |

## What I verified with the multimeter

Fuse in, then the XT60 connected. No servo, no USB.

| Measurement | Reading |
|---|---|
| PCA9685 V+ ↔ black bus bar, pack connected | **6.0V** |
| Red bus bar ↔ black bus bar, pack connected | **4.98V** |
| PCA9685 V+ ↔ black bus bar, XT60 unplugged | **0V**, reached over a few seconds as the capacitors discharged |

The rail now follows the pack. Nothing else on the bench changed: the 5V rail reads what it read in
session 5.

Free positions after the relay's wires came off: **seven on the red bar, two on the black bar.**

## Power-up order, settled

The written procedure used the fuse as the on/off switch. It was written around the relay and it is
the wrong way round: whichever contact closes last takes the spark of the capacitors charging, and a
blade fuse holder is not a switch — its clips loosen with repeated insertion, and a loose clip at 10A
heats. The XT60 is a connector made to be mated and unmated. From now on the fuse stays in, and the
XT60 is connected last and disconnected first. `Power-Up & Power-Down Procedures.md` is rewritten
around this.

## What is still open

- **A connected pack now means live servos.** There is no software control of the servo power any
  more. Unplug the XT60 before touching anything on the servo side.
- **The main switch** is owned and not mounted. Once mounted it becomes the servo power control, so
  its DC current rating has to be checked against the 10A fuse first.
- **Charge the pack** before session 7. It sits at about half charge.
- `code/relay_off_on_safe` has no job any more and stays only as a record.
