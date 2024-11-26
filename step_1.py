import dht
from machine import Pin
import time

# Set up the DHT11 sensor on GPIO16
dht_pin = Pin(16)
dht_sensor = dht.DHT11(dht_pin)

# Main loop 
while True:
    try:
        # Trigger the sensor to measure
        dht_sensor.measure()
        # Get the temperature in Celsius
        temperature = dht_sensor.temperature() 
        # Get the humidity in percentage
        humidity = dht_sensor.humidity()

        print('Temperature: {}°C  Humidity: {}%'.format(temperature, humidity))
        
    except OSError as e:
        print('Failed to read sensor.')

    time.sleep(5)

