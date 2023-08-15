import pygame,sys,time
from random import randint, uniform
#pygame.org <- documentation
def laser_update(laser_List, speed = 300):
   for lasers in laser_List:
      if lasers.bottom < 0:
         laser_List.remove(lasers)
      lasers.y -= round(speed * DeltaTime)
def display_Score():
   score_text = f'Score: {pygame.time.get_ticks() // 1000}'
   text_Surface = font.render(score_text, True , 'cyan')
   text_Rect = text_Surface.get_rect(midbottom = (window_Width/2 , window_Height - 80))
   display_Surface.blit(text_Surface,text_Rect)
def laser_Timer(can_shoot, duration = 100):
   if not can_shoot:
      current_time = pygame.time.get_ticks()
      if current_time - shoot_time > duration:
         can_shoot = True
   return can_shoot
def asteroid_Update(asteroid_List, speed = 200):
   for asteroids_tuple in asteroid_List:
      direction = asteroids_tuple[1]
      asteroids = asteroids_tuple[0]
      if asteroids.top > window_Height:
         asteroid_List.remove(asteroids_tuple)
      asteroids.center += direction * speed * DeltaTime
      #asteroids.y += round(speed * DeltaTime)
pygame.init()
window_Width = 1280
window_Height = 720
display_Surface = pygame.display.set_mode((window_Width,window_Height))
pygame.display.set_caption("Asteroid Shooter without Classes")
clock = pygame.time.Clock()
#import graphics
# convert_alpha for transparency and convert for not transparent
#ship
ship_Surface = pygame.image.load('graphics/ship.png').convert_alpha()
ship_Rect = ship_Surface.get_rect(center = (window_Width/2 , window_Height/2))
back_Surface = pygame.image.load('graphics/background.png').convert()
#laser
laser = pygame.image.load('graphics/laser.png').convert_alpha()
laser_List = []
laser_Rect = laser.get_rect(midbottom = ship_Rect.midtop)
#laser timer
can_shoot = True
shoot_time = None
#import text
font = pygame.font.Font('graphics/subatomic.ttf',50)
text_Surface = font.render('Score : ' , True , 'cyan')
text_Rect = text_Surface.get_rect(midbottom = (window_Width/2 , window_Height - 80))
#asteroids
asteroid = pygame.image.load('graphics/meteor.png').convert_alpha()
asteroid_List = []
asteroid_Rect = asteroid.get_rect(center = (640, -100) )
asteroid_Timer = pygame.event.custom_type()
pygame.time.set_timer(asteroid_Timer, 1000) 
#sound
laser_sound = pygame.mixer.Sound("sounds/laser.ogg")
laser_sound.set_volume(0.2)
explode_sound = pygame.mixer.Sound("sounds/explosion.wav")
explode_sound.set_volume(0.2)
bg_music = pygame.mixer.Sound("sounds/music.wav")
bg_music.set_volume(0.1)
bg_music.play(loops= -1)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if pygame.mouse.get_pressed()[0] and can_shoot:
           #create laser
           laser_Rect = laser.get_rect(midbottom = ship_Rect.midtop)
           laser_List.append(laser_Rect)
           #time between shooting
           can_shoot = False
           shoot_time = pygame.time.get_ticks()
           #play sound
           laser_sound.play()
        if event.type == asteroid_Timer:
           #random position generation
           asteroid_X = randint(0,window_Width)
           asteroid_Y = randint(-100,-50)
           #create rectangle
           asteroid_Rect = asteroid.get_rect(center = (asteroid_X, asteroid_Y))
           #direction makes asteroid go in random direction
           direction = pygame.math.Vector2(uniform(-0.5 , 0.5),1)
           asteroid_List.append((asteroid_Rect,direction))
    DeltaTime = clock.tick(120) / 1000	
# ORDER MATTERS FOR DRAWING ON THE DISPLAY SURFACE
    #ship follows your mouse
    ship_Rect.center = pygame.mouse.get_pos()
    display_Surface.blit(back_Surface,(0,0))
    laser_update(laser_List)
    asteroid_Update(asteroid_List)
    can_shoot = laser_Timer(can_shoot, 500)
    #collisions (meteor-ship)
    for a_tuple in asteroid_List:
       asteroid_Rect = a_tuple[0]
       if ship_Rect.colliderect(asteroid_Rect):
          pygame.quit()
          sys.exit()
   #collisions(laser-meteor)
    for lasers in laser_List:
     for a_tuple in asteroid_List:
       if lasers.colliderect(a_tuple[0]):
          asteroid_List.remove(a_tuple)
          laser_List.remove(lasers)
          explode_sound.play()
    display_Score()
    for laser_Rect in laser_List:
       display_Surface.blit(laser,laser_Rect)
    for asteroids_tuple in asteroid_List:
       display_Surface.blit(asteroid, asteroids_tuple[0])
    display_Surface.blit(ship_Surface,ship_Rect)
    pygame.display.update()