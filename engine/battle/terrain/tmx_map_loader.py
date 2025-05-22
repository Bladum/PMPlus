import os
import xml.etree.ElementTree as ET

class TMXMapLoader:
    @staticmethod
    def load_tilesets(tmx):
        """
        Loads all tilesets referenced in the TMX file and returns a dict mapping GID to tile properties.
        """
        gid_map = {}
        for ts in tmx.tilesets:
            tsx_path = ts.source
            if not os.path.isabs(tsx_path):
                tsx_path = os.path.join(os.path.dirname(tmx.filename), tsx_path)
            try:
                tree = ET.parse(tsx_path)
                root = tree.getroot()
                for tile in root.findall('tile'):
                    id_ = int(tile.attrib['id']) + ts.firstgid
                    props = {}
                    properties = tile.find('properties')
                    if properties is not None:
                        for prop in properties.findall('property'):
                            props[prop.attrib['name']] = prop.attrib.get('value')
                    gid_map[id_] = props
            except Exception:
                continue
        return gid_map

    @staticmethod
    def layer_to_2d(layer, width, height):
        data = list(layer.data)
        return [data[y*width:(y+1)*width] for y in range(height)]

