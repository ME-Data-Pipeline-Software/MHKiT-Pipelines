import xarray as xr
from pathlib import Path
from tsdat import PipelineConfig, assert_close


def test_river_example_pipeline():
    config_path = Path("pipelines/river_example/config/pipeline.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/river_example/test/data/input/USGS_08313000_Jan2019_daily.json"
    expected_file = (
        "pipelines/river_example/test/data/expected/mhkit.river_example.a1.20190101.000000.nc"
    )

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)
