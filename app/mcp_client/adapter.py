
from typing import Any, Optional, Union
from pydantic import Field, create_model
from langchain_core.tools import StructuredTool


def json_type_to_python(schema: dict) -> Any:
    """Convert common JSON Schema types into Python types."""

    schema_type = schema.get("type", "string")

    type_map = {
        "string": str,
        "integer": int,
        "number": float,
        "boolean": bool,
        "object": dict[str, Any],
        "array": list[Any],
    }

    python_type = type_map.get(schema_type, str)

    if schema.get("nullable"):
        python_type = Optional[python_type]

    return python_type


def build_args_schema(tool_name: str, input_schema: dict):
    """Create a Pydantic model from an MCP JSON input schema."""

    properties = input_schema.get("properties", {})
    required_fields = input_schema.get("required", [])

    fields = {}

    for field_name, field_schema in properties.items():
        python_type = json_type_to_python(field_schema)
        description = field_schema.get("description", "")

        if field_name in required_fields:
            default = ...
        else:
            default = field_schema.get("default", None)
            if not field_schema.get("nullable") and default is None:
                python_type = Optional[python_type]

        fields[field_name] = (
            python_type,
            Field(default=default, description=description),
        )

    return create_model(f"{tool_name.title()}Input", **fields)


def format_mcp_result(result) -> str:
    """Convert an MCP result into text for LangChain."""

    if getattr(result, "isError", False):
        raise RuntimeError(f"MCP tool returned an error: {result}")

    structured = getattr(result, "structuredContent", None)

    if structured is None:
        structured = getattr(result, "structured_content", None)

    if structured is not None:
        return str(structured)

    text_parts = []

    for item in getattr(result, "content", []):
        item_text = getattr(item, "text", None)

        if item_text is not None:
            text_parts.append(item_text)
        else:
            text_parts.append(str(item))

    return "\n".join(text_parts) or str(result)


class MCPToolAdapter:
    """Convert tools from connected MCP servers into LangChain tools."""

    def __init__(self, mcp_manager):
        self.mcp_manager = mcp_manager

    async def build_tools(self):
        langchain_tools = []

        for server_name, session in self.mcp_manager.sessions.items():
            discovered = await session.list_tools()

            for mcp_tool in discovered.tools:
                original_tool_name = mcp_tool.name

                # Prefix names to avoid collisions between MCP servers.
                langchain_name = (
                    f"{server_name}_{original_tool_name}"
                )

                input_schema = getattr(
                    mcp_tool,
                    "inputSchema",
                    {},
                ) or {}

                args_schema = build_args_schema(
                    langchain_name,
                    input_schema,
                )

                async def execute_tool(
                    server=server_name,
                    tool=original_tool_name,
                    **kwargs,
                ):
                    result = await self.mcp_manager.call_tool(
                        server,
                        tool,
                        kwargs,
                    )
                    return format_mcp_result(result)

                langchain_tool = StructuredTool(
                    name=langchain_name,
                    description=(
                        mcp_tool.description
                        or f"Execute {original_tool_name} "
                           f"on the {server_name} MCP server."
                    ),
                    args_schema=args_schema,
                    coroutine=execute_tool,
                )

                langchain_tools.append(langchain_tool)

        return langchain_tools
