# Stepper Motor controller
# 516.096 steps/revolution

from time import sleep
from machine import Pin

# Half step sequence
Seq = [[1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1],
       [1,0,0,1]]


class Stepper:
    def __init__(self, pins=[2,3,4,5]):
        self.pins = pins
        self.step_pins = []
        
        for x in range(0,4):
            self.step_pins.append(Pin(self.pins[x], Pin.OUT))
            self.step_pins[x].value(1)
        
    def de_energise(self):
        for pin in range(0,4):
            self.step_pins[pin].value(0)

    def stepMotor(self, direction = 'clockwise', number_of_steps = 1):

        step_direction = 1
        step_count = 0
        
        # Set direction
        if direction == 'clockwise':
            step_count = 0
            step_direction = 1
        elif direction == 'anticlockwise':
            step_count = 7
            step_direction = -1

        WaitTime = 0.005

        for nstep in range (0, number_of_steps):
            for step in range (0, 8):
                for pin in range(0, 4):
                    self.step_pins[pin].value(Seq[step_count][pin])
                sleep(WaitTime)
                step_count += step_direction
            if direction == 'clockwise':
                step_count = 0
            elif direction == 'anticlockwise':
                step_count = 7

        self.de_energise()
