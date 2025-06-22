from typing import Any, overload

class ResourceTarget:
    @overload
    def __init__(self, type_: str, name: str): ...
    @overload
    def __init__(self, resid: str): ...
    def __init__(self, **kwargs: str):
        # TODO: Implement __init__
        self.type_ = resid.split("/", 1)[0]
        self.name = resid.split("/", 1)[1]
    def __str__(self):
        return f"@{self.type_}/{self.name}"
    def __repr__(self):
        return f"ResourceTarget(resid={self.__str__()})"

class Resource(ResourceTarget):
    @overload
    def __init__(self, type_: str, name: str, value: Any):
        super().__init__(type_, name)
        self.value = value
    @overload
    def __init__(self, resid: str, value: Any):
        self.type_ = resid.split("/", 1)[0]
        self.name = resid.split("/", 1)[1]
        self.value = value
    def __str__(self):
        return f"@{self.type_}/{self.name}"
    def __repr__(self):
        return f"ResourceTarget(resid={self.__str__()}, value={self.value})"

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
