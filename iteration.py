import math

# major, minor, lat, lon, dist
data = []
beacons = []
"""
data.append([2,1,200, 200, 20])
data.append([2,1,230, 200, 10])
data.append([2,1,200, 230, 40])

data.append([2,2,200, 200, 10])
data.append([2,2,230, 200, 30])
data.append([2,2,200, 230, 20])

data.append([1,1,200, 200, 20])
data.append([1,1,230, 200, 10])
data.append([1,1,205, 230, 40])
data.append([1,1,240, 230, 60])
"""

def trilateration(N1, N2, N3):
    S = (N3[0]**2 - N2[0]**2 + N3[1]**2 - N2[1]**2 + N2[2]**2 - N3[2]**2) / 2.0
    T = (N1[0]**2 - N2[0]**2 + N1[1]**2 - N2[1]**2 + N2[2]**2 - N1[2]**2) / 2.0
    yy = ((T * (N2[0] - N3[0])) - (S * (N2[0] - N1[0]))) / (((N1[1] - N2[1]) * (N2[0] - N3[0])) - ((N3[1] - N2[1]) * (N2[0] - N1[0])))
    xx = ((yy * (N1[1] - N2[1])) - T) / (N2[0] - N1[0])
    return [xx, yy]


class BeaconData:
    def __init__(self, major, minor):
        self.measurement = []
        self.major = major
        self.minor = minor
        self.position = [0,0]

    def read_measurement(self, lat, lon, dist):
        self.measurement.append([lat, lon, dist])

    def calculate_position(self):
        n = len(self.measurement)
        estimated_positions = []
        if n > 2:
            for k1 in range(0,n-2) :
                n1 = self.measurement[k1]
                for k2 in range(k1+1, n-1):
                    n2 = self.measurement[k2]
                    for k3 in range(k2 + 1, n):
                        n3 = self.measurement[k3]
                        estimated_positions.append(trilateration(n1,n2,n3))
            sum_positionx = 0
            sum_positiony = 0
            for i in estimated_positions:
                sum_positionx += i[0]
                sum_positiony += i[1]
            return [sum_positionx / float(len(estimated_positions)), sum_positiony / float(len(estimated_positions))]
        return False


def check_if_created(major, minor):
    for i in beacons:
        if major == i.major and minor == i.minor:
            return i
    return 0


def store_kalman_data(raw_data):  # starts when server gets new mesurements from a copter
    print(raw_data)
    lat = raw_data.pop(0)
    lon = raw_data.pop(0)
    latLonDist = []
    while len(raw_data) > 2:
        latLonDist.append([raw_data.pop(0), raw_data.pop(0), raw_data.pop(0)])
    print(latLonDist)
    for i in latLonDist:
        bcn = check_if_created(i[0], i[1])
        if bcn == 0:
            beacons.append(BeaconData(i[0], i[1]))
            beacons[-1].read_measurement(lat, lon, i[2])
        else:
            bcn.read_measurement(lat, lon, i[2])


#print(beacons[0].calculate_position())
