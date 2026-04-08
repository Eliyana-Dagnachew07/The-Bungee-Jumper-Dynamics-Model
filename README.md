
# The Bungee Jumper Dynamics Model
A 3D physical simulation developed in **Web VPython 3.2** to analyze the complex motion of a bungee jumper. This project explores the interaction of gravitational, elastic, and damping forces using numerical methods.
## 📌 Project Overview
This simulation models a jumper's descent from a building to study Newtonian mechanics and oscillatory motion. It specifically calculates real-time dynamics such as:
 * **Maximum Cord Stretch:** 18.9 m
 * **Maximum G-Force:** 1.77 g
 * **Minimum Height Above Ground:** 26.4m
## 🚀 Physics & Methodology
The motion is governed by Newton's Second Law (m \frac{d^2x}{dt^2} = \sum F). The simulation accounts for three primary forces:
 1. **Gravity (F_g = mg):** The dominant force during the initial free fall.
 2. **Spring Force (F_s = -k(x - L_0)):** The restoring force provided by the bungee cord (Hooke's Law).
## 📊 Key Observations
 * **Free Fall:** Initially, gravity causes the jumper to accelerate downward.
 * **Restoring Phase:** As the cord stretches, the spring force eventually exceeds the jumper's weight, decelerating the mass.
 * **Oscillation & Damping:** The competition between forces creates an oscillation that gradually subsides due to damping, preventing indefinite bouncing.
## 🛠️ Challenges & Solutions
 * **Time Step (dt) Calibration:** Finding the balance between calculation speed and numerical stability.
 * **Real-time Tracking:** Implementing loops to continuously monitor peak g-forces and stretch lengths.
 * **Parameter Tuning:** Adjusting the spring constant (k) and mass (m) to avoid unrealistic results or "overshoot".
## 👥 Contributors (Section B)
* **Group 1:**
Dagmawit Tademe, Eldana Kibru, Sara Abate, Sabrin Abuna, Sena Abyi, Yerosen Belete, Yerosen Getachew.
* **Group 7:**
Arsema Akalu, Eliyana Dagnachew, Etsubdink Gebru, Maraki Elias, Saron Solomon, Siyam Abdurezak.
### 🔗 Related Links
 * https://github.com/Eliyana-Dagnachew07/The-Bungee-Jumper-Dynamics-Model/blob/main/bungee-jump.py
 * https://www.glowscript.org/#/user/Eliyanadagnachew/folder/MyPrograms/program/bungeejumpsimulation/edit
 * [https://www.overleaf.com/2953134999kyfdbcbgyqkr#9b5916](https://www.overleaf.com/read/mhpckkcspnqc#cab928)
    ## Simulation overview
   <table>
  <tr>
    <th>free fall</th>
    <th>rebound</th>
    <th>stretching</th>
  </tr>
  <tr>
    <td><img src="free_fall.jpg" width="300"/></td>
    <td><img src="rebound.jpg" width="300"/></td>
    <td><img src="cord_stretching.jpg" width="300"/></td>
  </tr>
</table>
