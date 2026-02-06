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
    # Parse arguments
    parser = argparse.ArgumentParser(description="MCP Bug Hunter - CSV Report Generator")
    parser.add_argument("file", help="Path to the code file to analyze")
    parser.add_argument("-o", "--output", default="bug_report.csv", help="Output CSV filename (default: bug_report.csv)")
    parser.add_argument("--quick", action="store_true", help="Quick scan mode (top 3 bugs only)")
    args = parser.parse_args()
    
    code_content = read_file_content(args.file)
    print(f"📂 Loaded: {args.file} ({len(code_content)} chars)")

    # Connect to MCP Server
    client = MultiServerMCPClient(
        {
            "bug_hunter": {
                "transport": "stdio",
                "command": "python",
                "args": ["server.py"], 
            }
        }
    )
    
    print("🔌 Connecting to BugHunter MCP Server...")
    try:
        tools = await client.get_tools()
        print(f"✅ Connected! Available tools: {', '.join([t.name for t in tools])}\n")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        return

    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        google_api_key=os.getenv("GEMINI_API_KEY"), 
        temperature=0
    )
    llm_with_tools = llm.bind_tools(tools)

    # Execute analysis
    if args.quick:
        print("🚀 Running Quick Scan (Top 3 Critical Bugs)...\n")
        
        # Find and call quick_scan tool directly
        for tool in tools:
            if tool.name == "quick_scan":
                result = await tool.ainvoke({"code": code_content})
                print("="*60)
                print("           QUICK SCAN RESULTS")
                print("="*60)
                print(result)
                print("="*60)
                return
    else:
        print(f"🚀 Generating Full Bug Report → {args.output}\n")
        
        # Find and call generate_bug_report_csv tool directly
        for tool in tools:
            if tool.name == "generate_bug_report_csv":
                result = await tool.ainvoke({
                    "code": code_content,
                    "output_filename": args.output
                })
                print(result)
                
                # Display the CSV contents
                if os.path.exists(args.output):
                    print(f"\n📊 Report Preview ({args.output}):")
                    print("="*60)
                    with open(args.output, 'r') as f:
                        print(f.read())
                    print("="*60)
                return

if __name__ == "__main__":
    asyncio.run(main())