import sys
import os
import asyncio
import argparse
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from dotenv import load_dotenv

load_dotenv()

def read_file_content(file_path: str) -> str:
    """Safely reads the content of a file."""
    if not os.path.exists(file_path):
        print(f"❌ Error: File '{file_path}' not found.")
        sys.exit(1)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        sys.exit(1)

async def main():
    # 1. Parse Command Line Arguments
    parser = argparse.ArgumentParser(description="MCP Bug Hunter Client")
    parser.add_argument("file", help="Path to the code file you want to analyze")
    args = parser.parse_args()
    
    code_content = read_file_content(args.file)
    print(f"📂 Loaded file: {args.file} ({len(code_content)} chars)")

    # 2. Connect to the MCP Server
    client = MultiServerMCPClient(
        {
            "bug_hunter": {
                "transport": "stdio",
                "command": "python",
                "args": ["server.py"], 
            }
        }
    )
    
    print("🔌 Connecting to MCP Server...")
    try:
        tools = await client.get_tools()
        print(f"✅ Connected! Found {len(tools)} tools:")
        for tool in tools:
            print(f"   • {tool.name}")
    except Exception as e:
        print(f"❌ Failed to connect to server: {e}")
        return

    # 3. Initialize LLM with tools
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        google_api_key=os.getenv("GEMINI_API_KEY"), 
        temperature=0
    )
    
    llm_with_tools = llm.bind_tools(tools)

    # 4. Execute Analysis with agentic loop
    print("\n🚀 Starting Intelligent Bug Analysis...\n")
    
    system_prompt = """You are an expert debugging assistant with access to specialized tools.

Your job is to analyze code intelligently by calling the appropriate tools in a logical sequence:

1. ALWAYS start with `parse_code` to check syntax
2. If syntax is valid, use `identify_bug` to find issues
3. Use `locate_bug_lines` to pinpoint where bugs occur
4. Use `explain_impact` to analyze severity and impact
5. Optionally use `suggest_fix` to provide solutions

Be intelligent: 
- Don't call tools you don't need
- If syntax is invalid, stop there and report it
- Adapt based on what you find
- Provide a final summary of your findings

Call tools one at a time and analyze their output before deciding what to do next."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"Please analyze this code for bugs:\n\n```python\n{code_content}\n```")
    ]
    
    max_iterations = 10
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        
        # Invoke LLM
        response = await llm_with_tools.ainvoke(messages)
        messages.append(response)
        
        # Check if there are tool calls
        if not response.tool_calls:
            # No more tool calls, agent is done
            print(f"\n✅ Analysis complete after {iteration} iterations\n")
            break
        
        # Execute tool calls
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_call_id = tool_call["id"]
            
            print(f"🔧 [{iteration}] Calling: {tool_name}")
            
            # Find and execute the tool
            tool_result = None
            for tool in tools:
                if tool.name == tool_name:
                    try:
                        tool_result = await tool.ainvoke(tool_args)
                        # Print a preview of the result
                        preview = str(tool_result)[:100] + "..." if len(str(tool_result)) > 100 else str(tool_result)
                        print(f"   ↳ {preview}")
                    except Exception as e:
                        tool_result = f"Error executing tool: {str(e)}"
                        print(f"   ⚠️  {tool_result}")
                    break
            
            # Add tool result to messages
            messages.append(
                ToolMessage(
                    content=str(tool_result),
                    tool_call_id=tool_call_id
                )
            )
    
    # Get final response
    if not messages[-1].tool_calls:
        final_response = messages[-1].content
    else:
        # If last message had tool calls, get one more response
        response = await llm_with_tools.ainvoke(messages)
        final_response = response.content
    
    # Print final report
    print("\n" + "="*60)
    print("                    FINAL BUG REPORT")
    print("="*60 + "\n")
    
    # Handle the response format
    if isinstance(final_response, list):
        for item in final_response:
            if isinstance(item, dict) and item.get('type') == 'text':
                print(item.get('text', ''))
    elif isinstance(final_response, str):
        print(final_response)
    else:
        print(final_response)
    
    print("\n" + "="*60)

if __name__ == "__main__":
    asyncio.run(main())