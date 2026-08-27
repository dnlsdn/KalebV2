# Session 05 — The 6V Servo Rail, and a Relay That Cannot Be Commanded at 3.3V

**Date:** August 27, 2026

## What I set out to do

Wire the 6V servo rail: SZBK07 to the relay, the relay to the PCA9685's V+, the relay's control pin
to GPIO27, and verify with the multimeter that the rail reads 0V with the relay open and 6V with it
closed. No servo connected at any point, pack disconnected and fuse out for the whole build, fuse in
only at the end for the measurement.

The rail was verified. The control pin was not — and the reason is the most useful thing this
session produced.

## Two open questions answered before touching anything

**Is the relay module's contact rating enough?** The module is an **SRD-05VDC-SL-C**, printed
`10A 250VAC / 10A 125VAC / 10A 30VDC / 10A 28VDC`. The rail is 6V, so the voltage margin is a factor
of five. The rating is adequate and no part needs changing.

The real caveat is not the number but how it is used: what destroys relay contacts on DC is breaking
under load and the inrush of charging capacitance, not steady current. **The relay is only ever
switched with the servos idle** — rail on before the PCA9685 sends pulses, off after it stops.

**Does Leika expect the relay on GPIO27?** No. I searched the whole repository: **Leika contains no
relay at all**, in code or in its component list, which specifies a manual main power switch instead.
Leika does confirm SDA 21 / SCL 22, matching this build, and it has an `[env:esp32dev]` target, so a
plain ESP32 is supported.

The consequence is worth writing down now rather than rediscovering it later: **when Leika is flashed,
nothing will ever drive GPIO27**, so the servo rail will stay open and the servos will get no power.
That is a two-line patch in Leika's setup, or a bypass link in place of the relay, and it belongs to
the session where Leika is flashed. It is now in the backlog instead of being a surprise.

## Power side — what got wired

- **SZBK07 OUT+ to relay COM**, AWG14. The NO terminal was identified by measurement rather than by
  the silkscreen, which is not in a language I read: at rest a relay has exactly one closed contact,
  COM–NC, so the terminal with continuity to nothing is NO. No guessing involved.
- **Relay NO to PCA9685 V+**, **AWG16** — not AWG14 as planned. The green 2-pole screw terminal on
  the PCA9685 is a 3.5mm-pitch block rated to 1.5mm², and AWG14 at 2.08mm² does not fit by design.
  Thinning the AWG14 by cutting strands was rejected: it reduces the section exactly where the
  mechanical stress is, and the cut strands sit millimetres from the GND screw.
- **PCA9685 GND to the black bus bar**, AWG16. **This connection was not in the session plan and it
  should have been.** The plan described how servo current gets in and said nothing about how it gets
  back out. The PCA9685's ground reached the bar through a Dupont wire sized when that board drew
  logic current only. Twelve MG996R returning through 0.08mm² is the same mistake as the V+ side,
  seen from the other end of the circuit, and it would not have shown up until something got hot.
  The old Dupont was removed once the AWG16 was in.

AWG16 is the right conductor here and not a compromise. The run is short, so the resistance
difference against AWG14 is in the milliohms; the current is capped upstream by a 10A relay; and the
real bottleneck is downstream anyway — the PCA9685's own V+ traces are thin, which is why Leika's
documentation recommends reinforcing them with solder. That reinforcement is now in the backlog.

## The capacitor that did not need to be added

The plan called for a 1000µF capacitor local to the PCA9685. **This board already has one, 1000µF
10V, fitted on the servo rail.** Verified rather than assumed: its positive leg beeps against the
`V+` screw and its negative against `GND`, so it sits on the servo rail and not on the 3.3V logic
supply.

A second capacitor was deliberately **not** added. Capacitance in parallel simply adds, and 2000µF
would do no harm in itself, but the inrush through the relay contacts at closing scales with it, and
contact life is a standing concern on this build. 10V of working voltage on a 6V rail is adequate
margin.

The 1000µF 16V from the drawer is kept as a documented remedy: if the ESP32 browns out or the
PCA9685 drops off the bus once twelve servos move together, that is the signature of a rail
collapsing on peaks, and the cure is more bulk capacitance — added **before the relay, on the SZBK07
output**, so it does not make the contact inrush worse.

## Continuity checks before any power

Pack out, fuse out, USB unplugged, so the relay coil was genuinely at rest.

| Check | Result |
|---|---|
| SZBK07 OUT+ ↔ PCA9685 V+ | open — the relay is really open at rest, and the wire is on NO, not NC |
| PCA9685 V+ ↔ black bus bar | open — no short across the servo rail |
| PCA9685 V+ ↔ PCA9685 GND | open — no strand bridging inside the green terminal |
| PCA9685 OE ↔ black bus bar | continuity — OE is still grounded after the Dupont was removed |
| Onboard capacitor legs ↔ V+ and GND | continuity on both — it is on the servo rail |

