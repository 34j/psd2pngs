from typing import TypedDict
from PIL import Image
from psd_tools import PSDImage
from pathlib import Path
import click
from tqdm import tqdm
import concurrent.futures
from logging import getLogger, DEBUG
import multiprocessing



@click.command()
@click.argument('psd_path', type=click.Path(exists=True))
@click.option('--out-dir-path', '-o', type=click.Path(exists=True), default=None,
              help='Output directory path. If not specified, output to the same directory as the PSD file.')
@click.option('--multiprocessing', '-m', is_flag=True, 
              help='Use multiprocessing. Note that multiprocessing is slower in most cases because pickling layers is slow.')
def psd2pngs(psd_path: str, out_dir_path: str = '', multiprocessing:bool = False):
    psd_path_ = Path(psd_path).absolute() 
    out_dir_path_ = psd_path_.parent
    if out_dir_path is not None:
        out_dir_path_ = Path(out_dir_path).absolute()
    if psd_path_.suffix != '.psd':
        raise ValueError('The suffix of psd_path must be .psd')

    psd = PSDImage.open(psd_path_)
    
    out_dir_path_ = out_dir_path_.joinpath(psd_path_.stem)
    out_dir_path_.mkdir(parents=True, exist_ok=True)
    
    logger = getLogger(__name__)
    logger.setLevel(DEBUG)
    
    # search all layers
    logger.info('Searching all layers...')
    all_layers = list(tqdm(search_all_layers(psd, out_dir_path_, []), unit='layer(s)'))
    
    # save layers
    logger.info('Saving layers...')
    tasks = []
    
    if multiprocessing:
        logger.warning('Note that multiprocessing is slower in most cases because pickling layers is slow.')
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for layer_info in all_layers:
                tasks.append(executor.submit(save_layer, psd.size, layer_info))
            [future.result() for future in tqdm(
                concurrent.futures.as_completed(tasks), total=len(tasks), unit='file(s)')]
    else:
        pbar = tqdm(all_layers, unit='file(s)')
        for layer_info in pbar:
            save_layer(psd.size, layer_info)


def _get_safe_name(name: str):
    return name.translate(str.maketrans('*\\/:?"<>| ', '-_________'))


class LayerInfo(TypedDict):
    absolute_path: Path
    layer: PSDImage


def search_all_layers(layer: PSDImage, current_dir: Path, founds: list[LayerInfo]) -> list[LayerInfo]:
    layer_safe_name = _get_safe_name(layer.name)
    absolute_path = current_dir.joinpath(layer_safe_name)
    is_group = layer.is_group()
    if not is_group:
        absolute_path = absolute_path.with_suffix('.png')

    if is_group:
        absolute_path.mkdir(parents=True, exist_ok=True)
        for child in layer:
            for child_found in search_all_layers(child, absolute_path, founds):
                yield child_found
    else:
        for found in founds:
            yield found 
        yield LayerInfo(absolute_path=absolute_path, layer=layer)
    return founds

def save_layer(image_size: tuple[int, int], layer_info: LayerInfo) -> None:
    with Image.new('RGBA', image_size, (0, 0, 0, 0)) as img:
        img_pil = layer_info['layer'].topil()
        if img_pil is not None:
            with img_pil:
                img.paste(img_pil, layer_info['layer'].offset)  # type: ignore
                img.save(layer_info['absolute_path'])


if __name__ == '__main__':
    multiprocessing.freeze_support()
    psd2pngs()
