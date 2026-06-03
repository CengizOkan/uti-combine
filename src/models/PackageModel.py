from pydantic import Field
from typing import Any, Literal
from sdks.novavision.src.base.model import (
    Package, Inputs, Configs, Outputs, 
    Response, Request, Output, Input, Config
)

# Step 1: Define Input Classes (En esnek yapı - Any kullanımı yasak olduğu için dict ve list)
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

# Step 2: Define Output Classes
class OutputDetections(Output):
    name: Literal["outputDetections"] = "outputDetections"
    value: dict | list
    type: str = "object"
    
    class Config:
        title = "Combined Detections"

# Step 3: Define Config Options
class ExecutorConfigs(Configs):
    pass

# Step 4: Build Config Parameters & Requests/Responses
class ExecutorInputs(Inputs):
    # Arayüzde zorunlu olarak belirmesi için
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
    value: ExecutorRequest | ExecutorResponse
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