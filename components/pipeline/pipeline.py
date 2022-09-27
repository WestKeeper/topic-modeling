from typing import List, Optional

from components.pipeline.pipeline_data_structure import PipelineDataStructure
from components.pipeline.pipeline_module import PipelineModule
from components.pipeline.pipeline_module_factory import create_pipeline_module
from components.pipeline.pipeline_module_name import PipelineModuleName


class Pipeline:
    """"""
    def __init__(self, module_names: Optional[List[PipelineModuleName]] = None):
        """"""
        self.create_modules(module_names)

    def create_modules(self, module_names: List[PipelineModuleName]):
        self._modules = []
        for module_name in module_names:
            module = create_pipeline_module(module_name)
            self._modules.append(module)

    def add_modules(self, module_names: List[PipelineModuleName]):
        for module_name in module_names:
            module = create_pipeline_module(module_name)
            self._modules.append(module)

    def process_modules(self, data: PipelineDataStructure) -> PipelineDataStructure:
        """"""
        for module in self._modules:
            data = module.process(data)

        return data
