import os
import csv
import pandas as pd
import xarray as xr
from typing import Dict, Union, Any
from pydantic import BaseModel, Extra
from tsdat import DataReader

from mhkit import wave


class NDBCDataReader(DataReader):
    """---------------------------------------------------------------------------------
    Custom DataReader that can be used to read data from a specific format.

    Built-in implementations of data readers can be found in the
    [tsdat.io.readers](https://tsdat.readthedocs.io/en/latest/autoapi/tsdat/io/readers)
    module.

    ---------------------------------------------------------------------------------"""

    class Parameters(BaseModel, extra=Extra.forbid):

        ndbc_parameter: str = 'swden'
        water_depth_m: float = 60
        requests_proxy: Dict[str, Any] = {}  # {"http": 'http:wwwproxy.yourProxy:80/'}

    parameters: Parameters = Parameters()
    """Extra parameters that can be set via the retrieval configuration file. If you opt
    to not use any configuration parameters then please remove the code above."""

    def read(self, input_key: str) -> Union[xr.Dataset, Dict[str, xr.Dataset]]:

        # HACK to get around mhkit assertion
        pd.read_csv(input_key).to_csv('ndbc_data.txt', 
                                      sep=' ', 
                                      index=False, 
                                      quoting=csv.QUOTE_NONE, 
                                      escapechar=' ')

        #wave.io.ndbc.request_data(self.parameters.ndbc_parameter, input_key, proxy=self.parameters.requests_proxy)
        [raw_ndbc_data, meta] = wave.io.ndbc.read_file('ndbc_data.txt')

        os.remove('ndbc_data.txt')

        ds = xr.Dataset()
        ds['spectra'] = xr.DataArray(raw_ndbc_data.values, 
                                     coords={'time':raw_ndbc_data.index.values,
                                             'frequency':raw_ndbc_data.columns.values})
        ds.attrs['water_depth'] = self.parameters.water_depth_m
        
        return ds
