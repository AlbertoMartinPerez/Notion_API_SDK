from rich import print_json
import json


def print_block(
    notion_block    : dict) -> dict:
    """
    Print with indents a dictionary Notion block for readability purposes.

    Parameters
    ----------
    - `notion_block`    : Notion block to view structure.
    """
    print(f"Printing {notion_block['type']} Notion block")
    print_json(json.dumps(notion_block, indent=2))

def add_children_to_block(
    parent          : dict,
    children        : dict) -> dict:
    """
    Adds children object to dictionary containing a Notion block.

    Parameters
    ----------
    - `parent`      : Notion parent block to append children
    - `children`    :

    Returns
    -------
    Dictionary with Notion format to be used as children
    """

    # Create 'children' key and add block
    if 'children' not in parent[parent['type']]:
        parent[parent['type']]['children'] = [children]
    # If there is already a children in the block, append the new one
    else:
        parent[parent['type']]['children'].append(children)

def append_blocks(
    blocks  : list) -> list:
    """
    Make a children Notion block to be appended to anything (like a page). 

    Parameters
    ----------
    - `blocks`: List of Notion block dictionaries.
    """
    return {
        "children" : [block for block in blocks]
    }

def create_annotations(
    bold            : bool  = False,
    italic          : bool  = False,
    strikethrough   : bool  = False,
    underline       : bool  = False,
    code            : bool  = False,
    color           : str   = 'default' ) -> dict:
    """
    Generates annotations dictionary to apply to rich text objects.

    Parameters
    ----------
    - `bold`: Whether the text is bolded.
    - `italic`: Whether the text is italicized.
    - `strikethrough`: Whether the text is struck through.
    - `underline`: Whether the text is underlined.
    - `code`: Whether the text is code style.
    - `color`: Color of the text. Possible values are:
        - `default`
        - `gray`
        - `brown`
        - `orange`
        - `yellow`
        - `green`
        - `blue`
        - `purple`
        - `pink`
        - `red`
        - `gray_background`
        - `brown_background`
        - `orange_background`
        - `yellow_background`
        - `green_background`
        - `blue_background`
        - `purple_background`
        - `pink_background`
        - `red_background`
    
    Returns
    -------
    Dictionary with annotations for the rich text object.
    """
    return {
        "bold": bold,
        "italic": italic,
        "strikethrough": strikethrough,
        "underline": underline,
        "code": code,
        "color": color
    }

def add_text_to_block(
    content     : str,
    href        : str   = None,
    annotations : dict  = {}) -> dict:
    """
    Create text object to be appended to a Notion block.

    Parameters
    ----------
    - `content`     : Text for the block
    - `href`        : The URL of any link or internal Notion mention in the text, if any.
    - `annotations` : All annotations that apply to the rich text

    Returns
    -------
    Dictionary with the text object for a Notion block.
    """
    return {
        "type": "text",
        "text": {
            "content": content,
            "link": href
        },
        "annotations": {
            "bold": annotations['bold'] if 'bold' in annotations.keys() else False,
            "italic": annotations['italic'] if 'italic' in annotations.keys() else False,
            "strikethrough": annotations['strikethrough'] if 'strikethrough' in annotations.keys() else False,
            "underline": annotations['underline'] if 'underline' in annotations.keys() else False,
            "code": annotations['code'] if 'code' in annotations.keys() else False,
            "color": annotations['color'] if 'color' in annotations.keys() else "default"
        },
        "plain_text": content,
        "href": href
    }

def append_text_to_block(
    notion_block: dict,
    content     : str,
    href        : str   = None,
    annotations : dict  = {}) -> None:
    """
    Append text object to dictionary Notion block.

    Parameters
    ----------
    - `notion_block`: Dictionary with Notion block information.
    - `content`     : Text for the block
    - `href`        : The URL of any link or internal Notion mention in the text, if any.
    - `annotations` : All annotations that apply to the rich text

    Returns
    -------
    Dictionary with the paragraph block.
    """
    block_type = notion_block['type']
    notion_block[block_type]['text'].append(
        add_text_to_block(content, href, annotations)
    )

def paragraph(
    content     : str,
    href        : str   = None,
    annotations : dict  = {}) -> dict:
    """
    Create paragraph Notion block.

    Parameters
    ----------
    - `content`     : Text for the block
    - `href`        : The URL of any link or internal Notion mention in the text, if any.
    - `annotations` : All annotations that apply to the rich text

    Returns
    -------
    Dictionary with the paragraph block.
    """
    return  {
                "object": "block",
                "type": "paragraph",
                "paragraph":{
                    "text":
                    [
                        add_text_to_block(content, href, annotations)
                    ]
                }
            }

def heading(
    heading_num : int,
    content     : str,
    href        : str   = None,
    annotations : dict  = {}) -> dict:
    """
    Create heading Notion block.

    Parameters
    ----------
    - `heading_num` : Either 1, 2 or 3.
    - `content`     : Text for the block
    - `href`        : The URL of any link or internal Notion mention in the text, if any.
    - `annotations` : All annotations that apply to the rich text

    Returns
    -------
    Dictionary with the heading block.
    """
    return  {
                "object": "block",
                "type": f"heading_{heading_num}",
                f"heading_{heading_num}":{
                    "text":
                    [
                        add_text_to_block(content, href, annotations)
                    ]
                }
            } 

