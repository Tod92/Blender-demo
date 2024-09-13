

class RigAxibo:
    """Testing purpose"""

    _timeout = 3

    def get_axies_from_api(self):
        """Returns a list of available axies from API"""
        match self.mock_mode:
            case 1:
                return [
                    {
                        "axis": "tilt",
                        "position": 6,
                        "minRange": -90,
                        "maxRange": 90,
                        "isBusy": 0
                    },
                    {
                        "axis": "pan",
                        "position": 30.35,
                        "minRange": -500,
                        "maxRange": 500,
                        "isBusy": 1
                    },
                    {
                        "axis": "slide",
                        "position": 200,
                        "minRange": -5,
                        "maxRange": 525,
                        "isBusy": 0
                    },
                    {
                        "axis": "focus",
                        "position": -42.5,
                        "minRange": 0,
                        "maxRange": 90,
                        "isBusy": 0
                    }
                ]
            case 2:
                return [
                    {"axis": "tilt", "position": 4, "isBusy": 0},
                    {"axis": "pan", "position": 42.35, "isBusy": 0},
                    {"axis": "slide", "position": 150, "isBusy": 0},
                ]
            case 3:
                return 'ConnectionError'
            case 4:
                raise ValueError('Request failed')
            case _:
                return None

    def move_axies_to(self, destinations):
        print('Je suis MockRig et j\'ai reçu l\'ordre de bouger vers ' + str(destinations))

    def move_axies_to_current(self, speed=5):
        """Asks API to move MyRig's axies to current position"""
        json_req = {}
        for axis in self.axies:
            json_req[axis.name] = [axis.position, speed]
        self.move_axies_to(json_req)

    def reboot(self):
        print('Je suis MockRig et j\'ai reçu l\'ordre de REBOOT')
