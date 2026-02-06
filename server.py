import ast
import os
import csv
from io import StringIO
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

# Load bug classification database
def load_bug_classifications():
    """Load bug classifications from bug_descriptions.txt"""
    try:
        with open('bug_descriptions.txt', 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "No bug classification database found."

BUG_DATABASE = load_bug_classifications()

def _parse_code_impl(code: str) -> str:
    """Internal implementation of parse_code."""
    try:
        ast.parse(code)
        return "✅ Syntax Valid: Code parsed successfully."
    except SyntaxError as e:
        return f"❌ Syntax Error: {e.msg} at line {e.lineno}, column {e.offset}"

@mcp.tool()
def parse_code(code: str) -> str:
    """
    Parses Python code to check for syntax errors.
    Returns 'valid' if syntax is correct, or detailed error message if invalid.
    """
    return _parse_code_impl(code)

async def _classify_bugs_impl(code: str) -> str:
    """Internal implementation of classify_bugs."""
    # Number the code lines for reference
    lines = code.split('\n')
    numbered_code = '\n'.join([f"{i+1}: {line}" for i, line in enumerate(lines)])
    
    messages = [
        SystemMessage(content=f"""You are a bug classification expert. Analyze the provided code and classify ALL bugs found according to this bug database:

{BUG_DATABASE}

For EACH bug you find:
1. Identify the exact line number(s) where it occurs
2. Match it to the most appropriate category from the database
3. Assign the severity from the database
4. Provide a brief description specific to this code
5. Suggest a solution based on the database recommendations

Return your findings ONLY as a CSV with these exact columns:
Line,Category,Severity,Description,Solution

Example:
3,Logic Error,High,Division by zero - no check for empty list,Add length check before division
5,Security,Critical,SQL Injection - unsanitized user input,Use parameterized queries

IMPORTANT:
- Return ONLY the CSV data, no markdown, no explanations, no preamble
- One row per bug found
- If multiple lines have the same bug, list as "3-5" or "3,5,7"
- Use exact category names from the database
- Keep descriptions concise (under 100 chars)
"""),
        HumanMessage(content=f"Analyze this code:\n\n{numbered_code}")
    ]
    
    response = await llm.ainvoke(messages)
    return response.content

@mcp.tool()
async def classify_bugs(code: str) -> str:
    """
    Analyzes code and classifies bugs according to predefined bug categories.
    Returns a CSV-formatted string with: Line Number, Bug Category, Severity, Description, Solution
    
    Uses the bug classification database to identify and categorize issues.
    """
    return await _classify_bugs_impl(code)

@mcp.tool()
async def generate_bug_report_csv(code: str, output_filename: str = "bug_report.csv") -> str:
    """
    Generates a complete bug report as a CSV file.
    
    Args:
        code: Source code to analyze
        output_filename: Name of the output CSV file (default: bug_report.csv)
    
    Returns: Success message with filename and bug count
    """
    # First check syntax using internal implementation
    syntax_result = _parse_code_impl(code)
    
    if "Syntax Error" in syntax_result:
        # Create CSV with syntax error
        csv_data = "Line,Category,Severity,Description,Solution\n"
        csv_data += f"N/A,Syntax Error,Critical,{syntax_result},Fix syntax errors first\n"
        
        with open(output_filename, 'w', newline='') as f:
            f.write(csv_data)
        
        return f"❌ Syntax errors found. Report saved to {output_filename}"
    
    # Get bug classifications using internal implementation
    bug_csv = await _classify_bugs_impl(code)
    
    # Clean up the CSV (remove markdown code blocks if present)
    bug_csv = bug_csv.replace('```csv', '').replace('```', '').strip()
    
    # Save to file
    with open(output_filename, 'w', newline='') as f:
        f.write(bug_csv)
    
    # Count bugs (subtract 1 for header)
    bug_count = len(bug_csv.split('\n')) - 1
    
    return f"✅ Analysis complete! Found {bug_count} bug(s). Report saved to {output_filename}"

@mcp.tool()
async def quick_scan(code: str) -> str:
    """
    Quick scan that returns top 3 most critical bugs as a formatted string.
    Useful for getting a quick overview without generating a full CSV.
    """
    messages = [
        SystemMessage(content=f"""You are a bug detection expert. Using this bug database:

{BUG_DATABASE}

Identify the TOP 3 MOST CRITICAL bugs in the code. For each:
- Line number
- Bug category
- Brief description
- Why it's critical

Format as a simple numbered list, most critical first."""),
        HumanMessage(content=code)
    ]
    
    response = await llm.ainvoke(messages)
    return response.content

if __name__ == "__main__":
    mcp.run(transport="stdio")