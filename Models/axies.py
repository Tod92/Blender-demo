import bpy


class Axis(bpy.types.PropertyGroup):

    name: bpy.props.StringProperty()
    minRange: bpy.props.FloatProperty()
    maxRange: bpy.props.FloatProperty()   
    is_busy: bpy.props.BoolProperty()
    def update_position(self, context):       
        if self.position < self.minRange:
            print(f'{self} position({self.position}) lower than minRange({self.minRange})!')
            self.position = self.minRange
        elif self.position > self.maxRange:
            print(f'{self} position({self.position}) higher than maxRange({self.maxRange})!')
            self.position = self.maxRange
    position: bpy.props.FloatProperty(update=update_position)
