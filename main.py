from math import atan, degrees

def point2angle(point):
    # this will convert a point (x, y) into an angle from y axis
    angle = None
    px = point[0]
    py = point[1]

    angle = abs(degrees(atan(px/py)))

    if py < 0 and px < 0: # bottom left
        angle += 180
    elif py < 0: # bottom right
        angle = 180 - angle
    elif px < 0: # top left
        angle = 360 - angle
    # else: # top right -> nothing to change

    return angle
