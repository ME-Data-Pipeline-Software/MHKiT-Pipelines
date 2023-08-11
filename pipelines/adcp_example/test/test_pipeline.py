import xarray as xr
from pathlib import Path
from tsdat import PipelineConfig, assert_close


def test_ADCP_pipeline():
    config_path = Path("pipelines/adcp_example/config/pipeline.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/adcp_example/test/data/input/Sig1000_tidal.ad2cp"
    expected_file = "pipelines/adcp_example/test/data/expected/pnnl.sig1000.b1.20200815.072000.nc"

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)
