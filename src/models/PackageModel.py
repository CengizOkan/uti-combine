from pydantic import validator
from typing import Union, Literal
from sdks.novavision.src.base.model import (
    Package, Inputs, Configs, Outputs, 
    Response, Request, Output, Input, Config
)

class InputDetectionsOne(Input):
    name: Literal["inputDetectionsOne"] = "inputDetectionsOne"
    value: Union[dict, list, None] = None
    type: str = "object"
    
    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, v, values):
        val = values.get('value')
        if isinstance(val, list):
            return "list"
        return "object"
    
    class Config:
        title = "Detections One"

class InputDetectionsTwo(Input):
    name: Literal["inputDetectionsTwo"] = "inputDetectionsTwo"
    value: Union[dict, list, None] = None
    type: str = "object"
    
    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, v, values):
        val = values.get('value')
        if isinstance(val, list):
            return "list"
        return "object"
    
    class Config:
        title = "Detections Two"

class OutputDetections(Output):
    name: Literal["outputDetections"] = "outputDetections"
    value: Union[dict, list]
    type: str = "object"
    
    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, v, values):
        val = values.get('value')
        if isinstance(val, list):
            return "list"
        return "object"
    
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
    configs: Union[ExecutorConfigs, list, dict, None] = None
    
    class Config:
        json_schema_extra = {"target": "configs"}

class ExecutorResponse(Response):
    outputs: ExecutorOutputs

class DetectionsCombine(Config):
    name: Literal["DetectionsCombine"] = "DetectionsCombine"
    value: Union[ExecutorRequest, ExecutorResponse]
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