# htu21d-esp8266
This is a micropython module / class to measure data from the htu21d

# Example (D1 Mini)

This code works on a D1 Mini, SCL on pin labeled D1, SDA on pin labeled D2.

```
scl = machine.Pin(5, machine.Pin.OPEN_DRAIN, machine.Pin.PULL_UP)
sda = machine.Pin(4, machine.Pin.OPEN_DRAIN, machine.Pin.PULL_UP)
htu = htu21d.HTU21D(scl, sda)
while True:
    print('temp %f humid %f' % (htu.temperature, htu.humidity))
    time.sleep(2)
```
