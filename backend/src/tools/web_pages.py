import backend.src.pike_tool as pt
import bs4
import requests as req
import pydantic as pyd
import socket

def host_resolvable(url: str) -> bool:
    """
    Check if the host of a URL is resolvable.

    Parameters
    ----------
    url : str
        The URL to check.

    Returns
    -------
    bool
        True if the host is resolvable, False otherwise.
    """
    try:
        host = pyd.HttpUrl(url).host
        socket.gethostbyname(host)
        return True
    except socket.gaierror as e:
        e.msg = f"Host {host} is not resolvable: {e}"
        raise e

@pt.pike_tool
#(display="Parse Webpage", icon="web-page-website-svgrepo-com.svg")
def parse_webpage(website: str) -> str:
    """
    Parse a webpage and return its textual content.

    Parameters
    ----------
    website : str
        The URL of the webpage to parse.

    Returns
    -------
    str
        The extracted and concatenated textual content from the webpage separated by newlines.

    Raises
    ------
    pydantic.ValidationError
        If the URL does not conform to expected requirements/sanitize properly.
    requests.HTTPError
        If the HTTP request for the webpage fails.
    socket.gaierror
        If the host of the URL is not resolvable.
    """
    sanitized_url = pyd.HttpUrl(website)
    host_resolvable(sanitized_url) # Throw a host unresolvable error to short-circuit response
    response = req.get(sanitized_url, timeout=10, allow_redirects=False)
    response.raise_for_status()  # Raise an error for bad responses
    content = bs4.BeautifulSoup(response.content, "html.parser")
    extracted_text = []
    for descendant in content.descendants:
        if type(descendant) == bs4.NavigableString:
            extracted_string = str(descendant.string)
        elif isinstance(descendant, bs4.Tag):
            if descendant.name == "img":  #Extract alt text from images
                extracted_string = descendant.attrs.get('alt', '')
            elif descendant.name == "meta": #Extract content from meta tags
                if 'name' in descendant.attrs and descendant.attrs['name'] == 'description':
                    extracted_string = descendant.attrs.get('content', '')
        else:
            continue
        extracted_string=extracted_string.strip()
        if extracted_string != '':
            extracted_text.append(extracted_string)
    return "\n".join(extracted_text)
