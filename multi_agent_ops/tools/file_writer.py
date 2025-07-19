from crewai.tools import tool  # ✅ not from crewai.tools

@tool  # ✅ decorator style, no arguments
def write_to_file(text: str) -> str:
    """
    Writes the given Python code to a file named generated_output.py.
    """
    filename = "generated_output.py"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    return f"✅ Code written to {filename}"
