import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from tsdat import IngestPipeline

from mhkit import tidal


class TidalExample(IngestPipeline):
    """---------------------------------------------------------------------------------
    This is an example ingestion pipeline meant to demonstrate how one might set up a
    pipeline using this template repository.

    ---------------------------------------------------------------------------------"""

    def hook_customize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        # (Optional) Use this hook to modify the dataset before qc is applied

        width_direction = 1
        s = dataset['water_speed'].to_pandas()
        d = dataset['water_direction'].to_pandas()

        # Compute two principal flow directions
        directions = tidal.resource.principal_flow_directions(d, width_direction)
        dataset.attrs['principal_directions'] = list(directions)

        # Calculate exceedance probability of data
        dataset['exceed_prob'].values = tidal.resource.exceedance_probability(s).squeeze().astype('float32')

        return dataset

    def hook_finalize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        # (Optional) Use this hook to modify the dataset after qc is applied
        # but before it gets saved to the storage area
        return dataset

    def hook_plot_dataset(self, dataset: xr.Dataset):
        # (Optional, recommended) Create plots.

        with plt.style.context("shared/styling.mplstyle"):

            fig, ax = plt.subplots(2,1, figsize=(10,10))
            # Plot entire dataset
            tidal.graphics.plot_current_timeseries(
                dataset['water_direction'].to_pandas(), 
                dataset['water_speed'].to_pandas(), 
                dataset.principal_directions[0], 
                ax=ax[0])
            
            # Plot a particular slice of time
            time_slc = slice(np.datetime64('2017-12-01'),
                             np.datetime64('2017-12-31'))
            tidal.graphics.plot_current_timeseries(
                dataset['water_direction'].sel(time=time_slc).to_pandas(), 
                dataset['water_speed'].sel(time=time_slc).to_pandas(), 
                dataset.principal_directions[0], 
                ax=ax[1])
            plot_file = self.get_ancillary_filepath("flow_speed")
            fig.savefig(plot_file)
            plt.close(fig)


            ## Plot the joint probability distributions
            # Set the joint probability bin widths
            width_direction = 1   # in degrees
            width_velocity  = 0.1 # in m/s

            fig, ax = plt.subplots(figsize=(10,7), subplot_kw={'projection': 'polar'})
            ax = tidal.graphics.plot_joint_probability_distribution(
                dataset['water_direction'].to_pandas(), 
                dataset['water_speed'].to_pandas(),
                width_direction, 
                width_velocity, 
                flood=dataset.principal_directions[0], 
                ebb=dataset.principal_directions[1],
                ax=ax)
            plot_file = self.get_ancillary_filepath("prob_distribution")
            fig.savefig(plot_file)
            plt.close(fig)


            ## Plot roses
            # Define bin sizes
            width_direction = 10   # in degrees
            width_velocity  = 0.25 # in m/s

            fig, ax = plt.subplots(figsize=(10,7), subplot_kw={'projection': 'polar'})
            tidal.graphics.plot_rose(
                dataset['water_direction'].to_pandas(), 
                dataset['water_speed'].to_pandas(),
                width_direction, 
                width_velocity, 
                flood=dataset.principal_directions[0], 
                ebb=dataset.principal_directions[1],
                ax=ax)
            plot_file = self.get_ancillary_filepath("rose")
            fig.savefig(plot_file)
            plt.close(fig)

            ## Plot exceedance probability Curve
            fig, ax = plt.subplots(figsize=(10,7))
            tidal.graphics.plot_velocity_duration_curve(
                dataset['water_speed'].to_pandas(), 
                dataset['exceed_prob'].to_pandas(), 
                ax=ax)
            plot_file = self.get_ancillary_filepath("exceedance")
            fig.savefig(plot_file)
            plt.close(fig)

            ## Plot phase probability bar chart
            fig, ax = plt.subplots(figsize=(10,7))
            tidal.graphics.tidal_phase_probability(
                dataset['water_direction'].to_pandas(),
                dataset['water_speed'].to_pandas(),
                flood=dataset.principal_directions[0], 
                ebb=dataset.principal_directions[1],
                ax=ax)
            plot_file = self.get_ancillary_filepath("phase_prob")
            fig.savefig(plot_file)
            plt.close(fig)

            ## Plot phase exceedance
            fig, ax = plt.subplots(figsize=(10,7))
            tidal.graphics.tidal_phase_exceedance(
                dataset['water_direction'].to_pandas(),
                dataset['water_speed'].to_pandas(),
                flood=dataset.principal_directions[0], 
                ebb=dataset.principal_directions[1],
                ax=ax)
            plot_file = self.get_ancillary_filepath("phase_exceedance")
            fig.savefig(plot_file)
            plt.close(fig)
