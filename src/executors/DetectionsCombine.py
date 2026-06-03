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
        
        # Parametreleri al (None olarak gelse bile)
        self.input_detections_one = self.request.get_param("inputDetectionsOne")
        self.input_detections_two = self.request.get_param("inputDetectionsTwo")
        
        # Şartname gereği flow control için branchstop eklenir
        self.branchstop = False
    
    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}
    
    def _normalize(self, data):
        if not data:
            return []
        if isinstance(data, dict):
            return [data]
        if isinstance(data, list):
            return data
        return []

    def process(self):
        # Güvenli birleştirme
        list1 = self._normalize(self.input_detections_one)
        list2 = self._normalize(self.input_detections_two)
        
        # İki listeyi uç uca ekle
        return list1 + list2
    
    def run(self):
        # İşlem yap ve self.output_detections içine ata
        self.output_detections = self.process()
        
        # Yanıtı derle
        package_model = build_response(context=self)
        return package_model

if "__main__" == __name__:
    Executor(sys.argv[1]).run()