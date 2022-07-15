class PluginResourceNotFoundError(Exception):
    def __init__(self, plugin_name, resource_name, message = "An error occured in plugin"):
        self.message = f"Plugin {plugin_name} Exception: resource {resource_name} not found"
        super().__init__(self.message)