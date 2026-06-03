"""
    Combines two separate sets of detection predictions into a single unified set of detections.
    Preserves all detection properties from both inputs for multi-source detection aggregation.
"""
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.DetectionsCombine.src.utils.response import build_response
from components.DetectionsCombine.src.models.PackageModel import PackageModel

class DetectionsCombine(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        
        # Parse request with model
        self.request.model = PackageModel(**(self.request.data))
        
        # Extract inputs mapped strictly from camelCase names
        self.input_detections_one = self.request.get_param("inputDetectionsOne")
        self.input_detections_two = self.request.get_param("inputDetectionsTwo")
    
    @staticmethod
    def bootstrap(config: dict) -> dict:
        # Package does not require state persistence across frames
        return {}
    
    def _normalize_detections(self, detections) -> list:
        """
        Normalizes detection inputs to a standard list format.
        Ensures both empty values and single object structures are safely merged.
        """
        if not detections:
            return []
        if isinstance(detections, list):
            return detections
        return [detections]

    def process(self):
        # Normalize and merge both inputs
        dets_one = self._normalize_detections(self.input_detections_one)
        dets_two = self._normalize_detections(self.input_detections_two)
        
        combined_detections = dets_one + dets_two
        return combined_detections
    
    def run(self):
        # Process inputs
        self.output_detections = self.process()
        
        # Build and return standard response chain
        package_model = build_response(context=self)
        return package_model

if "__main__" == __name__:
    Executor(sys.argv[1]).run()