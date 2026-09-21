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

Order, per Leika's docs: **Build**, then **Upload Filesystem Image** once, then **Upload and Monitor**.
Always on USB with the XT60 unplugged — USB and the pack never power the ESP32 together.
