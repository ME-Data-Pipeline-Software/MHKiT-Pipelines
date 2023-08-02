import xarray as xr
from pathlib import Path
from tsdat import PipelineConfig, assert_close


def test_wave_module_example_pipeline():
    config_path = Path("pipelines/wave_module_example/config/pipeline.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/wave_module_example/test/data/input/data.zip"
    expected_file = "pipelines/wave_module_example/test/data/expected/mhkit.wave_module_example.a1.20180101.004000.nc"

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)
