#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Dropbox SDK using the Dropbox API in Python

    -------------------------------------------------------------------------
    AUTHOR

    Name:       Alberto Martín Pérez
    Contact:    alberto.martinperez@protonmail.com      

    ------------------------------------------------------------------------
    SUMMARY

    This file includes the functionality to view all files from a Dropbox  
    directory, upload all files from a local path and retrieve a dictionary  
    with the name of the uploaded file as key and its raw shared link URL as  
    value.
   """

from typing import List
import dropbox
from dropbox import exceptions, sharing
import os

class DropboxClient():

    def __init__(self, APP_TOKEN) -> None:
        self.dbx = self.__authenticate(APP_TOKEN)   # Dropbox connection
    
    def __authenticate(self, APP_TOKEN):
        try:
            return dropbox.Dropbox(APP_TOKEN)

        except dropbox.auth.AuthError as err:
            print(err)

    def view_files(
        self,
        dir : str = '') -> None:
        """
        Lists information of every file in specific `dir`.
        """
        #* List in directory all files
        dir = ''
        data = self.dbx.files_list_folder( path=dir )

        for entry in data.entries:
            if hasattr(entry, 'shared_folder_id'):
                print(entry.name+'/')
            else:
                print(f"File name: {entry.name} \t File size: {entry.size}")

            file = f'/{entry.name}'
            file_metadata = self.dbx.files_get_metadata(path=file)
            server_rev = file_metadata.rev
            server_modified = file_metadata.server_modified
            print('file modifed: ' + server_modified.strftime("%m/%d/%y") + ' | file revision: ' + server_rev)

    @staticmethod
    def get_raw_url(url : str) -> str:
        """
        Add /raw/ to URL to directly access the file without the Dropbox preview.

        Parameters
        ----------
        - `url`:    Dropbox shared link URL.

        Return
        ------
        Raw URL to access file without Dropbox preview.
        """
        # Check if given URL is from Dropbox
        if 'www.dropbox.com/s/' in url:
            splitted_url = url.split('/s/')
            return f"{splitted_url[0]}/s/raw/{splitted_url[1]}"
        else:
            print(f"Given URL is not from Dropbox.")

    def upload_all_files(
        self,
        dropbox_dir : str,
        local_dir   : str) -> List[str]:
        """
        Uploads all files from local directory to an specific Dropbox directory.
        Returns a list with raw shared links for every file uploaded.

        ONLY SUPPORTS `.png` FILES!

        Parameters
        ----------
        - `dropbox_dir`:    Dropbox directory to upload the files.
        - `local_dir`:      Local directory with files to upload.

        Returns
        -------
        A list with raw shared links for every file uploaded.
        """
        raw_urls = []

        # Get all files and directories
        for dir, dirs, files in os.walk(local_dir):
            # Upload the file and get the shared link to be embedded into Notion
            for file in files:
                # Check if file is an image
                if '.png' in file:
                    try:
                        print(f"Uploading local file ({local_dir+file}) to ({dropbox_dir+file})")

                        with open(f"{local_dir}{file}", 'rb' ) as f:
                            self.dbx.files_upload(f=f.read(), path=f"{dropbox_dir}/{file}", mode=dropbox.files.WriteMode.overwrite, mute=True)

                    except exceptions.ApiError as err:
                        print(f"Uploading file {file} failed with errpr: {err}")
                    
                    # Get file URL
                    try:
                        shared_link_metadata = self.dbx.sharing_create_shared_link_with_settings(f"{dropbox_dir}/{file}")
                        file_url = self.get_raw_url(shared_link_metadata.url)
                        raw_urls.append(file_url)

                    except exceptions.ApiError as err:
                        # Check if file share link already exists
                        if err.error.is_shared_link_already_exists():
                            print(f"Error: Shared link already exists!")
                            print(f"Returning existing shared link...")
                            shared_link_exists : sharing.SharedLinkAlreadyExistsMetadata = err.error.get_shared_link_already_exists()
                            if shared_link_exists.is_metadata():
                                shared_link_metadata = shared_link_exists.get_metadata()
                                file_url = self.get_raw_url(shared_link_metadata.url)
                                raw_urls.append(file_url)
        
        return raw_urls

if __name__ == "__main__":
    #**************************
    #* UPLOAD IMAGES TO DROPBOX
    #**************************
    from secrets import DROPBOX_TOKEN
    dbx = DropboxClient(DROPBOX_TOKEN)
    dbx.view_files('')
    raw_file_urls = dbx.upload_all_files(
        dropbox_dir = '',
        local_dir   = "./example_files/"
    )
    print(f"Printing raw file URLs: {raw_file_urls}")