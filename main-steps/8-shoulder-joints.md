# Session 08 — Shoulder Joints onto the Legs

**Date:** September 20, 2026

## What I set out to do

Do michaelkubina's step "Attach Shoulder Joint to upper Leg" on all four legs, and the step after it,
"Attach Servo to Shoulder Joint". This was believed to be done already; it was not. The legs were
finished up to "Complete Upper Leg", with the hip servo shafts bare and the four shoulder joint
sub-assemblies built but not fitted.

## The angles, and a correction to this repo

The reference guide does **not** put every servo at its centre. Each joint has its own position,
set before the horn goes on:

| Joint | Left legs | Right legs |
|---|---|---|
| Wrist (lower leg) | 0° | 180° |
| Upper leg (hip) | 120° | 60° |
| Shoulder | 90° | 90° |

The wrists were done that way in November 2025 (`Step_1-Wrist-Calibration-and-Assembly.md`, in the
git history). `STATE.md` claimed "ten of the twelve servos were centered at 1500µs", which was wrong
and is corrected there now.

Leika's own defaults agree with this geometry: at the servo centre it expects the shoulder neutral,
the upper leg about 45° off and the knee bent 90°, and it calibrates the remainder per channel in
software.

## What I actually did

**A sketch for arbitrary angles.** `code/servo_angle`, from `servo_center`, with a constant `ANGLE`
and a conversion that matches the Arduino `Servo` library used on the wrists in November: 0° = 544µs,
180° = 2400µs, so 60° = 1163µs, 90° = 1472µs, 120° = 1781µs. Three flashes covered the session.

**Per leg**, with the pack disconnected whenever a servo was plugged or unplugged, and USB never in
at the same time as the pack:

1. `ANGLE = 120`, both left hip servos driven and left alone.
2. Shoulder joints fitted on the left legs. The horn is not aligned with the arm that runs along the
   leg but with the next one round — one arm is 60°, one spline tooth is 14.4°.
3. `ANGLE = 60`, both right hip servos, then their shoulder joints, mirrored.
4. `ANGLE = 90`, the four shoulder servos, then each screwed into its joint with 4x M3x20.

The replacement servo centred at 1500µs in session 7 was re-driven to 90° (1472µs) so all four
shoulder servos match.

## What was verified

Photographs down the hip axis, compared against the guide's figure: on every leg the block stays
square while the thigh leaves it at roughly **30°**, and the pairs are **mirror images** of each
other.

**What could not be verified from photographs** is the sense of the one-arm offset — mirroring the
image mirrors the answer. If it is wrong it shows up during Leika's calibration as a leg that runs
out of travel forward instead of backward, and the fix is one screw: pull the block, rotate it two
arms, screw it back.

The direction each shoulder servo's shaft faces (towards the nose for the front legs, towards the
tail for the rear) was not checked either. The outer shoulder pieces only fit one way, so the next
mechanical step settles it.

## What is still open

- Sense of the shoulder joint offset, and shaft direction: both settle at
  "Connecting to the Shoulders".
- **Charge the pack** before all twelve servos are powered together.
- The tape labels on the legs carry an old channel map. They have to be rewritten to
  michaelkubina's — front left 0/1/2, front right 3/4/5, rear left 6/7/8, rear right 9/10/11 —
  before anything is wired.

<img width="482" height="656" alt="image" src="https://github.com/user-attachments/assets/63946c58-df6f-4bc9-9514-6bcb49919129" />
