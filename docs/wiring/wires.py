"""Every connection on the drawing.

Route mini-language: start at a pin ("part.pin"), then steps
    ("x", v)  move horizontally to x      ("y", v)  move vertically to y
    ("xy", pin) horizontal to the pin's x, then vertical onto it
    ("yx", pin) vertical to the pin's y, then horizontal onto it
    ("curve", pin) a loose curve, used for wires whose routing is not decided yet

status: ok = built and measured · plan = still to build, on the path to walking ·
        later = after the robot walks · open = exists but deliberately not connected
view:   both | current | final
"""

KINDS = {  # stroke width on the drawing, and the label shown in the details
    "awg14": (6.5, "AWG14 silicone"),
    "awg16": (4.8, "AWG16 silicone"),
    "pwr": (4.2, "power lead, soldered to the pad, gauge not recorded"),
    "dupont": (2.6, "Dupont jumper, ~0.08mm²"),
}

NETS = {  # colour on the drawing
    "BAT+": "#e53935", "6V": "#e53935", "5V": "#ff6b6b", "GND": "#161616", "3V3": "#c77dff",
    "SDA": "#ffd54a", "SCL": "#ff9f43", "SIG": "#4fc3f7", "ADC": "#9ccc65",
}

WAGO_DUPONT = "Dupont in a WAGO 221 is below its 0.14mm² minimum: fold the conductor back and tug-test."


def w(id, view, status, net, kind, frm, to, route, note=""):
    return dict(id=id, view=view, status=status, net=net, kind=kind, frm=frm, to=to, route=route, note=note)


