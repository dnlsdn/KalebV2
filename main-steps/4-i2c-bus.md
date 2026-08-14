# Session 04 — The I2C Bus, and the First Code This Robot Has Ever Run

**Date:** August 14, 2026

## What I set out to do

Wire the I2C bus between the ESP32, the PCA9685 and the MPU6050, and flash an I2C scanner. Nothing
else. No servo power, no servos connected, battery disconnected and the fuse out for the whole
session — the ESP32 ran from the computer's USB.

This is the step with no alternative in the whole project: the PCA9685 only speaks I2C, so until
this bus works, no servo can ever be given a command.

## What I found before I started

With the battery disconnected and the fuse out, I plugged the ESP32 into USB and measured the red
bus bar against the black one. It reads **4.93V**, not zero.

The ESP32's VIN pin is tied to the red bus bar, and USB power comes back out of VIN onto the bar,
waking up everything attached to it — relay, ACS712, both HC-SR04. At 4.93V against a nominal 5V,
this board clearly has no meaningful diode drop on that path.

Nothing about it is harmful, it is a few tens of milliamps. But it means **"battery disconnected"
does not mean "nothing is powered"** on this bench, and I would rather know that from a measurement
than discover it with a probe in my hand some evening.

## Moving the PCA9685 to 3.3V

The roadmap said the PCA9685 should sit on 3.3V while the wiring file said it was on the 5V bar.
Before changing anything I wanted to know whether that mattered, so with everything unpowered and
the VCC wire pulled off the bar I measured the resistance between the board's SDA pin and its VCC
pin, then SCL and VCC.

Both read **9.96kΩ**. The board carries 10k I2C pull-up resistors tied to VCC.

That settles it. Those pull-ups are what hold SDA and SCL high when nobody is driving them, so
**VCC sets the idle voltage of the entire bus**. Left on the 5V bar, both lines would have idled at
5V and sat 1.4V above the ESP32's absolute maximum of 3.6V — the same over-voltage problem as the
HC-SR04 ECHO lines, on two more pins, permanently. Moved to the ESP32's 3V3 pin, the whole bus
idles at 3.3V and needs no level shifting anywhere.

The fix removes complexity instead of adding it: one wire moved, and a problem that would have
needed level shifters stops existing.

## The WAGO problem

The ESP32 has a single 3V3 pin and two boards needed it, and SDA and SCL each had to reach two
boards from one GPIO. Three three-way junctions, so three WAGO connectors — the same approach
already used to split the ACS712 output, rather than a new kind of component.

**WAGO 221 connectors are specified from 0.14mm² upward. Dupont wire is about 0.08mm².** It is
below the minimum, and the lever does not reliably grip it.

This is not theoretical. On the continuity check before powering anything, SDA to GPIO21 did not
beep, and instead showed a resistance that climbed rather than settling — the meter charging the
bus capacitance through a path that was not really a connection. The wire was sitting in the WAGO
without being clamped.

The fix: strip three or four millimetres instead of the usual, fold the conductor back on itself to
double its cross-section, reinsert, and tug every wire afterwards. After that it beeped.

Worth stating plainly, because it is the failure this build keeps circling: that connection looked
finished. Powering up with it in place would have produced a scanner that found the MPU6050 and not
the PCA9685, and the obvious suspect would have been the code.

## What I verified with the multimeter

All with USB disconnected, in continuity mode.

Beeping, as required: PCA9685 VCC and MPU6050 VCC against the ESP32 3V3 pin; both SDA pins against
GPIO21; both SCL pins against GPIO22; PCA9685 OE against the black bus bar; both grounds against
the black bus bar.

Silent, as required: SDA against SCL — the mistake worth fearing with three identical connectors in
a row; the 3.3V WAGO against both bus bars; PCA9685 VCC against the red bus bar, confirming the old
wire was really gone.

Every wire in the three WAGOs was pulled on by hand after the lever was closed.

## The scanner

Arduino IDE, ESP32 Dev Module, an I2C scanner and nothing else on the board.

```
I2C scanner
Device found at 0x40
Device found at 0x68
---
```

**0x40 is the PCA9685 and 0x68 is the MPU6050.** Both answer. The bus works.

This is the first firmware ever flashed on this build.

## What is still open

- The relay contact rating has not been checked against what twelve MG996R can pull.
- Whether Leika expects the relay on GPIO27 is still unconfirmed in its source.
- Four replacement MG996R-180 were ordered today, estimated 23-28 August. Two servos had failed,
  most likely overloaded during testing on the old wiring that was scrapped in April.

## Current state

The power path is wired and verified, and now the I2C bus is too. The ESP32 can reach the servo
driver and the IMU. Nothing has ever been powered on the 6V rail, no servo has ever moved, and the
PCA9685 V+ pin is still deliberately disconnected.

Next session is the 6V servo rail and the relay: SZBK07 OUT+ to relay COM, relay NO to PCA9685 V+,
the 1000µF capacitor, and the relay control wire to GPIO27 with its 10k pull-up. End state is a
servo rail that can be switched on and off on command, with still no servo attached to it.
