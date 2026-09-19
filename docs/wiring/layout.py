"""Where every module sits on the drawing. Change a position here and the wires follow."""

import parts as P
import parts_logic as L

W, H = 1660, 1080

# name: (function, x, y, extra args, which drawings it appears in)
PLACEMENT = {
    "hc1": (L.hcsr04, 40, 60, ("HC-SR04 #1",), "both"),
    "hc2": (L.hcsr04, 180, 60, ("HC-SR04 #2",), "both"),
    "cam": (L.esp32cam, 340, 30, (), "final"),
    "esp": (L.esp32, 560, 60, (), "both"),
    "w33": (P.wago, 900, 150, (5, "3V3 WAGO"), "both"),
    "wsda": (P.wago, 1000, 150, (5, "SDA WAGO"), "both"),
    "wscl": (P.wago, 1090, 150, (3, "SCL WAGO"), "both"),
    "mpu": (L.mpu6050, 1230, 40, (), "both"),
    "oled": (L.oled, 1370, 40, (), "final"),
    "red": (P.bus_bar, 240, 250, ("red", "RED BUS BAR · 5V logic"), "both"),
    "bat": (P.lipo, 30, 440, (), "both"),
    "sw": (P.rocker_switch, 322, 465, (), "final"),
    "fuse": (P.blade_fuse, 400, 467, (), "both"),
    "acs": (P.acs712, 520, 450, (), "both"),
    "vsens": (L.voltage_sensor, 400, 560, (), "final"),
    "wsplit": (P.wago, 520, 560, (3, "split WAGO"), "both"),
    "lm": (P.lm2596, 660, 400, (), "both"),
    "sz": (P.szbk07, 660, 560, (), "both"),
    "wrail": (P.wago, 1010, 500, (2, "servo rail WAGO"), "both"),
    "pca": (L.pca9685, 1150, 460, (), "both"),
    "gtap": (P.wago, 990, 952, (5, "future GND tap"), "final"),
    "black": (P.bus_bar, 620, 950, ("black", "BLACK BUS BAR · ground star"), "both"),
}

# Servos: michaelkubina's channel map. Lower-leg servos get a 10-15cm extension.
SERVOS = [
    ("FL shoulder", 0), ("FL upper leg", 1), ("FL lower leg", 2),
    ("FR shoulder", 3), ("FR upper leg", 4), ("FR lower leg", 5),
    ("RL shoulder", 6), ("RL upper leg", 7), ("RL lower leg", 8),
    ("RR shoulder", 9), ("RR upper leg", 10), ("RR lower leg", 11),
]


def servo_xy(ch):
    """Two rows: front legs (ch0-5) and rear legs (ch6-11), each left to right in channel order."""
    row, col = divmod(ch, 6)
    return 1160 + col * 78, 650 + row * 120


# Servos plugged in on the bench today, by channel. The rest are drawn ghosted in the current view.
BENCH_SERVOS = {0: "replacement servo, horn off, centred at 1500us in session 7"}
