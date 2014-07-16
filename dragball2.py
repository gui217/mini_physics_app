from visual import *

#Display config:
scene.range = 10 # fixed size, no autoscaling
srange = 10
swidth = 720
sheight = 1280
##

#Ball config:
ball = sphere(pos=(0.1,0.0,0.0), color=color.cyan)
ball.velocity =vector(0.0,0.0,0.0)
ball.acc = vector(0.0,0.0,0.0)
##

#Three magnets:
magnet_size = (0.2,20,1)
mid_magnet = box(pos=(0,0,0), size=magnet_size, color=color.blue)
left_magnet = box(pos=(-(1.0)*((swidth/float(sheight)))*srange,0,0), size=magnet_size, color=color.red)
right_magnet = box(pos=(+(1.0)*((swidth/float(sheight)))*srange,0,0), size=magnet_size, color=color.red)
##


drag_pos = None # no object picked yet

#Boolean for if mouse is dragging the ball:
drag_on = False
##

def grab(evt):
    global drag_on
    drag_on = True
    global drag_pos
    print drag_pos
    if evt.pick == ball:
        drag_pos = evt.pickpos
        scene.bind('mousemove', move, ball)
        scene.bind('mouseup', drop)

def move(evt, obj):
    global drag_pos
    # project onto xy plane, even if scene rotated:
    new_pos = scene.mouse.project(normal=(0,0,1))
    print new_pos
    if new_pos != drag_pos: # if mouse has moved
        # offset for where the ball was touched:
        obj.pos += new_pos - drag_pos
        print new_pos
        drag_pos = new_pos # update drag position
        print str(obj.pos)
    
            
    

def drop(evt):
    scene.unbind('mousemove', move)
    scene.unbind('mouseup', drop)
    global drag_on
    drag_on = False

#bind mouse click events for dragging the ball:
scene.bind('mousedown', grab)

fps = 30.0 #Frames per second/
dt = (1/fps)*0.1 #time difference between two steps

q_mid = 800 #Strength of middle magnet
q_sides = 800 #Strength of side magnet

max_acc = 200 #Maximum acceleration the ball can be given.


#if the ball is as close as this value to an attracting magnet,
#the ball will freeze (it prevents the ball from looping):
min_attraction = 0.4

while True:
    rate(fps)

    #Calculate the distances to the three magnets:
    #Notice that the distance is calculated according to x_axis distance alone!
    r_mid = abs(ball.pos[0]-mid_magnet.pos[0])
    r_right = abs(ball.pos[0]-right_magnet.pos[0])
    r_left = abs(ball.pos[0]-left_magnet.pos[0])
    #
    
    #Because the formula for magnet strength is proportional to (1/r^2), one needs to
    #check the r is not zero, so to avoid zero division
    if (r_mid==0):
        print "r_mid is zero!!: ",ball.pos
        ball.pos = ball.pos + (vector(0.5,0.0,0))
    else:
        
        #The total acceleration is the sum of the the accelerations due to the three magnets:
        ball.acc[0] = (ball.pos[0]/abs(ball.pos[0]))*q_mid*(1.0/power(r_mid,2))
        ball.acc[0] = ball.acc[0] -((ball.pos[0]-right_magnet.pos[0])/abs(ball.pos[0]-right_magnet.pos[0]))*q_sides*(1.0/power(r_right,2))
        ball.acc[0] = ball.acc[0] -((ball.pos[0]-left_magnet.pos[0])/abs(ball.pos[0]-left_magnet.pos[0]))*q_sides*(1.0/power(r_left,2))
        #

        #If the object is really close to the middle magnet it can produce
        #a strong repel force resulting in "un-natural" phenomena that kicks
        #the ball away. this due to the limitations of !!dt!!.
        #The phenomena can either be solved using the followin if clause,
        #or, by lowering the value of dt.
        if (abs(ball.acc[0])>=max_acc):
            ball.acc[0]=(ball.acc[0]/abs(ball.acc[0]))*max_acc

        #if the ball is really close to an attracting magnet then stop moving:
        if (abs(ball.pos[0]-right_magnet.pos[0])<=min_attraction) or (abs(ball.pos[0]-left_magnet.pos[0])<=min_attraction):
            ball.acc[0] = 0
            ball.velocity[0] = 0
            
        ball.velocity = ball.acc

        #if the user is currently draging the ball, don't change it's position:
        if drag_on == False:
            ball.pos = ball.pos + (ball.velocity*dt)
        #
        
            
    
