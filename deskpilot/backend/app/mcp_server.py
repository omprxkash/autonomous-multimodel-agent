"""
Deskpilot MCP Server — exposes Gmail and Calendar tools via Model Context Protocol.
Run alongside the main FastAPI app: python -m app.mcp_server
Requires: pip install mcp
"""
import asyncio
import os
import sys
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("deskpilot")


def _get_service():
    """Build Gmail service from env vars (for single-user MCP usage)."""
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    creds = Credentials(
        token=os.getenv("GMAIL_ACCESS_TOKEN", ""),
        refresh_token=os.getenv("GMAIL_REFRESH_TOKEN", ""),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv("GOOGLE_CLIENT_ID", ""),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET", ""),
        scopes=["https://www.googleapis.com/auth/gmail.modify"],
    )
    return build("gmail", "v1", credentials=creds)


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="search_gmail",
            description="Search Gmail for emails matching a query. Returns up to 5 results with sender, subject, and date.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Gmail search query (e.g. 'from:boss@company.com subject:project')"},
                    "max_results": {"type": "integer", "default": 5},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="read_email",
            description="Read the full content of an email by its message ID.",
            inputSchema={
                "type": "object",
                "properties": {
                    "message_id": {"type": "string", "description": "Gmail message ID"},
                },
                "required": ["message_id"],
            },
        ),
        Tool(
            name="list_calendar_events",
            description="List upcoming Google Calendar events.",
            inputSchema={
                "type": "object",
                "properties": {
                    "max_results": {"type": "integer", "default": 10},
                },
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    from app.services import gmail as gmail_service
    from app.services import calendar as cal_service

    if name == "search_gmail":
        svc = _get_service()
        result = gmail_service.search_emails(svc, arguments["query"], arguments.get("max_results", 5))
        return [TextContent(type="text", text=result)]

    if name == "read_email":
        svc = _get_service()
        result = gmail_service.read_email(svc, arguments["message_id"])
        return [TextContent(type="text", text=result)]

    if name == "list_calendar_events":
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        creds = Credentials(
            token=os.getenv("GMAIL_ACCESS_TOKEN", ""),
            refresh_token=os.getenv("GMAIL_REFRESH_TOKEN", ""),
            token_uri="https://oauth2.googleapis.com/token",
            client_id=os.getenv("GOOGLE_CLIENT_ID", ""),
            client_secret=os.getenv("GOOGLE_CLIENT_SECRET", ""),
            scopes=["https://www.googleapis.com/auth/calendar.readonly"],
        )
        cal_svc = build("calendar", "v3", credentials=creds)
        result = cal_service.list_events(cal_svc, arguments.get("max_results", 10))
        return [TextContent(type="text", text=str(result))]

    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
