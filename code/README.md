# Code

Test sketches for this build. Each one does a single thing and nothing else — that is the point.
When something stops working, the fastest way to find out whether the fault is in the wiring or in
the code is to flash the smallest program that can answer the question.

These are Arduino IDE sketches, board **ESP32 Dev Module**. Each lives in a folder with the same
name as its `.ino`, which is what the Arduino IDE expects, so they open by double-clicking.

The real firmware is not here. It is [Leika by
runeharlyk](https://github.com/runeharlyk/SpotMicroESP32-Leika), it builds with PlatformIO, and it
comes at the end of the backlog in `STATE.md`.

---

## `i2c_scanner`

Walks every I2C address and prints the ones that answer. The first thing to flash after wiring the
bus, and the first thing to re-flash whenever a device goes quiet.

Serial monitor at **115200 baud**. Expected output on this build:

```
I2C scanner
Device found at 0x40
Device found at 0x68
---
```

**0x40** is the PCA9685 and **0x68** is the MPU6050 — 0x69 instead, if that board's AD0 pin is
pulled high.

Reading the result:

- **Nothing found at all** — the bus itself is the problem. Check SDA on GPIO21 and SCL on GPIO22,
  and that the pull-ups have a supply: on this build they tie to the PCA9685's VCC, which sits on
  3.3V, not on the 5V bar.
- **One device answers and another does not** — the bus is fine and the silent board is the
  suspect. Check its own supply and its two bus wires.

Before blaming either, pull on every Dupont wire sitting in a WAGO connector. They are thinner than
those connectors are rated for and one of them has already failed to make contact once, in session
4.

## `servo_center`

Drives PCA9685 channel 0 to 1500µs, the servo centre, and holds it. Used to centre a servo before its
horn goes on, and as the smallest test that the whole chain — ESP32, I2C, PCA9685, 6V rail — works
under a real load. Needs **Adafruit PWM Servo Driver Library** (3.0.3 used).

Flash on USB with the XT60 unplugged. Then unplug USB, plug the servo into channel 0 (brown GND, red
V+, orange PWM) and connect the pack. The servo moves once and holds. USB and the pack never go in
together — see `Power-Up & Power-Down Procedures.md`.

---

## `relay_off_on_safe` — retired

Kept only as a record. It drove GPIO27 high to hold the servo rail relay open, on the assumption
that the module was active-low with a plain input. Session 5 found its input is a PNP base that no
ESP32 pin can hold open, and the planned 10k pull-up would not have helped. The relay was removed in
session 6: the servo rail now follows the pack, as in Leika.
