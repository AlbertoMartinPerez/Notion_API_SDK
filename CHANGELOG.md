# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com).

## [1.0.2] - 2022-3-27
### Added
- Added examples on how to use blocks:
    - `blocks_example.py`

## [1.0.1] - 2022-01-23
### Added
- In `blocks.py`:
    - Added `add_icon()` method to include either an `emoji` or `external`  
    icon to a Notion rich object.
    - Support to new Notion blocks:
        - `callout`
- In `notion_example.py` added how to construct `callout` blocks.
- In `dropbox_sdk.py` added the `create_folder()` method to create a folder  
inside Dropbox.

### Deleted
- In `dropbox_sdk.py`:
    - The `view_files()` method.

### Changed
- Fixed `upload_all_files()` method from `DropboxClient` class in  
`dropbox_sdk.py` to support more file extensions.
- In `blocks.py`, `add_children()` method now checks if parent block  
support appending children blocks.

## [1.0.0] - 2022-01-22
- First major version because, why not? :)
### Added
- Support to new Notion blocks:
    - `embed`
    - `video`
    - `file`
    - `pdf`
    - `bookmark`
    - `equation`
    - `breadcrumb`

### Changed
- `notion.py` is now called `notion_example.py`.
- `dropbox_api.py` is now called `dropbox_sdk.py`.
- `markdown.py` is now called `markdown_parser.py`.

## [0.0.5] - 2022-01-21
### Added
- `markdown.py` to isolate all markdown parsing functionalities in a single file.
- `dropbox_api.py` to upload files to Dropbox and retrieve raw shared links  
to be used as embedded into Notion.
- `example_files` folder with sample images to be uploaded to Dropbox.

### Changed
- Updates in `blocks.py`:
    - Minor text modifications.
    - Added more blocks.
- Updates in `notion.py`:
    - Included example to know how to upload images to Dropbox and create  
    Notion image blocks from Dropbox URLs.
    - Updated method names to comply with modifications in `blocks.py`.
- In `secrets_template.py` Deleted IMGUR tokens to Dropbox app token.

## [0.0.4] - 2022-01-14
### Changed
- Updates in `blocks.py`:
    - Updated the `_clean_markdown()` to exclude comas next to delimiters.
- Updates in `notion.py`:
    - Do not use \ to separate a string into multiple lines. It will result in  
    multiple spaces in the Notion block.

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
