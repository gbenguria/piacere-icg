# Copyright 2022 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#-------------------------------------------------------------------------

from plugin import TemplateUtils


def createExecutionFileInstructions(iac_language, key, data):
    template_for_config_path = TemplateUtils.find_template_path(iac_language, key, "config")
    template_for_config = TemplateUtils.read_template(template_for_config_path)
    template_for_config_path_edited = TemplateUtils.edit_template(template_for_config, data)
    return template_for_config_path_edited
