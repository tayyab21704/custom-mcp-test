import ast
import os
from fastmcp import FastMCP
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()

# Initialize FastMCP
mcp = FastMCP("BugHunterPro")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    google_api_key=os.getenv("GEMINI_API_KEY"), 
    temperature=0
)

# --- Individual, Independent Tools ---

@mcp.tool()
def parse_code(code: str) -> str:
    """
    Parses Python code to check for syntax errors.
    Returns 'valid' if syntax is correct, or detailed error message if invalid.
    Use this FIRST before analyzing any code.
    """
    try:
        ast.parse(code)
        return "✅ Syntax Valid: Code parsed successfully. No syntax errors found."
    except SyntaxError as e:
        return f"❌ Syntax Error: {e.msg} at line {e.lineno}, column {e.offset}"

@mcp.tool()
async def identify_bug(code: str) -> str:
    """
    Analyzes code to identify potential bugs, logic errors, or security vulnerabilities.
    Returns a concise description of the main issue found.
    Call this after confirming syntax is valid.
    """
    messages = [
        SystemMessage(content="""You are a Senior QA Engineer. Analyze this code and identify the main bug, logic error, or security vulnerability. 
        Be concise but specific. Focus on:
        - Logic errors (e.g., division by zero, off-by-one errors)
        - Missing error handling
        - Security vulnerabilities
        - Edge cases not handled
        
        Return ONLY the bug description, nothing else."""),
        HumanMessage(content=code)
    ]
    response = await llm.ainvoke(messages)
    return response.content

@mcp.tool()
async def locate_bug_lines(code: str, bug_description: str) -> str:
    """
    Identifies the specific line numbers in the code where a bug occurs.
    Args:
        code: The source code
        bug_description: Description of the bug to locate
    Returns: Line numbers (e.g., "3" or "5-7" for a range)
    """
    messages = [
        SystemMessage(content="""You are a code analyzer. Given a bug description, identify the EXACT line number(s) where the bug occurs.
        Return ONLY the line number(s), nothing else. Examples:
        - Single line: "3"
        - Multiple lines: "3, 5, 7"
        - Range: "3-5"
        """),
        HumanMessage(content=f"Code:\n{code}\n\nBug: {bug_description}")
    ]
    response = await llm.ainvoke(messages)
    return response.content.strip()

@mcp.tool()
async def explain_impact(bug_description: str, code_context: str) -> str:
    """
    Provides detailed explanation of why something is a bug and what its impact is.
    Args:
        bug_description: The identified bug
        code_context: The relevant code snippet
    Returns: Detailed explanation of the bug's impact and severity
    """
    messages = [
        SystemMessage(content="""You are a Security Researcher. Given a bug description and code context:
        1. Explain WHY this is a bug (what rule/principle it violates)
        2. Describe the IMPACT (what could go wrong)
        3. Rate the SEVERITY (Low/Medium/High/Critical)
        4. Suggest a FIX if applicable
        
        Be clear and thorough but concise."""),
        HumanMessage(content=f"Bug: {bug_description}\n\nCode:\n{code_context}")
    ]
    response = await llm.ainvoke(messages)
    return response.content

@mcp.tool()
async def suggest_fix(code: str, bug_description: str) -> str:
    """
    Suggests a code fix for the identified bug.
    Args:
        code: The buggy code
        bug_description: Description of the bug
    Returns: Suggested fix with code example
    """
    messages = [
        SystemMessage(content="""You are a Senior Developer. Given buggy code and a bug description:
        1. Provide a fixed version of the code
        2. Explain what you changed and why
        
        Format your response as:
        FIXED CODE:
        ```python
        [fixed code here]
        ```
        
        EXPLANATION:
        [what was changed and why]
        """),
        HumanMessage(content=f"Buggy Code:\n{code}\n\nBug: {bug_description}")
    ]
    response = await llm.ainvoke(messages)
    return response.content

if __name__ == "__main__":
    mcp.run(transport="stdio")