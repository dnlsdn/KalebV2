Walks every I2C address and reports which ones answer. The first thing to flash after wiring the
bus, and the first thing to re-flash whenever a device stops responding — it separates a wiring
fault from a code fault in about ten seconds.

Arduino IDE, board **ESP32 Dev Module**, serial monitor at **115200 baud**.

Expected on this build: **0x40** for the PCA9685, **0x68** for the MPU6050 (0x69 if that board's
AD0 pin is pulled high).

```cpp
#include <Wire.h>

void setup() {
  Serial.begin(115200);
  delay(1000);
  Wire.begin(21, 22);
  Serial.println("I2C scanner");
}

void loop() {
  int found = 0;
  for (byte addr = 1; addr < 127; addr++) {
    Wire.beginTransmission(addr);
    if (Wire.endTransmission() == 0) {
      Serial.printf("Device found at 0x%02X\n", addr);
      found++;
    }
  }
  if (found == 0) Serial.println("No I2C devices found");
  Serial.println("---");
  delay(3000);
}
```

If nothing is found at all, the bus itself is the problem: check SDA on GPIO21, SCL on GPIO22, and
that the pull-ups have a supply — on this build they tie to the PCA9685's VCC, which sits on 3.3V.
If one device answers and another does not, the bus is fine and the silent board is the suspect.
