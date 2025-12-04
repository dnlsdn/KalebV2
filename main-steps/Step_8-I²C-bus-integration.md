# Step 8 — I²C Bus Integration (PCA9685 + MPU6050 + OLED + SDA/SCL Hubs)

## Objective

Create a complete and stable **I²C communication bus** connecting:

- PCA9685 (PWM driver)
- MPU6050 (IMU)
- OLED SSD1306 (display)
- ESP32 (master controller)

This step finalizes all *logic-level wiring* for multi-device I²C operation and ensures:

- shared clock (SCL)
- shared data line (SDA)
- shared 3.3V rail
- shared ground reference

The result is a fully functional multi-device I²C network.

---

## Materials

- PCA9685 module  
- MPU6050 module  
- OLED SSD1306 module  
- ESP32 DevKitC  
- WAGO connectors (Ground, 3.3V, SDA, SCL)  
- Dupont female–female cables  
- Dupont male–male cables (for bridging into WAGO hubs)  
- Multimeter (continuity test)

---

# L4 — 3.3V Line Expansion (WAGO 3.3V Hub)

### Purpose

The ESP32 has only one 3.3V pin available for peripherals.  
A **WAGO-based 3.3V hub** is created to safely distribute 3.3V to multiple I²C modules.

### Procedure

1. Disconnect the original PCA9685 VCC cable from the ESP32 3.3V pin.  
2. Insert a **male–male dupont** into the ESP32 3.3V pin.  
3. Connect the other end of this dupont into a new **WAGO hub** (3.3V).  
4. Insert PCA9685 VCC (dupont → male pin → WAGO) into the same hub.  
5. Leave additional slots available for other devices.

### Result

A stable and expandable 3.3V power rail.

---

# L5 — SDA Line Integration (WAGO SDA Hub)

### Goal

Create a single shared SDA bus for all I²C devices.

### Connections

- **ESP32 GPIO21 → WAGO SDA**
- **PCA9685 SDA → WAGO SDA**
- **OLED SDA → WAGO SDA**
- **MPU6050 SDA → PCA SDA (internally connected → WAGO SDA)**

### Notes

- The MPU6050 SDA is chained through the PCA9685 SDA pin.
- All SDA points form a single electrical node through the hub.

### Test

- No continuity between SDA and SCL (expected).
- All SDA wires firmly seated.

---

# L6 — SCL Line Integration (WAGO SCL Hub)

### Goal

Create a single shared clock line for all I²C devices.

### Connections

- **ESP32 GPIO22 → WAGO SCL**
- **PCA9685 SCL → WAGO SCL**
- **OLED SCK (SCL) → WAGO SCL**
- **MPU6050 SCL → PCA SCL (internally connected → WAGO SCL)**

### Notes

- SCK on the OLED = SCL.
- The WAGO hub ensures clean multi-device clock distribution.

### Test

- Multimeter: SDA ↛ SCL (no beep).  
- All SCL connections stable.

---

# L7 — MPU6050 Integration

### Power

- **MPU VCC → PCA VCC (3.3V from WAGO)**  
- **MPU GND → PCA GND**

### I²C

- **MPU SDA → PCA SDA (→ WAGO SDA)**  
- **MPU SCL → PCA SCL (→ WAGO SCL)**

### Result

The MPU6050 is correctly daisy-chained into the I²C bus.

---

# L8 — OLED SSD1306 Integration

### Power

- **OLED VDD → WAGO 3.3V**
- **OLED GND → ESP32 second GND pin (free)**

### I²C

- **OLED SDA → WAGO SDA**
- **OLED SCK → WAGO SCL**

### Result

OLED joins the I²C bus cleanly and safely.

---

# Final Results

- **Full I²C bus completed**: ESP32, PCA9685, MPU6050, OLED communication ready.  
- **3.3V rail expanded** through WAGO hub.  
- **SDA and SCL hubs** created with WAGO for clean multi-drop topology.  
- All modules share:
  - the same **3.3V rail**
  - the same **GND reference**
  - the same **I²C clock**
  - the same **I²C data line**
- No short circuits on SDA/SCL.  
- Bus validated via continuity tests.

---

## Acceptance Criteria

| Check | Status |
|-------|--------|
| 3.3V hub stable and powering PCA + OLED | **Pass** |
| MPU6050 integrated into I²C | **Pass** |
| OLED connected to I²C via hubs | **Pass** |
| SDA/SCL hubs fully operational | **Pass** |
| No SDA ↔ SCL continuity | **Pass** |
| All grounds unified | **Pass** |

---

The logic wiring subsystem is now **complete and healthy**, and the robot is ready for sensor integration (HC-SR04), relay wiring, and servo power distribution.

---

![IMG_0148](https://github.com/user-attachments/assets/cf4c22b5-729b-469e-b4f7-7bb3ba2b0ff9)
