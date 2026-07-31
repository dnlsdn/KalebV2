# Project State

Single source of truth for **where the build is right now and what the next session is**.

Read this file first when resuming after a break. Update it at the end of every session, in the
same commit as that session's log in `main-steps/`. If the two disagree, trust the session logs for
what happened and correct this file.

**Last updated:** 2026-07-31, session 2.

---

## Where the build is

**Mechanics.** Wrist, upper leg and shoulder done. All four legs assembled. Chassis / body still to
be printed and assembled.

**Electronics.** The old wiring (a chain of WAGO connectors with known electrical mistakes) was
scrapped on 2026-04-12 and rebuilt from scratch around two bus bars: black for the ground star, red
for the 5V logic rail. Every connection below was measured on 2026-07-31, not remembered. The pin
by pin map is in `current-power-&-wiring-connections.md`.

- LiPo 2S negative to the black bus bar; positive through a 10A fuse into the ACS712. 7.55V after
  the fuse, the same as the pack, so the fuse conducts and drops nothing.
- ACS712 output split to both step-downs. The 5V rail reads 4.98V with the logic drawing current,
  the 6V rail reads 6.00V with nothing drawing from it.
- Red bus bar feeds ESP32 VIN, PCA9685 VCC, relay VCC, ACS712 VCC and both HC-SR04 VCC. All six
  grounds are on the black bus bar. No short between the two bars.
- AWG14 for the power path, Dupont for logic.
- **The SZBK07 heatsink bars sit at battery potential.** They are tied to the positive input and
  isolated from ground.

**Battery.** Healthy. Cells at 3.78V each, perfectly balanced, pack at 7.55V. About half charge, so
it needs a top-up before any test that actually drives the servos.

**Not wired yet:** the 6V servo rail (PCA9685 V+ is deliberately disconnected — the servos have
never been powered), the relay control pin, the I2C bus, all signal pins, the twelve servos.

**Firmware.** Nothing. No sketch has ever been flashed on this build.

---

## Next session — Session 3: the HC-SR04 ECHO voltage dividers

Session 2 is done and written up in `main-steps/2-recon.md`. The bench was verified rather than
remembered: no short between the rails, all twelve supply and ground connections confirmed, rails
at 4.98V and 6.00V, healthy battery.

Only this next. Battery disconnected and fuse out for the whole session.

**Before starting, check the parts drawer:** two 1kΩ resistors and two 2kΩ resistors are needed. If
they are not there, this session is a shopping session and nothing else.

The roadmap used to draw this divider the wrong way round, 2kΩ in series and 1kΩ to ground, which
gives 1.67V and sits below the roughly 2.5V the ESP32 needs to read a pin as high. It was corrected
in session 2. Build what the roadmap says now: **1kΩ in series, 2kΩ to ground, 3.33V at the node.**

- [ ] Measure each resistor with the multimeter before wiring it. Colour bands are easy to misread
      and a swapped pair is exactly the mistake this session exists to avoid.
- [ ] Build both dividers. Sensor 1: ECHO through 1kΩ to the node, node to GPIO26, 2kΩ from node to
      the black bus bar. Sensor 2: the same, node to GPIO27.
- [ ] Wire TRIG directly, no divider: sensor 1 to GPIO13, sensor 2 to GPIO14. TRIG is an input on
      the sensor and the ESP32 drives it at 3.3V.
- [ ] Verify each divider with the multimeter before powering anything: 1kΩ from the ECHO pin to
      the node, 2kΩ from the node to ground, and continuity from the node to the right GPIO.
- [ ] Update `current-power-&-wiring-connections.md`, write `main-steps/3-echo-dividers.md`, update
      this file, one commit.

---

## Backlog — ordered, one per session, never two in the same evening

1. **6V servo rail.** SZBK07 OUT+ to relay COM, relay NO to PCA9685 V+, 1000µF close to the
   PCA9685, relay control wire to GPIO25 plus a 10k pull-up to 3.3V so the relay stays off through
   boot. AWG14 on this rail, never Dupont: twelve MG996R under load pull several amps. Relay OFF by
   default. End state: the 6V rail can be switched on and off on command, with **no servo connected
   yet**.
2. **I2C bus + first sketch.** SDA 21, SCL 22. Flash nothing but an I2C scanner: PCA9685 and
   MPU6050 must answer. Servos still disconnected, no other code on the board.
3. **One single servo.** Centered at 1500µs. One, not twelve.
4. **The remaining eleven servos**, channels 0-11.

Later, not planned yet: IMU and balance, ultrasonic sensors in firmware, ESP32-CAM, WS2812 ring,
chassis assembly and moving the electronics into the body, gait.

Before the robot ever walks, the Dupont connections have to be secured. They hold by friction alone
and vibration works them loose, which shows up as a firmware bug that is not a firmware bug. Hot
glue on the housings or crimped connectors.

Chassis printing is passive time and can run in parallel, but **mechanical assembly never shares a
session with wiring**.

---

## Open questions — answer before they cost something

- **Were the servos centered at 1500µs before the horns were mounted on the assembled legs?** If
  not, backlog items 4-5 may require taking the horns off again. Worth knowing before twelve servos
  are wired.

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

Each session log answers, in this order: what I set out to do, what I actually did, what I verified
with the multimeter, what is still open. If a second job turns up mid-session, it goes into "what is
still open" and into the backlog above — it does not get done today.
