from typing import Union
from typing import Generator, Iterable, TypedDict
from PIL import Image
from psd_tools import PSDImage
from pathlib import Path
from psd2pngs.safe_name import get_safe_name
from psd_tools.api.layers import Layer, Group, PixelLayer


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
        ImageLayerInfos for all layers.
    """
    
    # avoid to create 'Root' folder because it is just disruptive
    if layer.kind == "psdimage":    
        absolute_path = current_absolute_path
    else:
        layer_safe_name = get_safe_name(layer.name)
        absolute_path = current_absolute_path.joinpath(layer_safe_name)

    if layer.is_group():
        # create folder for group
        absolute_path.mkdir(parents=True, exist_ok=True)
        
        # recursively get all ImageLayerInfos for all children
        for child in layer:  # type: ignore
            yield from search_all_layers(child, absolute_path)
    else:
        # add suffix
        absolute_path = absolute_path.with_suffix(".png")
        # yield ImageLayerInfo
        yield ImageLayerInfo(absolute_path=absolute_path, layer=layer)


def save_layer(image_size: tuple[int, int], layer_info: ImageLayerInfo) -> None:
    """Save the given layer (layer_info['layer']) to the given path (layer_info['absolute_path']) using PIL.

    Parameters
    ----------
    image_size : tuple[int, int]
        The size of the root layer (any layer which you want it to be based on). psd.size is Recommended.
    layer_info : ImageLayerInfo
        The layer and absolute path to save the layer to.
    """
    # make sure that the size and position of the layer is maintained
    with Image.new("RGBA", image_size, (0, 0, 0, 0)) as img:
        # covert to PIL.Image
        img_pil = layer_info["layer"].topil()
        if img_pil is not None:
            with img_pil:
                # paste the layer onto the image to maintain the position
                img.paste(img_pil, layer_info["layer"].offset)  # type: ignore
                img.save(layer_info["absolute_path"])


def save_some_layers(psd_path: Path, out_dir_path: Path, layer_indcies: Iterable[int]):
    """Open the PSD file and save the given layers to the given path.
    The expected use case of this function is to use as a multiprocessing function.
    (Because heavy layers do not have to be pickled.)

    Parameters
    ----------
    psd_path : Path
        The path to the PSD file.
    out_dir_path : Path
        The base absolute path to create a folder in which layers will be saved.
    layer_indcies : Iterable[int]
        Indcies (for search_all_layers()) of the layers to save.
    """
    # open the PSD file
    psd = PSDImage.open(psd_path)

    # search layers
    image_layer_infos = list(search_all_layers(psd, out_dir_path))

    # save specified layers
    for i in layer_indcies:
        save_layer(psd.size, image_layer_infos[i])
