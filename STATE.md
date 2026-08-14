# Project State

Single source of truth for **where the build is right now and what the next session is**.

Read this file first when resuming after a break. Update it at the end of every session, in the
same commit as that session's log in `main-steps/`. If the two disagree, trust the session logs for
what happened and correct this file.

**Last updated:** 2026-08-14, session 4.

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

**Mechanics.** Wrist, upper leg and shoulder done. All four legs assembled. Ten of the twelve servos
were centered at 1500µs before their horns were mounted, so nothing has to be taken apart. Chassis
is printing.

**Two servos failed** — broken or misbehaving — and are being replaced. Four MG996R-180 were
ordered on 2026-08-14 from the same AliExpress listing and store the original twelve came from
(Kevixun Store), so the replacements are identical to the ten already on the legs: two for the
robot, two as spares. Estimated delivery 23-28 August. Nothing on the bench waits for them until
the twelve-servo session.

**Electronics.** The old wiring was scrapped on 2026-04-12 and rebuilt around two bus bars: black
for the ground star, red for the 5V logic rail. Every connection below was measured on 2026-07-31,
not remembered. The pin by pin map is in `current-power-&-wiring-connections.md`.

- LiPo 2S negative to the black bus bar; positive through a 10A fuse into the ACS712. 7.55V after
  the fuse, the same as the pack, so the fuse conducts and drops nothing.
- ACS712 output split to both step-downs. The 5V rail reads 4.98V with the logic drawing current,
  the 6V rail reads 6.00V with nothing drawing from it.
- Red bus bar feeds ESP32 VIN, relay VCC, ACS712 VCC and both HC-SR04 VCC. All grounds are on the
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

**The power path is finished and verified.** What remains on the signal side is the relay control
wire and the twelve servo channels.

**Battery.** Healthy. Cells at 3.78V each, perfectly balanced, pack at 7.55V. About half charge, so
it needs a top-up before any test that actually drives the servos.

**Not wired yet:** the 6V servo rail (PCA9685 V+ is deliberately disconnected — the servos have
never been powered), the relay control pin, the twelve servos. The voltage sensor is not mounted at
all.

**Firmware.** An I2C scanner was flashed in session 4, the first code ever run on this build.
Nothing else.

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
| Servo relay | 27 | michaelkubina |
| ACS712 output | 34 | Same everywhere |

**Pins for the optional peripherals are deliberately not fixed.** They get read from Leika's own
configuration at the time each one is integrated. The pinout is dictated by the firmware that runs,
not by a document.

---

## Next session — Session 5: the 6V servo rail and the relay

The first session that puts real current somewhere new, so the pack stays disconnected and the fuse
stays out for the whole build, and it only goes back in at the end for the measurement.

Parts confirmed in the drawer on 2026-08-14: 1000µF capacitor, 10k resistor, AWG14 offcuts.

- [ ] SZBK07 OUT+ to relay COM. **AWG14, never Dupont** — twelve MG996R under load pull several
      amps.
- [ ] Relay NO to PCA9685 V+. AWG14.
- [ ] 1000µF close to the PCA9685, watching polarity. It is the local charge reservoir for the
      servo current spikes.
- [ ] Relay IN to GPIO27, plus a **10k pull-up from that pin to 3.3V**. The module is active-low
      and the pin is undriven until `setup()` runs; without the pull-up the servo rail can close
      for a few milliseconds at power-up, before the PCA9685 has been told anything.
- [ ] Flash `code/relay_off_on_safe` before anything else, so the pin is explicitly driven high.
- [ ] Verify with the multimeter, relay OFF: PCA9685 V+ reads 0V. Then command it on and confirm
      the rail reaches 6V. **No servo connected for either measurement.**
- [ ] Update `current-power-&-wiring-connections.md`, write `main-steps/5-servo-rail.md`, update
      this file, one commit.

---

## Backlog — ordered, one per session, never two in the same evening

1. **One single servo.** Centered at 1500µs. One, not twelve.
2. **The remaining eleven servos**, on michaelkubina's channel map: front left 0/1/2, front right
   3/4/5, rear left 6/7/8, rear right 9/10/11, in the order shoulder, upper leg, lower leg. Waits
   on the replacement servos, estimated 23-28 August.
3. **Leika: build and flash.** PlatformIO, submodules, filesystem image. Calibrate all twelve
   channels.
4. **Legs onto the chassis, first steps.**

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
  on, like the other ten. That needs a working PCA9685, so it cannot happen before backlog item 2.
- **Is the relay module's contact rating enough?** A typical 5V relay module is rated 10A DC. Twelve
  MG996R stalling together would be far more than that, though they never all stall at once. Worth
  checking the module's own rating before the servo rail is closed under load.
- **Does Leika expect the relay on GPIO27?** Read its configuration before flashing. If not, it is
  one Dupont wire to move.

---

## Safety gates

- The pack stays disconnected while anything on the power path is being changed.
- The SZBK07 heatsink bars are live at battery potential. Nothing at ground touches them, no metal
  tool near them while powered, and they never get mounted against a conductive surface.
- The relay stays OFF unless a servo test is actively running.
- No firmware touches the ultrasonic sensors until the ECHO dividers are in place.
- Every voltage claim in a session log is a multimeter reading, not an assumption.

---

## Session rules

One session = one goal = one file in `main-steps/` = one commit.

A session starts by reading this file and ends by updating it. Nothing else keeps track of the
state of the bench between sessions.

**A session also starts by asking whether the step is worth doing at all** — whether it is on the
path to walking, whether it is urgent now, and whether something cheaper should come first. Session
3 exists because that question had never been asked. Answering it deleted four phases from the
roadmap and caught a pin conflict before it cost a rewiring.

Each session log answers, in this order: what I set out to do, what I actually did, what I verified
with the multimeter, what is still open. If a second job turns up mid-session, it goes into "what is
still open" and into the backlog above — it does not get done today.
