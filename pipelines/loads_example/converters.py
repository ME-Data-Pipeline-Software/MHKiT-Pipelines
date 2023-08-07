import xarray as xr
from typing import Any, Optional
from pydantic import BaseModel, Extra
from tsdat import DataConverter, DatasetConfig, RetrievedDataset
from mhkit import utils


class Excel2Datetime(DataConverter):
    """---------------------------------------------------------------------------------
    Custom DataConverter that can be used to preprocess input datasets and convert them
    into a suitable format for downstream processing.

    Built-in examples of DataConverters include the UnitsConverter to convert units
    (e.g., degF -> degC) and the StringToDatetime converter to convert time variables
    encoded as strings into np.datetime64 objects.

    ---------------------------------------------------------------------------------"""

    def convert(
        self,
        data: xr.DataArray,
        variable_name: str,
        dataset_config: DatasetConfig,
        retrieved_dataset: RetrievedDataset,
        **kwargs: Any,
    ) -> Optional[xr.DataArray]:
        """----------------------------------------------------------------------------
        Applies a custom conversion to the retrieved data.

        Args:
            data (xr.DataArray): The DataArray corresponding with the retrieved data
                variable to convert.
            variable_name (str): The name of the variable to convert.
            dataset_config (DatasetConfig): The output dataset configuration.
            retrieved_dataset (RetrievedDataset): The retrieved dataset structure.

        Returns:
            Optional[xr.DataArray]: The converted data as an xr.DataArray, or None if
                the conversion was done in place.

        ----------------------------------------------------------------------------"""
        time = utils.excel_to_datetime(data).values
        data = xr.DataArray(time,
                            name='time',
                            coords={'time':time})
        return data
