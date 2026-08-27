# Project State

Single source of truth for **where the build is right now and what the next session is**.

Read this file first when resuming after a break. Update it at the end of every session, in the
same commit as that session's log in `main-steps/`. If the two disagree, trust the session logs for
what happened and correct this file.

**Last updated:** 2026-08-27, session 5.

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
specifies a manual main power switch instead. So when Leika is flashed, nothing will drive the servo
rail control pin and the servos will never be powered. The fix is a two-line addition to Leika's
setup, or a link in place of the relay, and it belongs to the session where Leika is flashed. Leika
does confirm SDA 21 / SCL 22, matching this build, and it has an `[env:esp32dev]` target, so a plain
ESP32 is supported.

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

**Two servos failed** — broken or misbehaving — and were replaced. Four MG996R-180 were ordered on
2026-08-14 from the same AliExpress listing and store the original twelve came from (Kevixun Store),
so the replacements are identical to the ten already on the legs: two for the robot, two as spares.
**They arrived on 2026-08-27** and are on the bench. They are still not centred at 1500µs, and
cannot be until the servo rail can be commanded.

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

**The 6V servo rail is built and verified** — session 5. SZBK07 OUT+ to relay COM in AWG14; relay NO
to PCA9685 V+ in **AWG16**, because the board's green screw terminal is a 3.5mm block rated to
1.5mm² and AWG14 does not fit it by design; and a new **AWG16 ground return** from the PCA9685's GND
screw to the black bus bar, which the session plan had omitted entirely — the old Dupont there was
sized for logic current and would have carried the return of twelve MG996R.

Measured with the pack connected and USB unplugged: SZBK07 OUT+ at **6.0V**, PCA9685 V+ at **0V**
with the relay open, and **6.0V** with the relay closed by hand. No servo was connected. The rail
exists and the relay genuinely isolates it.

**No external capacitor was added.** This PCA9685 already carries a **1000µF 10V** on the servo
rail, verified by continuity against both screws. A second one would only enlarge the inrush the
relay contacts see at closing. The spare 1000µF 16V is kept as a documented remedy if the rail
collapses on peaks later, to be fitted **before the relay**, on the SZBK07 output.

**What remains on the signal side is the relay control, and the twelve servo channels.**

**Battery.** Healthy. Cells at 3.78V each, perfectly balanced, pack at 7.55V. About half charge, so
it needs a top-up before any test that actually drives the servos.

**The relay cannot be commanded from GPIO27 directly.** Found in session 5 and it is the finding that
matters most. The module is an SRD-05VDC-SL-C whose IN pin is the base of a **PNP transistor with its
emitter on VCC**: floating, IN sits at 4.2V, which is 4.93V minus exactly one base-emitter drop, and
an ohmmeter finds no resistive path between IN and VCC because there is a junction there and not a
resistor. The relay is open only while **IN stays above roughly 4.2V**.

An ESP32 pin can never do that. Driven high it reaches 3.3V — 3.1V measured on this board. Left in
high impedance it is clamped by its own protection diode near 3.9V. Both are below the threshold, so
**no state of the software holds this relay open** with GPIO27 wired to IN. Wired that way, the relay
closed and stayed closed. The pin and the sketch were both correct.

The planned 10k pull-up to 3.3V was **not installed and would not have helped**: GPIO27 and IN are one
node, so it would have pulled the same wire in the same direction, and to 3.3V rather than the 4.2V
the module needs. The related worry about 4.2V reaching GPIO27 during boot, over the ESP32's 3.6V
maximum, is closed by the same measurements — the source impedance is of the order of kilohms and the
clamp current is around a tenth of a milliamp for the length of a boot. **No series resistor needed.**

**Not wired yet:** the relay control (see next session), the twelve servos. The voltage sensor is not
mounted at all.

**The black bus bar has one free position.** The only thing still queued for it is the battery
voltage sensor, after the robot walks. A WAGO tapped off the bar, or a second bar, solves it when the
time comes.

**Firmware.** An I2C scanner in session 4, and `relay_off_on_safe` flashed in session 5. That sketch
is now **wrong for the hardware** and has to be rewritten once the transistor stage exists, because
the sense of the pin inverts.

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

## Next session — Session 6: the transistor stage on the relay control

