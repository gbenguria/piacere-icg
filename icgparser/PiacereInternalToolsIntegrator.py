import logging
from distutils.dir_util import copy_tree

from icgparser import IntermediateRepresentationUtility
from icgparser.IntermediateRepresentationUtility import IntermediateRepresentationResources


def extract_info_for_monitoring_agents(intermediate_representation):
    logging.info("Adding info for monitoring step")
    monitoring_object_step = {"programming_language": "ansible",
                              "step_name": "piacere_monitoring",
                              "data": {"piacere_monitoring": {"name": "piacere_monitoring"}}}
    vms = IntermediateRepresentationUtility.find_objects(IntermediateRepresentationResources.VIRTUAL_MACHINES,
                                                         intermediate_representation)
    # TODO restore these 2 commented lines: monitoring could be installed on multiple nodes!
    # monitoring_object_step["data"]["monitoring"]["nodes"] = []
    # monitoring_object_step["data"]["monitoring"]["nodes"] += vms
    # TODO remove this line: monitoring could be installed on multiple nodes!
    if vms:
        monitoring_object_step["data"]["piacere_monitoring"]["node"] = vms[0]
    logging.info(f"Monitoring step: {monitoring_object_step}")
    return monitoring_object_step


def add_internal_tool_information(intermediate_representation):
    monitoring_step = extract_info_for_monitoring_agents(intermediate_representation)
    intermediate_representation = IntermediateRepresentationUtility.add_step(monitoring_step,
                                                                             intermediate_representation,
                                                                             1)
    return intermediate_representation


def add_files_for_monitoring_agents(template_generated_folder_path):
    monitoring_folder_path = template_generated_folder_path + "/piacere_monitoring"
    logging.info(f"Adding monitoring agents folder in {monitoring_folder_path}")
    copy_tree("templates/ansible/ubuntu/monitoring", monitoring_folder_path)


def add_files_for_piacere_internal_tools(template_generated_folder_path):
    add_files_for_monitoring_agents(template_generated_folder_path)
