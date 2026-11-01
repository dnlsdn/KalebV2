# Project State

Single source of truth for **where the build is right now and what the next session is**.

Read this file first when resuming after a break. Update it at the end of every session, in the
same commit as that session's log in `main-steps/`. If the two disagree, trust the session logs for
what happened and correct this file.

**Last updated:** 2026-11-01, session 20 closed: bus bars replaced by WAGOs on the bench; the move onto the plate next.

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

**Mechanics.** **The robot is assembled** — chassis, both leg groups on it — through michaelkubina's
"Mount legs to chassis". The circuitry mounting plate is in place and **empty**: the electronics stay
on the bench until all twelve servos have run there. Only the covers, head and tail are left, and they
come after it walks.

**All four thighs slope towards the tail and every knee points back**, front and rear alike. That is
the design, confirmed against michaelkubina's photo of his robot. Unpowered, the robot rests with its
legs in the assembly pose and one pair of feet off the table; it must sit on a support when off.

**Printing** is tracked in `docs/print-list.md`. Inner Shoulder, Chassis Side, Top Shoulder and
Bottom Shoulder are printed, two of each; the circuitry mounting plate (SZBK07 Extended) is on the
printer; the three LiPo brackets follow.

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

**Every joint was checked at its mounting angle in session 11** and is right. The hips that moved in
session 10 were corrected, and the rear right knee (ch11), seated one horn arm off since November, was
turned back by one arm without opening the leg.

**Two servos failed** — broken or misbehaving — and were replaced. Four MG996R-180 were ordered on
2026-08-14 from the same AliExpress listing and store the original twelve came from (Kevixun Store),
so the replacements are identical to the ten already on the legs: two for the robot, two as spares.
**They arrived on 2026-08-27** and both went into the legs as shoulder servos in session 8, at 90°,
together with the two good originals.

