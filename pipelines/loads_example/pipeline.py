import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from tsdat import IngestPipeline, get_filename
from mhkit import loads, utils


class LoadsExample(IngestPipeline):
    """---------------------------------------------------------------------------------
    This is an example ingestion pipeline meant to demonstrate how one might set up a
    pipeline using this template repository.

    ---------------------------------------------------------------------------------"""

    def hook_customize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        # (Optional) Use this hook to modify the dataset before qc is applied

        # Calculate the damage equivalent load for blade root moments and tower base moments
        n_bin = 100
        dl = 600
        for var in [v for v in dataset.data_vars if 'TB' in v]:  # type: ignore
            DEL_tower = loads.general.damage_equivalent_load(dataset['TB_ForeAft'], m=4, bin_num=n_bin,data_length=dl)
            dataset[var].attrs['damage_equivalent_load'] = DEL_tower
        for var in [v for v in dataset.data_vars if 'BL' in v]:  # type: ignore
            DEL_blade = loads.general.damage_equivalent_load(dataset['BL1_FlapMom'], m=10, bin_num=n_bin,data_length=dl)
            dataset[var].attrs['damage_equivalent_load'] = DEL_blade
        
        return dataset

    def hook_finalize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        # (Optional) Use this hook to modify the dataset after qc is applied
        # but before it gets saved to the storage area
        return dataset

    def hook_plot_dataset(self, dataset: xr.Dataset):
        # (Optional, recommended) Create plots.

        # Calculate the means, maxs, mins, and stdevs for all data signals in the loads data file
        df = dataset[['uWind_80m', 'TB_ForeAft', 'BL1_FlapMom']].to_pandas()
        means,maxs,mins,std = utils.get_statistics(df, freq=50, period=600)

        plt.style.use("default")  # clear any styles that were set before
        plt.style.use("shared/styling.mplstyle")
        datastream: str = self.dataset_config.attrs.datastream
        with self.storage.uploadable_dir(datastream) as tmp_dir:

            plot_file = get_filename(dataset, title="blade_root", extension="png")
            loads.graphics.plot_statistics(means['uWind_80m'],
                                means['BL1_FlapMom'],
                                maxs['BL1_FlapMom'],
                                mins['BL1_FlapMom'],
                                y_stdev=std['BL1_FlapMom'],
                                xlabel='Wind Speed [m/s]',
                                ylabel='Blade Flap Moment [kNm]',
                                title = 'Blade Flap Moment Load Statistics', 
                                save_path = str(tmp_dir / plot_file))
            
            plot_file = get_filename(dataset, title="tower_base", extension="png")
            loads.graphics.plot_statistics(means['uWind_80m'],
                                means['TB_ForeAft'],
                                maxs['TB_ForeAft'],
                                mins['TB_ForeAft'],
                                y_stdev=std['TB_ForeAft'],
                                xlabel='Wind Speed [m/s]',
                                ylabel='Tower Base Moment [kNm]',
                                title = 'Tower Base Moment Load Statistics',
                                save_path = str(tmp_dir / plot_file))

        ## Create array containing wind speeds to use as bin edges
        # bin_edges = np.arange(3,26,1)
        # bin_against = means['uWind_80m']

        # # Apply function for means, maxs, and mins 
        # [bin_means, bin_means_std] = loads.general.bin_statistics(means,bin_against,bin_edges)
        # [bin_maxs, bin_maxs_std] = loads.general.bin_statistics(maxs,bin_against,bin_edges)
        # [bin_mins, bin_mins_std] = loads.general.bin_statistics(mins,bin_against,bin_edges)

        ## Specify center of each wind speed bin, and signal name for analysis
        # bin_centers = np.arange(3.5,25.5,step=1) 
        # signal_name = 'TB_ForeAft'          

        # # Specify inputs to be used in plotting
        # bin_mean = bin_means[signal_name]
        # bin_max = bin_maxs[signal_name]
        # bin_min = bin_mins[signal_name]
        # bin_mean_std = bin_means_std[signal_name]
        # bin_max_std = bin_maxs_std[signal_name]
        # bin_min_std = bin_mins_std[signal_name]

        # # Plot binned statistics
        # plot_file = get_filename(dataset, title="binned_stats", extension="png")
        # loads.graphics.plot_bin_statistics(bin_centers,bin_mean,bin_max,bin_min,
        #                         bin_mean_std,bin_max_std,bin_min_std,
        #                         xlabel='Wind Speed [m/s]',
        #                         ylabel=signal_name,
        #                         title='Binned Statistics',
        #                         save_path = str(tmp_dir / plot_file))