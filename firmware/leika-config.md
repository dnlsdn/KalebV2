# Leika, as configured for KalebV2

The firmware is [SpotMicroESP32-Leika by runeharlyk](https://github.com/runeharlyk/SpotMicroESP32-Leika).
It is **not vendored here**. It lives next to this repo:

- **Clone:** `~/Library/Developer/SpotMicroESP32-Leika`, with its `nanopb` submodule
  (`git clone --recurse-submodules`).
- **Based on:** upstream `9ccb0ff`, 2026-08-19.
- **Local branch:** `kalebv2`, two commits on top (`d071f83`, `fd7120f`). It is not pushed anywhere, so
  the full diff is below: if the clone is lost or Leika is updated, reapply these six changes by hand.

## The six changes, and why

The first three were made at the desk on 2026-09-21. The last three were forced by the first flash on
2026-10-03: without them Leika does not boot on this board, and once it boots nobody can reach it.

| File | Change | Why |
|---|---|---|
| `platformio.ini` | `default_envs = esp32dev` | Upstream defaults to a camera board. This build is a plain ESP32-DevKitC. Leika's defaults for that board are **SDA 21 / SCL 22**, matching the wiring. |
| `platformio.ini`, `[env:esp32dev]` | `-D I2C_FREQUENCY=400000UL` | Leika runs I2C at 1MHz. The **MPU6050 supports 400kHz at most** and shares the bus with the PCA9685, so at 1MHz it would drop off or return garbage. michaelkubina's 1MHz advice assumes the PCA9685 on a bus of its own. |
| `esp32/features.ini` | `USE_MPU6050=1`, `USE_WS2812=0` | Upstream ships the IMU off and the LED ring on. This build has the MPU6050 and no ring — and the ring would have driven **GPIO27**, the old relay pin. |
| `esp32/sdkconfig.defaults.esp32dev` (new), and `board_build.cmake_extra_args` in `[env:esp32dev]` | PSRAM off, flash 4MB, for this env only | The shared `sdkconfig.defaults` turns **PSRAM** on for every board. This ESP32-D0WD-V3 has none, so the firmware stopped at `PSRAM chip not found` and reset in a loop. Setting it in an env-only file leaves the camera boards, which do have PSRAM, as they were. The file matches a `sdkconfig.*` rule in Leika's `.gitignore`, so it was committed with `git add -f`. |
| `esp32/include/peripherals/drivers/mpu6050.h` | accept `WHO_AM_I` **0x70** | The sensor sold as an MPU6050 answers 0x70: it is an **MPU6500**, common on cheap GY-521 boards. Leika accepted only 0x68 and 0x72 and gave up. With 0x70 accepted the DMP loads, calibrates and follows tilt. |
| `esp32/src/wifi/wifi_idf.cpp` | `getMode()` returns the mode the class started | A Leika bug, not this hardware. Before the radio is started the Wi-Fi driver reports **AP**, its default; `APService` read that, believed the access point was up, and never started it. The class already records the real mode in `_mode`; returning it fixes the access point. |

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
+board_build.cmake_extra_args = -DSDKCONFIG_DEFAULTS="sdkconfig.defaults;esp32/sdkconfig.defaults.esp32dev" ; KalebV2: no PSRAM, 4MB flash
--- /dev/null
+++ b/esp32/sdkconfig.defaults.esp32dev
+# CONFIG_SPIRAM is not set
+CONFIG_ESPTOOLPY_FLASHSIZE_4MB=y
--- a/esp32/include/peripherals/drivers/mpu6050.h
+++ b/esp32/include/peripherals/drivers/mpu6050.h
-        if (whoami != 0x68 && whoami != 0x72) return false;
+        if (whoami != 0x68 && whoami != 0x72 && whoami != 0x70) return false;
--- a/esp32/src/wifi/wifi_idf.cpp
+++ b/esp32/src/wifi/wifi_idf.cpp
 wifi_mode_t WiFiClass::getMode() {
     if (!_initialized) return WIFI_MODE_NULL;
-    wifi_mode_t m;
-    if (esp_wifi_get_mode(&m) == ESP_OK) {
-        return m;
-    }
-    return WIFI_MODE_NULL;
+    return _mode;
 }
```

`sdkconfig.esp32dev`, in the project root, is generated from the defaults and git-ignored. It is only
regenerated when it is missing: after changing the defaults, delete it and build again.

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

**The flash really is 4MB.** The `Flash memory size mismatch… found 2MB` warning came from the generated
config. The filesystem image was written at `0x3D0000`, above 2MB, and verified; the bootloader reports
`SPI Flash Size : 4MB`. With the env-only defaults file the warning is gone. With the app embedded the
build now reports **Flash 89.2%**.

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

## Settings stored on the ESP32, not in the code

Leika keeps calibration in its filesystem, as `servoSettings.json`. **Uploading the filesystem image
again erases it**, so every value set from the app is also recorded here.

| Setting | Value | Set in | How it was found |
|---|---|---|---|
| Conversion, all twelve servos | **2.56** ticks per degree (Leika's default 2.0) | session 14 | measured over 180° on a spare MG996R, `main-steps/14-servo-conversion.md` |
| Center PWM, ch 0-11 | **306, 322, 338, 298, 261, 315, 286, 349, 308, 266, 306, 247** | session 15 | per joint, at knee 90° and foot under the hip, `main-steps/15-body-frame.md` |
| Center Angle, Direction | Leika's defaults, unchanged | — | — |

## Reaching it from a phone

- The robot's network has no internet, so **iOS treats it like a hotel Wi-Fi**: it opens a small
  "Wi-Fi Captive" window and keeps mobile data for everything else. The app works inside that window
  (the first page is a 404 for Apple's test URL; tap Home page). Otherwise close it, choose
  "Use without Internet", and open `http://192.168.4.1` in **Safari**. Brave failed with
  `ERR_CONNECTION_CLOSED`.
- **The Wi-Fi icon in the header is crossed out by design**: it shows the signal of a home network the
  robot is not on, not the link to the phone.
- **Pages that ask the robot for data show an empty result while they wait.** "No I2C devices found"
  with a spinning button means no answer yet, not no devices.
- **System Status shows Uptime wrong.** The firmware sends milliseconds (`esp_timer_get_time() / 1000`
  in `system_service.cpp`) and the app formats them as seconds: "1 day 7 hours" was 113 seconds. Reset
  Reason on the same page is right, and is how a brown-out was found in session 15.
- **Calibration mode turns the servos off** in this version, contrary to the documentation and
  discussion #118. Calibration is done from the Servo page instead: **Active** sends every connected
  servo to the angles in memory (all zero at boot, legs straight), the PWM slider moves one channel, and
  **Set center pwm** stores the slider's value for the selected servo.
- **The IMU chart says degrees and plots radians.** The driver's `atan2` returns radians and the app
  does not convert them: ±3.14 is ±180°, and a line jumping from +3 to −3 is the angle wrapping
  around, not noise.
