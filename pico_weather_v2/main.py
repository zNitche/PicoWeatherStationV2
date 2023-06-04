import machine


def main():
    i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
    led = machine.Pin("LED", machine.Pin.OUT)

    print(f"devices: {i2c.scan()}")

    led.on()


if __name__ == '__main__':
    main()
