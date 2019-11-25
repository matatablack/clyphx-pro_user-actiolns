""" The number of X-Controls to add shift functionality to. """
NUM_X_CONTROLS = 100


class TemplateBase:

    def __init__(self, trigger):
        self.trigger = trigger

    def handler(self, val):
        self.trigger("wait 15; MSG \"HOLA %s\";" % val)