# Session 12 — Twelve Servos on Their Channels

**Date:** September 21, 2026

## What I set out to do

Plug all twelve servos into their real PCA9685 channels and prove every joint answers on its own
channel, before Leika — which assumes the map is right and would make a swapped cable look like a
firmware bug. On the bench, not in the robot: the bench is open and measured, so if something failed
under twelve servos it would not also be a freshly redone harness. Moving the electronics in comes
after, and this session's sketch re-checks the channels in five minutes once it is done.

## Before starting

The pack was balance-charged on a SkyRC B6neo: LiPo, 2S, Balance CHG, 4.20V, 3.0A. It started at 7.52V
and took **3833mAh** to reach 8.40V — about three quarters of 5200mAh, so it had been nearer a quarter
full than the half its resting voltage suggested. Recorded in `STATE.md` with the charging steps.

## What I actually did

- All twelve servos plugged in on michaelkubina's map, shoulder / upper leg / wrist per leg: front
  left 0/1/2, front right 3/4/5, rear left 6/7/8, rear right 9/10/11. Brown on the black row; every
  brown lead checked to be on the same side.
- `code/channel_check`: the twelve mounting angles in an array indexed by channel. `setup()` brings
  each servo to its mounting angle **one every half second**, so the pack never sees twelve servos
  starting together. `loop()` then moves one joint at a time 15° towards the middle of its travel and
  back, and pauses four seconds before starting again from ch0.
- Robot on a box beside the bench, legs hanging free, pack as the only supply.

## What I verified

- **Every channel moved its own joint**, in the expected order, over several rounds. None swapped.
- **No servo buzzing** at its mounting angle, including the wrists at 0° and 180° at the ends of
  their travel.

| Measurement, all twelve holding | Reading |
|---|---|
| PCA9685 V+ ↔ black bus bar | **6.0V** |
| Red bus bar ↔ black bus bar | **5.0V** |

Both rails read what they read unloaded: neither noticed twelve holding servos.

## What is still open

- These are holding servos with no load on a box. Standing and walking draw far more; the PCA9685's
  V+ traces are still to be reinforced before the robot carries its own weight.
- The electronics are still on the bench.
- Leika is next.
