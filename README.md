This repository documents my personal journey building a **SpotMicro-style quadruped robot** using the excellent open-source work available at:

**SpotMicroESP32 by michaelkubina**  
https://github.com/michaelkubina/SpotMicroESP32/

---

## About Me

I am a Master's student in **Computer Engineering – Cybersecurity curriculum** at Roma Tre University (Italy).  
Robotics and electronics are not my main field of study — they are simply a **passion project** I pursue in my spare time.

Because of this, many of the steps in this repository may seem basic or overly detailed, but that is intentional:  
**my goal is to help beginners like me build a complex hobby robot from scratch without fear or confusion.**

---

## Purpose of This Repository

This project serves as:

- a **complete, step-by-step build log** of my SpotMicro robot  
- a **beginner-friendly guide**, with each step explained clearly and practically  
- a place to store **photos, wiring diagrams, and notes** for each stage  
- a **public reference** for anyone who wants to follow the same path  
- a **personal archive** of my progress, mistakes, and solutions  

Each step is documented inside the `main-steps/` directory.  
Most steps include photos or illustrations.

Test sketches live in [`code/`](code/) — small programs that each check one thing, so a fault can be
traced to the wiring or to the software without guessing.

For the current state of the build and what comes next, see [STATE.md](STATE.md).

---

## A note on the firmware

The reference project above is a **mechanical and electrical design** and states that it has no
programming part. Wiring this robot exactly as documented produces a machine that cannot move, and
it took me three sessions to notice.

The firmware I am targeting is [SpotMicroESP32-Leika by
runeharlyk](https://github.com/runeharlyk/SpotMicroESP32-Leika), one of the community forks the
reference project recommends. If you are following the same path, decide this early: the firmware
dictates the pinout, so choosing it after the wiring means doing the wiring twice.

---

## Contact & Feedback

I’m happy to receive:

- feedback  
- suggestions  
- improvements  
- alternative approaches  
- corrections  

If something is unclear or you want more information about a specific step, feel free to contact me — I will gladly help.

---

## Disclaimer

This is a hobby project.  
I am learning robotics and electronics as I go, so expect simple explanations, incremental learning, and occasional mistakes.  
Everything I publish here is meant to help other beginners who want to start a similar adventure.

---

## Acknowledgements

A huge thank you to the creators and contributors of the original **SpotMicroESP32** project, whose work inspired this entire repository.
