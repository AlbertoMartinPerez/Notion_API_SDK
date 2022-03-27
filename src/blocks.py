#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Notion blocks creation for Python

    -------------------------------------------------------------------------
    AUTHOR

    Name:       Alberto Martín Pérez
    Contact:    alberto.martinperez@protonmail.com      

    ------------------------------------------------------------------------
    SUMMARY

    This file includes some Notion blocks as dictionaries for Python. They can
    be used with the [notion-sdk-py](https://github.com/ramnes/notion-sdk-py) created by Guillaume Gelin ([ramnes](https://github.com/ramnes)
    Additionally, it provides further functionalities to print blocks and see their  
    structure, add children blocks to parent blocks and append blocks.  
   """

from rich import print_json
import json

from helpers import (
    add_icon, add_rich_text
)

#*****************************
#* NOTION SDK FUNCTIONALITIES
#*****************************
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

def add_children(
    parent          : dict,
    children        : dict) -> dict:
    """
    Adds children object to dictionary containing a Notion block.

    Parameters
    ----------
    - `parent`      : Notion parent block to append children.
    - `children`    : Notion children block to append.

    Returns
    -------
    Dictionary with Notion format to be used as children
    """
    # List of Notion blocks that support children objects
    support_children = [
        'paragraph', 
        'bulleted_list_item', 
        'numbered_list_item', 
        'toggle', 
        'to_do', 
        'quote', 
        'callout', 
        'synced_block', 
        'template', 
        'column', 
        'child_page', 
        'child_database', 
        'header_1', 
        'header_2', 
        'header_3', 
        'table'
    ]

    # Check if parent block type can support children
    if parent['type'] in support_children:
        # Create 'children' key and add block
        if 'children' not in parent[parent['type']]:
            parent[parent['type']]['children'] = [children]
        # If there is already a children in the block, append the new one
        else:
            parent[parent['type']]['children'].append(children)

def append_blocks(
    blocks  : list) -> dict:
    """
    Create a children object. It consists of an array of Notion block objects
    (or dictionaries). Useful when appending a set of blocks to anything like  
    a Notion page.

    Parameters
    ----------
    - `blocks`: List of Notion block dictionaries.

    Return
    ------
    Dictionary with `children` key and an array of Notion dictionary blocks.
    """
    return {
        "children" : [block for block in blocks]
    }

def append_rich_text(
    notion_block: dict,
    content     : str,
    href        : str   = None,
    annotations : dict  = {}) -> None:
    """
    Append rich text object to dictionary Notion block.
    Mainly used for the Notion markdown parser.

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
        add_rich_text(content, href, annotations)
    )


#**************************
#* SUPPORTED NOTION BLOCKS
#**************************

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
                        add_rich_text(content, href, annotations)
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
                        add_rich_text(content, href, annotations)
                    ]
                }
            } 

def callout(
    icon_type   : str,
    icon_str    : str   = "💡",
    content     : str   = None,
    href        : str   = None,
    annotations : dict  = {}) -> dict:
    """
    Create callout Notion block.
    Please note that it is not possible to change the color of the entire callout block
    through the Notion API. Only for the text inside.

    Parameters
    ----------
    - `icon_type`   : Type of icon. Valid options are `emoji` or `external` for URL image.
    - `icon_str`    : Emoji string or external link.
    - `content`     : Text for the block.
    - `href`        : The URL of any link or internal Notion mention in the text, if any.
    - `annotations` : All annotations that apply to the rich text.

    Returns
    -------
    Dictionary with the callout block.
    """
    return  {
                "object": "block",
                "type": "callout",
                "callout": {
                    "text": [
                        add_rich_text(content, href, annotations)
                    ],
                    "icon" : add_icon(icon_type, icon_str)
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
                        add_rich_text(content, href, annotations)
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
                        add_rich_text(content, href, annotations)
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
                        add_rich_text(content, href, annotations)
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
                        add_rich_text(content, href, annotations)
                    ],
                    "checked" : checked
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
                        add_rich_text(content, href, annotations)
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
                        add_rich_text(content, href, annotations)
                    ],
                    "language": language
                }
            } 

