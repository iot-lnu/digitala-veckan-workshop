import network
import urequests
import dht
from machine import Pin
import time

# Wi-Fi credentials
ssid = 'TP-Link_1BDE'
password = '63365483'

# Set up the LED on GPIO15 as an output pin
led_pin = Pin(15, Pin.OUT)

# Set up the DHT11 sensor on GPIO16
dht_pin = Pin(16)
dht_sensor = dht.DHT11(dht_pin)

# Function to connect to Wi-Fi
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print("Connecting to Wi-Fi...")
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        print("Waiting for connection...")
        time.sleep(1)

    if wlan.isconnected():
        print("Connected to Wi-Fi!")
        print("Network config:", wlan.ifconfig())
        # Turn on the LED to indicate successful Wi-Fi connection
        led_pin.value(1)
    else:
        print("Failed to connect.")
        # Blink the LED on failure
        for _ in range(5):
            led_pin.value(not led_pin.value())
            time.sleep(0.5)
        led_pin.value(0)

# Function to send data to the HTTP endpoint
def send_data(temperature, humidity, led_state):
    url = 'https://api.datacake.co/integrations/api/d7845d47-d94e-40bf-b117-f0183681b62a/'
    headers = {'Content-Type': 'application/json'}
    data = {
        "device": "d2d0918c-971c-4085-98e2-a1686cfc374c",
        "temperature": temperature,
        "humidity": humidity,
        "led_state": led_state
    }

    try:
        response = urequests.post(url, headers=headers, json=data)
        print('Data posted:', response.text)
        response.close()
    except Exception as e:
        print('Failed to send data:', e)

# Connect to the Wi-Fi
connect_to_wifi()

# Main loop to read from DHT11 and control the LED
while True:
    try:
        dht_sensor.measure()  # Trigger the sensor to measure
        temperature = dht_sensor.temperature()  # Get the temperature in Celsius
        humidity = dht_sensor.humidity()  # Get the humidity in percentage
        led_state = 0

        # Toggle LED based on temperature threshold
        if temperature > 24:
            led_pin.value(1)
            led_state = 1
        else:
            led_pin.value(0)
            led_state = 0

        print('Temperature: {}°C  Humidity: {}%'.format(temperature, humidity))
        
        # Send data to the endpoint
        send_data(temperature, humidity, led_state)

    except OSError as e:
        print('Failed to read sensor.')

    time.sleep(20)  # Wait for 2 seconds before the next reading


