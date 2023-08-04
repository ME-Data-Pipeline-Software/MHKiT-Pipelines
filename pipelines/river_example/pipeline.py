import xarray as xr
import matplotlib.pyplot as plt
from tsdat import IngestPipeline, get_filename
from mhkit import river


class RiverExample(IngestPipeline):
    """---------------------------------------------------------------------------------
    This is an example ingestion pipeline meant to demonstrate how one might set up a
    pipeline using this template repository.

    ---------------------------------------------------------------------------------"""

    def hook_customize_dataset(self, dataset: xr.Dataset) -> xr.Dataset:
        # (Optional) Use this hook to modify the dataset before qc is applied
        Q = dataset['discharge'].to_pandas()
        dataset['exceed_prob'].values = river.resource.exceedance_probability(Q).squeeze()

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
            # Plot discharge timeseries
            fig, ax = plt.subplots(figsize=(10,6))
            river.graphics.plot_discharge_timeseries(dataset['discharge'].to_pandas(),
                                                     ax=ax)

            plot_file = get_filename(dataset, title="discharge", extension="png")
            fig.savefig(tmp_dir / plot_file)
            plt.close(fig)

            # Plot exceedance probability
            fig, ax = plt.subplots(figsize=(10,6))
            river.graphics.plot_flow_duration_curve(dataset['discharge'].to_pandas(), 
                                                    dataset['exceed_prob'].to_pandas(),
                                                    ax=ax)

            plot_file = get_filename(dataset, title="exceedance", extension="png")
            fig.savefig(tmp_dir / plot_file)
            plt.close(fig)
