import xarray as xr
from pathlib import Path
from tsdat import PipelineConfig, assert_close


def test_power_example_pipeline():
    config_path = Path("pipelines/power_example/config/pipeline.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/power_example/test/data/input/2020224_181521_PowRaw.csv"
    expected_file = (
        "pipelines/power_example/test/data/expected/mhkit.power_example.a1.20200224.181521.nc"
    )

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)
