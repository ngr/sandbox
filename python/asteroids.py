# "ASTEROIDS"
# Nikolay Grishchenko, 2014
# web@grischenko.ru
#
# PLEASE BE AWARE THAT THIS CODE IS ADOPTED ONLY
# FOR CODESKULPTOR IN COURSERA CLASS.
# IT DOES NOT COMPILE AS IS!
#
import simplegui
import math
from random import random, randrange, choice

# Game settings. Constants.
LIVES = 3			# Default lives
WIDTH = 800			# Screen Width
HEIGHT = 600		# Screen Height
THRUST = 0.1		# Acceleration when thrust is ON
TURN_SPEED = 0.1	# Angular velocity modifier
FRICTION = 0.98		# Pseudo friction modifier
POINTS_FOR_ROCK = 10	# Scores for each asteroid
EXPLOSION_FRAMES = 24	# Explosion animation frames 
ROCK_LIFETIME = 0	# Asteroid selfdestroy timeout. 0 = n/a
ROCK_LIMIT = 10		# Maximum asteroids in space.
ROCK_SPEEDUP = [20.0, 50.0] # Smaller vals fasten rocks sooner
MIN_DISTANCE = 10	# Minimum distance from ship for new rocks
MISSILE_LIFETIME = 1	# Missile selfdestroy timeout
MISSILE_THRUST = 3	# Initial speed of the missile. 
MISSILE_SPEEDUP = 100.0	# Smaller vals increase faster

# Global variables
""" You can use arrows or wa[s]d to control the ship. Space
to fire. 1st element is type of vector,  2nd - direction """
inputs = { 	'w': [0, 1],
            'a': [1, -1],
            'd': [1, 1],
            'up': [0, 1],
            'left': [1, -1],
            'right': [1, 1],
            'space': [2, 1]
         }
best = 0			# Best results score

class ImageInfo:
    """ Parameters of images should be defined in this Class """
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated
    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, MISSILE_LIFETIME)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
if ROCK_LIFETIME:
    asteroid_info = ImageInfo([45, 45], [90, 90], 40, ROCK_LIFETIME)
else:
    asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 0.4, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

####################
# Helper functions #
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

###########
# Classes #
class Ship:
    """ This class should really be a child of Sprite because there
    are many same actions. But I am lazy to make refactoring now. """
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        """ Draw image and play sound with respect to self.thrust value """
        if self.thrust:
            canvas.draw_image(self.image,
                [self.image_center[0] + self.image_size[0], self.image_center[0]],
                self.image_size, self.pos, self.image_size, self.angle)
            ship_thrust_sound.play()
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                          self.pos, self.image_size, self.angle)
            ship_thrust_sound.rewind()

    def update(self):
        self.angle += self.angle_vel	# Update angle
        
        for p in range(2):				# Update position
            self.pos[p] += self.vel[p]
        
        # This update is a bit complex so that the ship wraps
        # only when it is completely out of screen (not center)
        self.pos[0] = ((self.pos[0] + self.radius) % (WIDTH + self.radius * 2)) - self.radius
        self.pos[1] = ((self.pos[1] + self.radius) % (HEIGHT + self.radius * 2)) - self.radius

        if self.thrust:					# Update velocity
            self.vel = [self.vel[i] + (angle_to_vector(self.angle)[i] * THRUST)\
                        for i in range(len(self.vel))]
        # Make some friction also used for speed limit.
        self.vel = [self.vel[i] * FRICTION for i in range(len(self.vel))]

    def update_vel(self, v):
        """ This updates thrust and angular velocity.
        'inputs' global dictionary helps understand this function """
        if v[0] == 0:
            self.thrust = True if v[1] == 1 else False
        elif v[0] == 1:
            self.angle_vel = v[1] * TURN_SPEED

    def get_params(self):
        """ Returns all Ship properties in a dictionary. """
        return({'pos': self.pos,
                'vel': self.vel,
                'angle': self.angle,
                'radius': self.radius,
                'cannon': [self.pos[0]+math.cos(self.angle)*self.radius,
                           self.pos[1]+math.sin(self.angle)*self.radius]
                })

