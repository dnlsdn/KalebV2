# Power-Up & Power-Down Procedures

## Correct Power-Up Sequence (Safe Startup)

Follow this sequence **every time** before testing or operating the robot:

1. **Connect USB to ESP32**
   - Powers logic and allows serial monitoring
   - Ensures firmware is running and stable

2. **Connect LiPo battery**
   - Battery is now physically connected but not yet driving the servo rail

3. **Insert the main fuse**
   - Enables the power distribution network
   - Servo rail is still disabled by the relay

4. **Verify relay state = OFF**
   - Servo power must be physically disconnected
   - PCA9685 V+ should read 0 V

5. **Enable relay (Relay ON)**
   - 6 V servo rail is applied to PCA9685
   - Servos power up in a controlled and predictable state

This sequence guarantees:
- No uncontrolled servo motion
- No current spikes at boot
- No brown-out on ESP32

---

## Correct Power-Down Sequence (Safe Shutdown)

Follow this order **every time** you shut the system down:

1. **Disable relay (Relay OFF)**
   - Immediately removes power from all servos

2. **Remove the main fuse**
   - Isolates the battery from the power system

3. **Disconnect LiPo battery**
   - Battery fully removed from the circuit

4. **Disconnect USB from ESP32**
   - Logic and debugging power removed

This ensures:
- Servos are never powered without control
- No accidental motion during shutdown
- Maximum electrical safety
