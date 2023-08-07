import xarray as xr
from pathlib import Path
from tsdat import PipelineConfig, assert_close


def test_loads_example_pipeline():
    config_path = Path("pipelines/loads_example/config/pipeline.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/loads_example/test/data/input/data_loads_example.csv"
    expected_file = (
        "pipelines/loads_example/test/data/expected/mhkit.loads_example.a1.20170301.012840.nc"
    )

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)
