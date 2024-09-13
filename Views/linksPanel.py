import bpy


class LinkPanelSubPanel(bpy.types.Panel):
    bl_label = "Link panel"
    bl_idname = "OBJECT_PT_link_panel_sub_panel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_parent_id = "OBJECT_PT_RemotePanel"

    def draw(self, context):
        layout = self.layout
        my_rig = context.window_manager.myrig
        row = layout.row(align=True)
        if my_rig.links is None:
            layout.label(text="No links. Use generate links")
        split = layout.split(factor=0.2)
        col = split.column()
        for li in my_rig.links:
            col.label(text=f'{li.name}')
        col = split.column()
        row = col.row(align=True)
        for li in my_rig.links:
            row = col.row(align=True)
            row.prop(li, "obj")
            row.prop(li, "obj_axis")
            op = row.operator("ctrl.add_link_operator", text='Link')
            op.link_name = li.name


class AddLinkOperator(bpy.types.Operator):
    bl_idname = "ctrl.add_link_operator"
    bl_label = "Link operator"

    link_name: bpy.props.StringProperty()

    def execute(self, context):
        WM = context.window_manager
        my_controller = WM.mycontroller
        my_rig = WM.myrig
        link = my_rig.links.get(self.link_name)
        my_controller.add_link(link)
        return {'FINISHED'}
