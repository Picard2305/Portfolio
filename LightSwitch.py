class LightSwitch():
    def __init__(self):
        self.switchIsOn = False

    def turnOn(self):
        #turn the switch on
        self.switchIsOn = True

    def turnOff(self):
        #turn the switch off
        self.switchIsOn = False

    def show(self): #added for testing
        print(self.switchIsOn)

oLightSwitch1 = LightSwitch()
oLightSwitch2 = LightSwitch()


oLightSwitch1.show()
oLightSwitch2.show()
oLightSwitch1.turnOn()
oLightSwitch2.turnOff()
oLightSwitch1.show()
oLightSwitch2.show()