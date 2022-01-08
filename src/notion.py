import requests
import json
from notion_client import Client
from secrets import NOTION_TOKEN, IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET

from rich import print_json

import pyimgur  # To upload images to Imgur

from blocks import *

def upload_to_imgur(
  file_path : str) -> str:
  """
  Upload local image to Imgur.

  Parameters
  ----------
  - `file_path`: Path in disk memory of image to upload.

  Returns
  -------
  Imgur URL of the uploaded image. 
  """
  im = pyimgur.Imgur(IMGUR_CLIENT_ID)

  uploaded_image = im.upload_image(file_path, title="Uploaded with PyImgur")
  print(uploaded_image.title)
  print(uploaded_image.link)
  print(uploaded_image.size)
  print(uploaded_image.type)

  return uploaded_image.link

def main():
  #*************
  #* NOTION IDS
  #*************
  database_id     = "9810f5a2b05f4e0c90588b51a2d46152"
  page_id         = "4a1ddb9c3d08409e9775d1c49212be19"

  notion = Client(auth = NOTION_TOKEN)


  #************************
  #* UPLOAD IMAGE TO IMGUR
  #************************
  PATH_IMAGE = f''
  # image_url = upload_to_imgur(file_path = PATH_IMAGE)


  #************************
  #* APPEND BLOCKS TO PAGE
  #************************
  # Create block as heading 1
  block_heading_1 = heading(
      heading_num = 1,
      content     = "This is a header",
      plain_text  = "Plain text",
      link        = None,
      href        = None,
      annotations = annotations
      (
        color         = "yellow_background"
      )
  )

  # Create block as paragraph
  block_paragraph_1 = paragraph(
    content     = "This is paragraph 1 text",
    annotations = {"bold" : True}
  )

  # Create block as paragraph
  block_paragraph_2 = paragraph(
    content     = "This is paragraph 2 text",
    annotations = {"italic" : True}
  )

  # Create block as to-do
  block_todo = to_do(
    checked     = False,
    content     = "To-do task",
    annotations = annotations
      (
        bold          = True,
        code          = True
      )
  )

  # Create image block
  image_url = "https://i.imgur.com/ijckbLX.png"
  block_image = image(image_url = image_url)

  # Make a children block with the previous blocks to be appended to page
  nested_blocks = make_children([block_heading_1, block_paragraph_1, block_paragraph_2, block_todo, block_image])

  updated_block = notion.blocks.children.append(page_id, **nested_blocks)

  # print(f"Printing received block: \n")
  # print_json(json.dumps(updated_block, indent=2))


  #*******************************
  #* CREATE BLOCKS USING MARKDOWN
  #*******************************

  notion_blocks = markdown_to_notion(
    "# This is a heading with markdown\nThis should be a simple paragraph\n[] This is a to-do made with markdown"
  )

  # Make a children block with the markdown text 
  payload = make_children(notion_blocks)

  updated_block = notion.blocks.children.append(page_id, **payload)

  # print(f"Printing received block: \n")
  # print_json(json.dumps(updated_block, indent=2))


if __name__ == "__main__":
  main()