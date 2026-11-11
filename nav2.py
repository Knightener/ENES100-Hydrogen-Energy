import math
import time
from enes100 import Enes100
from tank import Tank
import get_distance from ultrasonic_sensor

HALF_PI = math.pi / 2

DRIVING, CHECKING, FINISHING, FINISHED = 0, 1, 2, 3
state = DRIVING
checking_up = True

LEFT_ROT_PWM = 100
RIGHT_ROT_PWM = 100
LEFT_DRIVE_PWM = 255
RIGHT_DRIVE_PWM = 255
LEFT_SLOW_PWM = 100
RIGHT_SLOW_PWM = 100

CLOSE_DIST = 0.2
MIN_Y = 0.2
MAX_Y = 1.8
CHECK_DIST = 0.1
PRE_LOG_LINE = 3
FINISH_LINE = 3.7
THETA_TOLERANCE = 0.05


def drive_slow():
    Tank.set_left_motor_pwm(LEFT_SLOW_PWM)
    Tank.set_right_motor_pwm(RIGHT_SLOW_PWM)


def drive():
    Tank.set_left_motor_pwm(LEFT_DRIVE_PWM)
    Tank.set_right_motor_pwm(RIGHT_DRIVE_PWM)


def set_theta(theta, turn_ccw):
    curr = Enes100.get_theta()
    if abs(curr - theta) < THETA_TOLERANCE:
        return False

    if turn_ccw:
        Tank.set_left_motor_pwm(-LEFT_ROT_PWM)
        Tank.set_right_motor_pwm(RIGHT_ROT_PWM)
    else:
        Tank.set_left_motor_pwm(LEFT_ROT_PWM)
        Tank.set_right_motor_pwm(-RIGHT_ROT_PWM)

    while abs(curr - theta) >= THETA_TOLERANCE:
        curr = Enes100.get_theta()
        time.sleep_ms(1)
    Tank.turn_off_motors()
    return True


def d_squared(x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2


def move_dist(d_sq):
    drive_slow()
    x0 = Enes100.get_x()
    y0 = Enes100.get_y()
    while d_squared(x0, y0, Enes100.get_x(), Enes100.get_y()) < d_sq:
        time.sleep_ms(1)
    Tank.turn_off_motors()


def is_close_to_wall():
    d = Tank.read_distance_sensor(1)
    return 0 < d < CLOSE_DIST


def drive_logic():
    global state
    if set_theta(0, Enes100.get_theta() < 0):
        drive()
    if Enes100.get_x() > PRE_LOG_LINE:
        Tank.turn_off_motors()
        state = FINISHING
    elif is_close_to_wall():
        Tank.turn_off_motors()
        state = CHECKING
    else:
        time.sleep_ms(1)


def check_next():
    global checking_up
    y = Enes100.get_y()

    if y < MIN_Y:
        checking_up = True
    elif y > MAX_Y:
        checking_up = False

    if checking_up:
        set_theta(HALF_PI, True)
    else:
        set_theta(-HALF_PI, False)

    move_dist(CHECK_DIST * CHECK_DIST)

    if checking_up:
        set_theta(0, False)
    else:
        set_theta(0, True)


def check_logic():
    global state
    check_next()
    y = Enes100.get_y()

    if (not is_close_to_wall()
            and MIN_Y + CHECK_DIST <= y <= MAX_Y - CHECK_DIST):
        check_next()
        state = DRIVING
        drive()


def finish_logic():
    global state
    set_theta(-HALF_PI, False)
    drive()
    while not is_close_to_wall():
        time.sleep_ms(1)
    Tank.turn_off_motors()
    set_theta(0, True)
    drive()
    while Enes100.get_x() < FINISH_LINE:
        time.sleep_ms(1)
    Tank.turn_off_motors()
    state = FINISHED


def setup():
    Enes100.begin("Simulator", Enes100.HYDROGEN, 3, 1116, 8, 9)
    Tank.begin()
    set_theta(0, True)
    drive()


def main():
    setup()
    while True:
        if state == DRIVING:
            drive_logic()
        elif state == CHECKING:
            check_logic()
        elif state == FINISHING:
            finish_logic()
        else:
            time.sleep(1)


main()