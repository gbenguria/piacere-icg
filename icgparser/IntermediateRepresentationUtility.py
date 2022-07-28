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
    NETWORKS = "networks"
    SECURITY_GROUPS = "computingGroup"


def find_objects(object_name, intermediate_representation):
    logging.info(f"Searching for {object_name.value} in intermediate representation")
    steps = intermediate_representation[IntermediateRepresentationResources.STEPS.value]
    for step in steps:
        data = step[IntermediateRepresentationResources.DATA.value]
        if object_name.value in data.keys():
            return data[object_name.value]
    return []


def add_step(step, intermediate_representation, step_number):
    logging.info("Adding step into intermediate representation")
    steps = intermediate_representation[IntermediateRepresentationResources.STEPS.value]
    if step_number:
        steps.insert(step_number, step)
    else:
        steps.append(step)
    return intermediate_representation


def force_add_resources_name(to_resource, from_resource, intermediate_representation):
    sec_groups = find_objects(from_resource, intermediate_representation)
    sec_groups_names = []
    for key, sg in sec_groups[0].items():
        if isinstance(sg, dict) and sg["name"]:
            sec_groups_names.append(sg["name"])
    for resource in find_objects(to_resource, intermediate_representation):
        resource["infra_sgs"] = sec_groups_names
    return intermediate_representation
