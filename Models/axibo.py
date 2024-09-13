import requests
import json


class RigAxibo:
    """
    Rail permettant le mouvement de la camera physique
    Interogé via son API sur le reseau
    """
    API_REQUESTS = {
        'status': ['GET', 'http://', ':2200/v1/system/status'],
        'reboot': ['POST', 'http://', ':2200/v1/system/reboot'],
        'move_to': ['PUT', 'http://', ':2200/v1/direct-control/move-absolute']
    }
    _timeout = 3

    def contact_api(self, query, data=None):
        """Core API requests method"""
        method, url = query[0], query[1] + self.ip_address + query[2]
        if method == 'GET':
            response = requests.get(url, timeout=self._timeout)
        elif method == 'POST':
            response = requests.post(url, timeout=self._timeout)
        elif method == 'PUT':
            response = requests.put(url, json=data, timeout=self._timeout)
        if response.status_code == 200:
            obj = json.loads(response.content)
            return obj
        else:
            raise ValueError(f'Request failed code {response.status_code}')

    def get_axies_from_api(self):
        """Returns a list of available axies from API"""
        try:
            content = self.contact_api(self.API_REQUESTS['status'])
        except requests.exceptions.ConnectionError:
            return 'ConnectionError'
        result = []
        for axis in content['data']:
            result.append(
                {
                    'axis': axis['axis'],
                    'minRange': axis['minRange'],
                    'maxRange': axis['maxRange'],
                    'position': round(axis['position'], 2),
                    'isBusy': axis['isBusy']
                })
        return result

    def move_axies_to_current(self, speed=10):
        """Asks API to move MyRig's axies to current position"""
        json_req = {}
        for axis in self.axies:
            json_req[axis.name] = [axis.position, speed]
        print('Asking axibo to move axies to ', json_req)
        try:
            content = self.contact_api(
                self.API_REQUESTS['move_to'],
                data=json_req
            )
            return content
        except requests.exceptions.ConnectionError:
            return 'ConnectionError'

    def move_axies_to(self, destinations):
        print('moving axies to ', destinations)
        try:
            content = self.contact_api(self.API_REQUESTS['move_to'],
                                       data=destinations)
            return content
        except requests.exceptions.ConnectionError:
            return 'ConnectionError'

    def reboot(self):
        print('Asking Axibo RIG to reboot')
        self.contact_api(self.API_REQUESTS['reboot'])
