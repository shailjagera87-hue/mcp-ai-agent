class MCPToolDiscovery:

    def __init__(self, clients):

        self.clients = clients

    async def discover_tools(self):

        discovered_tools = {}

        for server_name, client in self.clients.items():

            try:

                tools = await client.list_tools()

                discovered_tools[server_name] = tools

                print(
                    f"\n{server_name.upper()} SERVER TOOLS:"
                )

                for tool in tools:

                    print(
                        f"Tool: {tool.name}"
                    )

                    print(
                        f"Description: {tool.description}"
                    )

            except Exception as error:

                print(
                    f"Discovery failed for {server_name}: {error}"
                )

                discovered_tools[server_name] = []

        return discovered_tools