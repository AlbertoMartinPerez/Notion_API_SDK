# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com).

## [0.0.2] - 2022-01-13
### Added
- Added `formated_notion_text_example.py` file to see how a Notion block  
with annotations is formated.

- Updates in `blocks.py`:
    - Added the following methods to start Mardown notation support:
        - `_clean_markdown()`
        - `_markdown_splitter()`
        - `_add_block_format()`
        - `_markdown_notation()`
    - Added `add_text_to_block()` method to add text object to a Notion  
    block.
    - Added `append_text_to_block()` method to append text object to a  
    Notion block.

### Changed
- Updates in `blocks.py`:
    - `markdown_to_notion()` method can create paragraph Notion blocks with  
    annotations. Future versions will add annotations to more blocks.
    - The methods to create Notion blocks (`image()`, `to_do()`, `heading()`  
    and `paragraph()`) now use the new method `add_text_to_block()`to add  
    text object to a block.

- Now `notion.py` shows how to use markdown notation in a string for a Notion  
block.

## [0.0.1] - 2022-01-08
### Added
- Added initial files to start working

### Changed

### Removed
