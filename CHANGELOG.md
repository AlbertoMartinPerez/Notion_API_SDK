# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com).

## [0.0.3] - 2022-01-14
### Changed
- Updates in `blocks.py`:
    - Updated the `_clean_markdown()` method to use `markdown_delimiter`  
    list by adding extra spaces. Previously, it used `clean_delimiter` list.
    - `_add_block_format()` method now accepts `block_type` adn `block_field`  
    parameters to support any Notion block.

### Deleted
- Updates in `blocks.py`:
    - Deleted `clean_delimiter` variable list, which was the same as  
    `markdown_delimiter` but with added spaces for each element.

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
