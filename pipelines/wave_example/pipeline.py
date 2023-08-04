import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from tsdat import IngestPipeline, get_filename
from mhkit import wave


class WaveExample(IngestPipeline):
    """---------------------------------------------------------------------------------
    This is an example ingestion pipeline meant to demonstrate how one might set up a
    pipeline using this template repository.

    ---------------------------------------------------------------------------------"""

    def hook_customize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        # (Optional) Use this hook to modify the dataset before qc is applied
        spectra = dataset['wave_energy_density'].to_pandas().transpose()
        power = dataset['device_power'].to_pandas()

        dataset['wave_hs'].values = wave.resource.significant_wave_height(spectra).squeeze()
        dataset['wave_te'].values = wave.resource.energy_period(spectra).squeeze()
        dataset['wave_ta'].values = wave.resource.average_wave_period(spectra).squeeze()
        dataset['wave_tp'].values = wave.resource.peak_period(spectra).squeeze()
        dataset['wave_tz'].values = wave.resource.average_zero_crossing_period(spectra).squeeze()
        
        J = wave.resource.energy_flux(spectra, h=dataset.attrs['water_depth'], deep=False, rho=1030, g=9.81, ratio=2)
        dataset['wave_energy_flux'].values = J.values.squeeze()

        L = wave.performance.capture_length(power, J['J'])
        dataset['device_capture_length'].values = L

        dataset['device_maep'] = wave.performance.mean_annual_energy_production_timeseries(L, J['J'])

        return dataset

    def hook_finalize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        # (Optional) Use this hook to modify the dataset after qc is applied
        # but before it gets saved to the storage area

        return dataset

    def hook_plot_dataset(self, dataset: xr.Dataset):
        # Create matrices and plot
        Hm0 = dataset['wave_hs'].values
        Te = dataset['wave_te'].values 
        L = dataset['device_capture_length'].values
        J = dataset['wave_energy_flux'].values

        # Generate bins for Hm0 and Te, input format (start, stop, step_size)
        Hm0_bins = np.arange(0, dataset['wave_hs'].max() + .5, .5)    
        Te_bins = np.arange(0, dataset['wave_te'].max() + 1, 1)

        #Mean capture length matrix
        LM_mean = wave.performance.capture_length_matrix(Hm0, Te, L, 'mean', Hm0_bins, Te_bins)
        # Create wave energy flux matrix using mean
        JM = wave.performance.wave_energy_flux_matrix(Hm0, Te, J, 'mean', Hm0_bins, Te_bins)
        # Create power matrix using mean
        PM_mean = wave.performance.power_matrix(LM_mean, JM)


        plt.style.use("default")  # clear any styles that were set before
        plt.style.use("shared/styling.mplstyle")

        datastream: str = self.dataset_config.attrs.datastream
        with self.storage.uploadable_dir(datastream) as tmp_dir:

            fig, ax = plt.subplots(figsize=(10,7))
            wave.graphics.plot_matrix(LM_mean, xlabel='Energy Period [s]', ylabel='Sig Wave Height [m]', \
              zlabel='Capture Length [m]', show_values=False, ax=ax)
            plot_file = get_filename(dataset, title="capture_length_matrix", extension="png")
            fig.savefig(tmp_dir / plot_file)
            plt.close(fig)

            fig, ax = plt.subplots(figsize=(10,7))
            wave.graphics.plot_matrix(PM_mean, xlabel='Energy Period [s]', ylabel='Sig Wave Height [m]', \
              zlabel='Mean Device Power [W]', show_values=False, ax=ax)
            plot_file = get_filename(dataset, title="power_matrix", extension="png")
            fig.savefig(tmp_dir / plot_file)
            plt.close(fig)

            fig, ax = plt.subplots(figsize=(10,7))
            wave.graphics.plot_matrix(JM, xlabel='Energy Period [s]', ylabel='Sig Wave Height [m]', \
              zlabel='Mean Resource Power [W]', show_values=False, ax=ax)
            plot_file = get_filename(dataset, title="wave_energy_matrix", extension="png")
            fig.savefig(tmp_dir / plot_file)
            plt.close(fig)
