# What is left to print

Source: [michaelkubina's part list](https://github.com/michaelkubina/SpotMicroESP32/blob/master/parts/SpotMicroESP32_parts_v1_0_0/README.md)
and the [STL folder](https://github.com/michaelkubina/SpotMicroESP32/tree/master/parts/SpotMicroESP32_parts_v1_0_0/stl).
Quantities and infill are his; the order and the notes are this build's.

**Already printed:** every leg part, the four shoulder joints, the two outer shoulders, the foot tips,
and from group 1 the Inner Shoulder, Chassis Side, Top Shoulder and Bottom Shoulder, two of each
(2026-09-20).

**Still to print:** the three LiPo brackets, the stand, then group 2. The circuitry mounting plate
is printed and in the chassis (2026-09-21).

**Material.** PLA for everything structural, as in the reference build. The foot tips are the only
TPU parts and they are done. The design prints **without supports** — that is the point of this
remix, so turn supports off and print parts in the orientation the STL arrives in.

---

## Group 1 — the chassis. Needed before the legs can carry the robot

| Part (STL) | Copies | Mirrored | Infill | Weight | Note |
|---|---|---|---|---|---|
| `Inner_Shoulder.stl` | 2 | no | 20% | 32g each | done |
| `Chassis_Side.stl` | 2 | no | 20% | 22g each | done |
| `Top_Shoulder.stl` | 2 | no | 20% | 20g each | done |
| `Bottom_Shoulder.stl` | 2 | no | 20% | 12g each | done |
| `Circuitry_Mountingplate_SZBK07_Extended.stl` | 1 | no | 20% | 66g | done. **Pick the SZBK07 version**, not the XL4016: that is the big step-down on this build |
| `LiPo_Mountingbracket_Front.stl` | 1 | no | 20% | 5g | |
| `LiPo_Mountingbracket_Middle.stl` | 1 | no | 20% | 3g | |
| `LiPo_Mountingbracket_Rear.stl` | 1 | no | 20% | 7g | |

About 190g. Nothing in this group is mirrored: the two copies are identical prints.

**Why the "Extended" mounting plate.** Both fit the SZBK07. The extended one has more surface, and
this build carries more than the reference: two bus bars, four WAGO connectors, an inline fuse
holder, the ACS712. This is a judgement, not a requirement — the plain `Circuitry_Mountingplate_SZBK07.stl`
also works and weighs 10g less.

## A stand — next, before the servos move

The robot has to sit on a support whenever it is off, and during calibration its legs must move
without touching the table. Leika ships one in
[`hardware/printable/helper_stand`](https://github.com/runeharlyk/SpotMicroESP32-Leika/tree/main/hardware/printable/helper_stand):
`2x_stand_top.stl`, `2x_stand_bottom.stl`, `2x_stand_brace.stl`, `4x_stand_feet.stl` — the prefix is
the quantity. No infill figures are given; 20% like the rest is a reasonable start. A box of the
right height does the same job until it is printed.

## Group 2 — the covers. After the robot walks

All at **100% infill** in the reference list, because they are thin shells.

| Part (STL) | Copies | Infill | Weight |
|---|---|---|---|
| `Front_Cover_Optimized.stl` | 1 | 100% | 58g |
| `Top_Cover_Split_Front.stl` | 1 | 100% | 48g |
| `Top_Cover_Split_Rear_with_OLED.stl` | 1 | 100% | 28g |
| `Bottom_Cover_Split_Front.stl` | 1 | 100% | 46g |
| `Bottom_Cover_Split_Rear.stl` | 1 | 100% | 26g |
| `Rear_Cover_Shell_Long.stl` | 1 | 100% | 40g |
| `Rear_Cover_Plate.stl` | 1 | 100% | 20g |

About 270g. Take the **Split** covers: they print in halves and are screwed together.
`Top_Cover_Split_Rear_with_OLED.stl` has the window for the OLED; its plain twin is marked
deprecated in the reference list.

## Group 3 — only with the camera, which comes last

| Part (STL) | Copies | Infill | Weight |
|---|---|---|---|
| `sensormount_esp32_cam.stl` | 1 | 20% | 17g |
| `cameramount_esp32_cam.stl` | 1 | 20% | 15g |
| `cameramount_esp32_cam_counterpiece.stl` | 1 | 20% | 4g |
| `TTL_Counterpiece.stl` | 1 | 20% | 5g |

Do not print the files marked **deprecated** in the reference list: `Sensormount.stl`,
`Cameramount.stl`, the TFT rear covers, `Front_Cover.stl`, `Top_Cover_Split_Rear.stl`. They belong
to older versions of the head and tail.

`Servohorn_6_B_Star.stl` is only needed if you run out of the horns that ship with the servos.
Twelve are needed in total: four on the knees, four on the shoulder joint caps, four on the outer
shoulders.
