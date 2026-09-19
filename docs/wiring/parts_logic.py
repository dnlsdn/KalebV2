"""Logic boards, sensors and servos. Same conventions as parts.py."""

from parts import PCB_BLUE, PCB_GREEN, SILK, TERMINAL_BLUE, header_pin, pcb, terminal_block, text

# ESP32-DevKitC, 38 pins. J3 runs along the top edge, J2 along the bottom, both listed from the
# USB end (left) to the antenna end (right), which is the reverse of the silkscreen numbering.
ESP32_J3 = ["CLK", "SD0", "SD1", "15", "2", "0", "4", "16", "17", "5", "18", "19", "GND", "21", "RX", "TX", "22", "23", "GND"]
ESP32_J2 = ["5V", "CMD", "SD3", "SD2", "13", "GND", "12", "14", "27", "26", "25", "33", "32", "35", "34", "VN", "VP", "EN", "3V3"]


def esp32(x, y):
    pitch = 13
    w, h = 19 * pitch + 60, 96
    s = pcb(x, y, w, h, fill="#1a1a1a", edge="#555", holes=False)
    s += (f'<rect x="{x - 10}" y="{y + 36}" width="22" height="24" rx="3" fill="#aab" stroke="#667"/>'
          + text(x + 1, y + 76, "USB", 7)
          + f'<rect x="{x + w - 92}" y="{y + 20}" width="84" height="56" rx="3" fill="#b8bec6" stroke="#778"/>'
          + text(x + w - 50, y + 44, "ESP32-WROOM-32", 7, fill="#222")
          + text(x + w - 50, y + 56, "antenna end", 7, fill="#444")
          + text(x + 90, y + 52, "ESP32-DevKitC · 38 pin", 10, weight=600))
    pins = {}
    for i, n in enumerate(ESP32_J3):
        cx = x + 28 + i * pitch
        s += header_pin(cx, y + 9) + text(cx, y + 26, n, 6)
        pins.setdefault(n if n != "GND" else f"GND_top{i}", (cx, y - 2))
    for i, n in enumerate(ESP32_J2):
        cx = x + 28 + i * pitch
        s += header_pin(cx, y + h - 9) + text(cx, y + h - 19, n, 6)
        pins.setdefault(n if n != "GND" else "GND_bot", (cx, y + h + 2))
    pins["GND"] = pins["GND_bot"]
    return s, pins


