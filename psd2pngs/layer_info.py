from typing import Iterable, TypedDict
from psd_tools import PSDImage
from psd2pngs.safe_name import get_safe_name
from pathlib import Path


class LayerInfo(TypedDict):
    local_path: str
    name: str
    safe_name: str
    is_visible: bool
    is_group: bool
    children: "Iterable[LayerInfo]"


def get_layer_info(layer: PSDImage, current_local_path: Path = Path("")) -> LayerInfo:
    name = layer.name
    safe_name = get_safe_name(name)
    is_visible = layer.is_visible()
    is_group = layer.is_group()
    children = []

    local_path = current_local_path

    if layer.kind != "psdimage":
        local_path = current_local_path.joinpath(get_safe_name(layer.name))

        if not is_group:
            local_path = local_path.with_suffix(".png")

    if is_group:
        children = [get_layer_info(child, local_path) for child in layer]

    return LayerInfo(
        local_path=str(local_path),
        name=name,
        safe_name=safe_name,
        is_visible=is_visible,
        is_group=is_group,
        children=children,
    )
