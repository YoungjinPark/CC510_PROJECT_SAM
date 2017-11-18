import pygame
import movingObjects
import random
import numpy as np

dt = 1/60
WHITE = (255,255,255)
pad_width = 1500
pad_height = 700

ix = 100
iy = 100
ivx = 0
ivy = 0

def drawVehicle(canvas, vehicle, pos, ang):
	rVeh=pygame.transform.rotate(vehicle, ang) # rotate
	size=rVeh.get_size() # size 
	hSize=[n/2 for n in size] # half size
	newPos =(pos[0]-hSize[0],pos[1]-hSize[1])  # adjust
	canvas.blit(rVeh,newPos) # draw

def runSimulation(values):
	# This funciton runs simulation of SAM system.

	# Initialize the Pygame Window
	pygame.init()
	canvas =pygame.display.set_mode((pad_width,pad_height))
	pygame.display.set_caption('SAM System')
	clock = pygame.time.Clock()

	# Load Vehicle Images
	aircraft_img = pygame.image.load('aircraft.png')
	vehicle_img = pygame.image.load('vehicle.png')
	missile_img = pygame.image.load('missile.png')
	bang_img = pygame.image.load('bang.png')

	# Load Background Images
	background = pygame.image.load('background.png')

	# Initialize Vehicles
	samVehicle = movingObjects.Vehicle(ix, iy, ivx, ivy, dt)
	enemyAircrafts = [movingObjects.Aircraft(1000,600,-100*np.cos(values[1]*np.pi/180),100*np.sin(values[1]*np.pi/180),dt)]

	# Run Simulation
	crashed=False
	d = 5
	vehicle_acc = 0 # init acc
	missileLaunched = False

	while not crashed: # unitl the program crashes
		canvas.fill(WHITE) # Fill Background

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				crashed=True

			# If there is keyboard input, determine acceleration input to missile vehicle
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					vehicle_acc = -10
				elif event.key == pygame.K_RIGHT:
					vehicle_acc = 10

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					missileLaunched = True
					samMissile = movingObjects.Missile(samVehicle.x, samVehicle.y, 0, values[0], dt)

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					vehicle_acc = 0

		# Give acceleration and move missile vehicle.
		samVehicle.update_pos(vehicle_acc)

		# Move aircraft
		enemyAircraft.update_pos()

		# Move missile
		if missileLaunched:
			samMissile.update_pos(enemyAircraft)

		# Draw
		drawVehicle(canvas, vehicle_img, (samVehicle.x, pad_height - samVehicle.y), samVehicle.dir)

		if missileLaunched and samMissile.shoot_flag == 0:
			drawVehicle(canvas, missile_img, (samMissile.x, pad_height - samMissile.y), samMissile.dir)

		if missileLaunched and samMissile.distance < 1000:
			samMissile.shoot_flag=1
			enemyAircraft.shoot_flag=1
			drawVehicle(canvas, bang_img, (samMissile.x, pad_height - samMissile.y),0)
		else:
			drawVehicle(canvas, aircraft_img, (enemyAircraft.x, pad_height - enemyAircraft.y), enemyAircraft.dir)

		# Display
		pygame.display.update()
		clock.tick(60)

	pygame.quit()