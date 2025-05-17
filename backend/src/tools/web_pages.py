import langchain_core.tools as lcct
import bs4
import requests as req
import re

# Should this perhaps be a separate, deterministic skill that we can plug into 
#   any tool call that needs to clean text?
def get_embedded_text(input: bs4.BeautifulSoup, strip:bool = False, separator: str = "") -> str:
    pass

@lcct.tool
def parse_webpage(website: str, embedded: bool = True) -> str:
    """Parse a webpage and return its textual content."""

    response = req.get(website)
    response.raise_for_status()  # Raise an error for bad responses
    content = bs4.BeautifulSoup(response.content, "html.parser")
    strings = []
    for descendant in content.descendants:
        desc_type = None
        if type(descendant) == bs4.NavigableString:
            string = str(descendant.string)
        elif isinstance(descendant,bs4.Tag):
            desc_type = "Tag"
            if descendant.name == "img":  #Extract alt text from images
                string = descendant.attrs.get('alt', '')
            elif descendant.name == "meta": #Extract content from meta tags
                if 'name' in descendant.attrs and descendant.attrs['name'] == 'description':
                    string = descendant.attrs.get('content', '')
        else:
            continue
        string=string.strip()
        if string != '':
            strings.append(string)
    return "\n".join(strings)
