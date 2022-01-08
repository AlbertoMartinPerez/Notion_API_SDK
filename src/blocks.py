
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

def annotations(
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

def paragraph(
    content     : str,
    plain_text  : str   = "",
    link        : str   = None,
    href        : str   = None,
    annotations : dict  = {}) -> dict:
    """
    Create paragraph Notion block.

    Parameters
    ----------
    - `content`     : Text for the block
    - `plain_text`  : The plain text without annotations for the rich text object
    - `link`        : Link for the rich block obkect
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
                        {
                            "type": "text",
                            "text": {
                            "content": content,
                            "link": link
                            },
                            "annotations": {
                            "bold": annotations['bold'] if 'bold' in annotations.keys() else False,
                            "italic": annotations['italic'] if 'italic' in annotations.keys() else False,
                            "strikethrough": annotations['strikethrough'] if 'strikethrough' in annotations.keys() else False,
                            "underline": annotations['underline'] if 'underline' in annotations.keys() else False,
                            "code": annotations['code'] if 'code' in annotations.keys() else False,
                            "color": annotations['color'] if 'color' in annotations.keys() else "default"
                            },
                            "plain_text": plain_text,
                            "href": href
                        }
                    ]
                }
            }

def heading(
    heading_num : int,
    content     : str,
    plain_text  : str   = "",
    link        : str   = None,
    href        : str   = None,
    annotations : dict  = {}) -> dict:
    """
    Create heading Notion block.

    Parameters
    ----------
    - `heading_num` : Either 1, 2 or 3.
    - `content`     : Text for the block
    - `plain_text`  : The plain text without annotations for the rich text object
    - `link`        : Link for the rich block obkect
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
                        {
                            "type": "text",
                            "text": {
                            "content": content,
                            "link": link
                            },
                            "annotations": {
                            "bold": annotations['bold'] if 'bold' in annotations.keys() else False,
                            "italic": annotations['italic'] if 'italic' in annotations.keys() else False,
                            "strikethrough": annotations['strikethrough'] if 'strikethrough' in annotations.keys() else False,
                            "underline": annotations['underline'] if 'underline' in annotations.keys() else False,
                            "code": annotations['code'] if 'code' in annotations.keys() else False,
                            "color": annotations['color'] if 'color' in annotations.keys() else "default"
                            },
                            "plain_text": plain_text,
                            "href": href
                        }
                    ]
                }
            } 

def to_do(
    checked     : bool,
    content     : str,
    plain_text  : str   = "",
    link        : str   = None,
    href        : str   = None,
    annotations : dict  = {}) -> dict:
    """
    Create paragraph Notion block.

    Parameters
    ----------
    - `checked`     : Either True or False.
    - `content`     : Text for the block
    - `plain_text`  : The plain text without annotations for the rich text object
    - `link`        : Link for the rich block obkect
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
                        {
                            "type": "text",
                            "text": {
                            "content": content,
                            "link": link
                            },
                            "annotations": {
                            "bold": annotations['bold'] if 'bold' in annotations.keys() else False,
                            "italic": annotations['italic'] if 'italic' in annotations.keys() else False,
                            "strikethrough": annotations['strikethrough'] if 'strikethrough' in annotations.keys() else False,
                            "underline": annotations['underline'] if 'underline' in annotations.keys() else False,
                            "code": annotations['code'] if 'code' in annotations.keys() else False,
                            "color": annotations['color'] if 'color' in annotations.keys() else "default"
                            },
                            "plain_text": plain_text,
                            "href": href
                        }
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

def markdown_to_notion(
    text : str) -> list:
    """
    Converts a text with markdown format to a list of Notion blocks.

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
                notion_block = heading(heading_num = heading_num, content = text)
            
            # Check if block should be a to-do
            elif md_block in ['[]']:
                notion_block = to_do(checked = False, content = text)

        # Create a Notion paragraph block instead 
        else:
            notion_block = paragraph(content = block)   # Since this is a paragraph, block only contains text
        
        notion_blocks.append(notion_block)

    return notion_blocks