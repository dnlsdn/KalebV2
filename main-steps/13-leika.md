# Session 13 — Leika on the ESP32

**Dates:** September 21, 2026 (computer side) and October 3, 2026 (bench side)

## What I set out to do

Get Leika, the firmware this build follows, running on the robot's ESP32: build it, flash it, and
check from a phone that it sees the PCA9685 and the MPU6050. No calibration and no standing — the
servos stay unpowered for the whole session.

## Before starting

Nothing on the power path was touched. The ESP32 ran on USB with the **XT60 unplugged** throughout,
as Espressif's DevKitC guide requires: USB and the pack never power it together. The pack stayed at
Storage voltage, because nothing tonight needed it.

## What I actually did

**On September 21, at the desk.** PlatformIO installed in VS Code, Leika cloned next to this repo on a
local branch `kalebv2`, three changes for this hardware (board, MPU6050 on and WS2812 off, I2C at
400kHz), and a build that embeds the web app — which needed `protoc`, a dependency Leika's docs do not
mention. All of it is in `firmware/leika-config.md`.

**On October 3, at the bench.** The filesystem image and the firmware flashed without errors. Then
three problems, one after the other, each found by reading the serial log rather than guessing:

1. **Boot loop: `PSRAM chip not found`, then `abort()`.** Leika's shared configuration turns on
   PSRAM — extra RAM on a separate chip — for every board. This ESP32-D0WD-V3 has none, so the
   firmware stopped before it started, rebooted, and did it again forever. Fixed with a configuration
   file that applies to `esp32dev` only, turning PSRAM off and setting the flash to 4MB.
2. **`MPU6050 initialization failed`.** Temporary log lines showed both devices on the bus (0x40, 0x68)
   but the sensor answering `WHO_AM_I` with **0x70** where Leika accepts 0x68 or 0x72. 0x70 is an
   **MPU6500**: the board sold as an MPU6050 carries its close relative, as many cheap GY-521 boards do.
   With 0x70 accepted, its DMP loaded and its start-up calibration completed.
3. **No `Spot-Micro` network on the phone.** Leika booted cleanly and never started its access point.
   A first guess — old Wi-Fi settings left in the NVS by the Arduino sketches — was wrong: erasing the
   NVS changed nothing. A log line in the access point loop then showed the real cause. Before the
   radio is started, the Wi-Fi driver reports the **AP** mode as its default; Leika read that, believed
   its access point was already up, and never turned it on. This is a bug in Leika, not in this
   hardware. Its Wi-Fi class already records the mode it really started, so `getMode()` now returns
   that.

All debug lines were removed before the final build. The six changes are committed on the local
`kalebv2` branch of the clone (`fd7120f`) and written out in `firmware/leika-config.md`.

**From the phone.** The robot's network has no internet, so iOS opens it in a small "Wi-Fi Captive"
window; Safari on `http://192.168.4.1`, after choosing "Use without Internet", works as well. Brave did
not. The app opened on the 3D model of the robot, mode **Deactivated**, which it stayed in.

## What I verified

No multimeter readings this session: nothing on the power path changed, and the servo rail was off.

| Check | Result |
|---|---|
| Bootloader | `SPI Flash Size : 4MB`; the filesystem written at `0x3D0000`, above 2MB, verified |
| Build with the web app | Flash 89.2% (1,753,422 bytes) |
| Access point | `Starting software access point: Spot-Micro`, app served at `192.168.4.1` |
| I2C page in the app | **[40]** and **[68]**, matching the serial log of the same scans |
| IMU page in the app | x, y and z traces; tilting the sensor board by hand moved them by about 1 rad and back |

The IMU chart is labelled in degrees and plots **radians**: Leika's driver returns `atan2` and the
app does not convert it. The ±3 jumps on the chart are the angle wrapping past ±180°.

## What is still open

- **The IMU failed to answer at boot on two of seven boots** (`I2C hardware timeout`), while the
  PCA9685 on the same bus never did. It is on Dupont only and hangs from its wires on the bench. Its four
  wires come first when the Dupont connections are secured.
- **At rest the IMU reads about 2 rad (~115°) on x and y.** The board was standing almost on its edge,
  so this may be right; check it once it is screwed flat on the robot.
- **The MPU6500's accelerometer offset registers are not where Leika writes them** (0x77 against
  0x06), so Leika's start-up accelerometer calibration likely does nothing on this chip. Only matters
  for IMU tuning, after it walks.
- **Servo calibration is next.** Leika's "Calibrate" sends all twelve servos to centre at once and its
  min/max search drives a servo to the ends of its travel, so the proposal in `STATE.md` is to
  calibrate a spare MG996R off the robot and copy its values.
