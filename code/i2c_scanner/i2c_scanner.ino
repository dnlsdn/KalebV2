// Walks every I2C address and reports which ones answer.
//
// Board: ESP32 Dev Module. Serial monitor at 115200 baud.
// Expected on this build: 0x40 = PCA9685, 0x68 = MPU6050 (0x69 if AD0 is pulled high).
//
// See code/README.md for what to check when a device does not answer.

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
