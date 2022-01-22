import requests
from notion_client import Client
from secrets import NOTION_TOKEN, DROPBOX_TOKEN

import blocks
from markdown_parser import markdown_to_notion
from dropbox_sdk import DropboxClient

def main():
  #*************
  #* NOTION IDS
  #*************
  database_id     = "9810f5a2b05f4e0c90588b51a2d46152"
  page_id         = "4a1ddb9c3d08409e9775d1c49212be19"
  block_id        = "73e88d7bbc6d4125936482ecb71dd26b"

  notion = Client(auth = NOTION_TOKEN)

  #**************************************
  #* RETRIEVE NOTION BLOCK TO SEE FORMAT 
  #**************************************

  # block_retrieved = notion.blocks.retrieve('f9ae26d4c9674122acc435909c5f350c')

  # blocks.print_block(block_retrieved)

  #***********************************************
  #* RETRIEVE NOTION CHILDREN BLOCK TO SEE FORMAT 
  #***********************************************

  # children_block_retrieved = notion.blocks.children.list(block_id)
  # blocks.print_block(children_block_retrieved)

  #**************************
  #* UPLOAD IMAGES TO DROPBOX
  #**************************
  dropbox = DropboxClient(DROPBOX_TOKEN)
  dropbox.view_files('')
  raw_file_urls = dropbox.upload_all_files(
    dropbox_dir = '',
    local_dir   = "./example_files/"
  )
  print(f"Printing raw file URLs: {raw_file_urls}")


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
      annotations = blocks.create_annotations
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
    annotations = blocks.create_annotations
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
    annotations = blocks.create_annotations
      (
        bold          = True,
      )
  )

  # Create numbered list item block
  block_number_list_2 = blocks.numbered_list_item(
    content   = 'This is the second block of a numbered list item',
    annotations = blocks.create_annotations
      (
        bold          = True,
      )
  )
  
  # Create quote block
  block_quote = blocks.quote(
    content   = 'This is a quote block',
    annotations = blocks.create_annotations
      (
        italic          = True,
      )
  )

  # Create toggle block
  block_toggle = blocks.toggle(
    content   = 'This is a toggle block',
    annotations = blocks.create_annotations
      (
        bold          = True,
      )
  )

  # Create image block from image uploaded to Dropbox
  block_image = blocks.image(image_url = raw_file_urls[0])

  # Append number list items inside thte toggle block
  blocks.add_children_to_block(parent = block_toggle, children = block_number_list_1)
  blocks.add_children_to_block(parent = block_toggle, children = block_number_list_2)

  blocks.add_children_to_block(parent = block_paragraph_2, children = block_todo)

  # Make a children block with the previous blocks to be appended to page
  nested_blocks = blocks.append_blocks([block_table_of_contents, block_divider, block_heading_1, block_paragraph_1, block_paragraph_2, block_code, block_quote, block_toggle, block_image])

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