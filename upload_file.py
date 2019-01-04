from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload

def saveImage(fileName):
    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    SCOPES = 'https://www.googleapis.com/auth/drive.file'
    store = file.Storage('storage.json')
    creds = store.get()

    if not creds or creds.invalid:
        print("make new storage data file ")
        flow = client.flow_from_clientsecrets('client_secret2.json', SCOPES)
        creds = tools.run_flow(flow, store, flags) \
            if flags else tools.run(flow, store)

    DRIVE = build('drive', 'v3', http=creds.authorize(Http()))

    file_name = 'test.jpg'
    file_metadata = \
        {
        'name': fileName,
        'parents' : 'kakao'
                     }
    media = MediaFileUpload(fileName,
                            mimetype='image/jpeg')
    fileId = DRIVE.files().create(body=file_metadata,
                                media_body=media).execute()
    print('File ID: %s' % fileId.get('id'))
    return fileId.get('id')