def pca9685(x, y):
    """PCA9685 16-channel board as bought: logic pins both sides, 3-pin servo headers along the bottom."""
    w, h = 290, 104
    s = pcb(x, y, w, h)
    s += (f'<rect x="{x + 110}" y="{y + 38}" width="34" height="20" fill="#111"/>'
          + text(x + 127, y + 32, "PCA9685", 9, weight=700)
          + f'<rect x="{x + 176}" y="{y + 12}" width="26" height="34" rx="3" fill="#161616" stroke="#666"/>'
          + text(x + 189, y + 58, "1000µF", 7) + text(x + 189, y + 67, "10V", 7))
    tb, sc = terminal_block(x + 128, y - 18, 2, pitch=18)
    s += tb + text(sc[0][0], y - 22, "V+", 8, weight=700) + text(sc[1][0], y - 22, "GND", 8, weight=700)
    pins = {"V+": sc[0], "T_GND": sc[1]}
    for i, n in enumerate(["GND", "OE", "SCL", "SDA", "VCC", "V+"]):
        cy = y + 18 + i * 13
        s += header_pin(x + 10, cy) + text(x + 20, cy + 3, n, 7, anchor="start")
        pins[f"L_{n}"] = (x - 2, cy)
    for ch in range(16):
        cx = x + 24 + ch * 16 + (ch // 4) * 4
        for r, col in enumerate(("#1a1a1a", "#c62828", "#f5c518")):
            s += f'<rect x="{cx - 4}" y="{y + h - 32 + r * 9}" width="8" height="8" fill="{col}" fill-opacity=".85"/>'
        s += text(cx, y + h - 36, str(ch), 6)
        pins[f"ch{ch}"] = (cx, y + h + 2)
    s += text(x + w - 6, y + h - 6, "GND · V+ · PWM", 6, anchor="end")
    s += text(x + w - 8, y + 18, "PCA9685 · I2C 0x40", 9, anchor="end", weight=600)
    return s, pins


def mpu6050(x, y):
    w, h = 64, 44
    s = pcb(x, y, w, h)
    s += f'<rect x="{x + 22}" y="{y + 12}" width="16" height="16" fill="#111"/>'
    pins = {}
    for i, n in enumerate(["VCC", "GND", "SCL", "SDA"]):
        cx = x + 10 + i * 10
        s += header_pin(cx, y + h - 7)
        pins[n] = (cx, y + h + 2)
    s += text(x + w / 2, y - 6, "MPU6050 · 0x68", 9, cls="lbl")
    return s, pins


def hcsr04(x, y, label):
    w, h = 110, 50
    s = pcb(x, y, w, h, fill=PCB_GREEN, edge="#0f3d20", holes=False)
    for cx in (x + 28, x + 82):
        s += (f'<circle cx="{cx}" cy="{y + 25}" r="18" fill="#c9ced4" stroke="#8a9098"/>'
              f'<circle cx="{cx}" cy="{y + 25}" r="11" fill="#3b3f45"/>')
    pins = {}
    for i, n in enumerate(["VCC", "TRIG", "ECHO", "GND"]):
        cx = x + 40 + i * 10
        s += header_pin(cx, y + h - 4)
        pins[n] = (cx, y + h + 4)
    s += text(x + w / 2, y - 6, label, 9, cls="lbl")
    return s, pins


def servo(x, y, name, ch, extension=False):
    s = (f'<rect x="{x}" y="{y}" width="40" height="22" rx="2" fill="#141414" stroke="#555"/>'
         f'<circle cx="{x + 30}" cy="{y + 11}" r="6" fill="#d8d8d8"/>'
         + text(x + 13, y + 14, "MG996R", 5, fill="#aaa"))
    s += text(x + 20, y + 36, f"ch{ch}", 8, weight=700)
    s += text(x + 20, y + 47, name.split(" ", 1)[0], 7, fill="#b9c4d0")
    s += text(x + 20, y + 57, name.split(" ", 1)[1], 7, fill="#b9c4d0")
    return s, {"in": (x + 8, y)}


def voltage_sensor(x, y):
    w, h = 64, 44
    s = pcb(x, y, w, h, holes=False)
    tb, sc = terminal_block(x + 6, y + 6, 2, pitch=16, color=TERMINAL_BLUE)
    s += tb + f'<circle cx="{x + 50}" cy="{y + 16}" r="7" fill="#e8d9a0"/>'
    pins = {"VCC": sc[0], "GND": sc[1]}
    for i, n in enumerate(["S", "+", "-"]):
        cx = x + 14 + i * 14
        s += header_pin(cx, y + h - 7) + text(cx, y + h - 14, n, 6)
        pins[n] = (cx, y + h + 2)
    s += text(x + w / 2, y + h + 30, "voltage sensor 25V", 9, cls="lbl")
    return s, pins


def oled(x, y):
    w, h = 70, 56
    s = pcb(x, y, w, h, fill="#123a7a")
    s += f'<rect x="{x + 6}" y="{y + 16}" width="{w - 12}" height="32" fill="#05070b" stroke="#445"/>'
    pins = {}
    for i, n in enumerate(["GND", "VCC", "SCL", "SDA"]):
        cx = x + 17 + i * 12
        s += header_pin(cx, y + 7)
        pins[n] = (cx, y - 2)
    s += text(x + w / 2, y + h + 14, "OLED 0.96in SSD1306", 9, cls="lbl")
    return s, pins


def esp32cam(x, y):
    w, h = 64, 96
    s = pcb(x, y, w, h, fill="#1a1a1a", edge="#555", holes=False)
    s += (f'<circle cx="{x + 32}" cy="{y + 36}" r="13" fill="#222" stroke="#888"/>'
          f'<circle cx="{x + 32}" cy="{y + 36}" r="6" fill="#335"/>')
    pins = {"5V": (x + w + 2, y + 64), "GND": (x + w + 2, y + 76), "UART": (x + w + 2, y + 88)}
    for n, (px, py) in pins.items():
        s += header_pin(x + w - 8, py) + text(x + w - 16, py + 3, n, 6, anchor="end")
    s += text(x + w / 2, y + h + 14, "ESP32-CAM", 9, cls="lbl")
    return s, pins
