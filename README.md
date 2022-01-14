# Notion API Python SDK
Basic scripts to automatically upload and update blocks to Notion using Python.

Scripts are based on [notion-sdk-py](https://github.com/ramnes/notion-sdk-py) by Guillaume Gelin ([ramnes](https://github.com/ramnes))

# Usage

When trying to access to any Notion page, database or block, remember to share  
the Notion workspace or page with the Notion Integration created. 

## Markdown
It is necessary to use the `markdown_to_notion()` method with strings containing markdown  
delimiters.

### For text formatting
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

### Creating Notion blocks
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

# Issues

## Known issues

## Solved issues
1. **[SOLVED IN 0.0.3]** When formatting markdown notation for Notion blocks, sometimes the methods  
do not add necessary spaces between words with different formats.
    - E.g. '`inline code` and' leads to '`inline code`and'