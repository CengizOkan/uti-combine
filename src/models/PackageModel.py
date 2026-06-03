from pydantic import Field
from typing import Literal, Optional
from sdks.novavision.src.base.model import (
    Package, Inputs, Configs, Outputs, 
    Response, Request, Output, Input, Config
)

class InputDetectionsOne(Input):
    name: Literal["inputDetectionsOne"] = "inputDetectionsOne"
    value: dict | list | None = None
    type: str = "object"
    class Config:
        title = "Detections One"

class InputDetectionsTwo(Input):
    name: Literal["inputDetectionsTwo"] = "inputDetectionsTwo"
    value: dict | list | None = None
    type: str = "object"
    class Config:
        title = "Detections Two"

class OutputDetections(Output):
    name: Literal["outputDetections"] = "outputDetections"
    value: dict | list
    type: str = "object"
    class Config:
        title = "Combined Detections"

class ExecutorConfigs(Configs):
    pass

class ExecutorInputs(Inputs):
    inputDetectionsOne: InputDetectionsOne
    inputDetectionsTwo: InputDetectionsTwo

class ExecutorOutputs(Outputs):
    outputDetections: OutputDetections

class ExecutorRequest(Request):
    inputs: ExecutorInputs
    configs: ExecutorConfigs | list | dict | None = None
    class Config:
        json_schema_extra = {"target": "configs"}

class ExecutorResponse(Response):
    outputs: ExecutorOutputs

class DetectionsCombine(Config):
    name: Literal["DetectionsCombine"] = "DetectionsCombine"
    value: ExecutorRequest | ExecutorResponse
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    class Config:
        title = "Combine Detections"
        json_schema_extra = {"target": {"value": 0}}

class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: DetectionsCombine
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    class Config:
        title = "Task"
        json_schema_extra = {"target": "value"}

class PackageConfigs(Configs):
    executor: ConfigExecutor

class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DetectionsCombine"] = "DetectionsCombine"