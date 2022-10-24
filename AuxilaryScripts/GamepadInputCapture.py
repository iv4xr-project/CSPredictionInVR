# inputs library from https://github.com/zeth/inputs. Follow installation guide in README.md
# script adapted from https://github.com/kevinhughes27/TensorKart/blob/master/utils.py

from inputs import get_gamepad
import math
import threading
import time
from datetime import datetime

start_time = time.time()
elapsed_seconds_old = 0

class XboxController(object):
	MAX_TRIG_VAL = math.pow(2, 8)
	MAX_JOY_VAL = math.pow(2, 15)
	
	def __init__(self):
		self.LeftJoystickY = 0
		self.LeftJoystickX = 0
		self.RightJoystickY = 0
		self.RightJoystickX = 0
		self.LeftTrigger = 0
		self.RightTrigger = 0
		self.LeftBumper = 0
		self.RightBumper = 0
		self.A = 0
		self.X = 0
		self.Y = 0
		self.B = 0
		self.LeftThumb = 0
		self.RightThumb = 0
		self.Back = 0
		self.Start = 0
		self.LeftDPad = 0
		self.RightDPad = 0
		self.UpDPad = 0
		self.DownDPad = 0
		
		self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
		self._monitor_thread.daemon = True
		self._monitor_thread.start()


	def read(self): # return the buttons/triggers that you care about in this method
		#Pitch & Yaw
		lj_x = self.LeftJoystickX
		lj_y = self.LeftJoystickY
		
		#Afterburner - Can be discarded
		lt = self.LeftTrigger
		
		#Thruster
		rt = self.RightTrigger
		
		#Confirm
		a = self.A
		
		#Cancel/Reverse
		b = self.B
		
		#Reset FWD - Can be discarded
		ddpad = self.DownDPad
		
		#Change View - Can be discarded
		x = self.X
		
		#Roll
		rj_x = self.RightJoystickX
		rj_y = self.RightJoystickY
		
		# ignore really tiny values so the neutral joystick always counts as zero even if it's small
		if(lj_x <= 0.1 and lj_x >= -0.1):
			lj_x = 0.0
		if(lj_y <= 0.1 and lj_y >= -0.1):
			lj_y = 0.0
			
		if(rj_x <= 0.1 and rj_x >= -0.1):
			rj_x = 0.0
		if(rj_y <= 0.1 and rj_y >= -0.1):
			rj_y = 0.0
		
		elapsed_seconds = round(time.time() - start_time,2)
		
		if(elapsed_seconds - elapsed_seconds_old >= 0.01):
			return str(elapsed_seconds) + "," + str(lj_x) + "," + str(lj_y) + "," + str(rt) + "," + str(a) + "," + str(b) + "," + str(rj_x) + "," + str(rj_y)
		else:
			return ""
	def _monitor_controller(self):
		while True:
			events = get_gamepad()
			for event in events:
				if event.code == 'ABS_Y':
					self.LeftJoystickY = round(event.state / XboxController.MAX_JOY_VAL,2) # normalize between -1 and 1
				elif event.code == 'ABS_X':
					self.LeftJoystickX = round(event.state / XboxController.MAX_JOY_VAL,2) # normalize between -1 and 1
				elif event.code == 'ABS_RY':
					self.RightJoystickY = round(event.state / XboxController.MAX_JOY_VAL,2) # normalize between -1 and 1
				elif event.code == 'ABS_RX':
					self.RightJoystickX = round(event.state / XboxController.MAX_JOY_VAL,2) # normalize between -1 and 1
				elif event.code == 'ABS_Z':
					self.LeftTrigger = round(event.state / XboxController.MAX_TRIG_VAL,2) # normalize between 0 and 1
				elif event.code == 'ABS_RZ':
					self.RightTrigger = round(event.state / XboxController.MAX_TRIG_VAL,2) # normalize between 0 and 1
				elif event.code == 'BTN_TL':
					self.LeftBumper = event.state
				elif event.code == 'BTN_TR':
					self.RightBumper = event.state
				elif event.code == 'BTN_SOUTH':
					self.A = event.state
				elif event.code == 'BTN_NORTH':
					self.Y = event.state
				elif event.code == 'BTN_WEST':
					self.X = event.state
				elif event.code == 'BTN_EAST':
					self.B = event.state
				elif event.code == 'BTN_THUMBL':
					self.LeftThumb = event.state
				elif event.code == 'BTN_THUMBR':
					self.RightThumb = event.state
				elif event.code == 'BTN_SELECT':
					self.Back = event.state
				elif event.code == 'BTN_START':
					self.Start = event.state	
				elif event.code == 'BTN_TRIGGER_HAPPY1':
					self.LeftDPad = event.state
				elif event.code == 'BTN_TRIGGER_HAPPY2':
					self.RightDPad = event.state
				elif event.code == 'BTN_TRIGGER_HAPPY3':
					self.UpDPad = event.state
				elif event.code == 'BTN_TRIGGER_HAPPY4':
					self.DownDPad = event.state




if __name__ == '__main__':
	joy = XboxController()
	
	# generate filename with datetime and modify it to satisfy file naming conventions
	filename = str(datetime.now())
	for i in range(len(filename)):
		if filename[i] == ':':
			filename = filename[:i] + '-' + filename[i+1:]
		elif filename[i] == '.':
			filename = filename[:i+3]
			break
			
	f = open(filename + ".txt","w")
	f.write(filename+"\n")
	f.write("ElapsedSeconds,LJ_X,LJ_Y,RT,A,B,RJ_X,RJ_Y\n")
	
	while True:
		#print(str(joy.read()))
		f.write(str(joy.read())+"\n")
		time.sleep(0.01)
		
	f.close()