import xarray as xr
from pathlib import Path
from tsdat import PipelineConfig, assert_close


def test_ADV_pipeline():
    config_path = Path("pipelines/adv_example/config/pipeline.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/adv_example/test/data/input/vector_data01.VEC"
    expected_file = "pipelines/adv_example/test/data/expected/nrel.adv.b1.20120612.190002.nc"

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)
