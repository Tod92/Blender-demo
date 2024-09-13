

class LinkManager:

    def add_link(self, link):
        # Cas doublon
        doublon = self.links.get(link.name)
        if doublon:
            print('Link refusé : doublon détécté')
            return None
        # Cas problème avec l'objet blender linké
        try:
            link.position
        except AttributeError:
            print('Link refusé : objet blender lié inexistant ou non conforme')
            return None
        self.copy_link(link)

    def copy_link(self, link):
        print('copying link : ' + link.name)
        new_link = self.links.add()
        new_link.name = link.name
        new_link.obj = link.obj
        new_link.obj_axis = link.obj_axis
        new_link.offset = link.offset
        new_link.scale = link.scale

    def clear_links(self):
        print('KineticController clearing all links')
        self.links.clear()
