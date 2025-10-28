import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

CAR_RED = 17
CAR_YELLOW = 27
CAR_GREEN = 22
PED_RED = 25
PED_GREEN = 6
WHITE_LED = 0
BUTTON = 24

for pin in [CAR_RED, CAR_YELLOW, CAR_GREEN, PED_RED, PED_GREEN, WHITE_LED]:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

ped_request = False


def cars_red(): 
    GPIO.output(CAR_RED, 1)
    GPIO.output(CAR_YELLOW, 0)
    GPIO.output(CAR_GREEN, 0)

def cars_yellow(): 
    GPIO.output(CAR_RED, 0)
    GPIO.output(CAR_YELLOW, 1)
    GPIO.output(CAR_GREEN, 0)

def cars_green(): 
    GPIO.output(CAR_RED, 0)
    GPIO.output(CAR_YELLOW, 0)
    GPIO.output(CAR_GREEN, 1)

def cars_yellow_blink():
    """Vilguta kollast tuld 3 korda (kokku 2 sekundit), seejärel lülitu kohe punasele."""
    GPIO.output(CAR_GREEN, 0)
    GPIO.output(CAR_RED, 0)
    for _ in range(3):
        GPIO.output(CAR_YELLOW, 1)
        time.sleep(0.4)
        GPIO.output(CAR_YELLOW, 0)
        time.sleep(0.4)
    GPIO.output(CAR_RED, 1)
    GPIO.output(CAR_YELLOW, 0)
    GPIO.output(CAR_GREEN, 0)

def peds_red():
    GPIO.output(PED_RED, 1)
    GPIO.output(PED_GREEN, 0)

def peds_green():
    GPIO.output(PED_RED, 0)
    GPIO.output(PED_GREEN, 1)

try:
    print("Polling mode running. Väljumiseks vajuta Ctrl+C.")
    peds_red()

    while True:
        cars_red()
        print("Cars: RED | Pedestrians:", "GREEN" if ped_request else "RED")
        start = time.time()
        while time.time() - start < 5:
            if ped_request:
                peds_green()
            else:
                peds_red()

            if GPIO.input(BUTTON) == GPIO.LOW and not ped_request:
                ped_request = True
                GPIO.output(WHITE_LED, 1)
                print("Nupp on vajutatud — soov on salvestatud.")
            time.sleep(0.1)

        if ped_request:
            print("✅ Jalakäijate tsükkel on lõpetatud.")
        peds_red()
        ped_request = False
        GPIO.output(WHITE_LED, 0)

        cars_yellow()
        print("Cars: YELLOW")
        for _ in range(10):
            if GPIO.input(BUTTON) == GPIO.LOW and not ped_request:
                ped_request = True
                GPIO.output(WHITE_LED, 1)
                print("Nupp on vajutatud — soov on salvestatud.")
            time.sleep(0.1)

        cars_green()
        print("Cars: GREEN")
        for _ in range(50):
            if GPIO.input(BUTTON) == GPIO.LOW and not ped_request:
                ped_request = True
                GPIO.output(WHITE_LED, 1)
                print("Nupp on vajutatud — soov on salvestatud.")
            time.sleep(0.1)

        print("Cars: BLINKING YELLOW")
        cars_yellow_blink()  
        for _ in range(20):
            if GPIO.input(BUTTON) == GPIO.LOW and not ped_request:
                ped_request = True
                GPIO.output(WHITE_LED, 1)
                print("Nupp on vajutatud — soov on salvestatud.")
            time.sleep(0.1)

except KeyboardInterrupt:
    print("\nProgramm peatatud kasutaja poolt.")
finally:
    GPIO.cleanup()
