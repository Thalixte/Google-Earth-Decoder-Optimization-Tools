import bpy

TEXT_EDITOR_AREA = "TEXT_EDITOR"


def exec_script_from_menu(script_path):
    text = bpy.data.texts.load(script_path)

    for area in bpy.context.screen.areas:
        if area.type == TEXT_EDITOR_AREA:
            area.spaces.active.text = text

            ctx = bpy.context.copy()
            ctx['edit_text'] = text
            ctx['area'] = area
            bpy.ops.text.run_script(ctx)
            bpy.ops.text.unlink(ctx)
            break
