# Power-Up & Power-Down Procedures

Rewritten in session 6, when the relay was removed. The servo rail now follows the battery: **a
connected pack means live servos.**

## The rule

- **The fuse stays in.** It is protection, not a switch. It comes out only while something on the
  power path is being changed, and a blade fuse holder's clips loosen if it is used as a switch.
- **The XT60 is connected last and disconnected first.** Whichever contact closes last takes the
  spark of the step-down and PCA9685 capacitors charging, and the XT60 is made for that.
- Once the main switch is mounted, the switch turns the robot on and off, and the XT60 is only mated
  or unmated with the switch off.

## Power-up

1. **Check what is plugged in.** Know whether servos are connected: they will be powered the moment
   the pack is.
2. **Fuse in**, if it was taken out.
3. **USB to the ESP32**, if the session needs serial or flashing. Optional: the ESP32 also runs from
   the red bus bar once the pack is in.
4. **Connect the XT60.** The 5V logic rail and the 6V servo rail come up together. The PCA9685 holds
   all its outputs off at power-up, so servos get power but no pulse until the firmware sends one.

## Power-down

1. **Stop the servos** — no motion, no load — before cutting power.
2. **Unplug the XT60.** The rails decay to 0V over a few seconds as the capacitors discharge.
3. **Unplug USB.** The red bus bar is live at 4.93V from USB alone, through the ESP32's VIN pin.
4. **Fuse out** only if the next job touches the power path.

## Before touching the power path

Pack unplugged, fuse out, USB unplugged, and **0V between the red and black bus bars** on the
multimeter before starting.
