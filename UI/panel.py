import bpy
    

class InitMsfsSceneryProjectPanel(bpy.types.Operator):
    """Tooltip"""
    bl_space_type = 'TEXT_EDITOR'
    bl_idname = 'wm.init_msfs_scenery_project'
    bl_label = 'Initialize a new MSFS project scenery'

    @classmethod
    def poll(cls, context):
        # return not os.path.isdir(os.path.join(settings.projects_path, settings.project_name))
        return True
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        self.layout.label(text='Hello world')

    def execute(self, context): # test call
        # bpy.ops.wm.init_msfs_scenery_project('INVOKE_DEFAULT')
        return {'FINISHED'}


classes = (
    InitMsfsSceneryProjectPanel,
)


def register():
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            pass
        
   


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()