class Sprite:
    """ Main class for 'space' objects. """
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def get_obj_type(self):
        return self.obj_type
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size,\
                          self.pos, self.image_size, self.angle)

    def update(self):
        self.angle += self.angle_vel	# Update angle
        
        for p in range(2):				# Update position
            self.pos[p] += self.vel[p]
        # Warps object when it goes of the screen
        self.pos[0] = ((self.pos[0] + self.radius) % (WIDTH + self.radius * 2)) - self.radius
        self.pos[1] = ((self.pos[1] + self.radius) % (HEIGHT + self.radius * 2)) - self.radius

        self.age += 0.01666667 # Approximately 1/60 of a second or 1 Tick
        
        # Self destruct object if too old
        if self.age >= self.lifespan:
            if self in missiles:
                missiles.remove(self)
            elif self in rocks:
                rocks.remove(self)
            elif self in explosions:
                explosions.remove(self)
        
        # Animate
        if self.animated:
            ii = ((self.age % EXPLOSION_FRAMES) // 1) + 1
            self.image_center = [self.image_center[0] / ii + self.image_size[0] * ii,
                                 self.image_center[1]]

    def collide(self, obj):
        """ Returns True if obj collides with self """
        return dist(self.pos, obj.get_params()['pos']) < (self.radius + obj.get_params()['radius'])

    def get_params(self):
        """ Returns main Sprite properties in a dictionary. """
        return({'pos': self.pos,
                'vel': self.vel,
                'angle': self.angle,
                'radius': self.radius
                })
    def set_lifespan(self, t):
        """ Sets the new self.lifespan and resets age """
        self.lifespan = t
        self.age = 0

######################
# Gameplay functions #
def game_reset():
    """ Resets global variables (game over) """
    global running, score, lives, time, missiles, rocks, explosions, my_ship
    running = False		# Game running flag
    score = 0			# Initial score
    lives = LIVES		# Initial player "lives".
    time = 0.5			# Some Joe's magic for background animation
    
    missiles = set([])	# Collection of missile objects
    rocks = set([])		# Collection of rock objects
    explosions = set([])# Collection of explosion objects
    
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
    soundtrack.rewind()
    soundtrack.play()

def group_update(group, canvas):
    """ Update status and draw elements of given group """
    for i in group:
        i.update()
        i.draw(canvas)

def group_collide(group, obj):
    """ Any group element to collide with obj explodes """
    """ Number of explosions or False is returned """
    r = False
    for i in group:
        if i.collide(obj):
            explode(i)			# Draw explosion
            i.set_lifespan(0)	# Initiate object self destruction
            r += 1
    return r

def explode(obj):
    """ Draws explosion at position of given object """
    params = obj.get_params()
    explosions.add(Sprite([params['pos'][0], params['pos'][1]], [0, 0],
                     0, 0, explosion_image, explosion_info))
    explosion_sound.rewind()
    explosion_sound.play()
    
def group_group_collide(group, group2):
    """ Checks collisions between groups. Elements of group2 
    explode on collision and total number is returned. """
    r = set([])
    for i in group:
        if group_collide(group2, i):
            r.add(i)
    group.difference_update(r)
    return len(r)

def fire_missile():
    """ The missile fires with constant speed in the
    direction of the cannon + current ship velocity is
    added to this vector. This looks realistic. """
    lp = my_ship.get_params() # lp stands for "launch point"
    # Missile self speed increases with score to compensate rocks
    m_speed = MISSILE_THRUST 
    m_speed += MISSILE_THRUST * (score / MISSILE_SPEEDUP) if score > 0 else 0
    missiles.add(Sprite([lp['cannon'][0], lp['cannon'][1]],
                     [lp['vel'][0] + math.cos(lp['angle']) * m_speed,
                     lp['vel'][1] + math.sin(lp['angle']) * m_speed],
                    0, 0, missile_image, missile_info,
                    missile_sound) )

def rock_spawner():
    """ Spawns a new rock if required. """
    new_pos = [randrange(0, WIDTH), randrange(0, HEIGHT)]
    # If it happens that a new rock wants to spawn too close to the ship, 
    # we skip this attempt. I'm lazy to retry spawn. Will autoretry in 500ms.
    if dist(new_pos, my_ship.get_params()['pos']) < \
        MIN_DISTANCE + my_ship.get_params()['radius'] + asteroid_info.get_radius():
            rock_spawner()
            return
    # We increase the speed of new rocks as the score grows
    # Horizontal speed is increased faster than vertical
    new_vel = [random() * choice([-1, 1]) * (score / ROCK_SPEEDUP[0]),
               random() * choice([-1, 1]) * (score / ROCK_SPEEDUP[1])]
    
    # Spawn new rock if game running and not enough rocks
    if running and len(rocks) < ROCK_LIMIT:
        rocks.add(Sprite(new_pos, new_vel,
                        randrange(0, 6), # ~ 0-360 degrees
                        random() * choice([-1, 1]) / 20,
                        asteroid_image, asteroid_info))

# Call updates and draw elements
def draw(canvas):
    global time, lives, score, best

    # Animate background //by Joe and his guys
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # Draw score and lifes
    canvas.draw_text('Best Score: ' + str(best), [50, 30], 38, 'White')
    canvas.draw_text('Score: ' + str(score), [WIDTH - 170, 30], 38, 'Lime')
    canvas.draw_text('Lives: ' + str(lives), [WIDTH - 170, 70], 38, 'Lime')
    
    # Update ship and sprites
    my_ship.update()
    my_ship.draw(canvas)
    
    group_update(rocks, canvas)
    group_update(missiles, canvas)
    group_update(explosions, canvas)

    # Check collisions and update score/lives respectively
    if group_collide(rocks, my_ship):
        lives -= 1
    score += group_group_collide(rocks, missiles) * POINTS_FOR_ROCK
    best = score if score > best else best

    if lives <= 0:
        game_reset()
        
    # Draw splash image when not running game
    if not running:
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                          splash_info.get_size())

# Interface Event Handlers
def click(pos):
    global running
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not running) and inwidth and inheight:
        running = True

def key_down(k):
    if not running: return
    if k == simplegui.KEY_MAP['space']:
        fire_missile()
        return
    for i in inputs:
        if k == simplegui.KEY_MAP[i]:
            my_ship.update_vel(inputs[i])

def key_up(k):
    if not running: return
    for i in inputs:
        if k == simplegui.KEY_MAP[i]:
            my_ship.update_vel([inputs[i][0],0])

##########################
# Make the puppets dance #
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(500.0, rock_spawner)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(click)

game_reset()
timer.start()
frame.start()
