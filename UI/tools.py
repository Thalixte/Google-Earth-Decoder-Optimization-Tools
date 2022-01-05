import bpy
from bpy import context
from utils import isolated_print


def reload_topbar_menu():
    try:
        if hasattr(bpy.types.TOPBAR_MT_editor_menus.draw, "_draw_funcs"):
            for f in bpy.types.TOPBAR_MT_editor_menus.draw._draw_funcs:
                if not repr(f).startswith("<function TOPBAR_MT_editor_menus.draw"):
                    bpy.types.TOPBAR_MT_editor_menus.draw._draw_funcs.remove(f)
    except AttributeError:
        pass


def invoke_current_operator():
    eval("bpy.ops." + context.scene.panel_props.current_operator + "(\"INVOKE_DEFAULT\")")


def reload_setting_props():
    setting_props = context.scene.setting_props
    for name in setting_props.__annotations__.keys():
        if hasattr(setting_props.bl_rna.properties[name], "default"):
            setting_props[name] = getattr(setting_props.bl_rna.properties[name], "default")