def to_do(
    checked     : bool,
    content     : str,
    href        : str   = None,
    annotations : dict  = {}) -> dict:
    """
    Create paragraph Notion block.

    Parameters
    ----------
    - `checked`     : Either True or False.
    - `content`     : Text for the block
    - `href`        : The URL of any link or internal Notion mention in the text, if any.
    - `annotations` : All annotations that apply to the rich text

    Returns
    -------
    Dictionary with the paragraph block.
    """
    return  {
                "object": "block",
                "type": "to_do",
                "to_do":{
                    "text":
                    [
                        add_text_to_block(content, href, annotations)
                    ],
                    "checked" : checked
                }
            }  

def image(
    image_url : str) -> dict:
    """
    Create image Notion block.

    Parameters
    ----------
    - `image_url`   : URL of already uploaded image.

    Notes
    -----
    Supported image URL endings are:
    - `.png`
    - `.jpg`
    - `.jpeg`
    - `.gif`
    - `.tif`
    - `.tiff`
    - `.bmp`
    - `.svg`
    - `.heic`

    Returns
    -------
    Dictionary with the image block.
    """
    return  {
                "object": "block",
                "type": "image",
                "image": {
                    "type": "external",
                    "external": {
                        "url": image_url
                    }
                }
            }  

def toggle(
    content     : str,
    href        : str   = None,
    annotations : dict  = {}) -> dict:
    """
    Create toggle Notion block.

    Parameters
    ----------
    - `content`     : Text for the block
    - `href`        : The URL of any link or internal Notion mention in the text, if any.
    - `annotations` : All annotations that apply to the rich text

    Returns
    -------
    Dictionary with the toggle block.
    """
    return  {
                "object": "block",
                "type": "toggle",
                "toggle":{
                    "text":
                    [
                        add_text_to_block(content, href, annotations)
                    ]
                }
            }

def bulleted_list_item(
    content     : str,
    href        : str   = None,
    annotations : dict  = {}) -> dict:
    """
    Create bulleted list item Notion block.

    Parameters
    ----------
    - `content`     : Text for the block
    - `href`        : The URL of any link or internal Notion mention in the text, if any.
    - `annotations` : All annotations that apply to the rich text

    Returns
    -------
    Dictionary with the bulleted list item block.
    """
    return  {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item":{
                    "text":
                    [
                        add_text_to_block(content, href, annotations)
                    ]
                }
            }

def numbered_list_item(
    content     : str,
    href        : str   = None,
    annotations : dict  = {}) -> dict:
    """
    Create bulleted list item Notion block.

    Parameters
    ----------
    - `content`     : Text for the block
    - `href`        : The URL of any link or internal Notion mention in the text, if any.
    - `annotations` : All annotations that apply to the rich text

    Returns
    -------
    Dictionary with the bulleted list item block.
    """
    return  {
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item":{
                    "text":
                    [
                        add_text_to_block(content, href, annotations)
                    ]
                }
            } 

def quote(
    content     : str,
    href        : str   = None,
    annotations : dict  = {}) -> dict:
    """
    Create quote Notion block.

    Parameters
    ----------
    - `content`     : Text for the block
    - `href`        : The URL of any link or internal Notion mention in the text, if any.
    - `annotations` : All annotations that apply to the rich text

    Returns
    -------
    Dictionary with the quote block.
    """
    return  {
                "object": "block",
                "type": "quote",
                "quote":{
                    "text":
                    [
                        add_text_to_block(content, href, annotations)
                    ]
                }
            } 

def code(
    language    : str,
    content     : str,
    href        : str   = None,
    annotations : dict  = {}) -> dict:
    """
    Create code Notion block.

    Parameters
    ----------
    - `language`    : Coding language in code block.
    - `content`     : Text for the block
    - `href`        : The URL of any link or internal Notion mention in the text, if any.
    - `annotations` : All annotations that apply to the rich text

    Returns
    -------
    Dictionary with the code block.
    """
    supported_languages = ["abap", "arduino", "bash", "basic", "c", "clojure", "coffeescript", "c++", "c#", "css", "dart", "diff", "docker", "elixir", "elm", "erlang", "flow", "fortran", "f#", "gherkin", "glsl", "go", "graphql", "groovy", "haskell", "html", "java", "javascript", "json", "julia", "kotlin", "latex", "less", "lisp", "livescript", "lua", "makefile", "markdown", "markup", "matlab", "mermaid", "nix", "objective-c", "ocaml", "pascal", "perl", "php", "plain text", "powershell", "prolog", "protobuf", "python", "r", "reason", "ruby", "rust", "sass", "scala", "scheme", "scss", "shell", "sql", "swift", "typescript", "vb.net", "verilog", "vhdl", "visual basic", "webassembly", "xml", "yaml", "java/c/c++/c#"]
    
    # If given language is not in supported, raise error.
    try:
        if not language in supported_languages:
            raise AttributeError(f"Language is not supported. Supported languages are: \n{supported_languages}")
    except AttributeError as exc:
        print(exc)
    
    return  {
                "object": "block",
                "type": "code",
                "code":{
                    "text":
                    [
                        add_text_to_block(content, href, annotations)
                    ],
                    "language": language
                }
            } 

def table_of_contents() -> dict:
    """
    Create table of contents Notion block.

    Returns
    -------
    Dictionary with the table of contents block.
    """
    return {
    "type": "table_of_contents",
    "table_of_contents": {}
    }

def divider() -> dict:
    """
    Create divider Notion block.

    Returns
    -------
    Dictionary with divider block.
    """
    return {
    "type": "divider",
    "divider": {}
    }