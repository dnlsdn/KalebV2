# Session 07 — The First Servo That Moves

**Date:** September 19, 2026

## What I set out to do

Move one servo, not twelve: drive PCA9685 channel 0 to 1500µs and watch a servo go to its centre and
hold. One servo proves the whole chain — ESP32, I2C, PCA9685, 6V rail — under a real load, and if
something is wrong there is only one place to look.

The servo was one of the two replacements, horn off. It has to be centred before its horn goes on
anyway, so the first test did a real job.

## Two things settled before starting

**The pack did not need charging for this.** Measured on the XT60 and the balance lead: **7.55V**
total, **3.78V** on each cell, perfectly balanced and unchanged since session 5. Half charge is
plenty for one servo with no load. The charge is needed before several servos move together.

**USB and the pack never go in together.** Espressif's ESP32-DevKitC user guide states that power
must come from one and only one of USB, the 5V pin or the 3V3 pin, "otherwise the board and/or the
power supply source can be damaged". On this build the 5V pin is fed from the red bus bar, so a
connected pack plus a USB cable is exactly that. The procedure written in session 6 allowed it and
was wrong. The workflow is now: flash on USB with the XT60 unplugged, unplug USB, then connect the
pack. The sketch runs from flash.

## What I actually did

- Installed **Adafruit PWM Servo Driver Library 3.0.3** in the Arduino IDE.
- Wrote `code/servo_center`: I2C on 21/22, PCA9685 at 0x40, 50Hz, channel 0 to 1500µs, empty
  `loop()`. The PCA9685 repeats the pulse on its own, so the command is sent once, in `setup()`.
- Flashed it on USB, XT60 unplugged, no servo connected.
- Unplugged USB, plugged the servo into channel 0 (brown GND, red V+, orange PWM), connected the XT60.
  The servo moved once to its centre and held.

**The oscillator question, and why it did not matter.** The sketch assumes the PCA9685's nominal
25MHz; real boards run anywhere from 23 to 27MHz, so "1500µs" can land some tens of microseconds off.
Measuring it was considered and dropped: the MG996R spline has 25 teeth, so a horn can only be seated
in steps of 14.4°, and an 8% oscillator error moves the centre by less than one tooth. Leika
calibrates every channel later anyway.

## What I verified with the multimeter

Pack connected, USB unplugged, servo holding its centre:

| Measurement | Reading |
|---|---|
| PCA9685 V+ ↔ black bus bar | **6.0V** |
| Red bus bar ↔ black bus bar | **4.98V** |

The 6V rail does not sag under one holding servo, and the logic rail does not notice it.

## What is still open

- **This servo is centred but its horn is not on.** Unpowered, its gears hold the position; the
  shaft must not be turned by hand until the horn is seated.
- **The second replacement servo** still has to be centred, with the same sketch on channel 0.
- **Which two leg positions are waiting for the replacements** is not recorded here.
- **Charge the pack** before more than one servo is powered.
