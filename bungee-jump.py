web vpython 3.2
from vpython import *
from random import random

# ----------------------------- Scene Setup -----------------------------
scene.title = "Bungee Jump Simulation"
scene.width = 1000
scene.height = 600
scene.background = color.black
scene.range = 40
# FIXED CAMERA: Set the center once
scene.center = vector(5, 12, 0) 
scene.userspin = True

# ----------------------------- Stars and Moon -----------------------------
for i in range(100):
    sphere(pos=vector(random()*200-100, random()*80+10, random()*200-100),
           radius=0.3, color=color.white, emissive=True)
moon = sphere(pos=vector(80,80,-50), radius=7, color=color.gray(0.9), emissive=True)

# ----------------------------- Environment -----------------------------
ground = box(pos=vector(0,0,0), size=vector(60,1,60), color=vector(0.5,0.35,0.2))
building = box(pos=vector(-10,15,0), size=vector(4,30,4), color=color.gray(0.5))
top_edge = vector(-8,30,0)

# ----------------------------- Jumper -----------------------------
head = sphere(pos=vector(0,0,0), radius=0.4, color=color.yellow)
body = cylinder(pos=vector(0,0,0), axis=vector(0,-1.2,0), radius=0.2, color=color.red)
arm_left = cylinder(pos=vector(0,-0.2,0), axis=vector(0.8,0.8,0), radius=0.07, color=color.red)
arm_right = cylinder(pos=vector(0,-0.2,0), axis=vector(-0.8,0.8,0), radius=0.07, color=color.red)
leg1 = cylinder(pos=vector(0,-1.2,0), axis=vector(0.2,-0.8,0), radius=0.07, color=color.red)
leg2 = cylinder(pos=vector(0,-1.2,0), axis=vector(-0.2,-0.8,0), radius=0.07, color=color.red)
jumper = compound([head, body, arm_left, arm_right, leg1, leg2])

# ----------------------------- Initial State -----------------------------
# Start slightly out from the building with a tiny horizontal push
jumper.pos = top_edge + vector(0.5, 0, 0)
v = vector(1.5, 0, 0) 

# ----------------------------- Bungee Cord -----------------------------
cord = cylinder(pos=top_edge, axis=jumper.pos - top_edge, radius=0.1, color=color.cyan)

# ----------------------------- Physics -----------------------------
g = vector(0,-9.8,0)
m = 70
k = 100    # Spring stiffness
L0 = 8    # Unstretched length
b = 1.2    # Air resistance
dt = 0.01
t = 0

# Trackers
max_stretch = 0
max_g_force = 0
lowest_y = jumper.pos.y
lowest_reached = False

# Labels
live_info = label(pos=vector(-25,32,-10), height=14, box=False, color=color.white)
phase_info = label(pos=vector(25,32,-10), height=14, box=False, color=color.yellow)
fixed_info = label(pos=vector(0,-5,0), height=14, box=False, color=color.cyan)
record_info = label(pos=vector(40, 32, 10), box=False, height=15, color=color.yellow)
# ----------------------------- 5. CONTROLS -----------------------------
active = True

def control_physics(btn):
    global active
    active = not active
    btn.text = "PAUSE" if active else "RESUME"

def reset_jump():
    global v, t, max_stretch, max_g_force, lowest_y, lowest_reached, active
    
    jumper.pos = top_edge + vector(1, 0, 2)
    v = vector(1.5, 0, 0)
    t = 0
    
    # Zero out the stats
    max_stretch = 0
    max_g_force = 0
    lowest_y = jumper.pos.y
    lowest_reached = False
    
    # Clear the screen messages
    fixed_info.text = ""
    live_info.text = "Ready to jump..."
    active = True # Auto-start on reset
    scene.append_to_caption("\n") # Add space below the 3D window

button(text="Pause", bind=control_physics, color=color.orange)
button(text="Restart", bind=reset_jump, color=color.cyan)
# ----------------------------- 6. MAIN LOOP -----------------------------
while True:
    rate(100)
    if not active: continue
    
    t += dt

    # Physics Calculations
    r_vec = jumper.pos - top_edge
    distance = mag(r_vec)

    # Forces
    Fg = m * g
    Fspring = vector(0,0,0)
    stretch = 0

    if distance > L0:
        stretch = distance - L0
        # Hooke's Law: F = -k * x
        Fspring = -k * stretch * norm(r_vec)
        if stretch > max_stretch:
            max_stretch = stretch

    Fdrag = -b * v
    Fnet = Fg + Fspring + Fdrag

    # Motion Update
    a = Fnet / m
    v = v + a * dt
    jumper.pos = jumper.pos + v * dt
    
    # G-Force Tracker
    current_g = mag(a)/9.8
    if current_g > max_g_force:
        max_g_force = current_g

    # Phase Detection
    if distance < L0:
        phase = " Phase 1 Free fall"
    elif v.y < 0:
        phase = " Phase 2 Elastic streching"
    else:
        phase = "Phase 3 Rebounding and oscillation"
    
    phase_info.text = phase

    # Update Visual Cord
    cord.axis = jumper.pos - top_edge

    # Track lowest point
    if jumper.pos.y < lowest_y:
        lowest_y = jumper.pos.y
    if not lowest_reached and v.y > 0 and distance > L0:
        lowest_reached = True

    # Stop oscillation when energy is dissipated
    if lowest_reached and mag(v) < 0.2 and abs(distance - (L0 + (m*9.8/k))) < 0.1:
        v = vector(0,0,0)
 # 5. Update HUD
    live_info.text = (
        "Time: " + str(round(t,2)) + "s\n" +
        "Height: " + str(round(jumper.pos.y,1)) + "m\n" +
        "G-Force: " + str(round(current_g, 2)) + " g"
    )
    record_info.text = "MAX G: " + round(max_g_force, 2) + "\nMAX STRETCH: " + round(max_stretch, 1) + "m"


       # Equilibrium stop check
    equilibrium_dist = L0 + (mag(Fg)/k)
    if mag(v) < 0.05 and abs(distance - equilibrium_dist) < 0.1:
        v = vector(0,0,0)
        fixed_info.text = "Stable. Max G experienced: " + str(round(max_g_force, 2))
        break
