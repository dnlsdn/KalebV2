# Project State

Single source of truth for **where the build is right now and what the next session is**.

Read this file first when resuming after a break. Update it at the end of every session, in the
same commit as that session's log in `main-steps/`. If the two disagree, trust the session logs for
what happened and correct this file.

**Last updated:** 2026-09-20, session 8.

---

## The goal

Make the robot walk. Everything in this file is ordered by what that needs, and nothing else gets
built before it.

---

## Firmware — decided in session 3

The reference project, [SpotMicroESP32 by michaelkubina](https://github.com/michaelkubina/SpotMicroESP32),
**contains no firmware**. Its own README says the project lacks the whole programming part: it is a
mechanical and electrical design, and it points at three community forks for the software.

This was found in session 3 and it reframes the build. Following the reference project to the letter
produces a perfectly wired robot that cannot move, because the part that moves it is not in that
repository.

Of the three forks it recommends:

- **Maarten Weyn** — ESP-IDF, BLE phone control. Hardest toolchain of the three.
- **Blacksheep909 Nitro-Fork** — Arduino-based, easiest code to read, but requires a custom PCB and
  a FlySky FS-i6 RC transmitter. Hardware this build does not have.
- **[Leika, by runeharlyk](https://github.com/runeharlyk/SpotMicroESP32-Leika)** — inverse
  kinematics, two implemented gaits (12-point Bezier trot, 8-phase crawl), controlled from a phone
  browser over WiFi. PlatformIO, FreeRTOS.

**Leika is the target.** It is the only one of the three that requires no additional hardware.

The chassis is compatible: michaelkubina publishes the leg link geometry the community forks are
built around — L1 shoulder 10mm, L2 upper leg 60.5mm, L3 lower leg 111.1mm, L4 foot 118.5mm.

**Toolchain.** Arduino IDE for the small test sketches of the next sessions. PlatformIO only when
Leika itself is flashed — it is a submodule project with a filesystem image and a Svelte web app,
and it does not build in the Arduino IDE.

**Leika contains no relay** — checked in session 5, across its code and its component list, which
specifies a manual main power switch instead. Leika does confirm SDA 21 / SCL 22, matching this
build, and it has an `[env:esp32dev]` target, so a plain ESP32 is supported.

**Decided on 2026-09-19, done in session 6: there is no relay, and this build follows Leika.** The
servo rail is live whenever the pack is connected, and the main switch on battery + (owned, not
mounted yet) will become the servo power control. Leika runs unmodified. The alternatives
were weighed and dropped to keep the project simple: an NPN stage or a series LED in front of the
current module, or a KY-019 / HW-482 — the active-high NPN module michaelkubina and the Nitro-Fork
use, which a 3.3V pin drives directly. The module bought here is the blue low-level-trigger variant
of its AliExpress listing, which is why it never worked like the reference project's.

---

## Scope — what is on the path to walking

Only four things are required for the robot to move: **ESP32, PCA9685, twelve servos, power.** That
is michaelkubina's own mandatory list. Everything else in the component list is marked optional and
"not tested yet" by the reference project itself.

The MPU6050 is not strictly required but Leika treats it as effectively necessary for stable
locomotion, and it shares the I2C bus with the PCA9685, so it costs two wires. It is on the path.

Everything else — HC-SR04, ACS712, voltage sensor, ESP32-CAM, OLED, WS2812 — is kept in the project
but comes **after the robot walks**. They are integrations, not infrastructure. The WS2812 ring is
dropped entirely.

This ordering was wrong until session 3: the HC-SR04 voltage dividers were scheduled as the next
session, ahead of the entire servo chain, for a subsystem whose firmware is not planned yet.

---

## Where the build is

**Mechanics.** All four legs are complete through michaelkubina's "Attach Servo to Shoulder Joint":
wrist, upper leg, shoulder joint and shoulder servo. Chassis is printing.

**Servos are not all centred — each joint has its own angle**, set before its horn goes on, and this
file said otherwise until session 8:

| Joint | Left legs | Right legs | When |
|---|---|---|---|
| Wrist (lower leg) | 0° | 180° | November 2025 |
| Upper leg (hip) | 120° | 60° | session 8 |
| Shoulder | 90° | 90° | session 8 |

Angles are on the Arduino `Servo` library's scale, 0° = 544µs and 180° = 2400µs, which is what
`code/servo_angle` reproduces through the PCA9685. Leika's defaults assume this same geometry and
calibrate what is left over per channel.

**Two things about the legs are unverified**, both settled by the next mechanical step: the sense of
the one-arm offset on the shoulder joint horn, and whether each shoulder servo's shaft faces the
nose (front legs) or the tail (rear legs). A wrong offset shows up in calibration as a leg that runs
out of travel forward instead of backward, and costs one screw to fix.

**Two servos failed** — broken or misbehaving — and were replaced. Four MG996R-180 were ordered on
2026-08-14 from the same AliExpress listing and store the original twelve came from (Kevixun Store),
so the replacements are identical to the ten already on the legs: two for the robot, two as spares.
**They arrived on 2026-08-27** and both went into the legs as shoulder servos in session 8, at 90°,
together with the two good originals.

**Electronics.** The old wiring was scrapped on 2026-04-12 and rebuilt around two bus bars: black
for the ground star, red for the 5V logic rail. Every connection below was measured on 2026-07-31,
not remembered. The pin by pin map is in `current-power-&-wiring-connections.md`.

- LiPo 2S negative to the black bus bar; positive through a 10A fuse into the ACS712. 7.55V after
  the fuse, the same as the pack, so the fuse conducts and drops nothing.
- ACS712 output split to both step-downs. The 5V rail reads 4.98V with the logic drawing current,
  the 6V rail reads 6.00V with nothing drawing from it.
- Red bus bar feeds ESP32 VIN, ACS712 VCC and both HC-SR04 VCC. All grounds are on the
  black bus bar. No short between the two bars.
- AWG14 for the power path, Dupont for logic.
- **The SZBK07 heatsink bars sit at battery potential.** They are tied to the positive input and
  isolated from ground.
- **The red bus bar is live at 4.93V whenever the ESP32 is on USB**, battery or no battery: USB
  power back-feeds out of the VIN pin onto the bar. Measured in session 4. "Battery disconnected"
  does not mean "nothing is powered".

**The I2C bus works.** Built and verified in session 4: PCA9685 answers at 0x40 and MPU6050 at
0x68. The PCA9685 was moved off the 5V bar onto the ESP32's 3V3 pin, because its 10k I2C pull-ups
tie to VCC and would otherwise have idled SDA and SCL at 5V, above the ESP32's 3.6V maximum. 3.3V
and the two I2C lines are distributed with WAGO connectors.

**The 6V servo rail is built and verified.** Session 5 built it through a relay; session 6 removed the
relay, because this module (the blue low-level-trigger variant, PNP input) stays open only above
about 4.2V and no ESP32 pin gets there. SZBK07 OUT+ now joins the PCA9685 feed in a **WAGO 221-412**:
AWG14 in, AWG16 out, because the PCA9685's green terminal is a 3.5mm block rated to 1.5mm². An
**AWG16 ground return** runs from the PCA9685's GND screw to the black bus bar.

Measured in session 6, no servo connected: PCA9685 V+ at **6.0V** with the pack connected, **0V**
over a few seconds after unplugging the XT60, and the red bar unchanged at **4.98V**. **A connected
pack now means live servos.**

**No external capacitor.** This PCA9685 already carries a **1000µF 10V** on the servo rail. The spare
1000µF 16V is kept as a remedy if the rail collapses on peaks, to be fitted on the SZBK07 output.

**The first servo moved** — session 7. `code/servo_center` drove channel 0 to 1500µs and a
replacement servo went to its centre and held. V+ stayed at **6.0V** and the red bar at **4.98V**
while it held. The whole chain works under a real load.

**Battery.** 7.55V, cells at 3.78V each and balanced, measured at the start of session 7. About half
charge: enough for one servo, **charge it before several servos are powered together.**

**USB and the pack never go in together** — Espressif's DevKitC guide, found in session 7. Flash on
USB with the XT60 unplugged, then unplug USB before connecting the pack.

**Bus bars.** Seven free positions on the red bar, two on the black bar since the relay's wires came
off.

**Not wired yet:** the twelve servos on the robot; channel 0 holds the bench test servo. The voltage sensor is not mounted at all.

**Firmware.** An I2C scanner in session 4, `relay_off_on_safe` in session 5, `servo_center` in
session 7 (Adafruit PWM Servo Driver Library 3.0.3). That sketch
has no job since the relay was removed and stays in `code/` only as a record.

---

## Pinout — reconciled in session 3

The pinout in `Electronics-Roadmap.md` was partly invented and does not match michaelkubina. The
conflict that matters: michaelkubina uses **GPIO27 for the relay**, which the old roadmap had
assigned to the second sensor's ECHO. Had the dividers been built in session 3 as originally
planned, they would have had to be unwired.

| Function | Pin | Source |
|---|---|---|
| I2C SDA | 21 | Same everywhere |
| I2C SCL | 22 | Same everywhere |
| ~~Servo relay~~ | 27 | free since session 6, the relay is gone |
| ACS712 output | 34 | Same everywhere |

**Pins for the optional peripherals are deliberately not fixed.** They get read from Leika's own
configuration at the time each one is integrated. The pinout is dictated by the firmware that runs,
not by a document.

---

## Next session — Session 9: the legs onto the outer shoulders

michaelkubina's "Connecting to the Shoulders". A mechanical session, and the one that answers the
two open questions from session 8, because the outer shoulder pieces fit one way only.

- [ ] Check the two **Outer Shoulder** pieces are printed.
- [ ] Screw a servohorn to each outer shoulder piece (M2x8 and M2 nuts, middle hole of each arm).
- [ ] Shoulder servos are already at 90°: do not turn those shafts. Screw each leg to its outer
      shoulder with two M3x8, with the horn arms perpendicular as the guide shows.
- [ ] While the legs are in hand, **rewrite the tape labels** with the real channel map: front left
      0/1/2, front right 3/4/5, rear left 6/7/8, rear right 9/10/11, shoulder / upper leg / lower leg.
- [ ] Write `main-steps/9-outer-shoulders.md`, update this file, one commit.

Before session 10, when all twelve servos are wired: **charge the pack.**

---

## Backlog — ordered, one per session, never two in the same evening

1. **All twelve servos on the PCA9685**, on michaelkubina's channel map: front left 0/1/2, front right
   3/4/5, rear left 6/7/8, rear right 9/10/11, in the order shoulder, upper leg, lower leg. The
   replacement servos arrived on 2026-08-27, so nothing waits on delivery any more. An extension
   cable is on hand for every servo; the lower legs need them.
2. **Reinforce the PCA9685's V+ and GND traces with solder.** Leika's own documentation recommends
   it, and those traces are the narrowest point of the whole servo power path — narrower than the
   AWG16 feeding them. Before the robot carries its own weight.
3. **Leika: build and flash.** PlatformIO, submodules, filesystem image. Calibrate all twelve
   channels. With no relay, Leika runs unmodified.
4. **Mount the main switch** on battery +, between the XT60 and the fuse. Owned already. With no
   relay it is the only servo power control, so check its DC current rating first.
5. **Legs onto the chassis, first steps.**

**After it walks:** MPU6050 tuning, ACS712 output to GPIO34, voltage sensor, HC-SR04 with the
dividers, ESP32-CAM, OLED.

Chassis printing is passive time and runs in parallel, but **mechanical assembly never shares a
session with wiring**.

Before the robot ever walks, the Dupont connections have to be secured. They hold by friction alone
and vibration works them loose, which shows up as a firmware bug that is not a firmware bug. Hot
glue on the housings or crimped connectors.

**The same applies to Dupont wire inside the WAGO connectors, and it has already bitten once.**
WAGO 221 is specified from 0.14mm² and Dupont is about 0.08mm², below the minimum the lever can
grip. In session 4 one SDA wire sat in the connector without making contact and was only caught by
a continuity check before power. Strip longer and fold the conductor back on itself, and tug-test
every wire after closing the lever.

---

## Open questions — answer before they cost something

- **Why did the two servos fail?** Probably overloaded during testing on the old wiring, the one
  scrapped in April for having known electrical mistakes. Treated as a one-off from a configuration
  that no longer exists, not as evidence that the MG996R is too small. Re-open this if more of them
  fail once the robot actually carries its own weight — Leika recommends 20-36 kg servos and
  suggests going above the MG996R.
- **The replacement servos are not centered.** They must be driven to 1500µs before their horns go
  on, like the other ten. The first was centred in session 7, the second is session 8.
- **The relay questions are closed.** The module could not be driven at 3.3V (session 5), Leika
  expects no relay at all, and the module was removed in session 6.
- **Is the main switch rated for the servo current?** It will be the only servo power control. Read
  its DC rating before mounting it; the fuse caps the path at 10A.

---

## Safety gates

- The pack stays disconnected while anything on the power path is being changed. The fuse stays in
  otherwise, and the XT60 is connected last and unplugged first — see
  `Power-Up & Power-Down Procedures.md`.
- The SZBK07 heatsink bars are live at battery potential. Nothing at ground touches them, no metal
  tool near them while powered, and they never get mounted against a conductive surface.
- **A connected pack means live servos.** The servo rail follows the XT60, and later the main
  switch. Unplug the pack before touching anything on the servo side.
- Servo power is only ever switched with the servos idle — never under load.
- No firmware touches the ultrasonic sensors until the ECHO dividers are in place.
- Every voltage claim in a session log is a multimeter reading, not an assumption.

---

## Session rules

One session = one goal = one file in `main-steps/` = one commit.

A session starts by reading this file and ends by updating it. Nothing else keeps track of the
state of the bench between sessions.

**The wiring diagram is updated in the same commit.** `docs/wiring/` draws the bench as it is and the
robot as it will be. Any session that adds, moves or removes a wire edits `wires.py` (and
`layout.py` if a module moves), reruns `python3 build.py && python3 page.py` in that folder, and
republishes the interactive page.

**A session also starts by asking whether the step is worth doing at all** — whether it is on the
path to walking, whether it is urgent now, and whether something cheaper should come first. Session
3 exists because that question had never been asked. Answering it deleted four phases from the
roadmap and caught a pin conflict before it cost a rewiring.

Each session log answers, in this order: what I set out to do, what I actually did, what I verified
with the multimeter, what is still open. If a second job turns up mid-session, it goes into "what is
still open" and into the backlog above — it does not get done today.
