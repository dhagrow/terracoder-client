from .format import format

def world_state(data):
    return format(data)

def drone_get(data):
    return format(data)

def drone_state(data):
    return '\n'.join(format(drone) for drone in data)
