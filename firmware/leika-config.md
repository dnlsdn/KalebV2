# Leika, as configured for KalebV2

The firmware is [SpotMicroESP32-Leika by runeharlyk](https://github.com/runeharlyk/SpotMicroESP32-Leika).
It is **not vendored here**. It lives next to this repo:

- **Clone:** `~/Library/Developer/SpotMicroESP32-Leika`, with its `nanopb` submodule
  (`git clone --recurse-submodules`).
- **Based on:** upstream `9ccb0ff`, 2026-08-19.
- **Local branch:** `kalebv2`, one commit on top. It is not pushed anywhere, so the full diff is below:
  if the clone is lost or Leika is updated, reapply these three changes by hand.

## The three changes, and why

| File | Change | Why |
|---|---|---|
| `platformio.ini` | `default_envs = esp32dev` | Upstream defaults to a camera board. This build is a plain ESP32-DevKitC. Leika's defaults for that board are **SDA 21 / SCL 22**, matching the wiring. |
| `platformio.ini`, `[env:esp32dev]` | `-D I2C_FREQUENCY=400000UL` | Leika runs I2C at 1MHz. The **MPU6050 supports 400kHz at most** and shares the bus with the PCA9685, so at 1MHz it would drop off or return garbage. michaelkubina's 1MHz advice assumes the PCA9685 on a bus of its own. |
| `esp32/features.ini` | `USE_MPU6050=1`, `USE_WS2812=0` | Upstream ships the IMU off and the LED ring on. This build has the MPU6050 and no ring — and the ring would have driven **GPIO27**, the old relay pin. |

```diff
--- a/esp32/features.ini
+++ b/esp32/features.ini
-  -D USE_MPU6050=0
-  -D USE_WS2812=1
+  -D USE_MPU6050=1
+  -D USE_WS2812=0
--- a/platformio.ini
+++ b/platformio.ini
-default_envs = esp32-camera
+default_envs = esp32dev
 [env:esp32dev]
 board = esp32dev
 board_build.partitions = esp32/partition_table/min_spiffs.csv
 build_flags =
     ${env.build_flags}
+    -D I2C_FREQUENCY=400000UL ; KalebV2: the MPU6050 shares the bus and tops out at 400kHz
```

## Left at upstream defaults, on purpose

- **Wi-Fi SSID and password empty** in `esp32/factory_settings.ini`. Leika then opens its own access
  point, **`Spot-Micro`**, password `spot-leika`, app at **`http://192.168.4.1`**. No home Wi-Fi
  password ends up in a file.
- **Servo oscillator at 27MHz** (`FACTORY_SERVO_OSCILLATOR_FREQUENCY`). The test sketches in `code/`
  assume 25MHz; the difference is absorbed by Leika's calibration.
- **Relay:** Leika has none, and neither does this build since session 6.

## How it builds

PlatformIO with the **ESP-IDF** framework (`platform = espressif32 @ 6.8.1`), not Arduino. A pre-build
script also builds the SvelteKit app in `app/` with pnpm, so Node and pnpm must be installed — they are
on this Mac. The first build downloads the whole ESP32 toolchain and takes a long time.

**It also needs `protoc`** (`brew install protobuf`), which Leika's docs do not mention. The app
imports TypeScript generated from `platform_shared/*.proto`, and the pre-build script runs
`pnpm build:embedded`, which skips the step that generates it.

**Without `protoc` the build still succeeds, and the firmware has no app in it.** The script writes an
empty `esp32/include/WWWData.h`, and because that file is now newer than the app sources it never tries
again. The robot would boot, open its Wi-Fi, and serve nothing at `192.168.4.1`. This happened on
2026-09-21. How to tell: flash usage. Without the app the build reports **Flash 57.5%**; with it,
**Flash 91.0%** (1,789,793 bytes). If the app goes missing again:

```bash
cd ~/Library/Developer/SpotMicroESP32-Leika/app && pnpm proto
rm ../esp32/include/WWWData.h
```

then Build again and check the flash figure.

**One warning to watch on the first boot:** `Flash memory size mismatch detected. Expected 4MB, found
2MB`. Upstream's `sdkconfig.esp32dev` says 2MB, the board and the partition table say 4MB. It is
probably harmless, because esptool writes the real size into the bootloader when it flashes. If the
serial monitor reports that the filesystem failed to mount, this is the first suspect: the settings
partition sits above 2MB.

Order, per Leika's docs: **Build**, then **Upload Filesystem Image** once, then **Upload and Monitor**.
Always on USB with the XT60 unplugged — USB and the pack never power the ESP32 together.

## What Leika sends to the servos — read from the code, not yet seen

Worked out on 2026-09-21 from `esp32/include/peripherals/servo_controller.h`, with no hardware. It
is a prediction to check on the bench, not a measurement.

- **The servos stay limp after boot.** Leika puts the PCA9685 to sleep at start-up and wakes it only
  when the robot is activated from the app. Flashing and checking the I2C devices moves nothing.
- **The channel map is michaelkubina's**, the one wired in session 12: front left 0/1/2, front right
  3/4/5, rear left 6/7/8, rear right 9/10/11, shoulder / upper leg / lower leg.
- **On activation every servo jumps to the rest pose at once.** The joint angles start already at the
  rest values, so there is no slow approach from wherever the legs are. Converted to the Arduino
  `Servo` scale used in `code/`, assuming the oscillator really runs at the 27MHz Leika sets:

| Joint | Mounted at (left / right) | Leika's rest pose (left / right) |
|---|---|---|
| Shoulder | 90° / 90° | ~92° / ~92° |
| Upper leg | 120° / 60° | ~135° / ~50° |
| Lower leg | 0° / 180° | ~40° / ~144° |

  The signs agree with how the legs were mounted, left and right mirrored, so no joint should turn
  the wrong way. The knees still swing about 40° together: **first activation with the robot lifted
  on a support, legs free.**
- **The oscillator is an open question.** Leika sets 27MHz, the sketches in `code/` assumed 25MHz,
  and the real PCA9685 is somewhere in between. If it is near 25MHz every pulse comes out about
  100-120µs longer: centre at ~1616µs instead of ~1496µs. Leika's per-channel calibration absorbs it,
  which is one more reason not to skip calibration.
