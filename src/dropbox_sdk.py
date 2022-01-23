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

    def create_folder(
        self,
        path        : str,
        autorename  : bool) -> None:
        """
        Creates a folder in a specific Dropbox directory using the 
        `files_create_folder_v2()` method.

        Parameters
        ----------
        - `path`:       Path in the user’s Dropbox to create.
        - `autorename`: If there’s a conflict, have the Dropbox server try to autorename the folder to avoid the conflict.
        """
        try:
            self.dbx.files_create_folder_v2(
                path        = f"{path}",
                autorename  = autorename
            )
        except exceptions.ApiError as err:
            print(f"Error creating folder {path}. See error for details:\n{err}")

    def upload_all_files(
        self,
        dropbox_dir : str,
        local_dir   : str,
        folder_dir  : str) -> dict:
        """
        Uploads all files from local directory to an specific folder directory
        inside a Dropbox directory.
        Returns a list with raw shared links for every file uploaded.

        ONLY SUPPORTS `.json`, `.txt`, `.png`, `.log` FILES!

        Parameters
        ----------
        - `dropbox_dir`:    Dropbox directory to upload the files and create new folders.
        - `local_dir`:      Local directory with files to upload.
        - `folder_dir`:     Name of the new folder to upload the files

        Returns
        -------
        A dict with raw shared links as values for every file uploaded as keys.
        """
        extension_support = [
            '.json', 
            '.txt', 
            '.png', 
            '.log'
            ]

        raw_urls = {}

        # Create folder to upload all files
        root_folder = f"{dropbox_dir}/{folder_dir}"
        self.create_folder(
            path        = root_folder,
            autorename  = False
        )


        # Get all files and directories
        for dir, dirs, files in os.walk(local_dir):

            # Upload the file and get the shared link to be embedded into Notion
            for file in files:

                abs_dir     = os.path.abspath(dir)
                abs_file    = os.path.join(abs_dir, file)

                # Check if file extension is supported
                if f".{file.split('.')[-1]}" in extension_support:
                    try:
                        print(f"Uploading local file ({abs_file}) to ({dropbox_dir}/{folder_dir}/{file})")
                        with open(f"{abs_file}", 'rb' ) as f:
                            self.dbx.files_upload(f=f.read(), path=f"{dropbox_dir}/{folder_dir}/{file}", mode=dropbox.files.WriteMode.overwrite, mute=True)

                    except exceptions.ApiError as err:
                        print(f"Uploading file {file} failed with error: {err}")
                    
                    # Get file URL
                    try:
                        shared_link_metadata = self.dbx.sharing_create_shared_link_with_settings(f"{dropbox_dir}/{folder_dir}/{file}")
                        file_url = self.get_raw_url(shared_link_metadata.url)
                        # Create key in dictionary with file name and raw URL as value
                        if file not in raw_urls: 
                            raw_urls[file] = file_url
                        # If key exists, then just append the raw URL
                        else:
                            raw_urls[file].append(file_url)

                    except exceptions.ApiError as err:
                        # Check if file share link already exists
                        if err.error.is_shared_link_already_exists():
                            print(f"\tError: Shared link already exists! Returning existing shared link...")
                            shared_link_exists : sharing.SharedLinkAlreadyExistsMetadata = err.error.get_shared_link_already_exists()
                            if shared_link_exists.is_metadata():
                                shared_link_metadata = shared_link_exists.get_metadata()
                                file_url = self.get_raw_url(shared_link_metadata.url)
                                # Create key in dictionary with file name and raw URL as value
                                if file not in raw_urls: 
                                    raw_urls[file] = file_url
                                # If key exists, then just append the raw URL
                                else:
                                    raw_urls[file].append(file_url)
        
        return raw_urls


if __name__ == "__main__":
    import datetime
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    #**************************
    #* UPLOAD IMAGES TO DROPBOX
    #**************************
    from secrets import DROPBOX_TOKEN
    dbx = DropboxClient(DROPBOX_TOKEN)
    
    raw_file_urls = dbx.upload_all_files(
        dropbox_dir = '',
        local_dir   = "./example_files/",
        folder_dir  = f"{os.path.splitext(os.path.basename(__file__))[0]}_{timestamp}"
    )
    print(f"Printing raw file URLs: {raw_file_urls}")