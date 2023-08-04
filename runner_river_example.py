from utils.registry import PipelineRegistry

## Runs river_module pipeline and requests data from the specified station
# Station number
station = ["15515500"]

dispatcher = PipelineRegistry()
dispatcher.dispatch(station, clump=False, multidispatch=True)
