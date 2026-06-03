from pydantic import validator
from typing import List, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Inputs, Configs, Outputs, 
    Response, Request, Output, Input, Config
)

# Step 1: Define Input Classes (Her türlü dict/list veriyi kabul eder)
class InputDetectionsOne(Input):
    name: Literal["inputDetectionsOne"] = "inputDetectionsOne"
    value: Union[dict, list]
    type: str = "object"
    
    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, list):
            return "list"
        return "object"
    
    class Config:
        title = "Detections One"

class InputDetectionsTwo(Input):
    name: Literal["inputDetectionsTwo"] = "inputDetectionsTwo"
    value: Union[dict, list]
    type: str = "object"
    
    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, list):
            return "list"
        return "object"
    
    class Config:
        title = "Detections Two"

# Step 2: Define Output Classes
class OutputDetections(Output):
    name: Literal["outputDetections"] = "outputDetections"
    value: Union[dict, list]
    type: str = "object"
    
    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, list):
            return "list"
        return "object"
    
    class Config:
        title = "Combined Detections"

# Step 3: Define Config Options
class ExecutorConfigs(Configs):
    pass

# Step 4: Build Config Parameters & Requests/Responses
class ExecutorInputs(Inputs):
    # Girişler zorunlu, arayüzde port olarak çıkması için Optional kullanılmadı.
    inputDetectionsOne: InputDetectionsOne
    inputDetectionsTwo: InputDetectionsTwo

class ExecutorOutputs(Outputs):
    outputDetections: OutputDetections

class ExecutorRequest(Request):
    inputs: ExecutorInputs
    configs: ExecutorConfigs
    
    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class ExecutorResponse(Response):
    outputs: ExecutorOutputs

# Step 5: Define Executor Name Model
class DetectionsCombine(Config):
    name: Literal["DetectionsCombine"] = "DetectionsCombine"
    value: Union[ExecutorRequest, ExecutorResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"
    
    class Config:
        title = "Combine Detections"
        json_schema_extra = {
            "target": {
                "value": 0 
            }
        }

# Step 6: Define Config Executor
class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: DetectionsCombine
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"
    
    class Config:
        title = "Task"
        json_schema_extra = {
            "target": "value"
        }

# Step 7: Define Package Configs
class PackageConfigs(Configs):
    executor: ConfigExecutor

# Step 8: Define Package Model (Top Level)
class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DetectionsCombine"] = "DetectionsCombine"