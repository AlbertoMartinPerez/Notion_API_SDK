#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Notion Python SDK helper functions 

    -------------------------------------------------------------------------
    AUTHOR

    Name:       Alberto Martín Pérez
    Contact:    alberto.martinperez@protonmail.com      

    ------------------------------------------------------------------------
    SUMMARY

    This file includes functions when creating Notion dictionary blocks or pages.
    They can be used with the [notion-sdk-py](https://github.com/ramnes/notion-sdk-py) 
    created by Guillaume Gelin ([ramnes](https://github.com/ramnes).
      
   """

from ctypes import Union


def get_page_id(
    link : str) -> str:
    """
    Get page ID from Notion URL.

    Example
    -------
    >>> link = https://www.notion.so/Page-Title-7a5ddb2c3d48314e9775d2c49212be12
    >>> print(get_page_id(link))
    7a5ddb2c3d48314e9775d2c49212be12
    """
    return link.split('-')[-1]

def add_cover(
    url) -> dict:
    """
    Adds cover to any Notion dictionary.

    Parameters
    ----------
    - `url`   : External URL image for cover or `None` if no cover wants to be added.

    Returns
    -------
    Dictionary with cover object.
    """
    if isinstance(url, None): return None
    elif isinstance(url, str): return {
        "type": "external",
        "external": {
        "url": url
        }
    }

def add_icon(
    icon_type   : str,
    icon_str    : str) -> dict:
    """
    Adds icon to any Notion dictionary.

    Parameters
    ----------
    - `icon_type`   : Type of icon. Valid options are `emoji` or `external` for URL image.
    - `icon_str`    : Emoji string or external link.

    Returns
    -------
    Dictionary with an icon object.
    """
    supported_icon_types = ['emoji', 'external']

    # Check if input icon type is supported
    if icon_type in supported_icon_types:

        if icon_type == 'emoji':
            return {
                    "type": icon_type,
                    icon_type : icon_str
                }
        elif icon_type == 'external':
            return {
                    "type": icon_type,
                    icon_type : {
                        'url' : icon_str
                    }
                }
    else:
        print(f"Incorrect icon_type. It should be 'emoji' o 'external'. Provided {icon_type}")
        return None

def add_rich_text(
    content     : str,
    href        : str   = None,
    annotations : dict  = {}) -> dict:
    """
    Create rich text object to be appended to a Notion dictionary.

    Parameters
    ----------
    - `content`     : Text for the block
    - `href`        : The URL of any link or internal Notion mention in the text, if any.
    - `annotations` : All annotations that apply to the rich text

    Returns
    -------
    Dictionary with the text object for a Notion dictionary.
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

def add_annotations(
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
