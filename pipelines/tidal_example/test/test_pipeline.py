import xarray as xr
from pathlib import Path
from tsdat import PipelineConfig, assert_close


def test_tidal_example_pipeline():
    config_path = Path("pipelines/tidal_example/config/pipeline.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/tidal_example/test/data/input/s08010.json"
    expected_file = (
        "pipelines/tidal_example/test/data/expected/mhkit.tidal_example.a1.20161108.120400.nc"
    )

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)
