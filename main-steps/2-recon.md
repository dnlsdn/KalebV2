# Session 02 — Recon After a Long Break

**Date:** July 31, 2026

## What I did

Three and a half months had passed since the rewiring in session 1, so instead of picking up the
soldering iron I spent this session checking whether the bench still matched what I had written
down. No wiring was changed and nothing was soldered. The only goal was to find out what is true
right now.

I started with the battery, disconnected from everything. The pack is not swollen and the wires at
the connector are intact. Measured on the balance connector, cell 1 reads 3.78V and cell 2 reads
3.78V, with the whole pack at 7.55V. That is a healthy resting voltage, the two cells are identical
so there is no imbalance, and the sum of the cells matches the pack reading.

Then, still with the battery disconnected, I went through the wiring with the multimeter in
continuity mode. First the important one: the red bus bar against the black bus bar stays silent,
so there is no short between the 5V rail and ground. Then the ground star, testing the black bus
bar against the ground pin of every board: ESP32, PCA9685, relay module, ACS712 and both HC-SR04
all beep. Then the same against the red bus bar for the supply pins: ESP32 VIN, PCA9685 VCC, relay
VCC, ACS712 VCC and both HC-SR04 VCC all beep.

The ESP32 ground was the one connection worth a closer look. On the first attempt the resistance
climbed instead of settling, which can mean a poor contact rather than a real connection. Measured
again in resistance mode it sits at 0.005 ohm against a 0.000 ohm probe-to-probe reference, so the
connection is solid and the first reading was just the probe not touching properly.

Only at the end did I connect the battery and insert the fuse, and only for as long as the
measurements took. With the logic powered, the 5V rail reads 4.98V at the bus bar, the SZBK07
output reads 6.00V, and the voltage after the fuse reads 7.55V, exactly the pack voltage. Then I
pulled the fuse and disconnected the battery.

## What I found out

**The SZBK07 heatsink is live.** The two metal bars on the sides of the converter beep against the
positive input terminal, which means they sit at battery potential whenever the pack is connected.
They do not beep against ground, so nothing is shorting right now. From here on, nothing at ground
potential may touch those bars, no metal tool goes near them while the robot is powered, and when
the electronics move into the chassis that module cannot sit on a conductive surface — its mounting
screws have to be treated as live.

**The relay pin question is settled.** The roadmap said GPIO5 while `relay-off-on-safe.md` already
used GPIO25 in working code, so 25 is the one that was actually built. GPIO5 is also a strapping
pin, which the ESP32 reads at boot to decide how to start, so it is a poor choice for switching a
load. The roadmap now says GPIO25 everywhere.

**The voltage divider in the roadmap is drawn upside down.** Going over the plan for the next
session I noticed the ECHO divider is specified as 2kΩ in series and 1kΩ to ground, which delivers
one third of 5V, so 1.67V. The ESP32 needs around 2.5V before it reads a pin as high, so that
circuit would have produced sensors that behave erratically or never trigger at all. The series
resistor has to be the 1kΩ and the 2kΩ goes from the node to ground, giving 3.33V. Found on paper
before any resistor was soldered.

**The 5V rail reads 4.98V, not the 5.00V it was trimmed to.** That is the logic drawing current:
the regulator was set with nothing attached to it. Two tens of a percent is well inside what the
logic needs, so the trimmer was left alone.

**The 6.00V on the servo rail does not mean much yet.** Nothing is drawing from that branch. The
reading that matters is the one taken while the servos are actually pulling current, and that
measurement still has to be made.

## Documentation cleaned up

The Italian translation of the electronics roadmap was deleted. The repository is in English only,
so no document has a twin that can quietly drift out of sync with it. The remaining file was
renamed from `Electronis-Roadmap-EN.md` to `Electronics-Roadmap.md`, fixing the typo and dropping a
language suffix that no longer means anything.

`current-power-&-wiring-connections.md` was rewritten. It still described the wiring that was torn
out in April, which would have sent me down the wrong path sooner or later.

`STATE.md` was added at the root of the repository. It holds the current state of the build and the
next session, and it gets updated in the same commit as each session log.

## Current state

The power path and the 5V logic rail are wired, and now verified rather than remembered. The
battery is good but sits at about half charge, so it needs a top-up before any test that actually
drives the servos. The 6V servo rail, the relay control wire, the I2C bus, the signal pins and the
twelve servos are all still to be done, and no firmware has ever been flashed on this build.

Next session is the voltage dividers on the HC-SR04 ECHO lines, which are the one real hazard left
on the bench.
