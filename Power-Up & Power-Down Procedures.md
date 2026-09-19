# Power-Up & Power-Down Procedures

Rewritten in session 6, when the relay was removed. The servo rail now follows the battery: **a
connected pack means live servos.**

## The rule

- **The fuse stays in.** It is protection, not a switch. It comes out only while something on the
  power path is being changed, and a blade fuse holder's clips loosen if it is used as a switch.
- **The XT60 is connected last and disconnected first.** Whichever contact closes last takes the
  spark of the step-down and PCA9685 capacitors charging, and the XT60 is made for that.
- **USB and the pack are never connected together.** Espressif's DevKitC guide: power from one and
  only one of USB, the 5V pin or the 3V3 pin, or the board and the supply can be damaged. The 5V pin
  is fed from the red bus bar, so the pack counts. Flash on USB with the XT60 unplugged, unplug USB,
  then connect the pack. Corrected in session 7; session 6's version allowed both.
- Once the main switch is mounted, the switch turns the robot on and off, and the XT60 is only mated
  or unmated with the switch off.

## Power-up

1. **Check what is plugged in.** Know whether servos are connected: they will be powered the moment
   the pack is.
2. **Fuse in**, if it was taken out.
3. **USB unplugged.** Flashing is done before this, on USB alone with the XT60 unplugged. The sketch
   stays in flash and runs when the pack powers the board.
4. **Connect the XT60.** The 5V logic rail and the 6V servo rail come up together. The PCA9685 holds
   all its outputs off at power-up, so servos get power but no pulse until the firmware sends one.

## Power-down

1. **Stop the servos** — no motion, no load — before cutting power.
2. **Unplug the XT60.** The rails decay to 0V over a few seconds as the capacitors discharge.
3. **Fuse out** only if the next job touches the power path.

## Flashing

XT60 unplugged, then USB in. With USB alone the red bus bar is live at 4.93V through the ESP32's VIN
pin, and the PCA9685 runs from the ESP32's 3V3, so it already generates pulses — but the servo rail is
dead. Unplug USB before connecting the pack.

## Before touching the power path

Pack unplugged, fuse out, USB unplugged, and **0V between the red and black bus bars** on the
multimeter before starting.
