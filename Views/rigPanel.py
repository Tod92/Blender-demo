import bpy


class RigPanel(bpy.types.Panel):
    bl_label = "Rig Panel"
    bl_idname = "OBJECT_PT_RigPanel"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_parent_id = "OBJECT_PT_RemotePanel"

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        my_rig = context.window_manager.myrig
        row = layout.row(align=True)
        # Champ pour l'adresse IP
        layout.prop(my_rig, "ip_address")
        row = layout.row(align=True)
        # Bouton de connexion
        op = layout.operator("wm.button_operator_rig", text="CONNEXION AU RIG")
        op.method = 'RIG_Connect'
        row = layout.row(align=True)
        op = layout.operator("wm.button_operator_rig", text="REDEMARRER RIG")
        op.method = 'RIG_Reboot'

        if my_rig.is_connected is False:
            layout.label(text="Please connect to get axies list")
        else:
            # Affichage de la liste des axes
            row = layout.row(align=True)
            split = layout.split(factor=0.2)
            col = split.column()
            for a in my_rig.axies:
                col.label(text=f'{a.name}')
            col = split.column()
            row = col.row(align=True)
            for a in my_rig.axies:
                row = col.row(align=True)
                row.prop(a, "position")
                [row.label(text="is_busy") if a.is_busy else None]
            row = layout.row(align=True)
            op = row.operator("wm.button_operator_rig", text='GENERATE LINK PANEL')
            op.method = 'RIG_GenLinkPanel'
            op = row.operator("wm.button_operator_rig", text='MOVE RIG')
            op.method = 'RIG_MoveRig'


class RigButtonOperator(bpy.types.Operator):
    bl_idname = "wm.button_operator_rig"
    bl_label = "My Operator"

    method: bpy.props.EnumProperty(
        items=[
            ('RIG_Connect', "Method 1", "Connect to RIG"),
            ('RIG_Reboot', "Method 2", "Reboot RIG"),
            ('RIG_GenLinkPanel', "Method 3", "Generate Link Panel"),
            ('RIG_MoveRig', "Method 4", "Move rig to positions")
        ],
        default='RIG_Connect'
    )

    def execute(self, context):
        my_rig = context.window_manager.myrig
        match self.method:
            case 'RIG_Connect':
                my_rig.get_axies()
            case 'RIG_Reboot':
                my_rig.reboot()
            case 'RIG_GenLinkPanel':
                my_rig.get_links()
            case 'RIG_MoveRig':
                my_rig.move_axies_to_current()
        bpy.context.area.tag_redraw()
        return {'FINISHED'}
