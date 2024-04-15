import xarray as xr
import matplotlib.pyplot as plt
from tsdat import IngestPipeline

from mhkit import river


class RiverExample(IngestPipeline):
    """---------------------------------------------------------------------------------
    This is an example ingestion pipeline meant to demonstrate how one might set up a
    pipeline using this template repository.

    ---------------------------------------------------------------------------------"""

    def hook_customize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        # (Optional) Use this hook to modify the dataset before qc is applied
        Q = dataset['discharge'].to_pandas()
        dataset['exceed_prob'].values = river.resource.exceedance_probability(Q).squeeze().astype('float32')

        return dataset

    def hook_finalize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        # (Optional) Use this hook to modify the dataset after qc is applied
        # but before it gets saved to the storage area
        return dataset

    def hook_plot_dataset(self, dataset: xr.Dataset):
        # (Optional, recommended) Create plots.

        with plt.style.context("shared/styling.mplstyle"):
            # Plot discharge timeseries
            fig, ax = plt.subplots(figsize=(10,6))
            river.graphics.plot_discharge_timeseries(dataset['discharge'].to_pandas(),
                                                     ax=ax)
            plot_file = self.get_ancillary_filepath("discharge")
            fig.savefig(plot_file)
            plt.close(fig)

            # Plot exceedance probability
            fig, ax = plt.subplots(figsize=(10,6))
            river.graphics.plot_flow_duration_curve(dataset['discharge'].to_pandas(), 
                                                    dataset['exceed_prob'].to_pandas(),
                                                    ax=ax)
            plot_file = self.get_ancillary_filepath("exceedance")
            fig.savefig(plot_file)
            plt.close(fig)
