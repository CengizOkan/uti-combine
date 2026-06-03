from sdks.novavision.src.helper.package import PackageHelper
from components.DetectionsCombine.src.models.PackageModel import (
    PackageModel, PackageConfigs, ConfigExecutor,
    ExecutorOutputs, ExecutorResponse, DetectionsCombine,
    OutputDetections
)

def build_response(context):
    # Build outputs
    output_detections = OutputDetections(value=context.output_detections)
    outputs = ExecutorOutputs(outputDetections=output_detections)
    
    # Build response chain
    executor_response = ExecutorResponse(outputs=outputs)
    executor = DetectionsCombine(value=executor_response)
    config_executor = ConfigExecutor(value=executor)
    package_configs = PackageConfigs(executor=config_executor)
    
    # Build final package model
    package = PackageHelper(
        packageModel=PackageModel,
        packageConfigs=package_configs
    )
    package_model = package.build_model(context)
    
    return package_model