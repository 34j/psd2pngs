from typing import Iterable, TypedDict
from psd_tools import PSDImage
from psd2pngs.safe_name import get_safe_name
from pathlib import Path


class LayerInfo(TypedDict):
    """Layer information."""
    local_path: str
    """The local path to the layer. The file name is safe_name.png."""
    name: str
    """The name of the layer."""
    safe_name: str
    """The safe name (which could be used as a file name) of the layer."""
    is_visible: bool
    """Whether the layer is visible."""
    is_group: bool
    """Whether the layer is a group."""
    children: "Iterable[LayerInfo]"
    """LayerInfos of the child layers. Empty list if not a group.
    """


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
    # get names
    name = layer.name
    safe_name = get_safe_name(name)
    
    # get visibility
    is_visible = layer.is_visible()
    is_group = layer.is_group()

    # avoid to create 'Root' folder because it is just disruptive
    if layer.kind == "psdimage":
        local_path = current_local_path
    else:
        local_path = current_local_path.joinpath(get_safe_name(layer.name))

    # add suffix
    if not is_group:
        local_path = local_path.with_suffix(".png")

    # recursively get LayerInfo for all children 
    children = []
    if is_group:
        children = [get_layer_info(child, local_path) for child in layer]

    # return LayerInfo
    return LayerInfo(
        local_path=str(local_path),
        name=name,
        safe_name=safe_name,
        is_visible=is_visible,
        is_group=is_group,
        children=children,
    )
