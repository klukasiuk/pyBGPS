import settings
from settings import beacon_list, n


def beacon_averager(command):
    # get sending vehicle id
    last_seen_by = command[0]
    command.pop(0)

    # calculate square number
    square_no = int(command[0]) - 1

    # reduce command length so that is divisible by 3
    command.pop(0)

    # calculate current square's coordinates
    lat = settings.squares_matrix[square_no].lat
    lon = settings.squares_matrix[square_no].lon

    # calculate maximum discoverable distance
    d_100 = 10**((-65 + 100) / 10 / n)

    # iterate thru averaged beacons
    i = 0
    while i < len(command):

        # parse the command - single beacon data
        major = int(command[i])
        minor = int(command[i + 1])
        rssi = float(command[i + 2])

        # calculate pseudodistance and weight
        d_rssi = 10**((-65 - rssi) / 10 / n)
        weight = -1 / (d_100 - 1) * (d_rssi - d_100)

        # find the appriopriate beacon and update data
        for bcn in beacon_list:
            if bcn.major == major and bcn.minor == minor:
                # lat update
                bcn.lat = bcn.lat * bcn.weights_sum + lat * weight
                bcn.lat /= bcn.weights_sum + weight
                # print 'lat for beacon index %d: %f' % (i, bcn.lat)

                # lon update
                bcn.lon = bcn.lon * bcn.weights_sum + lon * weight
                bcn.lon /= bcn.weights_sum + weight
                # print 'lon for beacon index %d: %f' % (i, bcn.lon)

                # weight update
                bcn.weights_sum += weight

                # last seen update
                if bcn.last_seen_by == 0:
                    bcn.last_seen_by = last_seen_by

        i += 3
