from typing import Generator, Iterable, TypedDict
from PIL import Image
from psd_tools import PSDImage
from pathlib import Path
from psd2pngs.safe_name import get_safe_name


class ImageLayerInfo(TypedDict):
    absolute_path: Path
    layer: PSDImage


def search_all_layers(
    layer: PSDImage, current_absolute_path: Path
) -> Generator[ImageLayerInfo, None, None]:
    absolute_path = current_absolute_path
    if layer.kind != "psdimage":
        layer_safe_name = get_safe_name(layer.name)
        absolute_path = current_absolute_path.joinpath(layer_safe_name)

    is_group = layer.is_group()
    if not is_group:
        absolute_path = absolute_path.with_suffix(".png")

    if is_group:
        absolute_path.mkdir(parents=True, exist_ok=True)
        for child in layer:
            for child_found in search_all_layers(child, absolute_path):
                yield child_found
    else:
        yield ImageLayerInfo(absolute_path=absolute_path, layer=layer)


def save_layer(image_size: tuple[int, int], layer_info: ImageLayerInfo) -> None:
    with Image.new("RGBA", image_size, (0, 0, 0, 0)) as img:
        img_pil = layer_info["layer"].topil()
        if img_pil is not None:
            with img_pil:
                img.paste(img_pil, layer_info["layer"].offset)  # type: ignore
                img.save(layer_info["absolute_path"])


def save_some_layers(psd_path: Path, out_dir_path: Path, layer_indcies: Iterable[int]):
    psd = PSDImage.open(psd_path)
    layer_infos = list(search_all_layers(psd, out_dir_path))
    for i in layer_indcies:
        save_layer(psd.size, layer_infos[i])
