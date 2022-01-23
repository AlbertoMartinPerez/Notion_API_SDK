# About
- Notion API Python SDK is a list of basic scripts to upload and update blocks  
to Notion using Python.

- Scripts are based on [notion-sdk-py](https://github.com/ramnes/notion-sdk-py) by Guillaume Gelin ([ramnes](https://github.com/ramnes)),  
which manages the communication with Notion through its API.  

- This repository adds the following functionalities:
    - ✔️ **An easy way to build blocks** supported by the Notion API as well as  
    text formatting for those blocks.
    - ✔️ Provide a **markdown parser** to create Notion blocks.
    - ✔️ Simply functionality to **upload external files to Dropbox**, extract  
    their raw shared link URL to be used in blocks such as `image`, `video`,  
    `file`, `embed` or any that supports adding external links.  
    _(Please note that Notion API does not allow to upload files directly.)_

# Table of contents
1. [Notion requirements](#notion-requirements)
2. [Notion blocks for Python](#notion-blocks-for-python)
3. [Additional Notion SDK functionalities](#additional-notion-sdk-functionalities)
4. [Markdown parser](#markdown-parser)
5. [Dropbox requirements](#dropbox-requirements)
6. [Dropbox functionalities](#dropbox-functionalities)

# Notion requirements
## Python API package
Install the python package [notion-sdk-py](https://github.com/ramnes/notion-sdk-py) created by Guillaume Gelin ([ramnes](https://github.com/ramnes)) by running:  
`pip install notion-client` - or - `pythonX.Y -m pip install notion-client`  
(where `X.Y` correspond to the Python version you want to install the package in).

## Create Notion integration
1. Create a free Notion account.
2. Login to Notion and go to the workspace you want your intergration to be. Then,  
in the left tab go to **Settings & Members** > **Workspace** > **Integrations**.
3. Press the **Develop your own integrations** option, which will redirect you to a new page.
4. Press the **New integration** button. Then:
    1. Give it a name and upload a logo if desired.
    2. Associate the integration to your desired Notion workspace.
    3. Check all **Content Capabilities** (_**Read content**_, _**Update content**_ and  
    _**Insert content**_).
    4. Set the **User Capabilities** to any option.
    5. Afterwards, press the **Submit** button.
5. Access your to your created integration site and generate or copy the token from  
**Internal Integration Token**. Then paste it in the `NOTION_TOKEN` inside  
`secrets.py`. (_Simply create a copy of the `secrets_template.py` file_)

## Share page to Notion integration
To correctly access, append or modify data in a Notion page, you first have to share it  
with the created integration. To do so:
1. Go to the page you want to add information and press **Share** on the right top corner.
2. Press the **Invite** button and select your integration.
3. Then press the 3 horizontal dots **···** on the right top corner. Select **Copy link**  
and paste it somewhere. Then just extract the latest characters from the latest `-` separator.
Finally, use that as the `page_id` for the Notion page to add information to.
    - Example:
    ```
    https://www.notion.so/3-Aproximaci-n-2-ff80bb15e4f24a7daa729da24bf8177b
                         Start of page ID {*******************************}
    ```

# Notion blocks for Python
Currently the `blocks.py` provide Python dictionaries for the Notion blocks  
included in the table below. For further information, you can visit the official  
Notion API block reference using the links in the table. If you want to know  
how to create this blocks in Python, open the `notion.py` file for examples.

|    Notion block    | Support |
|:------------------:|:-------:|
|      [paragraph](https://developers.notion.com/reference/block#paragraph-blocks)     |    ✔️    |
|      [heading 1](https://developers.notion.com/reference/block#heading-one-blocks)     |    ✔️    |
|      [heading 2](https://developers.notion.com/reference/block#heading-two-blocks)     |    ✔️    |
|      [heading 3](https://developers.notion.com/reference/block#heading-three-blocks)     |    ✔️    |
|       [callout](https://developers.notion.com/reference/block#callout-blocks)      |    ✔️    |
|        [quote](https://developers.notion.com/reference/block#quote-blocks)       |    ✔️    |
| [bulleted_list_item](https://developers.notion.com/reference/block#bulleted-list-item-blocks) |    ✔️    |
| [numbered_list_item](https://developers.notion.com/reference/block#numbered-list-item-blocks) |    ✔️    |
|        [to_do](https://developers.notion.com/reference/block#to-do-blocks)       |    ✔️    |
|       [toggle](https://developers.notion.com/reference/block#toggle-blocks)       |    ✔️    |
|        [code](https://developers.notion.com/reference/block#code-blocks)        |    ✔️    |
|     [child_page](https://developers.notion.com/reference/block#child-page-blocks)     |    ❌    |
|   [child_database](https://developers.notion.com/reference/block#child-database-blocks)   |    ❌    |
|        [embed](https://developers.notion.com/reference/block#embed-blocks)       |    ✔️    |
|        [image](https://developers.notion.com/reference/block#image-blocks)       |    ✔️    |
|        [video](https://developers.notion.com/reference/block#video-blocks)       |    ✔️    |
|        [file](https://developers.notion.com/reference/block#file-blocks)        |    ✔️    |
|         [pdf](https://developers.notion.com/reference/block#pdf-blocks)        |    ✔️    |
|      [bookmark](https://developers.notion.com/reference/block#bookmark-blocks)      |    ✔️    |
|      [equation](https://developers.notion.com/reference/block#equation-blocks)      |    ✔️    |
|       [divider](https://developers.notion.com/reference/block#divider-blocks)      |    ✔️    |
|  [table_of_contents](https://developers.notion.com/reference/block#table-of-contents-blocks) |    ✔️    |
|     [breadcrumb](https://developers.notion.com/reference/block#breadcrumb-blocks)     |    ✔️    |
|       [columns](https://developers.notion.com/reference/block#column-list-and-column-blocks)       |    ❌    |
|    [link_preview](https://developers.notion.com/reference/block#link-preview-blocks)    |    ❓    |
|      [template](https://developers.notion.com/reference/block#template-blocks)      |    ❌    |
|    [link_to_page](https://developers.notion.com/reference/block#link-to-page-blocks)    |    ❌    |
|    [synced_block](https://developers.notion.com/reference/block#synced-block-blocks)    |    ❌    |
|        [table](https://developers.notion.com/reference/block#table-blocks)       |    ❌    |
|      [table_row](https://developers.notion.com/reference/block#table-row-blocks)     |    ❌    |

# Additional Notion SDK functionalities
_(All these functionalities can be found inside `blocks.py`)_
- Print with indents a dictionary Notion block for readability purposes using  
the `print_block()` function.
- Adds children object to dictionary containing a Notion block using the  
`add_children_to_block()` function.
- Make a children Notion block to be appended to anything (like a page) using  
the `append_blocks()` function.


# Markdown parser
⚠️ **WARNING**: Please note that the parser might not add every functionality.  
It is necessary to use the `markdown_to_notion()` method with strings containing markdown  
delimiters.

## For text formatting
⚠️ **WARNING**: Future versions will accept [slash commands](https://cheatsheets.namaraii.com/notion.html)
Use any delimiter in both sides of the text to format.
| Delimiter |  Format description |
|:---------:|:-------------------:|
|     **    |   **Bold text**     |
|     _     |    _Italic text_    |
|     ~     |~~Strikethrough tex~~|
|     \`    |    `Inline code`    |

```python
# Right way to create formatted text
notion_blocks = markdown_to_notion("**This is bolded text** and this is not")

# Wrong ways to create formatted text
notion_blocks = markdown_to_notion("# This is a heading")
notion_blocks = markdown_to_notion("#This is a heading #")
```

## Creating Notion blocks
For the **heading** (`#`, `##`, `###`) and **to-do** (`[]`) blocks, only add delimiter at the  
begining.

**To separate blocks**, use the `\n` delimiter.

```python
# Right way to create heading block
notion_blocks = markdown_to_notion("#This is a heading\n[]This is a to-do block")

# Wrong ways to create heading block
notion_blocks = markdown_to_notion("# This is a heading\n []This is a to-do block")
notion_blocks = markdown_to_notion("#This is a heading #\n []This is a to-do block[]")
```

# Dropbox requirements
## Python API package
Install the python package for the Dropbox API by running:  
`pip install dropbox` - or - `pythonX.Y -m pip install dropbox`  
(where `X.Y` correspond to the Python version you want to install the package in).

## Developer app
To interact with Dropbox, you first need to create an app inside. To do so:  
1. Create a free Dropbox account (with 2Gb os storage) or a paid account.
2. Go to [the developer website page](https://www.dropbox.com/developers/apps) and press **Create app**. Then:
    1. **Choose an API**: Select _Scoped access_.
    2. **Choose the type of access you need**: Select **App folder** (recommended) or  
    **Full Dropbox**.
    3. **Name your app**: Provide a name for the application.
3. Once the developer app is ready, access its page and configure the **Permissions** tab.
    - It is recommended to **check all `*.write` permissions** from **Account Info**,  
    **Files and folders** and **Collaboration** sections.
4. Go to the **Settings** tab and generate an **OAuth 2** token.
    - It is recommended to set the **Access token expiration** to _No expiration_.
5. Copy and secure the generated token. Then paste it in the `DROPBOX_TOKEN` inside  
`secrets.py`. (_Simply create a copy of the `secrets_template.py` file_)

# Dropbox functionalities
With the `dropbox_sdk.py` file you can create an instance of `DropboxClient` to:  
- View all files in a Dropbox directory using the `view_files()` method.  
- Upload all files included in a local path using the `upload_all_files()` method.  
Additionally, this function returns a dictionary with the name of each file  
uploaded with its corresponding raw share link from Dropbox (to be used for  
Notion blocks). 
