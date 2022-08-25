from typing import Optional
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


def convert(
    psd_path: str,
    out_dir_path: Optional[str] = None,
    single_process: bool = False,
    n_tasks=multiprocessing.cpu_count(),
    use_json: bool = False,
    use_json_camel_case: bool = False,
    json_only=False,
):
    psd_path_ = Path(psd_path).absolute()
    out_dir_path_ = psd_path_.parent
    if out_dir_path is not None:
        out_dir_path_ = Path(out_dir_path).absolute()
    if psd_path_.suffix != ".psd":
        raise ValueError("The suffix of psd_path must be .psd")

    if use_json and use_json_camel_case:
        raise ValueError("Cannot use both --json and --json-camel-case.")

    if json_only and not (use_json or use_json_camel_case):
        raise ValueError("Cannot use --json-only without --json or --json-camel-case.")

    psd = PSDImage.open(psd_path_)

    out_dir_path_ = out_dir_path_.joinpath(psd_path_.stem)
    out_dir_path_.mkdir(parents=True, exist_ok=True)

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

    if use_json or use_json_camel_case:
        logger.info("Saving JSON file...")
        json_path = out_dir_path_.joinpath(psd_path_.stem + ".json")
        layer_info = get_layer_info(psd)
        if use_json_camel_case:
            layer_info = humps.camelize(layer_info)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(layer_info, f, indent=4, ensure_ascii=False)

    if json_only:
        return

    # save layers
    logger.info("Saving layers...")

    if not single_process:
        logger.info("Using multiprocessing...")
        with concurrent.futures.ProcessPoolExecutor() as executor:
            tasks = []
            n_layers = len(all_layers)
            n_layers_per_task = np.ceil(n_layers / n_tasks).astype(int)
            for i in range(n_tasks):
                indcies = range(
                    i * n_layers_per_task,
                    np.min([(i + 1) * n_layers_per_task, n_layers]),
                )
                tasks.append(
                    executor.submit(save_some_layers, psd_path_, out_dir_path_, indcies)
                )
            [
                future.result()
                for future in tqdm(
                    concurrent.futures.as_completed(tasks),
                    total=len(tasks),
                    unit=" process(es)",
                )
            ]
    else:
        logger.info("Using single process...")
        pbar = tqdm(all_layers, unit="file(s)")
        for layer_info in pbar:
            save_layer(psd.size, layer_info)
