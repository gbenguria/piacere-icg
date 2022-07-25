import logging
from enum import Enum


class NoValue(Enum):
    def __repr__(self):
        return '<%s.%s>' % (self.__class__.__name__, self.name)


class IntermediateRepresentationResources(NoValue):
    STEP_NAME = 'step_name'
    STEPS = 'steps'
    DATA = 'data'
    LANGUAGE = "programming_language"
    VIRTUAL_MACHINES = 'vms'


def find_objects(object_name, intermediate_representation):
    logging.info(f"Searching for {object_name.value} in intermediate representation")
    steps = intermediate_representation[IntermediateRepresentationResources.STEPS.value]
    for step in steps:
        data = step[IntermediateRepresentationResources.DATA.value]
        if object_name.value in data.keys():
            return data[IntermediateRepresentationResources.VIRTUAL_MACHINES.value]
    return []


def add_step(step, intermediate_representation):
    logging.info("Adding step into intermediate representation")
    steps = intermediate_representation[IntermediateRepresentationResources.STEPS.value]
    steps.append(step)
    return intermediate_representation