The only thing standing between this build and a servo that moves. The pack stays disconnected and
the fuse stays out for the whole build; the stage can be tested entirely on USB, because it is
verified by whether the relay clicks, not by what the rail does.

Why a transistor and not a wire: the module's IN pin is a PNP base sitting at 4.2V, and the relay is
open only while IN stays above that. No ESP32 output level reaches it. An NPN between GPIO27 and IN
inverts the command and decouples the levels, and it makes the safe state the natural one — with the
transistor off, IN is simply left alone at 4.2V and **the relay is open with no software involved.**

The stage: GPIO27 through a **1k base resistor** to the base of a small NPN (2N2222, BC547, S8050 or
equivalent); **10k from base to ground** so the base cannot float while GPIO27 is undriven at boot;
**collector to the relay's IN pin**; **emitter to the black bus bar**. Confirm the parts are in the
drawer before starting — if there is no NPN on the bench, the alternative is an optocoupled relay
module with a separate JD-VCC jumper, which is a part to order.

- [ ] Confirm an NPN, a 1k and a 10k are on the bench.
- [ ] Build the stage. Emitter to the black bus bar, which has one free position left.
- [ ] Rewrite `code/relay_off_on_safe`: **the sense inverts.** GPIO27 LOW is now relay OFF, and
      that is also what an undriven pin gives, so the safe state costs nothing. Flash it before
      connecting the collector to IN.
- [ ] Write a second sketch that closes the rail on a serial command, so the relay can be commanded
      on deliberately rather than by touching a wire to ground.
- [ ] Verify on USB alone, no pack: relay silent with GPIO27 low, and it clicks on command. Then
      press EN and confirm it does not click during the reset — that is the boot window.
- [ ] Only then, pack in: PCA9685 V+ reads 0V with the rail off and 6.0V with it on, **no servo
      connected.**
- [ ] Update `current-power-&-wiring-connections.md`, write `main-steps/6-relay-control.md`, update
      this file, one commit.

---

## Backlog — ordered, one per session, never two in the same evening

1. **One single servo.** Centered at 1500µs. One, not twelve.
2. **The remaining eleven servos**, on michaelkubina's channel map: front left 0/1/2, front right
   3/4/5, rear left 6/7/8, rear right 9/10/11, in the order shoulder, upper leg, lower leg. The
   replacement servos arrived on 2026-08-27, so nothing waits on delivery any more.
3. **Reinforce the PCA9685's V+ and GND traces with solder.** Leika's own documentation recommends
   it, and those traces are the narrowest point of the whole servo power path — narrower than the
   AWG16 feeding them. Before the robot carries its own weight.
4. **Leika: build and flash.** PlatformIO, submodules, filesystem image. Calibrate all twelve
   channels. **Leika has no relay support**: GPIO27 will never be driven, so the servo rail will
   stay open until a two-line addition is made to its setup, or a link replaces the relay.
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
  on, like the other ten. That needs a working PCA9685, so it cannot happen before backlog item 2.
- **Is the relay module's contact rating enough?** **Answered in session 5.** The module is an
  SRD-05VDC-SL-C, printed 10A 250VAC / 10A 30VDC. On a 6V rail the margin is large and no part needs
  changing. The rule that follows is about use, not rating: what kills relay contacts on DC is
  breaking under load and capacitor inrush, so the relay is only ever switched with the servos idle.
- **Does Leika expect the relay on GPIO27?** **Answered in session 5: it expects no relay at all.**
  See the firmware section above.
- **Will the NPN stage actually switch this module?** The base resistor value assumes an ordinary
  small-signal NPN and a module whose input needs a few milliamps. If the relay does not pull in
  cleanly with 1k, the next step is to measure the current the IN pin draws when grounded and size
  the base resistor from that number rather than from a guess.

---

## Safety gates

- The pack stays disconnected while anything on the power path is being changed.
- The SZBK07 heatsink bars are live at battery potential. Nothing at ground touches them, no metal
  tool near them while powered, and they never get mounted against a conductive surface.
- The relay stays OFF unless a servo test is actively running, and it is only ever switched with the
  servos idle — never under load.
- **No servo is connected until the relay can be commanded off and on deterministically.** Until the
  transistor stage exists, the rail can only be closed by touching a wire to ground, which is not a
  control.
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
