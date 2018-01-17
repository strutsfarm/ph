#!/usr/bin/python

import time       # used for sleep delay and timestamps
import sys
import sqlite3
import Atlas      # Atlas Scientific device

PH_SENSOR_ADDR = 99
PH_MINUS_PUMP_ADDR = 103
PH_PLUS_PUMP_ADDR = 104
DAMPING = 50 # iterations where we only control in one direction
MEASUREMENT_LOOP_TIME = 10.0 # of seconds between measurements  
		
def main():

	device = Atlas.AtlasI2C() 	# creates the I2C port object, specify the address or bus if necessary
	conn = sqlite3.connect('atlas.db')

	c = conn.cursor()


	ph_set_value = 6.0
	ph_minus_dose = 0
	ph_plus_dose = 0
	ec_set_value = 0.0
	ec_current = 0
	ec_dose = 0
	controlling_down = 0
	controlling_up = 0
	ph_hysteresis = 0.1

	# main loop
	while True:
		start_loop_time = time.time()
		device.set_i2c_address(PH_SENSOR_ADDR)
		response = device.query("R") # Get a reading from the sensor
		# response is now a string of the pH value  if everything is ok
		try:
			ph_current = float(response)
		except:
			sys.exit()
		print("pH= ", ph_current)

		# Controlling DOWN
		if ph_current > ph_set_value + ph_hysteresis & controlling_up == 0 :
			# inject pH-minus by running the pump
			ph_minus_dose = 1
			device.set_i2c_address(PH_MINUS_PUMP_ADDR)
			device.write("D," + str(ph_minus_dose))
			time.sleep(0.5)
			response = device.read()
			controlling_down = DAMPING
			#print(response)
			#if response != "Command succeeded ":
				#print(response)
				#print("Error")

		#Controlling UP
		if ph_current < ph_set_value - ph_hysteresis & controlling_down == 0 :
			# inject pH-plus by running the pump
			ph_plus_dose = 1
			device.set_i2c_address(PH_PLUS_PUMP_ADDR)
			device.write("D," + str(ph_plus_dose))
			time.sleep(0.5)
			response = device.read()
			controlling_up = DAMPING
			#print(response)
			#if response != "Command succeeded ":
				#print(response)
				#print("Error")
		
		if controlling_down > 0: controlling_down -=1
		if controlling_up > 0: controlling_up -=1

		current_time = time.time()

		# Write data to database....
		# time TEXT, 
		# measured_pH real, target_pH real, PMP_pH_minus real, PMP_pH_plus real, 
		# measured_Ec real, target_Ec real, PMP_nutrition real)
		c.execute('INSERT INTO pH_data VALUES (datetime("now"), ?, ?, ?, ?)', (ph_current, ph_set_value, ph_minus_dose, ph_plus_dose))
		c.execute('INSERT INTO Ec_data VALUES (datetime("now"), ?, ?, ?)', 
			(ec_current, ec_set_value, ec_dose))
		c.execute('UPDATE temp SET createdAt = datetime("now") ,measured_pH = ?,target_pH = ?,PMP_pH_minus = ?,PMP_pH_plus = ?,measured_Ec = ?,target_Ec = ?,PMP_nutrition = ? WHERE rowid = 1', 
			(ph_current, ph_set_value, ph_minus_dose, ph_plus_dose, ec_current, ec_set_value, ec_dose))
		conn.commit()
		loop_time = current_time - start_loop_time
		# wait until we have MEASUREMENT_LOOP_TIME of seconds 
		if loop_time < MEASUREMENT_LOOP_TIME:
			time.sleep(MEASUREMENT_LOOP_TIME - loop_time)


	conn.close()

if __name__ == '__main__':
	main()

