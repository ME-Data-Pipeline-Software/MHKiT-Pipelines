from utils.registry import PipelineRegistry


# Retrieves "realtime" and "historic" datasets from online, 
# saving the entire "realtime" dataset and an except of time
# specified in pipelines/cdip_example/config/pipeline_historic.yaml
buoy_id = "201"

dispatcher = PipelineRegistry()
dispatcher.dispatch([buoy_id], clump=False, multidispatch=True)
