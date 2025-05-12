import pygame
from piservo import Servo
from cprint import cprint

# Initialize pygame and the joystick module
pygame.init()
pygame.joystick.init()

# Initialize the servo
myservo = Servo(18, frequency=333)
myservo.write(90)  # Set servo to the middle position

def map_range(unscaled, from_min=-1.000030518509476, from_max=1, to_min=0, to_max=180):
    """Map a value from one range to another."""
    return (to_max - to_min) * (unscaled - from_min) / (from_max - from_min) + to_min

def main():
    """Main function to handle joystick events and control the servo."""
    if pygame.joystick.get_count() == 0:
        print("No gamepad connected.")
        return

    # Get the first joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Gamepad connected: {joystick.get_name()}")

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION and event.axis == 0:
                    pos = map_range(float(event.value))
                    cprint.info(f"{pos:.2f} / {event.value:.2f}")
                    myservo.write(pos)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        # Quit pygame
        pygame.quit()

if __name__ == "__main__":
    main()