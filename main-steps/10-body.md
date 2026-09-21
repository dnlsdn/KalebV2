# Session 10 — The Body, and the Legs onto It

**Date:** September 21, 2026

## What I set out to do

michaelkubina's "Body" and "Mount legs to chassis": build the chassis frame around the circuitry
mounting plate and bolt the two leg groups to it. The mounting plate went in **empty**: the bench
electronics work and were measured piece by piece, so they move into the robot only after all twelve
servos have run on the bench. If something fails then, it is the servos and not a freshly redone
harness.

## What I actually did

- **Inner shoulders.** A Top Shoulder and a Bottom Shoulder block on each Inner Shoulder, two M3 nuts
  per block, screws from the face of the Inner Shoulder around its central opening. The first attempt
  "did not reach": each block has four hex pockets, two for this joint and two for the covers later,
  and the nuts have to sit in the two that line up with the plate's holes.
- **Chassis.** Four M3 nuts in each Chassis Side, flat face outwards, the long cutout at the bottom;
  the mounting plate slid into the cutouts; the two inner shoulder groups at the ends with four M3x8
  each, large block on top.
- **Legs.** A 625zz bearing on the pin of each shoulder block, running in the round holes of the inner
  shoulder; each Outer Shoulder bolted to its blocks with four M3x8. Front group towards the nose,
  rear towards the tail.

The mounting plate is `Circuitry_Mountingplate_SZBK07_Extended`. Its raised parts and standoffs are
michaelkubina's mounts for his own layout — the square tower sits next to where he puts the relay and
a USB breakout. Which way round the plate goes is not documented; it slides either way and is decided
when the electronics move in.

## What was checked, and a worry that turned out to be the design

**The shoulders.** Each shoulder servo driven to 90° with `servo_angle`: all four legs came out
perpendicular to their Outer Shoulder.

**All four thighs slope the same way**, front and rear, which looked wrong and made the robot rest
with one pair of feet off the table. It is the design: michaelkubina's own photo of his robot and the
guide's render both show every thigh sloping towards the tail and every knee pointing back. A front
left and a rear left leg are the same part; only the shoulder block is mirrored. The robot does not
rest level now because the legs sit in their assembly pose, knees fully closed at 0°/180°, and an
unpowered robot holds no pose at all. michaelkubina keeps his on a block under the belly for the same
reason.

## What is still open

- **The hips moved during assembly.** While the shoulder joints were fitted, the hip shafts turned,
  so their horns are no longer seated exactly at 120°/60°. Decided: finish assembling, check later.
  An error under about 15° is corrected in Leika's per-servo offset; a large one costs travel at one
  end of the joint and has to be fixed by re-seating the horn. **First thing of the next electrical
  session.**
- **The resting pose** under Leika has not been seen yet. Command it with the robot lifted and check it
  sits level.
- **A stand.** The robot must rest on a support whenever it is off. Leika ships one in
  `hardware/printable/helper_stand`; added to `docs/print-list.md`.
- **Moving the electronics in**: which way round the mounting plate goes, and whether the two 12-screw
  bus bars fit on it at all.

<img width="823" height="658" alt="image" src="https://github.com/user-attachments/assets/b188c35b-94b0-4e0f-a2f3-c3c2fe4fa764" />
