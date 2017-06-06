from FPS_Class import FPS_Class
fps=FPS_Class('home/pi/Desktop/ShopGUI')


from GPIO_Class import GPIO_Class
gpio=GPIO_Class()
gpio.LED_ON("blue")
import time
time.sleep(2)
gpio.LED_ON("red")
time.sleep(2)
gpio.LED_ON("yellow")
time.sleep(2)
gpio.LED_ON("green")

while (1):
	result = 0
	for i in range (1,200):
		result += gpio.ReadButton()
		time.sleep(.01)
	print result
fps.FPS_RemoveAll()