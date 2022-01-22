#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Markdown parser for Notion API in Python

    -------------------------------------------------------------------------
    AUTHOR

    Name:       Alberto Martín Pérez
    Contact:    alberto.martinperez@protonmail.com      

    ------------------------------------------------------------------------
    SUMMARY

    This file includes the functionality to parse markdown format text to  
    Notion blocks. You can format text and create multiple formatted Notion  
    blocks with a single string. 
   """

import re
from typing import Any   # To split delimiters from text

import blocks

# TODO: Add slash commands: https://cheatsheets.namaraii.com/notion.html

# There is no delimiter for underline text
# use delimiters on either side
markdown_delimiter = [
    '**',   # Bold text
    '_',    # Italic text
    '~',    # Strikethrough text
    '`',    # Inline code
    '#',    # Heading 1 block
    '##',   # Heading 2 block
    '###',  # Heading 3 block
    '[]',   # To-do block
    '>',    # Toggle block
    '+',    # Bullet list item block
    '\''    # Quote block
]

def _clean_markdown(
    list_str    : list[str]) -> None: 
    """
    Erase delimiters from list of strings and empty strings.

    Parameters
    ----------
    - `list_str`: List of strings with markdown notations. (Usually obtained after using
    `_markdown_splitter()`)
    """
    # For every string, search the delimiter to remove. Then update the string from the list
    for count, string in enumerate(list_str):
        #for delimiter in clean_delimiter:
        for delimiter in markdown_delimiter:
            # Check if a coma ',' was used after a markdown delimiter and also remove delimiter
            if f"{delimiter}," in string: list_str[count] = string.replace(f"{delimiter},", ',')

            # Delete delimiter in the string which has and space on the right
            if f"{delimiter} " in string: list_str[count] = string.replace(f"{delimiter} ", ' ') # Add an space
    
def _markdown_splitter(
    text        : str) -> list:
    """
    Analyze text and splits it by any markdown notation accepted in Notion.
    The splitted text contains makdown delimiters with spaces in unwanted strings.
    Therefore, the returned list should me cleaned using the `_clean_markdown` method.

    Parameters
    ----------
    - `text`: String with markdown format to be converted to Notion blocks.

    Returns
    -------
    Splitted text using the delimiters in a list.

    Notes
    -----
    - `**`: On either side for bold text
    - `_`:  On either side for italic text
    - ` :   On either side for inline code
    - `~`:  On either side for strikethrough text

    Solution based on: https://www.delftstack.com/howto/python/how-to-split-string-with-multiple-delimiters-in-python/
    and also: https://stackoverflow.com/questions/4998629/split-string-with-multiple-delimiters-in-python
    """
    regular_exp = '|'.join('(?={})'.format(re.escape(delim)) for delim in markdown_delimiter)
    return re.split(regular_exp, text)

def _add_block_format(
    list_str        : list[str],
    block_type      : str,
    special_field   : Any = None) -> dict:
    """
    Create Notion block with annotations based on Markdown notation.
    Only supports paragraph Notion blocks. 
    
    Parameters
    ----------
    - `list_str`        : List of strings with the text that may containg markdown notation    
    - `block_type`      : Type of Notion block to be created
    - `special_field`   : Extra field for the specific Notion block type. Depends on the `block_type` to be created.

    """

    for count, string in enumerate(list_str):
        # Reset format for every string
        bold = italic = strikethrough = code = False

        for delimiter in markdown_delimiter:
            # Check if delimiter is in the string
            if delimiter in string:

                # Remove markdown delimiter for the string
                string = string.replace(delimiter, '')

                # Create block format depending on the delimiter found
                if delimiter == '**': bold = True

                elif delimiter == '_': italic = True

                elif delimiter == '~': strikethrough = True

                elif delimiter == '`': code = True

        # If this is the first string, create a paragraph block
        if count == 0:

            if block_type == "paragraph":
                block = blocks.paragraph(
                            content     = string,
                            annotations = blocks.create_annotations(
                                bold = bold,
                                italic = italic,
                                strikethrough = strikethrough,
                                code = code
                            )
                        )
            elif block_type == "to_do":
                block = blocks.to_do(
                            checked     = special_field,
                            content     = string,
                            annotations = blocks.create_annotations(
                                bold = bold,
                                italic = italic,
                                strikethrough = strikethrough,
                                code = code
                            )
                        )
            elif block_type == "heading":
                block = blocks.heading(
                            heading_num = special_field,
                            content     = string,
                            annotations = blocks.create_annotations(
                                bold = bold,
                                italic = italic,
                                strikethrough = strikethrough,
                                code = code
                            )
                        )
            elif block_type == "toggle":
                block = blocks.toggle(
                            content     = string,
                            annotations = blocks.create_annotations(
                                bold = bold,
                                italic = italic,
                                strikethrough = strikethrough,
                                code = code
                            )
                        )
            elif block_type == "bulleted_list_item":
                block = blocks.bulleted_list_item(
                            content     = string,
                            annotations = blocks.create_annotations(
                                bold = bold,
                                italic = italic,
                                strikethrough = strikethrough,
                                code = code
                            )
                        )
            elif block_type == "quote":
                block = blocks.quote(
                            content     = string,
                            annotations = blocks.create_annotations(
                                bold = bold,
                                italic = italic,
                                strikethrough = strikethrough,
                                code = code
                            )
                        )

        # Append to paragraph block text with specific annotations if any
        else:
            blocks.append_text_to_block(
                notion_block    = block,
                content         = string,
                annotations     = blocks.create_annotations(
                                    bold = bold,
                                    italic = italic,
                                    strikethrough = strikethrough,
                                    code = code
                                )
            )

    return block

