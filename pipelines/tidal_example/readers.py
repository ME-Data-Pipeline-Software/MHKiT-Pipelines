from typing import Dict, Union
from pydantic import BaseModel, Extra
import xarray as xr
from tsdat import DataReader

from mhkit import tidal


class NOAAjsonReader(DataReader):
    """---------------------------------------------------------------------------------
    Custom DataReader that can be used to read data from a specific format.

    Built-in implementations of data readers can be found in the
    [tsdat.io.readers](https://tsdat.readthedocs.io/en/latest/autoapi/tsdat/io/readers)
    module.

    ---------------------------------------------------------------------------------"""

    def read(self, input_key: str) -> Union[xr.Dataset, Dict[str, xr.Dataset]]:

        data, metadata = tidal.io.noaa.read_noaa_json(input_key)
        data.index.name = 'time'
        ds = data.to_xarray()
        ds.attrs = metadata

        return ds


class NOAATideCurrentsRequest(DataReader):
    """---------------------------------------------------------------------------------
    Custom DataReader that can be used to read data from a specific format.

    Built-in implementations of data readers can be found in the
    [tsdat.io.readers](https://tsdat.readthedocs.io/en/latest/autoapi/tsdat/io/readers)
    module.

    ---------------------------------------------------------------------------------"""

    class Parameters(BaseModel, extra=Extra.forbid):
        parameter: str = 'currents'
        start_date: str = '20161101'
        end_date: str = '20180401'
        proxy: str = ''

    parameters: Parameters = Parameters()

    def read(self, input_key: str) -> Union[xr.Dataset, Dict[str, xr.Dataset]]:

        data, metadata = tidal.io.noaa.request_noaa_data(
            station=input_key,
            parameter=self.parameters.parameter,
            start_date=self.parameters.start_date, 
            end_date=self.parameters.end_date,
            proxy=self.parameters.proxy)
        
        return data.to_xarray()