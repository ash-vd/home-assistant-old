import appdaemon.appapi as appapi

#
# OnYourWayHome
#
# On every change from a sensor, checks if the value is lower then the previous change. If true, it adds one to the
# counter. When it reaches the defined number it calls a script.
#

class OnYourWayHome(appapi.AppDaemon):

    def initialize(self):
        self.counter = 0

        (self.distance, self.unit) = self.get_state(self.args["entity_id"], attribute="distance").split(" ")
        if self.unit == 'km':
            self.distance = float(self.distance) * 1000

        self.listen_state(self.checkValue, self.args["entity_id"])

    def checkValue(self, entity, attribute, old, new, kwargs):
        self.log('---')
        self.log(entity)
        self.log(old)
        self.log(new)

        (self.newDistance, self.newUnit) = self.get_state(self.args["entity_id"], attribute="distance").split(" ")
        if self.newUnit == 'km':
            self.newDistance = float(self.distance) * 1000

            self.log(self.newDistance)
            self.log(self.distance)

        if (float(self.distance) >= (float(self.newDistance) + float(self.args["treshold"])) and float(self.newDistance) > 1000):

            self.distance = self.newDistance
            self.counter = self.counter + 1

            self.log(self.counter)

            if float(self.counter) == float(self.args["moves"]):
                self.counter = 0
                self.log("Script called")
                self.turn_on(self.args["turn_on"])

        self.log('---')
