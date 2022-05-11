from uuid import uuid4
from xml.dom import minidom
from xml.dom.minidom import parse

from msfs_project.objects_xml import ObjectsXml
from msfs_project.object_xml import MsfsObjectXml


def create_new_definition_file(file_path, has_lods=True):
    new_guid = "{" + str(uuid4()) + "}"
    root = minidom.Document()
    model_info = root.createElement(MsfsObjectXml.MODEL_INFO_TAG)
    model_info.setAttribute(MsfsObjectXml.GUID_ATTR, new_guid)
    model_info.setAttribute(MsfsObjectXml.VERSION_ATTR, MsfsObjectXml.MODEL_INFO_VERSION)
    root.appendChild(model_info)
    if has_lods:
        lods = root.createElement(MsfsObjectXml.LODS_TAG)
        model_info.appendChild(lods)

    xml_str = "\n".join([line for line in root.toprettyxml(indent=" "*2).split('\n') if line.strip()])

    with open(file_path, "w") as f:
        f.write(xml_str)

    return new_guid


def add_new_lod(file_path, model_file, min_size_value):
    root = parse(file_path)
    lods = root.getElementsByTagName(MsfsObjectXml.LODS_TAG)
    if len(lods) > 0:
        lods = root.getElementsByTagName(MsfsObjectXml.LODS_TAG)[0]
        lod = root.createElement(MsfsObjectXml.LOD_TAG)
        lod.setAttribute(MsfsObjectXml.MODEL_FILE_ATTR, model_file)
        lod.setAttribute(MsfsObjectXml.MIN_SIZE_ATTR, min_size_value)
        lods.appendChild(lod)

        xml_str = "\n".join([line for line in root.toprettyxml(indent=" "*2).split('\n') if line.strip()])

        with open(file_path, "w") as f:
            f.write(xml_str)


def add_scenery_object(file_path, tile, templates):
    root = parse(file_path)
    fs_data = root.getElementsByTagName(ObjectsXml.FS_DATA_TAG)

    if len(fs_data) > 0:
        for template in templates:
            fs_data = root.getElementsByTagName(ObjectsXml.FS_DATA_TAG)[0]
            scenery_object = root.createElement(ObjectsXml.SCENERY_OBJECT_TAG)
            scenery_object.setAttribute(ObjectsXml.ALT_ATTR, template.get(ObjectsXml.ALT_ATTR))
            scenery_object.setAttribute(ObjectsXml.ALTITUDE_IS_AGL_ATTR, template.get(ObjectsXml.ALTITUDE_IS_AGL_ATTR))
            scenery_object.setAttribute(ObjectsXml.BANK_ATTR, template.get(ObjectsXml.BANK_ATTR))
            scenery_object.setAttribute(ObjectsXml.HEADING_ATTR, template.get(ObjectsXml.HEADING_ATTR))
            scenery_object.setAttribute(ObjectsXml.IMAGE_COMPLEXITY_ATTR, template.get(ObjectsXml.IMAGE_COMPLEXITY_ATTR))
            scenery_object.setAttribute(ObjectsXml.LAT_ATTR, template.get(ObjectsXml.LAT_ATTR))
            scenery_object.setAttribute(ObjectsXml.LON_ATTR, template.get(ObjectsXml.LON_ATTR))
            scenery_object.setAttribute(ObjectsXml.PITCH_ATTR, template.get(ObjectsXml.PITCH_ATTR))
            scenery_object.setAttribute(ObjectsXml.SNAP_TO_GROUND_ATTR, template.get(ObjectsXml.SNAP_TO_GROUND_ATTR))
            scenery_object.setAttribute(ObjectsXml.SNAP_TO_NORMAL_ATTR, template.get(ObjectsXml.SNAP_TO_NORMAL_ATTR))
            library_object = root.createElement(ObjectsXml.LIBRARY_OBJECT_TAG)
            library_object.setAttribute(ObjectsXml.NAME_ATTR, tile.xml.guid)
            library_object.setAttribute(ObjectsXml.SCALE_ATTR, "1")
            scenery_object.appendChild(library_object)
            fs_data.appendChild(scenery_object)

    xml_str = "\n".join([line for line in root.toprettyxml(indent=" "*2).split('\n') if line.strip()])

    with open(file_path, "w") as f:
        f.write(xml_str)
