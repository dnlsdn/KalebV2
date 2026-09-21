# Session 11 — Every Joint Back to Its Mounting Angle

**Date:** September 21, 2026

## What I set out to do

Check the four hips, which moved while the shoulder joints were fitted in session 10. Extended on the
spot to all twelve servos: each one driven to the angle it was mounted at, to find anything that
would need re-seating before calibration rather than after.

This is a mounting check, not calibration. Leika's calibration comes later and finds each servo's
travel and fine offset; this finds horns seated a spline or an arm off.

## How

The assembled robot on a box, legs hanging free. `code/servo_angle`, one servo at a time on
PCA9685 channel 0, pack unplugged whenever a servo was plugged or unplugged, USB never in with the
pack. Channel numbers below are the servos' names from the tape labels, not the channel they were on.

| Joint | Servos | Angle | Expected |
|---|---|---|---|
| Shoulder | ch0 ch3 ch6 ch9 | 90° | leg perpendicular to its Outer Shoulder |
| Upper leg | ch1 ch7 / ch4 ch10 | 120° / 60° | thigh about 30° from its shoulder block, sloping to the tail |
| Wrist | ch2 ch8 / ch5 ch11 | 0° / 180° | knee closed |

## What was found

- **Shoulders:** all four right (checked in session 10, unchanged).
- **Upper legs:** some had moved, as expected from session 10, and were corrected until all four sat
  at their reference angle. Which ones and by how much was not written down.
- **Wrists:** the two left knees matched each other. **The rear right knee (ch11) was about 60°
  open** at 180°, where the front right was closed. 60° is exactly one arm of the six-arm horn: it
  had been seated one arm off in November. The guide warns about exactly this in "Servohorn mount" —
  the 25-tooth spline is not symmetric, so which arm sits on top matters.

Left alone, that knee could never have closed fully: it would have hit the end of its travel 60°
early, and the robot would have rested crooked on that leg. Leika's offset cannot fix travel.

## The fix, without opening the leg

The knee horn is held to the servohorn mount by small M2 screws and to the servo shaft by the centre
screw. With ch11 driven to 180° and the pack unplugged, the M2 screws came out, the mount turned one
arm relative to the horn so that the knee closed, and everything went back in the same holes. Re-driven
to 180°: **closed like the front right, and no buzzing** — the guide's warning is a servo that ends
up pushing against the thigh at 0°/180° and stutters.

## What is still open

- **Charge the pack**, balance charge, before twelve servos are powered together.
- Twelve servos on their real channels, one channel at a time.