# TODO: Implement
def child_page(
    ) -> dict:
    """
    """
    pass

# TODO: Implement
def child_database(
    ) -> dict:
    """
    """
    pass

def embed(
    url : str) -> dict:
    """
    Create embed Notion block.

    Parameters
    ----------
    - `url`   : Link to website the embed block will display.

    Returns
    -------
    Dictionary with the image block.
    """
    return  {
                "object": "block",
                "type": "embed",
                "embed": {
                    "url": url
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

def video(
    url : str) -> dict:
    """
    Create a video Notion block.

    Parameters
    ----------
    - `url`   : Link to video file reference.

    Returns
    -------
    Dictionary with the video block.
    """
    return  {
                "object": "block",
                "type": "video",
                "video": {
                    "type": "external",
                    "external": {
                        "url": url
                    }
                }
            } 

def file(
    url         : str,
    caption     : str,
    content     : str,
    href        : str   = None,
    annotations : dict  = {}) -> dict:
    """
    Create a file Notion block.

    Parameters
    ----------
    - `url`         : Link to file reference.
    - `caption`     : Caption of the file block.
    - `content`     : Text for the block
    - `href`        : The URL of any link or internal Notion mention in the text, if any.
    - `annotations` : All annotations that apply to the rich text

    Returns
    -------
    Dictionary with the file block.
    """
    return  {
                "object": "block",
                "type": "file",
                "file": {
                    "type": "external",
                    "external": {
                        "url": url
                    },
                    "text":
                    [
                        add_rich_text(content, href, annotations)
                    ],
                },
                "caption" : caption
            }

def pdf(
    url : str) -> dict:
    """
    Create a pdf Notion block.

    Parameters
    ----------
    - `url`   : Link to pdf file reference.

    Returns
    -------
    Dictionary with the pdf block.
    """
    return  {
                "object": "block",
                "type": "pdf",
                "pdf": {
                    "type": "external",
                    "external": {
                        "url": url
                    }
                }
            }   

def bookmark(
    url         : str,
    caption     : str,
    content     : str,
    href        : str   = None,
    annotations : dict  = {}) -> dict:
    """
    Create a bookmark Notion block.

    Parameters
    ----------
    - `url`         : Link to bookmark file reference.
    - `caption`     : Caption of the bookmark file block.
    - `content`     : Text for the block
    - `href`        : The URL of any link or internal Notion mention in the text, if any.
    - `annotations` : All annotations that apply to the rich text

    Returns
    -------
    Dictionary with the bookmark block.
    """
    return  {
                "object": "block",
                "type": "bookmark",
                "bookmark": {
                    "type": "external",
                    "external": {
                        "url": url
                    },
                    "text":
                    [
                        add_rich_text(content, href, annotations)
                    ],
                },
                "caption" : caption
            } 

def equation(
    expression : str) -> dict:
    """
    Create an equation Notion block.

    Parameters
    ----------
    - `expression`   : A KaTeX compatible string.

    Returns
    -------
    Dictionary with the equation block.
    """
    return  {
                "object": "block",
                "type": "equation",
                "equation": {
                    "expression": expression
                }
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

def breadcrumb() -> dict:
    """
    Create breadcrumb Notion block.

    Returns
    -------
    Dictionary with breadcrumb block.
    """
    return {
    "type": "breadcrumb",
    "breadcrumb": {}
    }

# TODO: Implement
def columns(
    ) -> dict:
    """
    """
    pass

#?: Should be implemented? They are only returned as a response and cannot be created via de API.
def child_database(
    ) -> dict:
    """
    """
    pass

# TODO: Implement
def template(
    ) -> dict:
    """
    """
    pass

# TODO: Implement
def link_to_page(
    ) -> dict:
    """
    """
    pass

# TODO: Implement
def synced_block(
    ) -> dict:
    """
    """
    pass

# TODO: Implement
def table(
    ) -> dict:
    """
    """
    pass

# TODO: Implement
def table_row(
    ) -> dict:
    """
    """
    pass