def _markdown_notation(
    text            : str,
    block_type      : str,
    special_field   : Any = None) -> dict:
    """
    Analyze text and splits it by any markdown notation accepted in Notion.
    Returns a ready to use Notion block with formated text.

    Only creates paragraph Notion blocks!

    Parameters
    ----------
    - `list_str`        : List of strings with the text that may containg markdown notation    
    - `block_type`      : Type of Notion block to be created
    - `special_field`   : Extra field for the specific Notion block type. Depends on the `block_type` to be created.

    Returns
    -------
    Dict with formated Notion block.
    """
    splitted_text = _markdown_splitter(text)
    
    _clean_markdown(splitted_text)

    notion_block = _add_block_format(splitted_text, block_type, special_field)

    return notion_block
    
def markdown_to_notion(
    text        : str) -> list:
    """
    Converts a text with markdown format to a list of Notion blocks.

    Supports text formatting for paragraph blocks only!

    Parameters
    ----------
    - `text`: Notion blocks in string should be separated by `\\n`
        - Example:
        >>> text = "# Heading 1\\nThis is a paragraph"
    
    Notes
    -----
    This function does not support text format style, such as bold, italic or code.
    Supported Notion blocks are:
        - `heading_1`
        - `heading_2`
        - `heading_3`
        - `to_do`
        - `toggle`
        - `bulleted_list_item`
        - `quote`
    """
    notion_blocks = []

    # Defined functions that support certain Notion blocks
    supported_blocks = {
        '#'     : 'heading_1', 
        '##'    : 'heading_2',
        '###'   : 'heading_3',
        '[]'    : 'to_do',
        '>'     : 'toggle',
        '+'     : 'bulleted_list_item',
        '\''     : 'quote'
    }
    markdown_blocks = list(supported_blocks.keys())
    
    # Split each block from the text string
    for block in text.split("\n"):

        mask = [character in block for character in markdown_blocks]   # Mask to know which markdown notation has been used for the block

        # Check for any block different from paragrap
        if True in mask:
            
            md_block = [b for a, b in zip(mask, markdown_blocks) if a][-1] # Get the corresponding markdown notation
            text = block.split(f"{md_block} ")[-1]  # Extract text

            # Check if block should be a Heading
            if md_block in ['#', '##', '###']:
                heading_num = int(supported_blocks[md_block].split('_')[-1])
                notion_block = _markdown_notation(block, "heading", heading_num)
            
            # Check if block should be a to-do
            elif md_block in ['[]']:
                # notion_block = to_do(checked = False, content = text)
                notion_block = _markdown_notation(block, "to_do", False)
            
            # Check if block should be a toggle
            elif md_block in ['>']:
                # notion_block = to_do(checked = False, content = text)
                notion_block = _markdown_notation(block, "toggle")
            
            # Check if block should be a bulleted list item
            elif md_block in ['+']:
                # notion_block = to_do(checked = False, content = text)
                notion_block = _markdown_notation(block, "bulleted_list_item")
            
            # Check if block should be a bulleted list item
            elif md_block in ['\'']:
                # notion_block = to_do(checked = False, content = text)
                notion_block = _markdown_notation(block, "quote")

        # Create a Notion paragraph block instead 
        else:
            notion_block = _markdown_notation(block, "paragraph")    # Since this is a paragraph, block only contains text
        
        notion_blocks.append(notion_block)

    return notion_blocks
