import pigpio

class Servo:
    def __init__(self, gpio, min_value=0, max_value=180, min_pulse=0.5, max_pulse=2.4, frequency=50,pigp:pigpio.pi=pigpio.pi()):
        if min_pulse < 0:
            raise ValueError("The value of the argument min_pulse is out of range.")
        if max_pulse < 0:
            raise ValueError("The value of the argument max_pulse is out of range.")
        if max_pulse * 1000 >= 1000000 / frequency:
            raise ValueError("The value of the argument frequency is too large.")
        self.__gpio = gpio
        self.__min_pulse = min_pulse
        self.__max_pulse = max_pulse
        self.__frequency = frequency
        self.__min_value = min_value
        self.__max_value = max_value
        self.__value = None
        self.start(pigp)
        try:
            self.__servo.hardware_PWM(self.__gpio, self.__frequency, 0)
        except Exception:
            raise ValueError("The value of the argument gpio is out of range.")
    
    def write(self, value):
        if self.__servo is None:
            raise Exception("The function start is not being executed.")
        if value < self.__min_value or value > self.__max_value:
            raise ValueError("The value of the argument value is out of range.")
        self.__value = value
        write_value = (value - self.__min_value) / (self.__max_value - self.__min_value) * (self.__max_pulse - self.__min_pulse) + self.__min_pulse
        self.__servo.hardware_PWM(self.__gpio, self.__frequency, int(write_value * self.__frequency * 1000))
    
    def read(self):
        return self.__value
    
    def stop(self):
        self.__value = None
        self.__servo.set_mode(self.__gpio, pigpio.INPUT)
        self.__servo.stop()
        self.__servo = None
    
    def start(self,pigp:pigpio.pi):
        self.__servo = pigp
        self.__servo.set_mode(self.__gpio, pigpio.OUTPUT)
