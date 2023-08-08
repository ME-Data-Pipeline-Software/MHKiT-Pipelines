from typing import Dict, Union
from pydantic import BaseModel, Extra
import pandas as pd
import xarray as xr
from tsdat import DataReader
from mhkit import wave


class WECSimReader(DataReader):
    """---------------------------------------------------------------------------------
    Custom DataReader that can be used to read data from a specific format.

    Built-in implementations of data readers can be found in the
    [tsdat.io.readers](https://tsdat.readthedocs.io/en/latest/autoapi/tsdat/io/readers)
    module.

    ---------------------------------------------------------------------------------"""

    def read(self, input_key: str) -> Union[xr.Dataset, Dict[str, xr.Dataset]]:
        # Load data using the `wecsim.read_output` function which returns a dictionary of dataFrames
        wecsim_data = wave.io.wecsim.read_output(input_key)
        ds = xr.Dataset()
        for ky in wecsim_data.keys():
            if isinstance(wecsim_data[ky], pd.DataFrame):
                ds_temp = wecsim_data[ky].to_xarray()
                for var in ds_temp.data_vars:
                    ds[ky+'_'+var] = ds_temp[var].rename(ky+'_'+var)
            elif isinstance(wecsim_data[ky], dict):
                for nm in wecsim_data[ky].keys():
                    ds_temp = wecsim_data[ky][nm].to_xarray()
                    for var in ds_temp.data_vars:
                        ds[nm+'_'+var] = ds_temp[var].rename(nm+'_'+var)

        return ds
