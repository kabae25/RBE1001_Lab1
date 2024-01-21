# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Evan                                                         #
# 	Created:      1/21/2024, 3:21:47 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Robot Map:
# Arm Motor is Port 12
# Ultrasonic Sensor is three wire port a
# Drivetrain



# Library imports
from vex import *

brain=Brain()
print('test')
brain.screen.print("Hello V5") # Debug test print

sonar = Sonar(brain.three_wire_port.a)

rightMotor = Motor(Ports.PORT15, False)
leftMotor = Motor(Ports.PORT11, True)
armMotor = Motor(Ports.PORT20, True)

class State():
    START = 0
    MOVE = 1
    RAISE = 2
    END = 3

class Finite_State_Machine():
    def __init__(self) -> None:
        self.current_state = State.START
        self.end_states = [State.END]
        self.task()

    def task(self):
        while self.current_state not in self.end_states:
            #print("Currently In:", self.current_state, " State")
            self.on_event()

    def on_event(self): # Statemachine on_event loop
        if self.current_state == State.START:
            return self.__START_handler()
        elif self.current_state == State.MOVE:
            return self.__MOVE_handler()
        elif self.current_state == State.RAISE:
            return self.__RAISE_handler()
        elif self.current_state == State.END:
            return self.__END_handler()

    def __START_handler(self):
        print("Program Start")
        i = 0
        while i < 5:
            self.getDistance()
            i+=1

        armMotor.set_position(0, TURNS)
        self.current_state = State.MOVE

    def __MOVE_handler(self):
        # if ultrasonic reading is greater than some value, move
        if self.getDistance() >= 4.0:
            rightMotor.spin(DirectionType.FORWARD, 30 * (60.0/12.0), RPM)
            leftMotor.spin(DirectionType.FORWARD, 30 * (60.0/120.0), RPM)
        else:
            rightMotor.stop()
            leftMotor.stop()
            
            self.current_state = State.RAISE
            

    def __RAISE_handler(self):
        # raise arm up to a height to pick up bucket
        print('Ultrasonic Distance: ', sonar.distance(DistanceUnits.IN))
        armMotor.spin_for(DirectionType.REVERSE, 75 * (60.0/12.0), DEGREES, True)
        armMotor.stop(BRAKE)
        self.current_state = State.END

    def __END_handler(self):
        # stop doing everything
        print('done')

    def getDistance(self):
        return sonar.distance(DistanceUnits.IN)

finite_state_machine = Finite_State_Machine() # Starts the state machine
