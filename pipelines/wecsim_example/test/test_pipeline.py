import xarray as xr
from pathlib import Path
from tsdat import PipelineConfig, assert_close


def test_wecsim_example_pipeline():
    config_path = Path("pipelines/wecsim_example/config/pipeline.yaml")
    config = PipelineConfig.from_yaml(config_path)
    pipeline = config.instantiate_pipeline()

    test_file = "pipelines/wecsim_example/test/data/input/RM3MooringMatrix_matlabWorkspace_structure.mat"
    expected_file = (
        "pipelines/wecsim_example/test/data/expected/mhkit.wecsim_example.a1.19700101.000000.nc"
    )

    dataset = pipeline.run([test_file])
    expected: xr.Dataset = xr.open_dataset(expected_file)  # type: ignore
    assert_close(dataset, expected, check_attrs=False)
