## Step 15 — Servo Power Validation via Relay + PCA9685 (Single-Channel Motion Test)

### Objective

Validate the **complete servo actuation chain** by confirming correct interaction between:

- ESP32 (logic control)
- Relay module (6V power gating)
- PCA9685 PWM driver (signal generation)
- SZBK07 (6V servo regulator)
- MG996R servo motor

The goal of this step is to ensure that:

- Servos remain **powered OFF** when the relay is OFF  
- PWM commands are generated correctly even without servo power  
- Servos receive power **only when the relay is enabled**  
- A single servo can move safely through **MIN → MAX → CENTER** positions  
- No unintended motion or oscillation occurs  

This step is a **critical safety and functionality milestone** before connecting all servos.

---

### Materials

- ESP32 DevKitC  
- PCA9685 PWM driver (I²C address `0x40`)  
- Relay module (low-level trigger, SRD-05VDC-SL-C)  
- SZBK07 buck converter (6.0V for servos)  
- MG996R servo motor (single unit for test)  
- Dupont cables  
- LiPo 2S battery (connected via fuse and ACS712)  
- Multimeter (for voltage verification)  
- Arduino IDE + USB cable  

---

### Safety

- ESP32 powered **via USB** during testing  
- LiPo connected only after relay logic was validated  
- Fuse installed before LiPo connection  
- Only **one servo connected** to avoid current spikes  
- No continuous motion loops in firmware  
- Relay state explicitly controlled in software  

---

### Procedure

#### **1. Initial State — Relay OFF**

- ESP32 boots with relay control pin set to **HIGH**  
- Relay is **inactive** (low-level trigger logic)  
- SZBK07 output is isolated from PCA9685 V+  
- Servo receives **no 6V power**

PWM center command (1500 µs) is sent to the PCA9685 **before** powering the servo.

**Expected behavior:**
- No relay click  
- Servo remains completely still  

---

#### **2. Delay & Safety Window**

A 5-second delay is introduced to ensure:

- I²C bus is stable  
- PCA9685 is fully initialized  
- PWM signals are already present before power delivery  

This prevents sudden or uncontrolled servo jumps.

---

#### **3. Relay Activation (Power Enable)**

- Relay control pin is set to **LOW**  
- Relay switches ON  
- 6V from SZBK07 reaches PCA9685 V+  

**Expected behavior:**
- Audible relay click  
- Servo becomes powered and immediately holds the center position  

---

#### **4. Controlled Servo Motion Test**

With relay ON and stable power:

- Servo commanded to **MIN position**  
- Servo commanded to **MAX position**  
- Servo returned to **CENTER**  

All movements are slow, deliberate, and non-repeating.

---

### Serial Monitor Output (Verified)

Relay OFF
Servo command sent (CENTER, no power yet)
Waiting 5 seconds...
Relay ON
Servo -> MIN
Servo -> MAX
Servo -> CENTER
TEST COMPLETE


---

### Results

- Relay correctly gates the 6V servo power line  
- PCA9685 generates valid PWM signals regardless of relay state  
- Servo remains OFF when relay is OFF  
- Servo moves only after relay is enabled  
- All commanded positions are reached smoothly  
- No jitter, no oscillation, no unexpected movement  

---

### Interpretation

This confirms that:

- The **relay safety architecture is correct**  
- Servo power is **fully isolated** from logic when disabled  
- PCA9685 + ESP32 timing is stable  
- The system is safe for multi-servo expansion  

The robot now has a **professionally designed servo power control system**, equivalent to industrial robotics standards.

---

### Acceptance Criteria

| Check | Status |
|------|--------|
| Relay OFF → servo unpowered | **Pass** |
| Relay ON → servo powered | **Pass** |
| PCA9685 PWM generation | **Pass** |
| MIN / MAX / CENTER motion | **Pass** |
| No unintended motion | **Pass** |
| Safe power-up sequence | **Pass** |

---

### Code

// Step 15 — Servo Power Validation via Relay + PCA9685 (Single-Channel Motion Test)
// Hardware:
// - ESP32 SDA=21, SCL=22
// - PCA9685 at I2C 0x40
// - Relay (LOW-level trigger) on GPIO5
// - Servo connected to PCA channel 0
//
// Behavior:
// 1) Relay OFF at boot (servo unpowered)
// 2) Initialize PCA9685 and send CENTER command (1500us) with no servo power
// 3) Wait 5s (safety window)
// 4) Relay ON (servo powered)
// 5) Move MIN -> MAX -> CENTER once, then stop

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#define RELAY_PIN 5
#define SERVO_CH  0

Adafruit_PWMServoDriver pca = Adafruit_PWMServoDriver(0x40);

// Convert microseconds to PCA9685 ticks at 50Hz (20ms period)
int usToTicks(int us) {
  long ticks = (long)us * 4096L / 20000L;
  if (ticks < 0) ticks = 0;
  if (ticks > 4095) ticks = 4095;
  return (int)ticks;
}

void setServoUs(uint8_t ch, int us) {
  pca.setPWM(ch, 0, usToTicks(us));
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("BOOT");

  // Relay OFF for safety (LOW-level relay: HIGH = OFF)
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH);
  Serial.println("Relay OFF");

  // I2C + PCA9685 init
  Wire.begin(21, 22);
  pca.begin();
  pca.setPWMFreq(50);
  delay(10);

  // Send center command before powering servos
  setServoUs(SERVO_CH, 1500);
  Serial.println("Servo command sent (CENTER, no power yet)");

  Serial.println("Waiting 5 seconds...");
  delay(5000);

  // Relay ON (servo rail powered)
  digitalWrite(RELAY_PIN, LOW);
  Serial.println("Relay ON");
  delay(500);

  // Controlled motion test
  Serial.println("Servo -> MIN");
  setServoUs(SERVO_CH, 500);
  delay(1500);

  Serial.println("Servo -> MAX");
  setServoUs(SERVO_CH, 2500);
  delay(1500);

  Serial.println("Servo -> CENTER");
  setServoUs(SERVO_CH, 1500);

  Serial.println("TEST COMPLETE");
}

void loop() {
  // No loop: run once for safety
}


---

![IMG_0246](https://github.com/user-attachments/assets/0827076e-7dc1-499e-bc42-4db6ec38b8ad)
