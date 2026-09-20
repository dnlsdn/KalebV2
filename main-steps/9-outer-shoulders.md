# Session 09 — The Legs onto the Outer Shoulders

**Date:** September 20, 2026

## What I set out to do

michaelkubina's "Connecting to the Shoulders": screw two servohorns to each Outer Shoulder piece and
hang a pair of legs from each. It is also the step that answers what session 8 could not verify —
the sense of the shoulder joint offset and which way each shoulder servo's shaft faces — because the
outer shoulder pieces only fit one way.

## What I actually did

- **Two horns per Outer Shoulder piece**, screwed through the middle hole of each arm with M2x8 and
  an M2 nut on every screw. Without the nut the screw stands proud on the other side and fouls the
  servo.
- **Two legs per piece**, front pair on one and rear pair on the other. The shoulder servos were left
  at the 90° set in session 8; each leg was dry-fitted onto its horn, checked square against the
  piece, and then fixed with one M3x8 through the centre of the horn.
- The tape labels on the legs were rewritten with the real channel map before assembly: front left
  0/1/2, front right 3/4/5, rear left 6/7/8, rear right 9/10/11.

## What was verified

Photographs of both groups: in each one the two legs hang **parallel and symmetric**, perpendicular
to their Outer Shoulder piece, and the horns sit flat. Nothing came out reversed, which also clears
the shoulder servo shaft direction within each pair.

The one thing still unverified is that the two pieces face **outwards** — the front group's plate
towards the nose, the rear group's towards the tail. That settles itself when the groups go onto the
chassis, since the shoulder blocks only bolt on one way.

## Printing, in parallel

`docs/print-list.md` now holds everything still to print, in the order it is needed, with quantities,
infill and which files are deprecated. Printed so far from the chassis group: Inner Shoulder, Chassis
Side, Top Shoulder and Bottom Shoulder, two of each. On the printer: the circuitry mounting plate,
the **SZBK07 Extended** version, because the big step-down on this build is the SZBK07. Left after
that: the three LiPo brackets.

## What is still open

- **The ball bearings.** The Body step needs 4x 625zz for the shoulder joints. The bill of materials
  lists 8x for the whole robot and four went into the legs; check four are left before that session.
- **Charge the pack** before all twelve servos are powered together.
- The hip travel check — more room backwards than forwards — is still worth doing once the robot
  stands on its chassis and "forward" is unambiguous.
