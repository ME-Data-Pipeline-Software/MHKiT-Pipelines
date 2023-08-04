from typing import Dict, Union
from pydantic import BaseModel, Extra
import xarray as xr
from tsdat import DataReader
from mhkit import river


class USGSjsonReader(DataReader):
    """---------------------------------------------------------------------------------
    Custom DataReader that can be used to read data from a specific format.

    Built-in implementations of data readers can be found in the
    [tsdat.io.readers](https://tsdat.readthedocs.io/en/latest/autoapi/tsdat/io/readers)
    module.

    ---------------------------------------------------------------------------------"""

    def read(self, input_key: str) -> Union[xr.Dataset, Dict[str, xr.Dataset]]:
        # Read USGS json file
        data = river.io.usgs.read_usgs_file(input_key)

        # Set index name to time
        data.index.name = 'time'
        # Convert pandas to xarray dataset
        ds = data.to_xarray()

        return ds
    

class USGSWaterServicesRequest(DataReader):
    """---------------------------------------------------------------------------------
    Custom DataReader that can be used to read data from a specific format.

    Built-in implementations of data readers can be found in the
    [tsdat.io.readers](https://tsdat.readthedocs.io/en/latest/autoapi/tsdat/io/readers)
    module.

    ---------------------------------------------------------------------------------"""

    class Parameters(BaseModel, extra=Extra.forbid):
        parameter: str = '00060'  # Discharge
        start_date: str = '2018-01-01'
        end_date: str = '2018-12-31'
        data_type: str = 'Daily'
        proxy: str = ''

    parameters: Parameters = Parameters()

    def read(self, input_key: str) -> Union[xr.Dataset, Dict[str, xr.Dataset]]:
        # Request USGS river data
        data = river.io.usgs.request_usgs_data(
            station=input_key,
            parameter=self.parameters.parameter,
            start_date=self.parameters.start_date, 
            end_date=self.parameters.end_date,
            data_type=self.parameters.data_type,
            proxy=self.parameters.proxy)
        
        # Set index name to time
        data.index.name = 'time'
        # Convert pandas to xarray dataset
        ds = data.to_xarray()

        return ds