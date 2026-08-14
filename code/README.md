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

## `relay_off_on_safe`

Drives GPIO27 high so the servo rail relay is explicitly open. Flash it before wiring anything to
the relay's control pin.

It is a safety default, not a feature: the relay module is active-low, and between power-up and the
first line of `setup()` nothing drives that pin at all. A **10k pull-up from GPIO27 to 3.3V** is
what actually holds the rail open during those milliseconds. Without it, the 6V rail can close at
boot before the PCA9685 has been told anything, with twelve servos on the other side of it.
