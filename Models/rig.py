import bpy
# from .mockrig import RigAxibo
from .axibo import RigAxibo
from .links import Link
from .axies import Axis


class MyRig(bpy.types.PropertyGroup, RigAxibo):
    """Physical RIG class, communicates via API @LAN ip to send to and recieve
    from RIG's motors (Axies). Links used to prepare interconnexion with Blender's
    objects used for the 'virtual RIG'.
    Loaded in Blender's API in bpy.context.window_manager.myrig (see init)
    Todo feature : multi-rig"""

    ip_address: bpy.props.StringProperty(name='IP',
                                        description="Entrez une adresse IP",
                                        default='0.0.0.0',
                                        update=lambda self, context: self.update_ip_address())
    axies: bpy.props.CollectionProperty(type=Axis)
    links: bpy.props.CollectionProperty(type=Link)
    is_connected: bpy.props.BoolProperty(default=False)
    message: bpy.props.StringProperty(name='message',
                                    default='-MyRig-')
    # Voir RigMocked.get_axies_from_api()
    mock_mode: bpy.props.IntProperty(default=1)

    @property
    def is_busy(self):
        """Ask API for axies positions and status
        Returns True if at least one axis is busy"""
        self.get_axies()
        for axis in self.axies:
            if axis.is_busy is True:
                return True
        return False

    def clear_axies(self):
        # print(f'{self}clearing all axies')
        self.axies.clear()

    def add_axis(self, unique_name, minRange, maxRange, position, is_busy):
        # print(f'{self}adding axis : ' + unique_name)
        new_axis = self.axies.add()
        new_axis.name = unique_name
        new_axis.minRange = minRange
        new_axis.maxRange = maxRange
        new_axis.position = position
        new_axis.is_busy = is_busy

    def get_axies(self):
        """Get axies from RIG's API and updates axies if successfull.
        Manages is_connected bool. Prompt user with result via message string."""
        self.clear_axies()
        try:
            api_content = self.get_axies_from_api()
        except ValueError:
            return None
        if api_content == 'ConnectionError':
            self.message = f'Can\'t reach RIG at {self.ip_address}'
            self.is_connected = False
            return None
        elif api_content is None:
            self.message = 'No axies found'
            return None
        self.message = f'{len(api_content)} axies found'
        self.is_connected = True
        for a in api_content:
            self.add_axis(
                a['axis'],
                a['minRange'],
                a['maxRange'],
                a['position'],
                a['isBusy']
            )
        return api_content

    def clear_links(self):
        print(f'{self}clearing all links')
        self.links.clear()

    def add_link(self, unique_name):
        print(f'{self}adding link : ' + unique_name)
        new_link = self.links.add()
        new_link.name = unique_name

    def get_links(self):
        """Creates a link for each axies. Will be used by kinetic
        controller"""
        self.clear_links()
        print(f'{self}generating links')
        for a in self.axies:
            self.add_link(a.name)

    # Checking user input for ip address
    def check_ip_address_format(self, ip):
        octets = ip.split('.')
        if len(octets) != 4:
            return False
        for octet in octets:
            if not octet.isdigit() or not 0 <= int(octet) <= 255:
                return False
        return True

    def update_ip_address(self):
        if not self.check_ip_address_format(self.ip_address):
            self.ip_address = "0.0.0.0"
            self.message = "Adresse IP invalide. Veuillez saisir une adresse IP au format correct"
