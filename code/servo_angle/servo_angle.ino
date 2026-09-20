// Drives PCA9685 channel 0 to ANGLE degrees, on the Arduino Servo library's scale, and holds it.
//
// Board: ESP32 Dev Module. Flash on USB with the XT60 unplugged, then unplug USB
// and connect the pack: the servo moves once and holds.

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pca = Adafruit_PWMServoDriver(0x40);

const int ANGLE = 90;  // 60, 90 or 120: change it and flash again

// Same mapping the Arduino Servo library used for the wrists in November:
// 0 degrees = 544us, 180 degrees = 2400us.
int angleToMicros(int angle) {
  return 544 + (long)angle * (2400 - 544) / 180;
}

void setup() {
  Wire.begin(21, 22);                    // I2C on SDA 21, SCL 22, as wired
  pca.begin();
  pca.setOscillatorFrequency(25000000);
  pca.setPWMFreq(50);
  pca.writeMicroseconds(0, angleToMicros(ANGLE));
}

void loop() {
  // nothing: the PCA9685 repeats the pulse on its own
}