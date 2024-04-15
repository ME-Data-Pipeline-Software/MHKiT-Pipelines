import xarray as xr
import matplotlib.pyplot as plt
from tsdat import IngestPipeline, FileSystem

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
    
        with plt.style.context("shared/styling.mplstyle"):
            # Velocity plot
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(ds.time, ds["vel"][0], label='Streamwise')
            ax.plot(ds.time, ds["vel"][1], label='Cross-stream')
            ax.plot(ds.time, ds["vel"][2], label='Vertical')
            ax.set(xlabel="Time (UTC)", ylabel="Velocity [m/s]", ylim=(-2, 2))

            plot_file = self.get_ancillary_filepath("velocity")
            fig.savefig(plot_file)
            plt.close(fig)

            # Beam correlation plot
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(ds.time, ds["corr"][0], label='Beam 1')
            ax.plot(ds.time, ds["corr"][1], label='Beam 2')
            ax.plot(ds.time, ds["corr"][2], label='Beam 3')
            ax.set(xlabel="Time (UTC)", ylabel="Correlation")

            plot_file = self.get_ancillary_filepath("correlation")
            fig.savefig(plot_file)
            plt.close(fig)

            # Beam amplitude plot
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(ds.time, ds["amp"][0], label='Beam 1')
            ax.plot(ds.time, ds["amp"][1], label='Beam 2')
            ax.plot(ds.time, ds["amp"][2], label='Beam 3')
            ax.set(xlabel="Time (UTC)", ylabel="Amplitude [dB]")

            plot_file = self.get_ancillary_filepath("amplitude")
            fig.savefig(plot_file)
            plt.close(fig)
