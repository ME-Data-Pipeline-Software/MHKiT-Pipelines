
import xarray as xr
import matplotlib.pyplot as plt
from tsdat import IngestPipeline, get_filename
from mhkit import power


class PowerExample(IngestPipeline):
    """---------------------------------------------------------------------------------
    This is an example ingestion pipeline meant to demonstrate how one might set up a
    pipeline using this template repository.

    ---------------------------------------------------------------------------------"""

    def hook_customize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        # (Optional) Use this hook to modify the dataset before qc is applied

        voltage = dataset[['a_voltage','b_voltage','c_voltage']].to_pandas()
        current = dataset[['a_current','b_current','c_current']].to_pandas()
        dataset['ac_power'].values = power.characteristics.ac_power_three_phase(voltage, current, float(dataset.power_factor)).squeeze()
        
        dataset['a_inst_freq'].values[1:] = power.characteristics.instantaneous_frequency(voltage)['a_voltage']
        dataset['b_inst_freq'].values[1:] = power.characteristics.instantaneous_frequency(voltage)['b_voltage']
        dataset['c_inst_freq'].values[1:] = power.characteristics.instantaneous_frequency(voltage)['c_voltage']

        return dataset

    def hook_finalize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        # (Optional) Use this hook to modify the dataset after qc is applied
        # but before it gets saved to the storage area
        return dataset

    def hook_plot_dataset(self, dataset: xr.Dataset):
        # (Optional, recommended) Create plots.
        current = dataset[['a_current','b_current','c_current']].to_pandas()
        harmonics = power.quality.harmonics(current, int(dataset.sample_freq), int(dataset.grid_freq))


        plt.style.use("default")  # clear any styles that were set before
        plt.style.use("shared/styling.mplstyle")
        datastream: str = self.dataset_config.attrs.datastream
        with self.storage.uploadable_dir(datastream) as tmp_dir:
            ## Plot AC Power
            fig, ax = plt.subplots(figsize=(15,5))
            ax.plot(dataset.time, dataset['ac_power'])
            ax.set(ylabel='Power [W]', xlabel='Time (UTC)')
            
            plot_file = get_filename(dataset, title="ac_power", extension="png")
            fig.savefig(tmp_dir / plot_file)
            plt.close(fig)

            ## Plot instantaneous frequency
            fig, ax = plt.subplots(figsize=(15,5))
            ax.plot(dataset.time, dataset['a_inst_freq'], label='A')
            ax.plot(dataset.time, dataset['b_inst_freq'], label='B')
            ax.plot(dataset.time, dataset['c_inst_freq'], label='C')
            ax.set(ylabel='Frequency [Hz]', xlabel='Time (UTC)', ylim=(0,120))
            
            plot_file = get_filename(dataset, title="inst_frequency", extension="png")
            fig.savefig(tmp_dir / plot_file)
            plt.close(fig)


            ## Plot current harmonics
            fig, ax = plt.subplots(figsize=(15,5))
            ax.plot(harmonics.index, harmonics['a_current'], label='A')
            ax.plot(harmonics.index, harmonics['b_current'], label='B')
            ax.plot(harmonics.index, harmonics['c_current'], label='C')
            ax.set(ylabel='Harmonic Amplitude', xlabel='Frequency [Hz]', xlim=(0,900))
            ax.legend()

            plot_file = get_filename(dataset, title="harmonics", extension="png")
            fig.savefig(tmp_dir / plot_file)
            plt.close(fig)
