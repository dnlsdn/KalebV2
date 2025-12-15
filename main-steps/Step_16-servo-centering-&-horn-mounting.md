## Step 16 — Servo Centering & Horn Mounting (3-at-a-time)

### Objective

Establish a **consistent electrical and mechanical neutral position** for all **12 MG996R servos** used in the Spot Micro ESP32 robot.

This step ensures that:

- Every servo shares the same **electrical center (1500 µs PWM)**
- All servo horns are mounted with a **common mechanical reference**
- Later mechanical orientations (0° / 180° / 60° / 120°) can be applied **reliably**
- No servo-specific offsets exist before assembling the legs

This is a **mandatory calibration step** before any mechanical assembly.

---

### Materials

- ESP32 DevKitC  
- PCA9685 16-channel PWM driver (I²C address `0x40`)  
- Relay module (low-level trigger, GPIO 5)  
- SZBK07 buck converter (6.0V servo rail)  
- 12× MG996R servos  
- Servo horns (6-arm type)  
- LiPo 2S battery (with fuse installed)  
- USB cable (ESP32 power & programming)  

---

### Safety

- Servos are powered **only through the relay**
- PWM commands are sent **before** enabling servo power
- Only **3 servos connected at a time** to limit current spikes
- Power-down sequence always respected:
  1. Disconnect LiPo  
  2. Disconnect USB  

---

### Servo Grouping

Servos were calibrated in **four groups of three**:

| Group | PCA Channels |
|------|--------------|
| A | CH0, CH1, CH2 |
| B | CH3, CH4, CH5 |
| C | CH6, CH7, CH8 |
| D | CH9, CH10, CH11 |

---

### Procedure (Repeated for Each Group)

1. Connect only the three servos belonging to the active group.
2. Upload the centering firmware (see code below).
3. Power ESP32 via USB.
4. Connect LiPo battery.
5. Observe sequence:
   - Relay OFF at boot
   - 1500 µs PWM preloaded
   - Relay ON
   - Small confirmation movement (wiggle)
   - Servos hold center position
6. Mount servo horns:
   - Servo observed **frontally**
   - Using 6-arm horn
   - One arm aligned **as vertically upward as possible**
   - ±1 tooth deviation accepted
7. Secure horn screw.
8. Power down safely (LiPo → USB).
9. Move to next group.

---

### Firmware Used (Center + Visual Confirmation)

```c
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#define RELAY_PIN 5
#define START_CH  0   // Change to 0, 3, 6, 9 for each group
#define COUNT_CH  3

Adafruit_PWMServoDriver pca = Adafruit_PWMServoDriver(0x40);

int usToTicks(int us) {
  long ticks = (long)us * 4096L / 20000L; // 50Hz => 20ms
  if (ticks < 0) ticks = 0;
  if (ticks > 4095) ticks = 4095;
  return (int)ticks;
}

void setGroupUs(int us) {
  int t = usToTicks(us);
  for (int ch = START_CH; ch < START_CH + COUNT_CH; ch++) {
    pca.setPWM(ch, 0, t);
  }
}

void setup() {
  Serial.begin(115200);
  delay(500);

  // Relay OFF (low-level trigger)
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH);
  Serial.println("Relay OFF");

  // PCA9685 init
  Wire.begin(21, 22);
  pca.begin();
  pca.setPWMFreq(50);
  delay(10);

  // Preload CENTER before servo power
  setGroupUs(1500);
  Serial.println("CENTER preloaded (no power yet)");
  delay(2000);

  // Enable servo power
  digitalWrite(RELAY_PIN, LOW);
  Serial.println("Relay ON");
  delay(500);

  // Visual confirmation wiggle
  setGroupUs(1400);
  delay(700);
  setGroupUs(1600);
  delay(700);
  setGroupUs(1500);

  Serial.println("HOLD — mount horns now");

  // Hold position
  while (true) delay(1000);
}

void loop() {}
```

---

### Results

All 12 servos were successfully:

Electrically centered at 1500 µs

Mechanically aligned via horn mounting

No unexpected motion occurred

Relay-based power gating worked correctly

Servo behavior was consistent across all channels

---

### Interpretation

This step establishes a clean, reproducible reference point for every servo.
All subsequent mechanical assembly steps can now rely on the assumption:

1500 µs PWM equals true mechanical neutral.

This prevents asymmetries, mechanical stress, and gait instability later in the project.

---

### Acceptance Criteria

Check	Status

Group A centered & horn mounted	Pass
Group B centered & horn mounted	Pass
Group C centered & horn mounted	Pass
Group D centered & horn mounted	Pass
No servo jitter or drift	Pass
Safe power sequencing respected	Pass


---

![IMG_0246](https://github.com/user-attachments/assets/7fbbe405-a135-4fa4-8816-ac1b2734725f)
