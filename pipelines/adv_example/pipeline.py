import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
from mhkit.dolfyn.adp import api
from tsdat import IngestPipeline, FileSystem, get_filename

from shared.writers import MatlabWriter


class ADVExample(IngestPipeline):
    """---------------------------------------------------------------------------------
    This is an example ingestion pipeline meant to demonstrate how one might set up a
    pipeline using this template repository.

    ---------------------------------------------------------------------------------"""

    def hook_customize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        # (Optional) Use this hook to modify the dataset before qc is applied

        # Speed and Direction
        dataset["U_mag"].values = dataset.velds.U_mag
        dataset["U_dir"].values = dataset.velds.U_dir
        dataset["U_dir"].attrs['units'] = dataset.velds.U_dir.units
        
        return dataset

    def hook_finalize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        # (Optional) Use this hook to modify the dataset after qc is applied
        # but before it gets saved to the storage area

        # Create additional storage handler to save mat file
        storage = FileSystem()
        storage.handler.writer = MatlabWriter()

        storage.save_data(dataset)

        return dataset

    def hook_plot_dataset(self, ds: xr.Dataset):
    
        plt.style.use("default")  # clear any styles that were set before
        plt.style.use("shared/styling.mplstyle")
        
        datastream: str = self.dataset_config.attrs.datastream
        with self.storage.uploadable_dir(datastream) as tmp_dir:
            # Velocity plot
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(ds.time, ds["vel"][0], label='Streamwise')
            ax.plot(ds.time, ds["vel"][1], label='Cross-stream')
            ax.plot(ds.time, ds["vel"][2], label='Vertical')
            ax.set(xlabel="Time (UTC)", ylabel="Velocity [m/s]", ylim=(-2, 2))

            plot_file = get_filename(ds, title="velocity", extension="png")
            fig.savefig(tmp_dir / plot_file)
            plt.close(fig)

            # Beam correlation plot
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(ds.time, ds["corr"][0], label='Beam 1')
            ax.plot(ds.time, ds["corr"][1], label='Beam 2')
            ax.plot(ds.time, ds["corr"][2], label='Beam 3')
            ax.set(xlabel="Time (UTC)", ylabel="Correlation")

            plot_file = get_filename(ds, title="correlation", extension="png")
            fig.savefig(tmp_dir / plot_file)
            plt.close(fig)

            # Beam amplitude plot
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(ds.time, ds["amp"][0], label='Beam 1')
            ax.plot(ds.time, ds["amp"][1], label='Beam 2')
            ax.plot(ds.time, ds["amp"][2], label='Beam 3')
            ax.set(xlabel="Time (UTC)", ylabel="Amplitude [dB]")

            plot_file = get_filename(ds, title="amplitude", extension="png")
            fig.savefig(tmp_dir / plot_file)
            plt.close(fig)
