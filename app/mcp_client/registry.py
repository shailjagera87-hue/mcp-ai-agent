class MCPToolRegistry:

    def __init__(self):

        self.tools = {}

    def register_tools(self, server_name, tools):

        for tool in tools:

            tool_name = f"{server_name}_{tool.name}"

            self.tools[tool_name] = {
                "server": server_name,
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            }

    def get_tool(self, tool_name):

        return self.tools.get(tool_name)

    def get_all_tools(self):

        return self.tools

    def print_tools(self):

        print("\nREGISTERED MCP TOOLS")

        for name, tool in self.tools.items():

            print(
                f"{name} -> {tool['description']}"
            )