OE was checked because it had not occurred to me until the ground wire was rerouted: OE is
active-low, and if it floats high all twelve PWM outputs are disabled. That failure looks exactly
like a firmware bug and is not one.

## The relay module cannot be held off by 3.3V

This is the finding of the session, and it came out of refusing to install a part on faith.

The plan called for a 10k pull-up from GPIO27 to 3.3V, to hold the servo rail open during the
milliseconds between power-up and the first line of `setup()`. Before soldering it I measured what
the module actually does with its IN pin left floating. Battery out, so the contacts switched
nothing.

| Measurement | Reading |
|---|---|
| Red bus bar (USB back-feed, no battery) | 4.91V |
| IN pin, floating, module powered | **4.2V** |
| IN ↔ VCC, module unpowered, ohms | open — no resistive path |
| IN with a 10k to ground | relay chatters on the switching threshold |
| GPIO27 driven high by `relay_off_on_safe`, IN disconnected | 3.1V |
| IN connected to GPIO27, sketch driving high | **relay closed**, COM–NO continuity, node at 2.0V |

Every one of those fits a single explanation. The IN pin is the base of a **PNP transistor with its
emitter on VCC**. The 4.2V is not a resistive pull-up — it is 4.93V minus one base-emitter drop,
which is also why the ohmmeter finds nothing between IN and VCC: a junction, not a resistor, and the
sub-half-volt test voltage of an ohmmeter cannot turn it on. The relay is therefore off only while
**IN sits above roughly 4.2V**.

And an ESP32 pin can never sit above 4.2V. Driven high it reaches 3.3V — 3.1V measured on this
board. Left in high impedance it is clamped by the ESP32's own protection diode at around 3.9V. Both
are below the threshold, so **no state of the software can hold this relay open with GPIO27 wired
straight to IN**. The pin was doing its job correctly; the module simply cannot be spoken to at this
voltage.

The 2.0V measured on the node while the relay was closed is the red bus bar sagging: with the coil
energised, the bar was being fed backwards through the ESP32's VIN pin from USB, which is a weak
path.

**The 10k pull-up was therefore not installed, and it never should have been.** GPIO27 and IN are one
electrical node — the external resistor and the module's own clamp would have pulled the same wire in
the same direction, and at 3.3V rather than the 4.2V the module needs. It was redundant against a
problem it could not have solved.

The related worry about GPIO27 seeing 4.2V during boot, above the ESP32's 3.6V absolute maximum, is
closed by the same measurement: a 10k to ground was enough to drag that node to its threshold, so the
source impedance is of the order of kilohms and the current into the protection clamp is around a
tenth of a milliamp, for the duration of a boot. **No series resistor is needed.** This is written
down so the omission reads as a decision and not as something forgotten.

## What was verified with the pack connected

USB unplugged, so the battery was the only source and the numbers are the real operating ones. The
Dupont between IN and GPIO27 was removed, which leaves the relay open by its own nature.

| Measurement | Reading |
|---|---|
| SZBK07 OUT+ ↔ black bus bar | **6.0V** — the rail is live up to the relay |
| PCA9685 V+ ↔ black bus bar, relay open | **no voltage** — the meter's auto V/Ω mode fell back to resistance, which is what it does when there is nothing to measure |
| PCA9685 V+ ↔ black bus bar, IN momentarily grounded by hand | **6.0V**, returning to nothing when the wire was lifted |

No servo was connected for any of it. The PCA9685 received V+ for the first time in this project
tonight, with nothing on its outputs.

**The 6V servo rail exists, reaches the PCA9685, and the relay genuinely isolates it.** That was the
goal of the session and it is met. What is missing is only the way to command it.

## What is still open

- **The NPN stage between GPIO27 and IN.** The fix for the level problem, and the first job of the
  next session. It inverts the command and decouples the levels, and it has a property the original
  plan did not: with the transistor off, IN is simply left alone at its natural 4.2V and **the relay
  is open by default**, with no software involved. Safer than what was planned.
- **`code/relay_off_on_safe` will need rewriting** once that stage exists, because the sense of the
  pin inverts: GPIO27 high will mean relay on.
- **The black bus bar has one free position left.** The only thing still queued for it is the battery
  voltage sensor, which comes after the robot walks. When it is needed, a WAGO tapped off the bar or a
  second bar solves it.
- **The two replacement servos arrived on August 27** and are on the bench. They are still not
  centred at 1500µs, and cannot be until the rail can be commanded.
