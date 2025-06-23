from typing import Any, overload
import shutil
import os

class ResourceTarget:
    @overload
    def __init__(self, type_: str, name: str): ...
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
    def __init__(self, type_: str, name: str, value: Any): ...
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
        manifest = root + "/AndroidManifest.xml"
        with open(manifest, "w") as f:
            f.write(f"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
            f.write(f"<manifest xmlns:android=\"http://schemas.android.com/apk/res/android\" package=\"{self.pkgName}\">\n")
            f.write(f"    <application android:hasCode=\"false\" />\n")
            f.write(f"    <overlay android:targetPackage=\"{self.targetPkg}\" android:targetName=\"{self.targetName}\" android:resourcesMap=\"@xml/overlays\" android:isStatic=\"{"true" if self.static else "false"}\" android:priority=\"{self.priority}\" />\n")
            f.write(f"</manifest>\n")
