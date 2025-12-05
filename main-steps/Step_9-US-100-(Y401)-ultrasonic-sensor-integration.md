# Step 9 — US-100 (Y401) Ultrasonic Sensor Integration (Power + TRIG + Protected ECHO)

## Objective

Integrate the **US-100 ultrasonic distance sensor** into the SpotMicro ESP32 platform using:

- a regulated **5V logic rail** (from LM2596)
- shared **Ground Star Point**
- a safe **TRIG connection** to GPIO13
- a fully protected **ECHO line** using a 2kΩ/1kΩ voltage divider  
  (5V → 3.3V safe for ESP32)

This step ensures reliable ultrasonic readings **without risking damage** to the microcontroller.

---

## Materials

- US-100 (Y401) ultrasonic sensor  
- WAGO connectors:
  - 5V logic hub  
  - Ground Star hub + Ground Expansion hub  
  - Partitioner node hub (2 × WAGO)
- Dupont cables (female–female or female–male)  
- 2kΩ resistor  
- 1kΩ resistor  
- Multimeter (continuity + resistance mode)

---

# L9.0 — Creation of the 5V Logic Rail (WAGO Hub)

### Purpose

The ESP32 DevKitC **cannot supply enough current** for sensors.  
Therefore the US-100 must be powered directly from:

- **LM2596 OUT+** → stable 5.00 V  
- through a dedicated **WAGO 5V hub** (expandable)

### Procedure

1. Insert a dupont **female** onto LM2596 OUT+ (already soldered pin).  
2. Insert the **male** end into a new WAGO, creating **WAGO 5V LOGIC**.  
3. Reconnect ESP32 **5V pin** using a dupont f–f from this new hub.

### Tests

- OUT+ ↛ GND → **no beep**  
- OUT+ → ESP32 5V → **beep** (continuity OK)  
- WAGO 5V ↛ GND → **no beep**

### Result

All 5V peripherals (US-100, relè, ESP32-CAM, etc.) will draw power from the **same clean regulated rail**.

---

# L9.1 — Powering the US-100

### Connections

| US-100 Pin | Destination |
|------------|-------------|
| **VCC** | WAGO 5V LOGIC |
| **GND** | WAGO Ground Star Point |

### Notes

- A dupont **female** connects to the US-100 pins.  
- The other end goes to WAGO using male dupont or metal terminal.  
- The sensor jumper (UART mode) was **removed**, enabling TRIG/ECHO mode.

### Tests

- XT60 Negative → US-100 GND → **beep**  
- WAGO 5V → US-100 VCC → **no beep**  
- 3.3V → US-100 VCC → **no beep**

### Result

The sensor is safely powered and referenced to system ground.

---

# L9.2 — TRIG Line → GPIO13

### Purpose

The TRIG pin is an output from the ESP32 and is safe to connect directly.

### Connections

- **US-100 TRIG → GPIO13 (ESP32)** using a dupont f–f.

### Tests

- TRIG ↔ GPIO13 → **beep**  
- TRIG ↛ Ground → **no beep**

### Result

TRIG is fully operational and isolated from ground.

---

# L9.3 — ECHO Line Protection (2kΩ / 1kΩ Divider)

### Purpose

The US-100 ECHO pin outputs **5V pulses**, but the ESP32 can only tolerate **3.3V max**.  
A voltage divider reduces:

5V → (2kΩ / (2kΩ + 1kΩ)) → ≈ 3.33V


which is safe and recognized as HIGH by the ESP32.

---

# L9.3A — Construction of the Divider Node (WAGO1 + WAGO2)

### WAGO1 (Main Node)
Contains:

- ECHO from US-100  
- GPIO26 from ESP32  
- One leg of the **2kΩ** resistor

### WAGO2 (Expansion Node)
Contains:

- The **second leg of the 2kΩ** resistor (bridging to WAGO1)  
- One leg of the **1kΩ** resistor  

These two WAGOs form the **electrical midpoint** of the divider.

---

# L9.3B — Ground Termination (WAGO3)

Because the main Ground Star was full, a **Ground Expansion WAGO** was created:

- Connected to the Ground Star via a black AWG24 jumper
- Contains:
  - GND from US-100  
  - The **second leg of the 1kΩ** resistor  

This completes the divider:

ECHO → 2kΩ → (Nodo WAGO1/WAGO2) → 1kΩ → GND
|
GPIO26


---

# L9.3C — Divider Tests

### **Test F — Node ↔ GPIO26**
→ **beep** (correct continuity through direct wire)

### **Test G — Node ↛ 5V**
→ **no beep**

### **Test H — Node ↛ GND**
→ **no beep**  
(multimeter shows values due to resistors — correct)

### **Test I — GPIO26 ↛ 5V**
→ **no beep**

### **Test L — GPIO26 ↛ GND**
→ **no beep**

### Result
The divider is electrically perfect and fully protects GPIO26.

---

# Final Results

The US-100 is now fully integrated into the SpotMicro logic architecture:

- Powered via **LM2596 5V rail**
- Sharing the **Ground Star Point**
- TRIG line connected safely to GPIO13
- ECHO line protected by a proper **2kΩ/1kΩ divider**
- No shorts or illegal voltage paths
- All continuity and isolation tests passed

The sensor is now ready for firmware testing and distance measurement routines.

---

## Acceptance Criteria

| Check | Status |
|-------|--------|
| Jumper removed (TRIG/ECHO mode) | **Pass** |
| Power rails correct (5V + GND) | **Pass** |
| TRIG → GPIO13 | **Pass** |
| ECHO divider produces ~3.3V | **Pass** |
| No shorts to 5V or GND | **Pass** |
| Node topology stable | **Pass** |

---

The ultrasonic subsystem is now safely integrated and ready for motion planning and obstacle detection.

---

![IMG_0151](https://github.com/user-attachments/assets/ca281765-475e-45fe-8a45-61cf9b06aeda)
