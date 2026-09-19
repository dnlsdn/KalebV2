// Drives PCA9685 channel 0 to 1500us, the servo centre, and holds it there.
//
// Board: ESP32 Dev Module. Flash on USB with the XT60 unplugged, then unplug USB
// and connect the pack: the sketch runs from flash, the servo moves once and holds.

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pca = Adafruit_PWMServoDriver(0x40);

void setup() {
  Wire.begin(21, 22);                    // I2C on SDA 21, SCL 22, as wired
  pca.begin();
  pca.setOscillatorFrequency(25000000);  // datasheet nominal, real boards run 23-27MHz
  pca.setPWMFreq(50);                    // one pulse every 20ms, what servos expect
  pca.writeMicroseconds(0, 1500);        // channel 0, centre
}

void loop() {
  // nothing: the PCA9685 repeats the pulse on its own
}