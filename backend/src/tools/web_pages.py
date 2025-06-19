import langchain_core.tools as lcct
import bs4
import requests as req
import pydantic as pyd
import socket
from ..models import skill as sk
from ..models import icon_process as ip


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

# Candidate Icon:
# https://plus.unsplash.com/premium_photo-1685086785230-2233cf5d8f28?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OXx8d2Vic2l0ZSUyMGljb258ZW58MHx8MHx8fDA%3D

class WebPageParserSkill(sk.Skill):
    name: str = "Webpage Parser"
    description: str = "Parse and extract textual content from web pages"
    icon: str = ip.encode_icon_url_safe_utf8("web-page-website-svgrepo-com.svg")

    def parse_webpage(website: str) -> str:
        """
        Parse a webpage and return its textual content.

        Parameters:
        -----------
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
        host_resolvable(
            sanitized_url
        )  # Throw a host unresolvable error to short-circuit response
        response = req.get(sanitized_url, timeout=10, allow_redirects=False)
        response.raise_for_status()  # Raise an error for bad responses
        content = bs4.BeautifulSoup(response.content, "html.parser")
        extracted_text = []
        for descendant in content.descendants:
            if type(descendant) == bs4.NavigableString:
                extracted_string = str(descendant.string)
            elif isinstance(descendant, bs4.Tag):
                if descendant.name == "img":  # Extract alt text from images
                    extracted_string = descendant.attrs.get("alt", "")
                elif descendant.name == "meta":  # Extract content from meta tags
                    if (
                        "name" in descendant.attrs
                        and descendant.attrs["name"] == "description"
                    ):
                        extracted_string = descendant.attrs.get("content", "")
            else:
                continue
            extracted_string = extracted_string.strip()
            if extracted_string != "":
                extracted_text.append(extracted_string)
        return "\n".join(extracted_text)

    tool: lcct.Tool = lcct.tool(name.replace(" ","_"))(parse_webpage)
