Web VPython 3.2
from vpython import *

scene.title = "Bungee Jump Simulation"
scene.background = color.white 
scene.width = 800
scene.height = 600

# --- Objects ---
# Building (Moved to the side so jumper can fall)
building = box(pos=vector(-10, 15, 0), size=vector(4, 30, 4), color=color.gray(0.5))
top_edge = vector(-8, 30, 0) # The point where the cord is tied

# Jumper (Created as a compound for easy movement)
head = sphere(pos=vector(0,0,0), radius=0.4, color=color.yellow)
body = cylinder(pos=vector(0,0,0), axis=vector(0,-1.2,0), radius=0.2, color=color.red)
arm_left = cylinder(pos=vector(0,-0.2,0), axis=vector(0.8, 0.8, 0), radius=0.07, color=color.red)
arm_right = cylinder(pos=vector(0,-0.2,0), axis=vector(-0.8, 0.8, 0), radius=0.07, color=color.red)
leg1 = cylinder(pos=vector(0,-1.2,0), axis=vector(0.2,-0.8,0), radius=0.07, color=color.red)
leg2 = cylinder(pos=vector(0,-1.2,0), axis=vector(-0.2,-0.8,0), radius=0.07, color=color.red)
jumper = compound([head, body, arm_left, arm_right, leg1, leg2])

# Initial position (standing on the edge)
jumper.pos = top_edge + vector(1, 0, 0)

# Bungee cord (using a curve for better visuals)
cord = cylinder(pos=top_edge, axis=jumper.pos - top_edge, radius=0.08, color=color.blue)

# --- Physics Constants ---
g = vector(0, -9.8, 0)
m = 70
k = 30        # Spring constant (stiffness)
L0 = 10       # Natural (unstretched) length of cord
b = 0.5       # Air resistance/damping (keeps them from bouncing forever)

# Initial conditions
v = vector(5, 3, 0)  # Initial jump: 3 units right, 2 units up
dt = 0.01
t = 0

# --- Animation Loop ---
while True:
    rate(100)
    
    # 1. Calculate displacement from the anchor point
    r_vec = jumper.pos - top_edge
    distance = mag(r_vec)
    
    # 2. Forces
    # Gravity
    Fg = m * g
    
    # Spring Force (only pulls if distance > natural length)
    Fspring = vector(0,0,0)
    if distance > L0:
        stretch = distance - L0
        # Hooke's Law: F = -k * x * direction
        Fspring = -k * stretch * norm(r_vec)
    
    # Damping (Air resistance)
    Fdrag = -b * v
    
    # Net Force
    Fnet = Fg + Fspring + Fdrag
    
    # 3. Update Physics (Euler-Cromer Integration)
    a = Fnet / m
    v = v + a * dt
    jumper.pos = jumper.pos + v * dt
    
    # 4. Update Visual Cord
    cord.axis = jumper.pos - top_edge
    
    t += dt