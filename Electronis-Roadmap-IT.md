# Spot Micro ESP32 — Roadmap Completa per Collegare l’Elettronica

Versione: 1.0

Questa roadmap descrive tutta l’elettronica necessaria per costruire lo Spot Micro ESP32 utilizzando:

* 12× MG996R
* ESP32 DevKitC
* ESP32-CAM
* PCA9685
* MPU6050
* 2× HC-SR04
* OLED SSD1306
* WS2812 Ring
* Relè 5V
* LM2596, SZBK07
* Sensore tensione 25V
* ACS712 30A

Contiene:

* Architettura generale
* Pinout ESP32 dedicato
* Roadmap dettagliata passo per passo
* Schema ASCII

---

# 1. Architettura generale

```text
         ┌──────────────────────── LiPo 2S (7.4V) ────────────────────────┐
         │                                                                │
         │                 (+)                                  (-) GND   │
         │                  │                                    │        │
         │           [ Fusibile 10A ]                            │        │
         │                  │                                    │        │
         └───────────[ ACS712 30A ]───────────────┬──────────────┘
                                                  │
                                       ┌──────────┴───────────┐
                                       │                      │
                             Ramo LOGICA (5V)        Ramo SERVI (6V)
                                LM2596                     SZBK07
                                 5.0V                       6.0V
                                   │                          │
                             ┌─────┴─────┐             ┌──────┴──────┐
                             │           │             │             │
                        ESP32 DevKit   ESP32-CAM     Relè 5V      PCA9685
                        Sensori I2C    (video)        (6V ON/OFF)  + 12× MG996R
                        HC-SR04        Wi-Fi           │
                        WS2812 ring                    │
                        Pulsante LED              → 6V verso servi
                        Voltage sensor
                        ACS712 output → ADC
                             │
                     Tutti i GND in comune
                         (stella unica)
```

---

# 2. Pinout dedicato ESP32

| Funzione                    | GPIO |
| --------------------------- | ---- |
| I2C SDA                     | 21   |
| I2C SCL                     | 22   |
| Relè servomotori            | 5    |
| WS2812 DATA                 | 23   |
| HC-SR04 #1 TRIG             | 13   |
| HC-SR04 #1 ECHO (partitore) | 26   |
| HC-SR04 #2 TRIG             | 14   |
| HC-SR04 #2 ECHO (partitore) | 27   |
| Pulsante                    | 18   |
| LED pulsante opzionale      | 19   |
| Sensore tensione 25V        | 36   |
| ACS712 uscita               | 34   |

---

# 3. Roadmap Step-by-Step

## Fase 0 — Setup e Sicurezza

* Piano non conduttivo
* LiPo scollegata
* Preparare multimetro e strumenti

---

## Fase 1 — Regolare LM2596 e SZBK07

* Regola LM2596 a 5.00V
* Regola SZBK07 a 6.00V

---

## Fase 2 — Fusibile e ACS712

* LiPo + → Fusibile 10A → IN+ ACS712
* OUT+ ACS712 → alimentazioni
* Cavo 14–16 AWG

---

## Fase 3 — Ramo logica, ramo servi, GND comune

* ACS712 OUT+ → LM2596 IN+, SZBK07 IN+
* GND unico a stella
* 1000µF vicino al PCA9685

---

## Fase 4 — Relè ON/OFF servi

* SZBK07 OUT+ → COM relè
* NO → 6V PCA9685
* Relè IN → GPIO 5

---

## Fase 5 — ESP32 + Bus I2C

* ESP32 alimentato a 5V
* SDA 21, SCL 22
* PCA9685 VCC 3.3V, V+ 6V
* MPU6050 3.3V
* OLED 3.3V

---

## Fase 6 — HC-SR04 (con partitore)

### Sensore 1

* TRIG → 13
* ECHO → partitore → 26

### Sensore 2

* TRIG → 14
* ECHO → partitore → 27

### Partitore:

```
ECHO → 2kΩ → nodo → GPIO
             |
            1kΩ
             |
            GND
```

---

## Fase 7 — WS2812 Ring

* DATA → GPIO 23 con resistenza da 330–500Ω
* 5V + GND
* 1000µF vicino al ring

---

## Fase 8 — ESP32-CAM

* 5V → modulo CAM
* GND comune
* Flash tramite FT232RL quando necessario

---

## Fase 9 — PCA9685 → 12× MG996R

* Servi su canali 0–11
* Segnale su PCA9685
* Rosso → 6V
* Nero → GND
* Centrare i servi a 1500µs prima del montaggio delle horn

---

## Fase 10 — Sensori batteria

### Sensore tensione

* OUT → GPIO 36
* IN+ → positivo dopo ACS712

### ACS712

* OUT → GPIO 34

---

## Fase 11 — Collaudi finali

* Scanner I2C
* Test OLED
* Test relè
* Test singoli servi
* Test HC-SR04
* Test WS2812
* Test ESP32-CAM
* Test batteria sotto carico

---

# Schema ASCII ESP32

```text
                ┌─────────────────────────┐
        3V3  ───│• 3V3               VIN •│── 5V
        GND  ───│• GND               GND •│── GND
        21   ───│• SDA               23  •│── WS2812
        22   ───│• SCL               5   •│── RELÈ
        13   ───│• TRIG1             14  •│── TRIG2
        26   ───│• ECHO1             27  •│── ECHO2
        18   ───│• BUTTON            19  •│── LED BUTTON
        36   ───│• VBAT SENSOR       34  •│── ACS712
                └─────────────────────────┘
```