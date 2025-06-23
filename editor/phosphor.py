from typing import Any, overload, Literal
import shutil
import os

class ResourceTarget:
    @overload
    def __init__(self, type_: Literal["color", "drawable", "mipmap", "string", "bool", "integer", "dimens", "fraction", "id", "layout", "anim", "animator", "interpolator", "menu", "xml", "font", "raw", "plurals", "style", "attr", "array"], name: str): ...
    @overload
    def __init__(self, resid: str): ...
    def __init__(self, *args: str):
        if len(args) == 1:
            self.type_ = args[0].split("/", 1)[0]
            self.name = argd[1].split("/", 1)[1]
        else:
            self.type_ = args[0]
            self.name = args[1]
    def __str__(self):
        return f"{self.type_}/{self.name}"
    def __repr__(self):
        return f"ResourceTarget(\"{self.__str__()}\")"

class Resource(ResourceTarget):
    @overload
    def __init__(self, type_: Literal["string", "bool", "integer", "plurals", "style", "attr", "array", "string-array"], name: str, value: Any): ...
    @overload
    def __init__(self, resid: str, value: Any): ...
    def __init__(self, *args):
        if len(args) == 2:
            super().__init__(args[0])
            self.value = args[1]
        else:
            super().__init__(args[0], args[1])
            self.value = args[2]
    def __str__(self):
        return f"{self.type_}/{self.name}"
    def __repr__(self):
        return f"ResourceTarget(\"{self.__str__()}\", \"{self.value}\")"

class Overlay:
    def __init__(self, targetPkg: str, targetName: str, pkgName: str, static: bool, priority: int):
        self.targetPkg = targetPkg
        self.targetName = targetName
        self.pkgName = pkgName
        self.static = static
        self.priority = priority
        self.overlays = {}

    def link_resource(self, target: ResourceTarget, res: Resource):
        self.overlays[target] = res

    def build_linux(self, folder: str | None = None):
        root = folder if folder else f"{self.targetPkg}-{self.targetName}-overlay"
        shutil.rmtree(root, ignore_errors=True)
        os.mkdir(root)

        # Manifest
        manifest = root + "/AndroidManifest.xml"
        with open(manifest, "w") as f:
            f.write(f"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
            f.write(f"<manifest xmlns:android=\"http://schemas.android.com/apk/res/android\" package=\"{self.pkgName}\">\n")
            f.write(f"    <application android:hasCode=\"false\" />\n")
            f.write(f"    <overlay android:targetPackage=\"{self.targetPkg}\" android:targetName=\"{self.targetName}\" android:resourcesMap=\"@xml/overlays\" android:isStatic=\"{"true" if self.static else "false"}\" android:priority=\"{self.priority}\" />\n")
            f.write(f"</manifest>\n")

        # Res
        res = root + "/res"
        os.mkdir(res)

        # Res > XML
        xml = res + "/xml"
        os.mkdir(xml)

        # Res > XML > Overlays
        overlays = xml + "/overlays.xml"
        with open(overlays, "w") as f:
            f.write(f"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
            f.write(f"<overlay xmlns:android=\"http://schemas.android.com/apk/res/android\">\n")
            for target, resource in self.overlays.items():
                f.write(f"    <item target=\"{target}\" value=\"@{resource}\" />\n")
            f.write(f"</overlay>\n")

        # Res > Values
        values = res + "/values"
        os.mkdir(values)

        # Res > Values > Strings
        strings = values + "/strings.xml"
        with open(strings, "w") as f:
            f.write(f"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
            f.write(f"<resources>\n")
            for resource in self.overlays.values():
                if resource.type_ == "string":
                    f.write(f"    <string name=\"{resource.name}\">{resource.value}</string>\n")
            f.write(f"</resources>\n")
        
        # Res > Values > Bools
        bools = values + "/bools.xml"
        with open(bools, "w") as f:
            f.write(f"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
            f.write(f"<resources>\n")
            for resource in self.overlays.values():
                if resource.type_ == "bool":
                    f.write(f"    <bool name=\"{resource.name}\">{resource.value}</bool>\n")
            f.write(f"</resources>\n")
        
        # Res > Values > Integers
        integers = values + "/integers.xml"
        with open(integers, "w") as f:
            f.write(f"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
            f.write(f"<resources>\n")
            for resource in self.overlays.values():
                if resource.type_ == "integer":
                    f.write(f"    <integer name=\"{resource.name}\">{resource.value}</integer>\n")
            f.write(f"</resources>\n")
        
        # Res > Values > Plurals
        plurals = values + "/plurals.xml"
        with open(plurals, "w") as f:
            f.write(f"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
            f.write(f"<resources>\n")
            for resource in self.overlays.values():
                if resource.type_ == "plurals":
                    f.write(f"    <plurals name=\"{resource.name}\">\n")
                    for quantity, value in resource.value:
                        f.write(f"        <item quantity=\"{quantity}\">{value}</item>\n")
                    f.write(f"    </plurals>\n")
            f.write(f"</resources>\n")
        
        # Res > Values > Styles
        styles = values + "/styles.xml"
        with open(styles, "w") as f:
            f.write(f"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
            f.write(f"<resources>\n")
            for resource in self.overlays.values():
                if resource.type_ == "style":
                    f.write(f"    <style name=\"{resource.name}\">\n")
                    for name, value in resource.value:
                        f.write(f"        <item name=\"{name}\">{value}</item>\n")
                    f.write(f"    </style>\n")
            f.write(f"</resources>\n")
        
        # Res > Values > Attrs
        attrs = values + "/attrs.xml"
        with open(attrs, "w") as f:
            f.write(f"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
            f.write(f"<resources>\n")
            for resource in self.overlays.values():
                if resource.type_ == "attr":
                    f.write(f"    <attr name=\"{resource.name}\" format=\"{resource.value}\" />\n")
            f.write(f"</resources>\n")
        
        # Res > Values > Arrays
        arrays = values + "/arrays.xml"
        with open(arrays, "w") as f:
            f.write(f"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
            f.write(f"<resources>\n")
            for resource in self.overlays.values():
                if resource.type_ == "array":
                    f.write(f"    <array name=\"{resource.name}\">\n")
                    for value in resource.value:
                        f.write(f"        <item>{value}</item>\n")
                    f.write(f"    </array>\n")
                if resource.type_ == "string-array":
                    f.write(f"    <string-array name=\"{resource.name}\">\n")
                    for value in resource.value:
                        f.write(f"        <item>{value}</item>\n")
                    f.write(f"    </string-array>\n")
            f.write(f"</resources>\n")