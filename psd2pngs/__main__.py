from psd2pngs.convert import convert
from psd2pngs.version import __version__
import multiprocessing
import click


CONTEXT_SETTINGS = dict(help_option_names=["-?", "-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__, "-v", "--version", prog_name="psd2pngs")
@click.argument("psd_path", type=click.Path(exists=True))
@click.option(
    "--out",
    "-o",
    "out_dir_path",
    type=click.Path(exists=True),
    default=None,
    help="Output directory path. If not specified, output to the same directory as the PSD file.",
)
@click.option(
    "--single-process", "-s", is_flag=True, help="Force not to use multiprocessing."
)
@click.option(
    "--tasks-count",
    "-t",
    "n_tasks",
    type=int,
    default=multiprocessing.cpu_count(),
    help=f"Number of tasks. Recommended to be less than or equal to the number of CPUs ({multiprocessing.cpu_count()}) because the process maximizes the use of CPUs.",
)
@click.option(
    "--json",
    "-j",
    "use_json",
    is_flag=True,
    help="Output JSON file containing layer information in snake case.",
)
@click.option(
    "--json-camel-case",
    "-jc",
    "use_json_camel_case",
    is_flag=True,
    help="Output JSON file containing layer information in camel case.",
)
@click.option(
    "--json-only",
    "-jo",
    "json_only",
    is_flag=True,
    help="Output JSON file only.",
)
def psd2pngs(*args, **kwargs):
    convert(*args, **kwargs)


# this should be called HERE
if __name__ == "__main__":  # for pyinstaller to work
    multiprocessing.freeze_support()
    psd2pngs()
