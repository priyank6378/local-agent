from fastmcp import FastMCP

import webbrowser
import os
import pypdf
import dotenv

dotenv.load_dotenv()


mcp = FastMCP("my_pc")

# @mcp.tool
# async def open_browser():
#     """
#     This tool is used to open chrome application on this computer
#     """
#     try:
#         webbrowser.open("https://www.google.com")
#         return "Opened web browser"
#     except Exception as e:
#         return f"error : {e}"

# @mcp.tool
# async def get_all_files() -> list[str]:
#     '''
#     Get all the files available on my pc
#     '''
#     base_path = r"D:\\"
#     matches = []



# @mcp.tool
# async def read_pdf(file_path: str) -> str:
#     """
#     Read the content of the pdf.
      
#     Arguments:
#         file_path: It is the absolute path of the pdf file you want to read
#     """
#     reader = pypdf.PdfReader(file_path)
#     full_text = ["\n".join(page.extract_text()) for page in reader.pages]
#     return full_text

@mcp.tool
async def internet_search(query: str) -> list[any]:
    '''
    Search internet for query.
    '''
    import ollama

    response = ollama.web_search(query)

    return response.results
    
    


if __name__=="__main__":
    mcp.run(transport="streamable-http")