import xarray as xr
import matplotlib.pyplot as plt
from tsdat import IngestPipeline, get_filename
from mhkit import wave


class WECSimExample(IngestPipeline):
    """---------------------------------------------------------------------------------
    This is an example ingestion pipeline meant to demonstrate how one might set up a
    pipeline using this template repository.

    ---------------------------------------------------------------------------------"""

    def hook_customize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        # (Optional) Use this hook to modify the dataset before qc is applied
        
        dataset['pto_generated_power_heave'].values = (-1*dataset['pto_internal_power_heave']/1000).values
        return dataset

    def hook_finalize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        # (Optional) Use this hook to modify the dataset after qc is applied
        # but before it gets saved to the storage area
        return dataset

    def hook_plot_dataset(self, dataset: xr.Dataset):
        # (Optional, recommended) Create plots.
        plt.style.use("default")  # clear any styles that were set before
        plt.style.use("shared/styling.mplstyle")
        datastream: str = self.dataset_config.attrs.datastream
        with self.storage.uploadable_dir(datastream) as tmp_dir:

            fig, ax = plt.subplots(figsize=(10,6))
            dataset["water_level"].plot(ax=ax, x="time")  # type: ignore
            plot_file = get_filename(dataset, title="water_level", extension="png")
            fig.savefig(tmp_dir / plot_file)
            plt.close(fig)

            fig, ax = plt.subplots(figsize=(10,6))
            ax.plot(dataset.time, dataset['body1_surge'], label='surge')
            ax.plot(dataset.time, dataset['body1_sway'], label='sway')
            ax.plot(dataset.time, dataset['body1_heave'], label='heave')
            ax.plot(dataset.time, dataset['body1_pitch'], label='pitch')
            ax.plot(dataset.time, dataset['body1_roll'], label='roll')
            ax.plot(dataset.time, dataset['body1_yaw'], label='yaw')
            ax.legend()
            plot_file = get_filename(dataset, title="body1", extension="png")
            fig.savefig(tmp_dir / plot_file)
            plt.close(fig)

            fig, ax = plt.subplots(figsize=(10,6))
            ax.plot(dataset.time, dataset['body2_surge'], label='surge')
            ax.plot(dataset.time, dataset['body2_sway'], label='sway')
            ax.plot(dataset.time, dataset['body2_heave'], label='heave')
            ax.plot(dataset.time, dataset['body2_pitch'], label='pitch')
            ax.plot(dataset.time, dataset['body2_roll'], label='roll')
            ax.plot(dataset.time, dataset['body2_yaw'], label='yaw')
            ax.legend()
            plot_file = get_filename(dataset, title="body2", extension="png")
            fig.savefig(tmp_dir / plot_file)
            plt.close(fig)

            fig, ax = plt.subplots(figsize=(10,6))
            dataset["pto_generated_power_heave"].plot(ax=ax, x="time")  # type: ignore
            plot_file = get_filename(dataset, title="PTO_power", extension="png")
            fig.savefig(tmp_dir / plot_file)
            plt.close(fig)


            # Use the MHKiT Wave Module to calculate the wave spectrum from the WEC-Sim Wave Class Data
            sample_rate=60
            nnft=1000        # Number of bins in the Fast Fourier Transform
            ws_spectrum = wave.resource.elevation_spectrum(dataset['water_level'].to_dataframe(), sample_rate, nnft)

            # Plot calculated wave spectrum
            fig, ax = plt.subplots(figsize=(10,6))
            wave.graphics.plot_spectrum(ws_spectrum, ax=ax)
            ax.set_xlim([0, 4])
            plot_file = get_filename(dataset, title="wave_spectrum", extension="png")
            fig.savefig(tmp_dir / plot_file)
            plt.close(fig)
