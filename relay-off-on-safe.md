```cpp
#define RELAY_PIN 25  // active-low: LOW=ON, HIGH=OFF

void setup() {
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH); // RELAY OFF
}

void loop() {
  // nothing
}
```
