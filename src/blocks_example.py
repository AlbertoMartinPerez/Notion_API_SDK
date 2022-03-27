#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Notion block creations and data upload to Dropbox for external links

    -------------------------------------------------------------------------
    AUTHOR

    Name:       Alberto Martín Pérez
    Contact:    alberto.martinperez@protonmail.com      

    ------------------------------------------------------------------------
    SUMMARY

    This file shows how to create Notion blocks and append them to an existing  
    Notion page. It also shows how to upload files from a local directory to  
    Dropbox and then extract the raw shared links to be used in Notion blocks.

   """

from notion_client import Client
from secrets import NOTION_TOKEN, DROPBOX_TOKEN

import blocks, pages
from helpers import(
  add_annotations
)
from markdown_parser import markdown_to_notion
from dropbox_sdk import DropboxClient

import datetime
import os

from rich import print_json
import json

def main():

  notion = Client(auth = NOTION_TOKEN)
  #*************
  #* NOTION IDS
  #*************
  page_id         = "4a1ddb9c3d08409e9775d1c49212be19"
  block_id        = "55793819476e42f5b53d5af5b1c24056"

  #**************************************
  #* RETRIEVE NOTION BLOCK TO SEE FORMAT 
  #**************************************

  # block_retrieved = notion.blocks.retrieve(block_id)

  # blocks.print_block(block_retrieved)

  #**************************
  #* UPLOAD IMAGES TO DROPBOX
  #**************************
  timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

  dropbox = DropboxClient(DROPBOX_TOKEN)

  raw_file_urls = dropbox.upload_all_files(
    dropbox_dir = '',
    local_dir   = "./example_files/",
    folder_dir  = f"{os.path.splitext(os.path.basename(__file__))[0]}_{timestamp}"
  )
  
  print(f"Printing raw file URLs: {raw_file_urls}")
  raw_file_keys = list(raw_file_urls.keys())


  #************************
  #* APPEND BLOCKS TO PAGE
  #************************

  # Create a table of contents block
  block_table_of_contents = blocks.table_of_contents()

  # Create a divider block
  block_divider = blocks.divider()

  # Create block as heading 1
  block_heading_1 = blocks.heading(
      heading_num = 1,
      content     = "This is a header",
      href        = None,
      annotations = add_annotations
      (
        color         = "yellow_background"
      )
  )

  # Create block as paragraph
  block_paragraph_1 = blocks.paragraph(
    content     = "This is paragraph 1 text",
    annotations = {"bold" : True}
  )

  # Create block as paragraph
  block_paragraph_2 = blocks.paragraph(
    content     = "This is paragraph 2 text",
    annotations = {"italic" : True}
  )

  # Create block as to-do
  block_todo = blocks.to_do(
    checked     = False,
    content     = "To-do task",
    annotations = add_annotations
      (
        bold          = True,
        code          = True
      )
  )

  # Create code block
  block_code = blocks.code(
    language  = 'python',
    content   = 'print(This is a code block example)'
  )

  # Create numbered list item block
  block_number_list_1 = blocks.numbered_list_item(
    content   = 'This is the first block of a numbered list item',
    annotations = add_annotations
      (
        bold          = True,
      )
  )

  # Create numbered list item block
  block_number_list_2 = blocks.numbered_list_item(
    content   = 'This is the second block of a numbered list item',
    annotations = add_annotations
      (
        bold          = True,
      )
  )
  
  # Create quote block
  block_quote = blocks.quote(
    content   = 'This is a quote block',
    annotations = add_annotations
      (
        italic          = True,
      )
  )

  # Create toggle block
  block_toggle = blocks.toggle(
    content   = 'This is a toggle block',
    annotations = add_annotations
      (
        bold          = True,
      )
  )

  # Append number list items inside thte toggle block
  blocks.add_children(parent = block_toggle, children = block_number_list_1)
  blocks.add_children(parent = block_toggle, children = block_number_list_2)

  blocks.add_children(parent = block_paragraph_2, children = block_todo)

  # Create emoji callout block
  block_callout_emoji = blocks.callout(
    icon_type   = 'emoji',
    icon_str    = "🐶",
    content     = 'This is a callout with emoji icon created from Python',
    href        = None,
    annotations = add_annotations(
      bold = True
    )
  )

  # Create callout block with external icon
  block_callout_external = blocks.callout(
    icon_type   = 'external',
    icon_str    = "https://img.icons8.com/ios/250/000000/barcode.png",
    content     = 'This is a callout with external icon created from Python',
    href        = None,
    annotations = add_annotations(
      bold = True
    )
  )

  # Create image block from image uploaded to Dropbox
  block_image = blocks.image(image_url = raw_file_urls[raw_file_keys[-1]])

  blocks.add_children(parent = block_callout_emoji, children = block_image)

  # Create equation block
  block_equation = blocks.equation(
    expression  = "\\frac{{ - b \pm \sqrt {b^2 - 4ac} }}{{2a}}"
  )

  # Make a children block with the previous blocks to be appended to page
  nested_blocks = blocks.append_blocks([block_table_of_contents, block_divider, block_heading_1, block_paragraph_1, block_paragraph_2, block_code, block_quote, block_toggle, block_callout_emoji, block_callout_external, block_equation])

  updated_block = notion.blocks.children.append(page_id, **nested_blocks)

  # print(f"Printing received block: \n")
  # print_block(updated_block)


  #*******************************
  #* CREATE BLOCKS USING MARKDOWN
  #*******************************

  notion_blocks = markdown_to_notion(
    "#This is a `code heading` with markdown _italics_\n'Quote block\n+Bullet list\n>**Toggle** `with inline code` :\nThis is simple text **with bolded words**, _italic words_, `inline code` and ~strikethrough~\n[]This is a **to-do** made with markdown"
  )

  # print_block(updated_block)

  # Make a children block with the markdown text 
  payload = blocks.append_blocks(notion_blocks)

  updated_block = notion.blocks.children.append(page_id, **payload)

  # print_block(updated_block)


if __name__ == "__main__":
  main()