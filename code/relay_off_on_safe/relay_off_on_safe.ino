// Keeps the 6V servo rail off through boot and reset.
//
// The relay module is active-low: LOW closes it, HIGH leaves it open. Until setup() runs the pin
// is not driven by anything, so the real work is done by a 10k pull-up from GPIO27 to 3.3V. This
// sketch only makes the state explicit once the board is up.
//
// Board: ESP32 Dev Module.
// GPIO27 matches the reference project's pinout. Confirm against Leika's configuration before
// flashing the real firmware.

#define RELAY_PIN 27  // active-low: LOW=ON, HIGH=OFF

void setup() {
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH);  // relay OFF
}

void loop() {
  // nothing
}