**Electronics.** The old wiring was scrapped on 2026-04-12 and rebuilt around two bus bars. **Session 20
took the bars out** (each 150 × 28mm, and the plate's mounting area is 106 × 150mm): the ground star is
now three WAGO 221-415 in a chain (A takes every heavy ground: battery, SZBK07 IN−, PCA9685 GND), the 5V
node is a fourth (D), and 3.3V and I2C pass through the PCA9685's two headers, which are joined pin for
pin on the board. Electrically the same circuit. The pin by pin map is in
`current-power-&-wiring-connections.md` and `docs/wiring/wires.py`.

**Neither step-down has an OUT− wire** — found in session 20, while the documentation since July said both
were on the bar, "verified". Both modules share ground between input and output, so the return currents
come back through IN−; it has always worked this way. Wiring OUT− to WAGO A (one free port) is the textbook
way, kept for later as one change on its own.

- LiPo 2S negative to the black bus bar; positive through a 10A fuse into the ACS712. 7.55V after
  the fuse, the same as the pack, so the fuse conducts and drops nothing.
- ACS712 output split to both step-downs. The 5V rail reads 4.98V with the logic drawing current,
  the 6V rail reads 6.00V with nothing drawing from it.
- WAGO D (5V) feeds ESP32 VIN, ACS712 VCC and both HC-SR04 VCC: 4.95V with the pack in, session 20.
  All grounds are in WAGOs A, B and C. No short between the 5V, 3.3V or 6V nodes and ground.
- AWG14 for the power path, Dupont for logic.
- **The SZBK07 heatsink bars sit at battery potential.** They are tied to the positive input and
  isolated from ground.
- **The 5V node is live at about 4.9V whenever the ESP32 is on USB**, battery or no battery: USB
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

**Battery.** Ovonic 2S1P LiPo, **5200mAh, 50C**, 7.4V nominal, 38.48Wh, Deans T-plug with a
T-to-XT60 adapter, 3-pin balance lead. **Fully charged on 2026-09-21**: 7.52V at rest before, 8.40V at
the end, **3833mAh** put in. That was about three quarters of the pack — it had been nearer a quarter
full than the half that 3.78V per cell suggested, because a LiPo's voltage barely moves across the
middle of its charge. Use the charger's mAh, not the voltage, to judge how full it is.

**Charging**, with a SkyRC B6neo on a USB-C PD supply (reads 20V in): battery off the bench first;
program **LiPo / 2S / Balance CHG / 4.20V / 3.0A**; XT60 into the charger's OUT, balance plug into
the `−123456` port with its black edge on `−`; Start. About 90 minutes from a quarter. Unplug XT60,
then balance lead, then USB-C. The charger came set to 4S: check the cell count every time.

**USB and the pack never go in together** — Espressif's DevKitC guide, found in session 7. Flash on
USB with the XT60 unplugged, then unplug USB before connecting the pack.

**Free ports.** One on WAGO A, one on WAGO B, none on C or D, and one spare 221-415 unused. The two bus
bars are off the bench and kept.

**All twelve servos are on their real channels** — session 12, checked with `code/channel_check`:
none swapped, none buzzing, V+ 6.0V and the red bar 5.0V with all twelve holding. The robot sits on a
box beside the bench; the electronics have not moved into it yet. The voltage sensor is not mounted at all.

**Firmware.** An I2C scanner in session 4, `relay_off_on_safe` in session 5, `servo_center` in
session 7 (Adafruit PWM Servo Driver Library 3.0.3). That sketch
has no job since the relay was removed and stays in `code/` only as a record.

**Leika is on the ESP32** — session 13, 2026-10-03, with six changes to upstream, all in
`firmware/leika-config.md`. It boots, opens the `Spot-Micro` access point, serves its app at
`http://192.168.4.1`, finds the PCA9685 at 0x40 and the IMU at 0x68 from the app's I2C page, and the
IMU chart follows the board when it is tilted. The servos have not been driven by Leika yet. Flashing
is done: from now on the ESP32 can run from the pack with no USB, and the phone talks to it over Wi-Fi.

**The IMU is an MPU6500, not an MPU6050.** It answers `WHO_AM_I` 0x70. Leika's MPU6050 driver loads its
DMP and reads it correctly once 0x70 is accepted. It is wired with Dupont only and hangs from its wires
on the bench, and it failed to answer at boot (`I2C hardware timeout`) on two of seven boots while the
PCA9685 on the same bus never did.

**Servo conversion measured** — session 14: **2.56 ticks per degree**, over 180° on a spare MG996R, against
Leika's default 2.0. Entered for all twelve channels and stored on the ESP32 (`servoSettings.json`);
uploading the filesystem image again would erase it, so it is also in `firmware/leika-config.md`.
**One of the two failed servos holds its position but does not follow commands**; it is labelled and
stays out of the robot.

**All twelve joints calibrated** — session 15: Center PWM per joint, measured one leg at a time at
knee 90° and foot under the hip; values in `firmware/leika-config.md`. Nine of twelve were 4° or more off
Leika's default, up to 23°. Center Angle and Direction are Leika's defaults. No pose has been commanded
through Leika's kinematics yet.

**Rest works** — session 18, the first pose from Leika's kinematics, robot lifted: thighs nearly level
towards the tail, knees folded, feet under the hips, the four legs symmetric, so the Directions are right.
Stand works too. Choosing a mode activates the servos; the Servo page's Active is a calibration tool that
sends every leg straight down, where the right knees stop bent by the 125 clamp (front about 16°, rear
about 42°).

**The board no longer stops answering** — session 19. Cause, from a serial log: a phone that dropped off
Wi-Fi stayed in Leika's client list with its socket open, and lwIP's 10 sockets ran out
(`error in accept (23)`). Fixed in Leika with keep-alive, a `close_fn` and 16 sockets; the same test then
gave 0 errors. The Restart button works now too, after two more Leika bugs (an empty request refused,
then a panic in `sendOk()`).

**Session 18's panic is still unexplained.** Not reproduced on USB. **Core dumps now go to flash**: if the
board panics on the pack, the next boot says `Found core dump`, and it is read over USB before anything
else (`firmware/leika-config.md`).

**The IMU sometimes fails to start after a reset** — 2 of 8 boots in session 19, all warm resets, with
`89 Hz` in the log. Leika carries on without it. Not yet known whether a cold power-on avoids it.

**The brown-out did not come back** — session 17. Session 15 saw *Reset Reason: Brownout reset* with three
servos moved one at a time. On the new board, in the same configuration (one leg, Active, three servos
moved one at a time) and with six minutes idle on the pack, there was no restart: Reset Reason stayed
power-on and the Uptime kept pace with the clock. Not reproduced is not explained: board, Duponts and
firmware all changed since, and session 16 found a GND Dupont off the black bar. Twelve servos activated
together did not bring it back either (session 18).

**A new ESP32 is on the bench** — session 17, an ESP-WROOM-32 / CP2102, 30 pins, D0WD-V3 4MB, the same
chip as the board lost in session 16. Same five Duponts, same pins. **The PCA9685 (0x40) and the IMU
(0x68) survived** and answer on the I2C page.

**Leika has thirteen changes now** — session 16 added a lock on the I2C bus (a real race: 21 errors in 109
slider moves, 0 in 812 after) and wrote the calibration in as the firmware's defaults, so the new board
starts calibrated. Session 19 added five: the web server's dead clients and sockets, Restart, core dumps.

**Deactivating does not relax the servos.** With Active off and the PCA9685 asleep, a leg stayed stiff.
STOP and Deactivated are not a safe state; unplugging the XT60 is.

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

## Next session — Session 21: the electronics onto the body

**Is it worth doing?** Yes: the robot cannot walk with its electronics on the bench, and session 20 removed
the obstacle, the bus bars. What goes on the plate now is what michaelkubina's plate was made for, plus
four small WAGOs. It also settles two open items: the IMU screwed flat (does it read level?) and the
Duponts secured before anything vibrates.

**Decide first: the PCA9685's traces (backlog 2).** Reinforcing its V+ and GND traces with solder needs
the board off and unwired, which this session does anyway. If it is done, it is done first, as its own
step, before anything is screwed down.

- [ ] Pack out, fuse out, USB out, **0V between a ground WAGO and WAGO D**. Photograph the bench first.
- [ ] **The LiPo brackets first** (printed on 2026-11-01). The pack's place in the body decides where the
      XT60 lands, so the length of every power wire.
- [ ] Plan the plate: the template's standoffs for SZBK07, LM2596, ESP32 and PCA9685, the WAGOs and the
      fuse holder in the space left, the SZBK07 heatsinks touching nothing conductive, the ESP32's USB port
      reachable for flashing and for reading a core dump.
- [ ] Move one module at a time; each wire that comes out of a WAGO goes back stripped 11mm and tug-tested.
- [ ] The same checks as session 20, unpowered: the WAGO links, ESP32 GND and VIN, and no short on 5V,
      3.3V and 6V. Then USB alone from cold: 0x40 and 0x68. Then the pack: 5V and 6V, Rest.
- [ ] The IMU: does it read level now that it sits flat?
- [ ] `docs/wiring/`: update the layout, rebuild, republish. Write `main-steps/21-*.md`, update this file,
      one commit.

---

## Backlog — ordered, one per session, never two in the same evening

1. ~~**All twelve servos on the PCA9685**~~ — done in session 12, on michaelkubina's channel map: front left 0/1/2, front right
   3/4/5, rear left 6/7/8, rear right 9/10/11, in the order shoulder, upper leg, lower leg. The
   replacement servos arrived on 2026-08-27, so nothing waits on delivery any more. An extension
   cable is on hand for every servo; the lower legs need them.
2. **Reinforce the PCA9685's V+ and GND traces with solder.** Leika's own documentation recommends
   it, and those traces are the narrowest point of the whole servo power path — narrower than the
   AWG16 feeding them. Before the robot carries its own weight.
3. ~~**Leika: build and flash.**~~ Done in session 13, with six changes to upstream. Calibration: the
   servo frame (conversion) done in session 14, body frame in session 15. New ESP32 in session 17, and
   the brown-out did not return with one leg; twelve servos together and Rest done in session 18.
   The firmware crash hunt in session 19 fixed "stops answering" and turned core dumps on.
4. **Mount the main switch** on battery +, between the XT60 and the fuse. Owned already. With no
   relay it is the only servo power control, so check its DC current rating first.
5. **Electronics onto the body** — the circuitry plate. The bus bars were replaced on the bench first, in
   session 20, because they did not fit; the move itself is session 21. One session of its own, re-verified like session 17 (3.3V short check,
   the two reds, I2C scan). It also settles two open items: the IMU screwed flat (does it read level?)
   and the Duponts secured before anything vibrates.
6. **Wire the two step-downs' OUT− to WAGO A.** Not needed to work, found missing in session 20.
7. **Legs onto the chassis, first steps.**

**After it walks:** MPU6050 tuning, ACS712 output to GPIO34, voltage sensor, HC-SR04 with the
dividers, ESP32-CAM, OLED.

Chassis printing is passive time and runs in parallel, but **mechanical assembly never shares a
session with wiring**.

Before the robot ever walks, the Dupont connections have to be secured — and the **IMU's four wires
first**: they are the only ones that have already failed intermittently, in session 13. They hold by friction alone
and vibration works them loose, which shows up as a firmware bug that is not a firmware bug. Hot
glue on the housings or crimped connectors.

**The same applies to Dupont wire inside the WAGO connectors, and it has already bitten once.**
WAGO 221 is specified from 0.14mm² and Dupont is about 0.08mm², below the minimum the lever can
grip. In session 4 one SDA wire sat in the connector without making contact and was only caught by
a continuity check before power. Strip longer and fold the conductor back on itself, and tug-test
every wire after closing the lever.

---

## Open questions — answer before they cost something

- **Does the IMU read level when it is level?** At rest on the bench it reads about 2 rad (~115°) on x
  and y, but it was standing almost on its edge, so that may be correct. Check once it is screwed flat
  on the circuitry plate. Note Leika's IMU chart is labelled in degrees and plots radians.
- **Is the MPU6500 a full substitute?** Its accelerometer offset registers start at **0x77**
  (XA_OFFSET_H, 0x7A, 0x7D), the MPU6050's at **0x06**, and Leika's driver writes 0x06 during its start-up
  calibration (`REG_XA_OFFS_H` in `mpu6050.h`). Checked against the MPU-6500 register map and the Linux
  `inv_mpu6050` driver (`INV_MPU6500_REG_ACCEL_OFFSET 0x77`), not on the bench. The gyro offsets are at
  0x13 on both. It only matters for IMU tuning, after it walks.

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
- **STOP and Deactivated do not make the servos limp** (session 15). Only unplugging the XT60 does.
- **Multimeter: black probe on the black bus bar, red probe on one pin.** Never both probes on a board's
  header pins: in session 16 a slip there cost the ESP32.
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
