Keeps the servo rail off through boot and reset. The pin is not driven by anything until `setup()`
runs, so the 10k pull-up to 3.3V does the real work — this sketch only makes the state explicit
once the board is up.

GPIO27 matches the reference project's pinout. Confirm against Leika's configuration before
flashing it.

```cpp
#define RELAY_PIN 27  // active-low: LOW=ON, HIGH=OFF

void setup() {
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH); // RELAY OFF
}

void loop() {
  // nothing
}
```
