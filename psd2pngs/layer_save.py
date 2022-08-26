from typing import Union
from typing import Generator, Iterable, TypedDict
from PIL import Image
from psd_tools import PSDImage
from pathlib import Path
from psd2pngs.safe_name import get_safe_name
from psd_tools.api.layers import Layer


class ImageLayerInfo(TypedDict):
    """Layer and

    Parameters
    ----------
    absolute_path: Path
        The absolute path to output the image.
    layer: Layer
        The layer to output.
    """

    absolute_path: Path
    """The absolute path to output the image.
    """
    layer: Layer
    """The layer to output.
    """


def search_all_layers(
    layer: Union[Layer, PSDImage], current_absolute_path: Path
) -> Generator[ImageLayerInfo, None, None]:
    """Get all ImageLayerInfos under the given layer. Recursively get all ImageLayerInfos for all children.

    Parameters
    ----------
    layer : Layer
        The base layer.
    current_absolute_path : Path
        The base absolute path to use for ImageLayerInfo["absolute_path"]

    Yields
    ------
    Generator[ImageLayerInfo, None, None]
        _description_
    """
    absolute_path = current_absolute_path
    if layer.kind != "Layer":
        layer_safe_name = get_safe_name(layer.name)
        absolute_path = current_absolute_path.joinpath(layer_safe_name)

    is_group = layer.is_group()
    if not is_group:
        absolute_path = absolute_path.with_suffix(".png")

    if is_group:
        absolute_path.mkdir(parents=True, exist_ok=True)
        for child in layer:  # type: ignore
            for child_found in search_all_layers(child, absolute_path):
                yield child_found
    else:
        yield ImageLayerInfo(absolute_path=absolute_path, layer=layer)


def save_layer(image_size: tuple[int, int], layer_info: ImageLayerInfo) -> None:
    """Save the given layer (layer_info['layer']) to the given path (layer_info['absolute_path']).

    Parameters
    ----------
    image_size : tuple[int, int]
        The size of the root layer (any layer which you want it to be based on). psd.size is Recommended.
    layer_info : ImageLayerInfo
        The layer and absolute path to save the layer to.
    """
    with Image.new("RGBA", image_size, (0, 0, 0, 0)) as img:
        img_pil = layer_info["layer"].topil()
        if img_pil is not None:
            with img_pil:
                img.paste(img_pil, layer_info["layer"].offset)  # type: ignore
                img.save(layer_info["absolute_path"])


def save_some_layers(psd_path: Path, out_dir_path: Path, layer_indcies: Iterable[int]):
    """Open the PSD file and save the given layers to the given path.

    Parameters
    ----------
    psd_path : Path
        The path to the PSD file.
    out_dir_path : Path
        The base absolute path to create a folder in which layers will be saved.
    layer_indcies : Iterable[int]
        Indcies (for search_all_layers()) of the layers to save.
    """
    psd = PSDImage.open(psd_path)
    layer_infos = list(search_all_layers(psd, out_dir_path))
    for i in layer_indcies:
        save_layer(psd.size, layer_infos[i])
