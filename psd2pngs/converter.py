from typing import Optional
from psd_tools import PSDImage
from pathlib import Path
import click
from tqdm import tqdm
import concurrent.futures
from logging import StreamHandler, getLogger, DEBUG
import numpy as np
import multiprocessing
from psd2pngs.version import __version__
from psd2pngs.layers import save_some_layers, search_all_layers, save_layer


CONTEXT_SETTINGS = dict(help_option_names=['-?', '-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__, '-v', '--version', prog_name='psd2pngs')
@click.argument('psd_path', type=click.Path(exists=True))
@click.option('--out-dir-path', '-o', type=click.Path(exists=True), default=None,
              help='Output directory path. If not specified, output to the same directory as the PSD file.')
@click.option('--single-process', '-s', is_flag=True,
              help='Force not to use multiprocessing.')
@click.option('--tasks-count', '-t', type=int, default=multiprocessing.cpu_count(),
              help=f'Number of tasks. Recommended to be less than or equal to the number of CPUs ({multiprocessing.cpu_count()}) because the process maximizes the use of CPUs.')
def psd2pngs(psd_path: str, out_dir_path: Optional[str] = None, single_process: bool = False, tasks_count=multiprocessing.cpu_count()):
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
    logger.addHandler(StreamHandler())
    logger.setLevel(DEBUG)

    # validate values
    if tasks_count > multiprocessing.cpu_count():
        logger.warning('--tasks-count is larger than the number of CPUs.')

    # search all layers
    logger.info('Searching all layers...')
    all_layers = list(tqdm(search_all_layers(
        psd, out_dir_path_), unit=' layer(s)'))

    # save layers
    logger.info('Saving layers...')

    if not single_process:
        logger.info('Using multiprocessing...')
        with concurrent.futures.ProcessPoolExecutor() as executor:
            tasks = []
            n_layers = len(all_layers)
            n_layers_per_task = np.ceil(n_layers / tasks_count).astype(int)
            for i in range(tasks_count):
                indcies = range(
                    i * n_layers_per_task,
                    np.min([(i + 1) * n_layers_per_task, n_layers]),
                )
                tasks.append(executor.submit(save_some_layers,
                             psd_path_, out_dir_path_, indcies))
            [future.result() for future in tqdm(
                concurrent.futures.as_completed(tasks), total=len(tasks), unit='process(es)')]
    else:
        logger.info('Using single process...')
        pbar = tqdm(all_layers, unit='file(s)')
        for layer_info in pbar:
            save_layer(psd.size, layer_info)
    
    if __name__ == '__main__':
        psd2pngs()
