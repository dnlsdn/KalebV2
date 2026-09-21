// Moves every servo, one channel at a time, to prove each joint answers on its own channel.
//
// Board: ESP32 Dev Module. Flash on USB with the XT60 unplugged, then unplug USB
// and connect the pack. All twelve go to their mounting angle one by one, then each
// joint in turn moves 15 degrees and back, starting again from ch0 after a pause.

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pca = Adafruit_PWMServoDriver(0x40);

// Mounting angle of every channel, in PCA9685 channel order.
// Each leg is shoulder, upper leg, wrist.
const int MOUNT[12] = {
  90, 120, 0,    // front left:  ch0 ch1 ch2
  90, 60, 180,   // front right: ch3 ch4 ch5
  90, 120, 0,    // rear left:   ch6 ch7 ch8
  90, 60, 180    // rear right:  ch9 ch10 ch11
};

const int NUDGE = 15;  // degrees each joint moves during the check

// Same mapping the Arduino Servo library used for the wrists:
// 0 degrees = 544us, 180 degrees = 2400us.
int angleToMicros(int angle) {
  return 544 + (long)angle * (2400 - 544) / 180;
}

void setup() {
  Wire.begin(21, 22);                    // I2C on SDA 21, SCL 22, as wired
  pca.begin();
  pca.setOscillatorFrequency(25000000);
  pca.setPWMFreq(50);

  // One at a time, so the pack never sees twelve servos starting together.
  for (int ch = 0; ch < 12; ch++) {
    pca.writeMicroseconds(ch, angleToMicros(MOUNT[ch]));
    delay(500);
  }
  delay(2000);
}

void loop() {
  for (int ch = 0; ch < 12; ch++) {
    // Move towards the middle of the travel: 0 goes to 15, 180 to 165, 90 to 75.
    int nudged = MOUNT[ch] < 90 ? MOUNT[ch] + NUDGE : MOUNT[ch] - NUDGE;

    pca.writeMicroseconds(ch, angleToMicros(nudged));
    delay(700);
    pca.writeMicroseconds(ch, angleToMicros(MOUNT[ch]));
    delay(1500);
  }
  delay(4000);  // a long pause marks the start of the next round, from ch0
}