bl_info = {
    "name": "OneClickKnife",
    "author": "OpenAI",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "3D Viewport > Object Mode > Right-click menu",
    "description": "Project the first selected mesh onto the active mesh with Knife Project",
    "category": "Mesh",
}

import bpy


class MESH_OT_one_click_knife(bpy.types.Operator):
    """Use the non-active selected mesh as the cutter and the active mesh as the target"""

    bl_idname = "mesh.one_click_knife"
    bl_label = "ナイフ投影"
    bl_description = (
        "最初に選択したメッシュをカッター、最後に選択した（アクティブな）メッシュを"
        "投影先として、現在のビュー方向からナイフ投影します"
    )
    bl_options = {'REGISTER', 'UNDO'}

    cut_through: bpy.props.BoolProperty(
        name="貫通",
        description="裏側の面も切断します",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        selected = context.selected_objects
        active = context.active_object
        return (
            context.mode == 'OBJECT'
            and len(selected) == 2
            and active is not None
            and active in selected
            and active.type == 'MESH'
            and next(obj for obj in selected if obj != active).type in {'MESH', 'CURVE'}
        )

    def execute(self, context):
        target = context.active_object
        cutter = next(obj for obj in context.selected_objects if obj != target)

        # Knife Project requires only the target to enter Edit Mode.  The cutter
        # must stay in Object Mode but remain selected, as in Blender's native
        # Knife Project workflow.
        cutter.select_set(False)
        context.view_layer.objects.active = target
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        cutter.select_set(True)
        context.view_layer.objects.active = target

        try:
            result = bpy.ops.mesh.knife_project(cut_through=self.cut_through)
        except RuntimeError as error:
            bpy.ops.object.mode_set(mode='OBJECT')
            self.report({'ERROR'}, f"ナイフ投影を実行できませんでした: {error}")
            return {'CANCELLED'}

        if 'FINISHED' not in result:
            bpy.ops.object.mode_set(mode='OBJECT')
            self.report({'ERROR'}, "ナイフ投影を実行できませんでした。3D ビュー上で実行してください。")
            return {'CANCELLED'}

        # Keep the interaction entirely in Object Mode from the user's point of
        # view.  Edit Mode is only used internally because Knife Project needs it.
        bpy.ops.object.mode_set(mode='OBJECT')
        self.report({'INFO'}, f"{cutter.name} を {target.name} にナイフ投影しました")
        return {'FINISHED'}


def draw_object_context_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.operator(MESH_OT_one_click_knife.bl_idname, icon='MOD_BOOLEAN')


classes = (MESH_OT_one_click_knife,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_object_context_menu.append(draw_object_context_menu)


def unregister():
    bpy.types.VIEW3D_MT_object_context_menu.remove(draw_object_context_menu)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
