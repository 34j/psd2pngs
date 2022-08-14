from typing import Generator, Iterable, TypedDict
from PIL import Image
from psd_tools import PSDImage
from pathlib import Path
from psd2pngs.version import __version__
from tqdm import tqdm

def _get_safe_name(name: str):
    return name.translate(str.maketrans('*\\/:?"<>| ', '-_________'))


class ImageLayerInfo(TypedDict):
    absolute_path: Path
    layer: PSDImage


def save_some_layers(psd_path: Path, out_dir_path: Path, layer_indcies: Iterable[int], pbar_position:int):
    psd = PSDImage.open(psd_path)
    layer_infos = list(search_all_layers(psd, out_dir_path))
    for i in tqdm(layer_indcies, position=pbar_position, desc=f'#{pbar_position}'):
        save_layer(psd.size, layer_infos[i])


def search_all_layers(layer: PSDImage, current_absolute_path: Path) -> Generator[ImageLayerInfo, None, None]:
    absolute_path = current_absolute_path
    if layer.kind != 'psdimage':    
        layer_safe_name = _get_safe_name(layer.name)
        absolute_path = current_absolute_path.joinpath(layer_safe_name)
        
    is_group = layer.is_group()
    if not is_group:
        absolute_path = absolute_path.with_suffix('.png')

    if is_group:
        absolute_path.mkdir(parents=True, exist_ok=True)
        for child in layer:
            for child_found in search_all_layers(child, absolute_path):
                yield child_found
    else:
        yield ImageLayerInfo(absolute_path=absolute_path, layer=layer)
    
class LayerInfo(TypedDict):
    local_path: str
    name: str
    safe_name: str
    is_visible: bool
    is_group: bool
    children: "Iterable[LayerInfo]"
    
def get_layer_info(layer: PSDImage, current_local_path: Path = Path('')) -> LayerInfo:  
    name = layer.name
    safe_name = _get_safe_name(name)
    is_visible = layer.is_visible()
    is_group = layer.is_group()
    children = []
    
    local_path = current_local_path
    
    if layer.kind != 'psdimage':
        local_path = current_local_path.joinpath(_get_safe_name(layer.name))
    
    if is_group:
        children = [get_layer_info(child, local_path) for child in layer]
    
    return LayerInfo(local_path=str(local_path), name=name, safe_name=safe_name, is_visible=is_visible, is_group=is_group, children=children)
        

def save_layer(image_size: tuple[int, int], layer_info: ImageLayerInfo) -> None:
    with Image.new('RGBA', image_size, (0, 0, 0, 0)) as img:
        img_pil = layer_info['layer'].topil()
        if img_pil is not None:
            with img_pil:
                img.paste(img_pil, layer_info['layer'].offset)  # type: ignore
                img.save(layer_info['absolute_path'])