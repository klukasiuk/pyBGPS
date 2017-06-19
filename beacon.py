import utm


class Beacon:
    def __init__(self, major, minor, lat, lon, weights_sum, points, last_seen_by=0):
        self.major = major
        self.minor = minor
        self.lat = lat
        self.lon = lon
        self.weights_sum = weights_sum
        self.points = points
        self.last_seen_by = last_seen_by

        temp = utm.from_latlon(self.lat, self.lon)
        self.easting = temp[0]
        self.northing = temp[1]

    @staticmethod
    def from_str(text):
        data = text.split()

        print(data)

        major = int(data[0])
        minor = int(data[1])
        lat = float(data[2])
        lon = float(data[3])
        weights_sum = float(data[4])
        points = int(data[5])

        if len(text) == 6:
            return Beacon(major, minor, lat, lon, weights_sum, points)
        if len(text) == 7:
            last_seen_by = text[6]
            return Beacon(major, minor, lat, lon, weights_sum, points, last_seen_by=last_seen_by)

    def __str__(self):
        text = []
        text.append(str(self.major))
        text.append(str(self.minor))
        text.append(str(self.lat))
        text.append(str(self.lon))
        text.append(str(self.weights_sum))
        text.append(str(self.points))

        if self.last_seen_by != 0:
            text.append(self.last_seen_by)

        return '\t'.join(text)
