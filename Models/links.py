import bpy
import math


class Link(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty()
    obj: bpy.props.PointerProperty(type=bpy.types.Object)
    obj_axis: bpy.props.EnumProperty(
        name='ax',
        items=[
            ('rot x', 'Rotation X', 'Rotation X'),
            ('rot y', 'Rotation Y', 'Rotation Y'),
            ('rot z', 'Rotation Z', 'Rotation Z'),
            ('loc x', 'Location X', 'Location X'),
            ('loc y', 'Location Y', 'Location Y'),
            ('loc z', 'Location Z', 'Location Z'),
        ]
    )
    scale: bpy.props.FloatProperty(default=1)
    speed: bpy.props.FloatProperty(default=10)

    def update_offset(self, context):
        """Updates offset value in self.obj considering obj_axis"""
        match self.obj_axis:
            case 'rot x':
                value = math.radians(self.offset)
                self.obj.delta_rotation_euler.x = value
            case 'rot y':
                value = math.radians(self.offset)
                self.obj.delta_rotation_euler.y = value
            case 'rot z':
                value = math.radians(self.offset)
                self.obj.delta_rotation_euler.z = value
            case 'loc x':
                self.obj.delta_location.x = self.offset
            case 'loc y':
                self.obj.delta_location.y = self.offset
            case 'loc z':
                self.obj.delta_location.z = self.offset

    offset: bpy.props.FloatProperty(default=0,
                                    update=update_offset)

    @property
    def position(self):
        value = None
        match self.obj_axis:
            case 'rot x':
                value = self.obj.rotation_euler.x
                value = math.degrees(value)
            case 'rot y':
                value = self.obj.rotation_euler.y
                value = math.degrees(value)
            case 'rot z':
                value = self.obj.rotation_euler.z
                value = math.degrees(value)
            case 'loc x':
                value = self.obj.location.x
            case 'loc y':
                value = self.obj.location.y
            case 'loc z':
                value = self.obj.location.z
        return round(value, 2)

    @property
    def scaled_position(self):
        value = self.position
        return round(value * self.scale, 2)
