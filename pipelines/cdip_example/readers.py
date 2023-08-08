from typing import Dict, Union
from pydantic import BaseModel, Extra
import numpy as np
import xarray as xr
import requests
from tsdat import DataReader
from mhkit import wave


class CDIPWaveRequest(DataReader):
    """---------------------------------------------------------------------------------
    Custom DataReader that pulls netcdf data from CDIP archives

    Built-in implementations of data readers can be found in the
    [tsdat.io.readers](https://tsdat.readthedocs.io/en/latest/autoapi/tsdat/io/readers)
    module.

    Realtime URL:
    https://thredds.cdip.ucsd.edu/thredds/fileServer/cdip/realtime/036p1_rt.nc

    Historic URL:
    https://thredds.cdip.ucsd.edu/thredds/fileServer/cdip/archive/036p1/036p1_historic.nc
    
    ---------------------------------------------------------------------------------"""

    class Parameters(BaseModel, extra=Extra.forbid):
        """Extra parameters that can be set via the retrieval configuration file."""

        data_type: str = "historic"
        start_date: str = "2020-02-01"
        end_date: str = "2020-05-01"

    parameters: Parameters = Parameters()

    def read(self, input_key: str) -> Union[xr.Dataset, Dict[str, xr.Dataset]]:
        # Get station number and data storage type
        station_number = input_key
        data_type = self.parameters.data_type

        if data_type == "historic":
            cdip_archive = "https://thredds.cdip.ucsd.edu/thredds/fileServer/cdip/archive"
            data_url = (
                f"{cdip_archive}/{station_number}p1/{station_number}p1_historic.nc"
            )
        elif data_type == "realtime":
            cdip_realtime = (
                "https://thredds.cdip.ucsd.edu/thredds/fileServer/cdip/realtime"
            )
            data_url = f"{cdip_realtime}/{station_number}p1_rt.nc"

        # Create filename to download file into
        fname = f"cdip.{station_number}.{data_type}.nc"

        print(f"Downloading file {data_url}...")
        r = requests.get(data_url)
        open(fname, "wb").write(r.content)

        print(f"Download complete.")
        ds = xr.open_dataset(fname)
        ds.attrs["cdip_title"] = ds.attrs["title"]  # reset in pipeline hook
        ds.attrs["fname"] = fname  # removed in pipeline hook

        # Select time
        start = self.parameters.start_date
        end = self.parameters.end_date
        
        if start or end:
            if start and end:
                time_slc = slice(np.datetime64(start), np.datetime64(end))
            elif start:
                time_slc = slice(np.datetime64(start), None)
            elif end: 
                time_slc = slice(None, np.datetime64(end))

            time_vars = [v for v in ds.coords if "time" in v.lower()]  # type: ignore
            for t in time_vars:
                ds = ds.sel({t: time_slc})

        return ds
