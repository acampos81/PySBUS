import time
from src import *

sbus = SBUS(tty='/dev/ttyUSB0', baud=98000)
sbus.begin()

channels = [0] * SBUSConsts.NUM_CHANNELS
ch_max = 1811
ch_min = 172
ch_range = ch_max - ch_min
current_heading = 0
current_speed = 0
reverse = False
max_yaw_rate = 180
last_millis = 0
last_aux_value = 0


def normalize(ch_value):
    ch_diff = ch_max - ch_value
    return round(1 - (ch_diff / ch_range),2)


def centralize(norm_value):
    return 2*norm_value - 1


def lerp(v0, v1, t):
    return (1 - t) * v0 + t * v1


def get_delta_time():
    global last_millis

    current_millis = time.time()

    if last_millis == 0:
        last_millis = current_millis

    delta = current_millis - last_millis
    last_millis = current_millis
    return delta


def wrap_heading(heading):
    if heading > 0:
        heading%360

def check_aux_toggle(aux_value):
    global last_aux_value
    toggled = aux_value > 0 and aux_value != last_aux_value
    last_aux_value = aux_value
    return toggled

while True:
    payload_ready, failsafe, lost_frame = sbus.read(channels)

    if payload_ready:
        norm_thr = normalize(channels[2])
        norm_yaw = normalize(channels[0])
        norm_aux = normalize(channels[4])
        cent_yaw = centralize(norm_yaw)
        yaw_rate = max_yaw_rate * cent_yaw
        current_heading += yaw_rate * get_delta_time()
        current_heading = round(current_heading % 360)
        current_speed = round(255 * norm_thr)
        reverse_toggled = check_aux_toggle(norm_aux)
        if reverse_toggled:
            print("reverse toggled")

