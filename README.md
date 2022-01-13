# Notion API Python SDK
Basic scripts to automatically upload and update blocks to Notion using Python.

Scripts are based on [notion-sdk-py](https://github.com/ramnes/notion-sdk-py) by Guillaume Gelin ([ramnes](https://github.com/ramnes))

# Usage

When trying to access to any Notion page, database or block, remember to share  
the Notion workspace or page with the Notion Integration created. 

# Known issues
1. When formatting markdown notation for Notion blocks, sometimes the methods  
do not add necessary spaces between words with different formats.
    - E.g. '`inline code` and' leads to '`inline code`and'