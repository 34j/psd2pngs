from typing import Iterable, TypedDict
from psd_tools import PSDImage
from psd2pngs.safe_name import get_safe_name
from pathlib import Path


class LayerInfo(TypedDict):
    """Layer information."""

    local_path: str
    name: str
    safe_name: str
    is_visible: bool
    is_group: bool
    children: "Iterable[LayerInfo]"


def get_layer_info(layer: PSDImage, current_local_path: Path = Path("")) -> LayerInfo:
    """Get LayerInfo for the given layer. Recursively get LayerInfo for all children.

    Parameters
    ----------
    layer : PSDImage
        The base layer.
    current_local_path : Path, optional
        The base path to use for LayerInfo["local_path"], by default Path("")

    Returns
    -------
    LayerInfo
        The LayerInfo for the given layer.
    """
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
