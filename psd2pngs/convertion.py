from typing import Optional, Union
from psd_tools import PSDImage
from pathlib import Path
from tqdm import tqdm
import concurrent.futures
from logging import StreamHandler, getLogger, DEBUG
import numpy as np
import multiprocessing
from psd2pngs.layer_save import save_some_layers, search_all_layers, save_layer
from psd2pngs.layer_info import get_layer_info
import json
import humps

from psd2pngs.unpack import unpack_nested_namedtuple


def convert(
    psd_path: Union[str, Path],
    out_dir_path: Optional[Union[str, Path]] = None,
    single_process: bool = False,
    n_tasks: int = multiprocessing.cpu_count(),
    use_json: bool = False,
    use_json_camel_case: bool = False,
    json_only: bool = False,
):
    """Convert a PSD file to multiple PNG files.
    When multiprocessing, since pickling Layers are very slow, each process will open the PSD file separately.

    Parameters
    ----------
    psd_path : str
        Path to the PSD file.
    out_dir_path : Optional[str], optional
        Output directory, by default None
    single_process : bool, optional
        Do not use multiprocessing, by default False
    n_tasks : _type_, optional
        Number of tasks when multiprocessing is used, by default multiprocessing.cpu_count() (Number of CPU Threads)
    use_json : bool, optional
        Whether to output a json file (snake_case), by default False
    use_json_camel_case : bool, optional
        Whether to output a json file (camelCase), by default False
    json_only : bool, optional
        Only generates a json file and do not convert the file, by default False

    Raises
    ------
    ValueError
        Raises if the suffix of the PSD file is not ".psd".
    ValueError
        Raises if use_json and use_json_camel_case are both True.
    ValueError
        Raises if use_json and use_json_camel_case are both False but json_only is True.
    """
    # Check paths
    psd_path_ = Path(psd_path).absolute()
    out_dir_path_ = psd_path_.parent
    if out_dir_path is not None:
        out_dir_path_ = Path(out_dir_path).absolute()
    if psd_path_.suffix != ".psd":
        raise ValueError("The suffix of psd_path must be .psd")

    # Check json options
    if use_json and use_json_camel_case:
        raise ValueError("Cannot use both --json and --json-camel-case.")
    if json_only and not (use_json or use_json_camel_case):
        raise ValueError("Cannot use --json-only without --json or --json-camel-case.")

    # Open the PSD file
    psd = PSDImage.open(psd_path_)

    # Create output directory
    out_dir_path_ = out_dir_path_.joinpath(psd_path_.stem)
    out_dir_path_.mkdir(parents=True, exist_ok=True)

    # Get and configure logger
    logger = getLogger(__name__)
    logger.addHandler(StreamHandler())
    logger.setLevel(DEBUG)

    # validate values
    if n_tasks > multiprocessing.cpu_count():
        logger.warning("--tasks-count is larger than the number of CPUs.")

    # search all layers
    logger.info("Searching all layers...")
    all_layers = list(
        tqdm(search_all_layers(psd, out_dir_path_), unit=" layer(s) found")
    )

    # save json files
    if use_json or use_json_camel_case:
        logger.info("Saving JSON file...")
        json_path = out_dir_path_.joinpath(psd_path_.stem + ".json")
        layer_info = unpack_nested_namedtuple(get_layer_info(psd))
        if use_json_camel_case:
            layer_info = humps.camelize(layer_info)  # type: ignore
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(layer_info, f, indent=4, ensure_ascii=False)

    if json_only:
        return

    # save layers
    logger.info("Saving layers...")

    if not single_process:
        # Use multiprocessing
        logger.info("Using multiprocessing...")
        with concurrent.futures.ProcessPoolExecutor() as executor:
            tasks = []

            # Calculate the number of layers that should be processed per task
            n_layers = len(all_layers)
            n_layers_per_task = np.ceil(n_layers / n_tasks).astype(int)

            for i in range(n_tasks):
                # Calculate the indcies of the layers that should be processed in this task
                indcies = range(
                    i * n_layers_per_task,
                    np.min([(i + 1) * n_layers_per_task, n_layers]),
                )

                # Create and append task
                tasks.append(
                    executor.submit(save_some_layers, psd_path_, out_dir_path_, indcies)
                )

            # Wait for all tasks to finish. As soon as one task finishes, tqdm progress bar will update.
            [
                future.result()
                for future in tqdm(
                    concurrent.futures.as_completed(tasks),
                    total=len(tasks),
                    unit=" process(es)",
                )
            ]
    else:
        # Use single process
        logger.info("Using single process...")

        for layer_info in tqdm(all_layers, unit="file(s)"):
            save_layer(psd.size, layer_info)
