Web VPython 3.2
from vpython import *

# --- Scene Setup ---
scene.title = " Bungee Jump simulation"
scene.background = color.white 
scene.width = 800
scene.height = 600

# --- Objects ---
# Ground at y=0
ground = box(pos=vector(0, -0.5, 0), size=vector(60, 1, 60), color=color.green)

# Building (30 units high)
building = box(pos=vector(-10, 15, 0), size=vector(4, 30, 4), color=color.gray(0.5))
top_edge = vector(-8, 30, 0) # The anchor point for the cord

# Jumper (Added make_trail to see the fall path)
head = sphere(pos=vector(0,0,0), radius=0.4, color=color.yellow)
body = cylinder(pos=vector(0,0,0), axis=vector(0,-1.2,0), radius=0.2, color=color.red)
arm_left = cylinder(pos=vector(0,-0.2,0), axis=vector(0.8, 0.8, 0), radius=0.07, color=color.red)
arm_right = cylinder(pos=vector(0,-0.2,0), axis=vector(-0.8, 0.8, 0), radius=0.07, color=color.red)
leg1 = cylinder(pos=vector(0,-1.2,0), axis=vector(0.2,-0.8,0), radius=0.07, color=color.red)
leg2 = cylinder(pos=vector(0,-1.2,0), axis=vector(-0.2,-0.8,0), radius=0.07, color=color.red)
jumper = compound([head, body, arm_left, arm_right, leg1, leg2])

# Initial position
jumper.pos = top_edge + vector(1, 0, 0)

# Bungee cord
cord = cylinder(pos=top_edge, axis=jumper.pos - top_edge, radius=0.1, color=color.orange)

# --- Physics Constants ---
g = vector(0, -9.8, 0)
m = 70
k = 120       # High stiffness to ensure a quick stop
L0 = 10       # Shorter natural length gives more "braking distance"
b = 1.8       # Higher damping to simulate cord internal friction and air resistance

# Initial conditions
v = vector(4, 2, 0)  # Initial outward jump velocity
dt = 0.01
# --- INITIALIZE THE TRACKERS HERE ---
max_stretch = 0
max_g_force = 0

# --- Animation Loop ---
while True:
    rate(100)
    
    # 1. Calculate vector and distance from anchor
    r_vec = jumper.pos - top_edge
    distance = mag(r_vec)
    
    # 2. Force Calculations
    # Gravity
    Fg = m * g
    
    # Spring Force (Hooke's Law: only pulls when distance > L0)
    Fspring = vector(0,0,0)
    if distance > L0:
        stretch = distance - L0
        Fspring = -k * stretch * norm(r_vec)
        if stretch > max_stretch:
            max_stretch = stretch
      
        
       
    # Air resistance (Damping)
    Fdrag = -b * v
    
    # Net Force
    Fnet = Fg + Fspring + Fdrag
    
    # 3. Physics Integration (Euler-Cromer)
    a = Fnet / m
    v = v + a * dt
    jumper.pos = jumper.pos + v * dt
    current_g = mag(a) / 9.8
    if current_g > max_g_force:
        max_g_force = current_g
    
    # 4. Visual Updates
    cord.axis = jumper.pos - top_edge
    
    # Failure condition: If the jumper's feet (approx y-1.5) hit the ground
    if v.y > 0 and distance > L0: 
        # 2. These lines are inside the "if" (2 tabs in)
        print("--- LOWEST POINT REACHED ---")
        print("MAX CORD STRETCH: ", round(max_stretch, 2), "m")
        print("MAX G-FORCE:      ", round(max_g_force, 2), "g")
        print("HEIGHT ABOVE GROUND: ", round(jumper.pos.y - 1.5, 2), "m")
        break