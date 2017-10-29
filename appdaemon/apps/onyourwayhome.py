import appdaemon.appapi as appapi

#
# Hello World App
#
# Args:
#

class OnYourWayHome(appapi.AppDaemon):

    def initialize(self):
        (self.distance, self.unit) = self.get_state(self.args["entity_id"], attribute="distance").split(" ")
        self.log(self.distance)
        if self.unit == 'km':
            self.distance = float(self.distance) * 1000

        self.log(self.distance)

        self.counter = 0

        self.listen_state(self.checkValue, self.args["entity_id"])

    def checkValue(self, entity, attribute, old, new, kwargs):
        if (float(new) >= float(old) + float(self.args["treshold"]) and float(new) > 10):
            self.log(new)
            self.counter = self.counter + 1

            if self.counter == self.args["moves"]:
                self.counter = 0
                self.log("Script called")
                self.turn_on(self.args["turn_on"], **kwargs)