WIRES = [
    # ---------------------------------------------------------------- battery to the two step-downs
    w("bat-fuse", "current", "ok", "BAT+", "awg14", "LiPo + (XT60)", "fuse holder",
      ["bat.pos", ("xy", "fuse.in")], "7.55V after the fuse, same as the pack. The fuse stays out while anything on the power path changes."),
    w("bat-sw", "final", "plan", "BAT+", "awg14", "LiPo + (XT60)", "main switch",
      ["bat.pos", ("xy", "sw.in")], "Main switch on battery +, as in michaelkubina and Leika. Owned, not mounted. With the relay gone it is the only servo power control, so it must be rated for the full 10A DC."),
    w("sw-fuse", "final", "plan", "BAT+", "awg14", "main switch", "fuse holder", ["sw.out", ("xy", "fuse.in")]),
    w("fuse-acs", "both", "ok", "BAT+", "awg14", "fuse holder", "ACS712 IP+",
      ["fuse.out", ("x", 495), ("yx", "acs.IP+")], "ATO 10A blade in an inline holder."),
    w("acs-split", "both", "ok", "BAT+", "awg14", "ACS712 IP−", "split WAGO",
      ["acs.IP-", ("x", 508), ("y", 612), ("xy", "wsplit.p1")]),
    w("split-lm", "both", "ok", "BAT+", "awg14", "split WAGO", "LM2596 IN+",
      ["wsplit.p2", ("y", 650), ("x", 648), ("yx", "lm.IN+")]),
    w("split-sz", "both", "ok", "BAT+", "awg14", "split WAGO", "SZBK07 IN+",
      ["wsplit.p3", ("yx", "sz.IN+")]),
    # ---------------------------------------------------------------- ground: three WAGOs in a chain (session 20)
    w("bat-gnd", "both", "ok", "GND", "awg14", "LiPo − (XT60)", "WAGO A",
      ["bat.neg", ("x", 310), ("y", 1030), ("xy", "gA.p1")],
      "Session 20: the bus bars came out. All the heavy ground wires share WAGO A, so the servo and battery current never crosses the WAGO-to-WAGO links."),
    w("sz-in-gnd", "both", "ok", "GND", "awg14", "SZBK07 IN−", "WAGO A",
      ["sz.IN-", ("x", 620), ("y", 1040), ("xy", "gA.p2")],
      "The SZBK07's OUT− has no wire, found in session 20; the documentation had it on the bar. Input and output share ground on the board, so the servo return comes back through IN−."),
    w("pca-gnd", "both", "ok", "GND", "awg16", "PCA9685 GND screw", "WAGO A",
      ["pca.T_GND", ("y", 410), ("x", 1625), ("y", 1050), ("xy", "gA.p3")],
      "Servo return current. Added in session 5, replacing a Dupont sized for logic."),
    w("gnd-ab", "both", "ok", "GND", "pwr", "WAGO A", "WAGO B", ["gA.p4", ("y", 1020), ("xy", "gB.p1")],
      "A short offcut of power wire, stripped 11mm at both ends."),
    w("lm-in-gnd", "both", "ok", "GND", "awg14", "LM2596 IN−", "WAGO B",
      ["lm.IN-", ("x", 640), ("y", 925), ("x", 905), ("y", 1060), ("xy", "gB.p2")],
      "The LM2596's OUT− has no wire either, found in session 20. Its input and output share ground, so the logic return comes back through IN−."),
    w("esp-gnd", "both", "ok", "GND", "dupont", "ESP32 GND", "WAGO B",
      ["esp.GND_top18", ("y", 44), ("x", 890), ("y", 1066), ("xy", "gB.p3")], WAGO_DUPONT),
    w("gnd-bc", "both", "ok", "GND", "pwr", "WAGO B", "WAGO C", ["gB.p4", ("y", 1020), ("xy", "gC.p1")],
      "A short offcut of power wire, stripped 11mm at both ends."),
    w("mpu-gnd", "both", "ok", "GND", "dupont", "MPU6050 GND", "WAGO C",
      ["mpu.GND", ("y", 110), ("x", 1615), ("y", 1070), ("xy", "gC.p2")], WAGO_DUPONT),
    w("acs-gnd", "both", "ok", "GND", "dupont", "ACS712 GND", "WAGO C",
      ["acs.GND", ("x", 632), ("y", 905), ("x", 1035), ("y", 1010), ("xy", "gC.p3")], WAGO_DUPONT),
    w("hc1-gnd", "both", "ok", "GND", "dupont", "HC-SR04 #1 GND", "WAGO C",
      ["hc1.GND", ("y", 140), ("x", 14), ("y", 1074), ("xy", "gC.p4")], WAGO_DUPONT),
    w("hc2-gnd", "both", "ok", "GND", "dupont", "HC-SR04 #2 GND", "WAGO C",
      ["hc2.GND", ("y", 150), ("x", 22), ("y", 1078), ("xy", "gC.p5")], WAGO_DUPONT),
    # ---------------------------------------------------------------- 5V logic: WAGO D
    w("lm-red", "both", "ok", "5V", "pwr", "LM2596 OUT+", "WAGO D",
      ["lm.OUT+", ("x", 800), ("y", 370), ("x", 307), ("xy", "w5.p1")], "5.00V trimmed with no load; 4.95V at WAGO D under the logic load, session 20."),
    w("esp-vin", "both", "ok", "5V", "dupont", "ESP32 5V (VIN)", "WAGO D",
      ["esp.5V", ("y", 345), ("xy", "w5.p2")], "USB back-feeds out of VIN: the 5V node reads about 4.9V with only USB plugged in."),
    w("acs-vcc", "both", "ok", "5V", "dupont", "ACS712 VCC", "WAGO D", ["acs.VCC", ("x", 628), ("y", 360), ("xy", "w5.p3")], WAGO_DUPONT),
    w("hc1-vcc", "both", "ok", "5V", "dupont", "HC-SR04 #1 VCC", "WAGO D", ["hc1.VCC", ("y", 350), ("xy", "w5.p4")], WAGO_DUPONT),
    w("hc2-vcc", "both", "ok", "5V", "dupont", "HC-SR04 #2 VCC", "WAGO D", ["hc2.VCC", ("y", 355), ("xy", "w5.p5")], WAGO_DUPONT),
    # ---------------------------------------------------------------- 6V servo rail
    w("sz-rail", "both", "ok", "6V", "awg14", "SZBK07 OUT+", "servo rail WAGO",
      ["sz.OUT+", ("x", 940), ("y", 560), ("xy", "wrail.p1")],
      "Session 6: the relay was removed and its two wires joined in a WAGO 221-412, stripped to 11mm and tug-tested. The rail is live whenever the pack is connected."),
    w("rail-pca", "both", "ok", "6V", "awg16", "servo rail WAGO", "PCA9685 V+ screw",
      ["wrail.p2", ("y", 585), ("x", 1095), ("y", 420), ("xy", "pca.V+")],
      "AWG16 because the 3.5mm terminal takes 1.5mm² at most. 6.01V with the pack connected, session 20."),
    # ---------------------------------------------------------------- 3.3V and I2C through the PCA9685's two headers (session 20)
    w("esp-3v3", "both", "ok", "3V3", "dupont", "ESP32 3V3", "PCA9685 VCC (header 1)",
      ["esp.3V3", ("y", 200), ("x", 1110), ("yx", "pca.L_VCC")],
      "The PCA9685's two 6-pin headers are joined pin for pin on the board, checked by continuity in session 20, so it distributes I2C and 3.3V. On 3.3V, not 5V: its 10k pull-ups tie to VCC."),
    w("esp-sda", "both", "ok", "SDA", "dupont", "ESP32 GPIO21", "PCA9685 SDA (header 1)",
      ["esp.21", ("y", 34), ("x", 1100), ("yx", "pca.L_SDA")]),
    w("esp-scl", "both", "ok", "SCL", "dupont", "ESP32 GPIO22", "PCA9685 SCL (header 1)",
      ["esp.22", ("y", 24), ("x", 1090), ("yx", "pca.L_SCL")]),
    w("pca-oe", "both", "ok", "GND", "dupont", "PCA9685 OE", "PCA9685 GND (header 1)",
      ["pca.L_OE", ("x", 1130), ("yx", "pca.L_GND")], "A short jumper on the same header. OE is active low: floating high it disables all sixteen outputs."),
    w("mpu-vcc", "both", "ok", "3V3", "dupont", "PCA9685 VCC (header 2)", "MPU6050 VCC",
      ["pca.R_VCC", ("x", 1470), ("y", 140), ("xy", "mpu.VCC")]),
    w("mpu-sda", "both", "ok", "SDA", "dupont", "PCA9685 SDA (header 2)", "MPU6050 SDA",
      ["pca.R_SDA", ("x", 1480), ("y", 150), ("xy", "mpu.SDA")]),
    w("mpu-scl", "both", "ok", "SCL", "dupont", "PCA9685 SCL (header 2)", "MPU6050 SCL",
      ["pca.R_SCL", ("x", 1490), ("y", 160), ("xy", "mpu.SCL")]),
    # ---------------------------------------------------------------- current sensor output
    w("esp-acs", "final", "later", "ADC", "dupont", "ESP32 GPIO34", "ACS712 OUT",
      ["esp.34", ("y", 335), ("x", 620), ("yx", "acs.OUT")],
      "Output is 2.5V at 0A, 66mV/A. michaelkubina orients the sensor so load current reads negative, keeping the ADC below 3.3V."),
    # ---------------------------------------------------------------- after it walks: routing not decided, drawn loose
    w("vs-in", "final", "later", "BAT+", "dupont", "after the fuse", "voltage sensor VCC", ["acs.IP+", ("curve", "vsens.VCC")]),
    w("vs-gnd", "final", "later", "GND", "dupont", "voltage sensor GND", "future GND tap", ["vsens.GND", ("curve", "gtap.p1")]),
    w("tap-bar", "final", "later", "GND", "pwr", "future GND tap", "WAGO A", ["gtap.p5", ("curve", "gA.p5")],
      "WAGO A keeps one free port since session 20. A spare 221-415 chained off it takes the late grounds."),
    w("cam-5v", "final", "later", "5V", "dupont", "ESP32-CAM 5V", "5V node", ["cam.5V", ("curve", "w5.p5")],
      "WAGO D is full: the camera needs a second 5V WAGO chained off it, decided when it is integrated."),
    w("cam-gnd", "final", "later", "GND", "dupont", "ESP32-CAM GND", "future GND tap", ["cam.GND", ("curve", "gtap.p2")]),
    w("oled-vcc", "final", "later", "3V3", "dupont", "OLED VCC", "IMU VCC, spliced", ["oled.VCC", ("curve", "mpu.VCC")],
      "Both PCA9685 headers are taken: the OLED joins the IMU's three wires with a soldered Y-splice."),
    w("oled-sda", "final", "later", "SDA", "dupont", "OLED SDA", "IMU SDA, spliced", ["oled.SDA", ("curve", "mpu.SDA")]),
    w("oled-scl", "final", "later", "SCL", "dupont", "OLED SCL", "IMU SCL, spliced", ["oled.SCL", ("curve", "mpu.SCL")]),
    w("oled-gnd", "final", "later", "GND", "dupont", "OLED GND", "future GND tap", ["oled.GND", ("curve", "gtap.p3")]),
]

# Loose ends: signals whose ESP32 pin is read from the firmware when the part is integrated.
STUBS = [
    dict(view="final", status="later", pin="hc1.TRIG", dx=0, dy=30, net="SIG", label="", note="TRIG: 3.3V from the ESP32 is enough. Pin comes from the firmware config."),
    dict(view="final", status="later", pin="hc1.ECHO", dx=0, dy=30, net="SIG", label="TRIG/ECHO · pins TBD", note="5V echo through a 1k/2k divider before the ESP32."),
    dict(view="final", status="later", pin="hc2.TRIG", dx=0, dy=30, net="SIG", label="", note="TRIG: 3.3V from the ESP32 is enough. Pin comes from the firmware config."),
    dict(view="final", status="later", pin="hc2.ECHO", dx=0, dy=30, net="SIG", label="TRIG/ECHO · pins TBD", note="5V echo through a 1k/2k divider before the ESP32."),
    dict(view="final", status="later", pin="vsens.S", dx=0, dy=40, net="ADC", label="S · ADC pin TBD", note="Divides by 5: 8.4V reads 1.68V."),
    dict(view="final", status="later", pin="cam.UART", dx=40, dy=0, net="SIG", label="UART · pins TBD", note="Serial link to the main ESP32."),
]
