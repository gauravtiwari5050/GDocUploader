'''
Created on 26-Jun-2011

@author: gauravt
'''



import gdata.docs.service
import gdata.docs.data
import gdata.docs.client
import os
import mimetypes
import getpass
import sys

client = gdata.docs.client.DocsClient(source='alld-docsync-v1')
client.ssl = True
client.http_client.debug = False

def Login():
    email = raw_input("Email:")
    password = getpass.getpass()
     
    print password
    client = gdata.docs.client.DocsClient(source='alld-docsync-v1')
    client.ssl = True
    client.http_client.debug = False
    client.ClientLogin(email,password,client.source)
    
    return client
    
def UploadFile(client,filesystem_path,destination_filename,folder):
    ms = gdata.data.MediaSource(file_path=filesystem_path,content_type=mimetypes.guess_type(filesystem_path)[0])
    try:
        if folder == None:
            print 'Uploading ',filesystem_path,'to root'
            entry = client.Upload(ms,destination_filename)
        else:
            print 'Uploading ',filesystem_path,'to ',folder.title.text
            entry = client.Upload(ms,destination_filename,folder_or_uri=folder)
        
            print filesystem_path,'uploaded to', entry.GetAlternateLink().href
    except Exception as e:
            print filesystem_path,' could not be uploaded .Skipping'
    

def CreateFolder(client,folder_name,parent_folder):
    if parent_folder == None:
        print 'Creating a folder as roots child'
        new_folder = client.Create(gdata.docs.data.FOLDER_LABEL, folder_name)
        print 'Folder "%s" created' % new_folder.title.text
        return new_folder
    else:
        print 'Creating folder as a child of ',parent_folder.title.text.encode('UTF-8')
        sub_folder = client.Create(gdata.docs.data.FOLDER_LABEL, folder_name, folder_or_id=parent_folder)
        print 'Folder "%s" created' % sub_folder.title.text
        return sub_folder
        
def UploadFolder(file_system_folder,destination_folder):
    if os.path.basename(file_system_folder).startswith('.') == True:
        print 'Hidden folder.Not Uploading'
        return
    print 'Uploading folder ',file_system_folder
    files = os.listdir(file_system_folder)
    for filename in files:
        if os.path.isfile(os.path.join(file_system_folder,filename)) == True:
            print 'uploading ',os.path.join(file_system_folder, filename),'as',filename
            UploadFile(client, os.path.join(file_system_folder, filename), filename, destination_folder)
        else:
            print 'creating subfolder',filename
            subfolder = CreateFolder(client, filename, destination_folder)
            UploadFolder(os.path.join(file_system_folder, filename), subfolder)

try:
    client = Login()
except Exception as e:
    print 'Login failed.Exiting'
    exit
upload_root = raw_input('File/dir to be uploaded')
if os.path.exists(upload_root) == False:
    print upload_root,' does not exist.Exiting'
    exit
if os.path.isfile(upload_root) == True:
    UploadFile(client, upload_root, os.path.basename(upload_root), None)
else:
    root = CreateFolder(client,os.path.basename(upload_root), None)
    UploadFolder(upload_root, root)


