import re
from typing import Any   # To split delimiters from text

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
    '[]'    # To-do block
]


def make_children(
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
    text    : str) -> list:
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
    list_str    : list[str],
    block_type  : str,
    block_field : Any = None) -> dict:
    """
    Create Notion block with annotations based on Markdown notation.
    Only supports paragraph Notion blocks. 
    
    Parameters
    ----------
    - `list_str`    : List of strings with the text that may containg markdown notation    
    - `block_type`  : Type of Notion block to be created
    - `block_field` : Extra field for the specific Notion block type. Depends on the `block_type` to be created.

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
                block = paragraph(
                            content     = string,
                            annotations = create_annotations(
                                bold = bold,
                                italic = italic,
                                strikethrough = strikethrough,
                                code = code
                            )
                        )
            elif block_type == "to_do":
                block = to_do(
                            checked     = block_field,
                            content     = string,
                            annotations = create_annotations(
                                bold = bold,
                                italic = italic,
                                strikethrough = strikethrough,
                                code = code
                            )
                        )
            elif block_type == "heading":
                block = heading(
                            heading_num = block_field,
                            content     = string,
                            annotations = create_annotations(
                                bold = bold,
                                italic = italic,
                                strikethrough = strikethrough,
                                code = code
                            )
                        )

        # Append to paragraph block text with specific annotations if any
        else:
            append_text_to_block(
                notion_block    = block,
                content         = string,
                annotations     = create_annotations(
                                    bold = bold,
                                    italic = italic,
                                    strikethrough = strikethrough,
                                    code = code
                                )
            )

    return block

def _markdown_notation(
    text        : str,
    block_type  : str,
    block_field : Any = None) -> dict:
    """
    Analyze text and splits it by any markdown notation accepted in Notion.
    Returns a ready to use Notion block with formated text.

    Only creates paragraph Notion blocks!

    Parameters
    ----------
    - `text`: String with markdown format to be converted to Notion blocks.

    Returns
    -------
    Dict with formated Notion block.

    Notes
    -----
    >>> markdown_delimiter = {
    >>>     '**',   # Bold text
    >>>     '_',    # Italic text
    >>>     '`',    # Inline code
    >>>     '~',    # Strikethrough text
    >>>     '#',    # Heading 1 block
    >>>     '##',   # Heading 2 block
    >>>     '###',  # Heading 3 block
    >>>     '[]'    # To-do block
    >>> }
    """
    splitted_text = _markdown_splitter(text)
    
    _clean_markdown(splitted_text)

    notion_block = _add_block_format(splitted_text, block_type, block_field)

    return notion_block
    


def markdown_to_notion(
    text : str) -> list:
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
    """
    notion_blocks = []

    # Defined functions that support certain Notion blocks
    supported_blocks = {
        '#'     : 'heading_1', 
        '##'    : 'heading_2',
        '###'   : 'heading_3',
        '[]'    : 'to_do'
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

        # Create a Notion paragraph block instead 
        else:
            notion_block = _markdown_notation(block, "paragraph")    # Since this is a paragraph, block only contains text
        
        notion_blocks.append(notion_block)

    return notion_blocks