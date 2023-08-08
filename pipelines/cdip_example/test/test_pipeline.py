import numpy as np
import xarray as xr
from pathlib import Path
from tsdat import PipelineConfig, assert_close


# CDIP "historic" data - "realtime" changes every year
def test_cdip_pipeline_hist():
    config_path = Path("pipelines/cdip_example/config/pipeline_historic.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "036"
    expected_file = "pipelines/cdip_example/test/data/expected/cdip.036.c1.20200210.180000.nc"

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore

    assert_close(dataset, expected, check_attrs=False)
