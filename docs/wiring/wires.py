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
BAR_SHARED = "Screw positions on the bars are illustrative; the bench keeps one free position on the black bar."


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
    w("bat-gnd", "both", "ok", "GND", "awg14", "LiPo − (XT60)", "black bus bar",
      ["bat.neg", ("x", 310), ("y", 930), ("xy", "black.s1")]),
    w("lm-in-gnd", "both", "ok", "GND", "awg14", "LM2596 IN−", "black bus bar",
      ["lm.IN-", ("x", 640), ("y", 925), ("xy", "black.s2")]),
    w("sz-in-gnd", "both", "ok", "GND", "awg14", "SZBK07 IN−", "black bus bar",
      ["sz.IN-", ("x", 656), ("y", 915), ("xy", "black.s4")]),

    # ---------------------------------------------------------------- 5V logic rail
    w("lm-red", "both", "ok", "5V", "pwr", "LM2596 OUT+", "red bus bar",
      ["lm.OUT+", ("x", 800), ("y", 370), ("xy", "red.s12")], "5.00V trimmed with no load, 4.98V under the logic load."),
    w("lm-out-gnd", "both", "ok", "GND", "pwr", "LM2596 OUT−", "black bus bar",
      ["lm.OUT-", ("x", 880), ("y", 920), ("xy", "black.s3")]),
    w("esp-vin", "both", "ok", "5V", "dupont", "ESP32 5V (VIN)", "red bus bar",
      ["esp.5V", ("y", 210), ("xy", "red.s11")], "USB back-feeds out of VIN: the red bar reads 4.93V with only USB plugged in."),
    w("esp-gnd", "both", "ok", "GND", "dupont", "ESP32 GND", "black bus bar",
      ["esp.GND_top18", ("y", 44), ("x", 890), ("y", 900), ("xy", "black.s7")]),

    # ---------------------------------------------------------------- 6V servo rail
    w("sz-rail", "both", "ok", "6V", "awg14", "SZBK07 OUT+", "servo rail WAGO",
      ["sz.OUT+", ("x", 940), ("y", 560), ("xy", "wrail.p1")],
      "Session 6: the relay was removed and its two wires joined in a WAGO 221-412, stripped to 11mm and tug-tested. The rail is live whenever the pack is connected."),
    w("rail-pca", "both", "ok", "6V", "awg16", "servo rail WAGO", "PCA9685 V+ screw",
      ["wrail.p2", ("y", 585), ("x", 1095), ("y", 420), ("xy", "pca.V+")],
      "AWG16 because the 3.5mm terminal takes 1.5mm² at most. Session 6: 6.0V with the pack connected, 0V after unplugging, decaying over a few seconds."),
    w("pca-gnd", "both", "ok", "GND", "awg16", "PCA9685 GND screw", "black bus bar",
      ["pca.T_GND", ("y", 410), ("x", 1625), ("y", 905), ("xy", "black.s6")],
      "Servo return current. Added in session 5, replacing a Dupont sized for logic."),
    w("sz-out-gnd", "both", "ok", "GND", "awg14", "SZBK07 OUT−", "black bus bar",
      ["sz.OUT-", ("x", 870), ("y", 910), ("xy", "black.s5")]),

    # ---------------------------------------------------------------- 3.3V and I2C
    w("esp-3v3", "both", "ok", "3V3", "dupont", "ESP32 3V3", "3V3 WAGO", ["esp.3V3", ("y", 200), ("xy", "w33.p1")], WAGO_DUPONT),
    w("esp-sda", "both", "ok", "SDA", "dupont", "ESP32 GPIO21", "SDA WAGO",
      ["esp.21", ("y", 34), ("x", 985), ("y", 205), ("xy", "wsda.p1")], WAGO_DUPONT),
    w("esp-scl", "both", "ok", "SCL", "dupont", "ESP32 GPIO22", "SCL WAGO",
      ["esp.22", ("y", 24), ("x", 1080), ("y", 212), ("xy", "wscl.p1")], WAGO_DUPONT),
    w("pca-vcc", "both", "ok", "3V3", "dupont", "3V3 WAGO", "PCA9685 VCC",
      ["w33.p2", ("y", 240), ("x", 1140), ("yx", "pca.L_VCC")],
      "On 3.3V, not 5V: its 10k I2C pull-ups tie to VCC and would idle SDA/SCL above the ESP32's 3.6V limit."),
    w("pca-sda", "both", "ok", "SDA", "dupont", "SDA WAGO", "PCA9685 SDA", ["wsda.p2", ("y", 250), ("x", 1130), ("yx", "pca.L_SDA")]),
    w("pca-scl", "both", "ok", "SCL", "dupont", "SCL WAGO", "PCA9685 SCL", ["wscl.p2", ("yx", "pca.L_SCL")]),
    w("pca-oe", "both", "ok", "GND", "dupont", "PCA9685 OE", "black bus bar",
      ["pca.L_OE", ("x", 1085), ("y", 870), ("xy", "black.s11")], "OE is active low: floating high it disables all sixteen outputs."),
    w("mpu-vcc", "both", "ok", "3V3", "dupont", "3V3 WAGO", "MPU6050 VCC", ["w33.p3", ("y", 232), ("xy", "mpu.VCC")]),
    w("mpu-sda", "both", "ok", "SDA", "dupont", "SDA WAGO", "MPU6050 SDA", ["wsda.p3", ("y", 222), ("xy", "mpu.SDA")]),
    w("mpu-scl", "both", "ok", "SCL", "dupont", "SCL WAGO", "MPU6050 SCL", ["wscl.p3", ("y", 200), ("xy", "mpu.SCL")]),
    w("mpu-gnd", "both", "ok", "GND", "dupont", "MPU6050 GND", "black bus bar",
      ["mpu.GND", ("y", 110), ("x", 1615), ("y", 875), ("xy", "black.s11")], BAR_SHARED),

    # ---------------------------------------------------------------- current sensor and ultrasonic power
    w("acs-vcc", "both", "ok", "5V", "dupont", "ACS712 VCC", "red bus bar", ["acs.VCC", ("x", 628), ("y", 380), ("xy", "red.s10")]),
    w("acs-gnd", "both", "ok", "GND", "dupont", "ACS712 GND", "black bus bar", ["acs.GND", ("x", 632), ("y", 890), ("xy", "black.s9")]),
    w("esp-acs", "final", "later", "ADC", "dupont", "ESP32 GPIO34", "ACS712 OUT",
      ["esp.34", ("y", 335), ("x", 620), ("yx", "acs.OUT")],
      "Output is 2.5V at 0A, 66mV/A. michaelkubina orients the sensor so load current reads negative, keeping the ADC below 3.3V."),
    w("hc1-vcc", "both", "ok", "5V", "dupont", "HC-SR04 #1 VCC", "red bus bar", ["hc1.VCC", ("y", 200), ("xy", "red.s1")]),
    w("hc2-vcc", "both", "ok", "5V", "dupont", "HC-SR04 #2 VCC", "red bus bar", ["hc2.VCC", ("y", 190), ("xy", "red.s3")]),
    w("hc1-gnd", "both", "ok", "GND", "dupont", "HC-SR04 #1 GND", "black bus bar",
      ["hc1.GND", ("y", 140), ("x", 14), ("y", 885), ("xy", "black.s10")], BAR_SHARED),
    w("hc2-gnd", "both", "ok", "GND", "dupont", "HC-SR04 #2 GND", "black bus bar",
      ["hc2.GND", ("y", 150), ("x", 22), ("y", 880), ("xy", "black.s10")], BAR_SHARED),

    # ---------------------------------------------------------------- after it walks: routing not decided, drawn loose
    w("vs-in", "final", "later", "BAT+", "dupont", "after the fuse", "voltage sensor VCC", ["acs.IP+", ("curve", "vsens.VCC")]),
    w("vs-gnd", "final", "later", "GND", "dupont", "voltage sensor GND", "future GND tap", ["vsens.GND", ("curve", "gtap.p1")]),
    w("tap-bar", "final", "later", "GND", "awg16", "future GND tap", "black bus bar", ["gtap.p5", ("curve", "black.s12")],
      "The black bar has two free positions since session 6. A WAGO off one of them takes the late grounds."),
    w("cam-5v", "final", "later", "5V", "dupont", "ESP32-CAM 5V", "red bus bar", ["cam.5V", ("curve", "red.s5")]),
    w("cam-gnd", "final", "later", "GND", "dupont", "ESP32-CAM GND", "future GND tap", ["cam.GND", ("curve", "gtap.p2")]),
    w("oled-vcc", "final", "later", "3V3", "dupont", "OLED VCC", "3V3 WAGO", ["oled.VCC", ("curve", "w33.p4")]),
    w("oled-sda", "final", "later", "SDA", "dupont", "OLED SDA", "SDA WAGO", ["oled.SDA", ("curve", "wsda.p4")]),
    w("oled-scl", "final", "later", "SCL", "dupont", "OLED SCL", "SCL WAGO", ["oled.SCL", ("curve", "wscl.p3")],
      "One of the two I2C WAGOs on the bench is a 3-port 221-413 and is already full. Swap it for a 221-415 first."),
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
