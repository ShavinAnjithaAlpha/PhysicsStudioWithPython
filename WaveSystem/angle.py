import math

def return_angle(sin, cos):
    if sin >= 0 and cos >= 0:
        print("one")
        return math.degrees(math.acos(cos))
    elif sin >= 0 and cos < 0:
        print("second")
        return math.degrees(math.acos(cos))

    elif sin < 0 and cos < 0:
        print("third")
        return 180 + math.degrees(math.acos(abs(cos)))

    else:
        print("fourth")
        return 360+(math.degrees(math.asin(sin)))


print(return_angle(-0.85, -0.5))