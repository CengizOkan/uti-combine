"""
    Combines two separate sets of detection predictions into a single unified set of detections.
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
        
        self.request.model = PackageModel(**(self.request.data))
        
        # Girişleri çekiyoruz
        self.input_detections_one = self.request.get_param("inputDetectionsOne")
        self.input_detections_two = self.request.get_param("inputDetectionsTwo")
    
    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}
    
    def _normalize_detections(self, detections) -> list:
        """
        Ne tür bir veri gelirse gelsin güvenle standart bir listeye çevirir.
        """
        if not detections:
            return []
        if isinstance(detections, dict):
            return [detections]
        if isinstance(detections, list):
            return detections
        return []

    def process(self):
        # İki girişi de liste formatına getir ve birleştir
        dets_one = self._normalize_detections(self.input_detections_one)
        dets_two = self._normalize_detections(self.input_detections_two)
        
        combined_detections = dets_one + dets_two
        return combined_detections
    
    def run(self):
        self.output_detections = self.process()
        
        package_model = build_response(context=self)
        return package_model

if "__main__" == __name__:
    Executor(sys.argv[1]).run()