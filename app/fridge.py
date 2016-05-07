class Fridge:

    def __init__(self, name):
        self.name = name.decode('utf-8')
        self.sensors = list()

    def add_sensor(self, sensor):
        self.sensors.append(sensor)


class Sensor:

    def __init__(self, name, sensorid):
        self.name = name.decode('utf-8')
        self.id = sensorid