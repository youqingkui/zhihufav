#!/usr/bin/env python
#coding=utf-8

import requests
import hashlib
import evernote.edam.type.ttypes as Types
from evernote.api.client import EvernoteClient



class EvernoteMethod():

    def __init__(self):
        pass

    @staticmethod
    def makeNote(noteStore, noteTitle, noteBody, sourceUrl='', resources=[], parentNotebook=None):
        nBody = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
        nBody += "<!DOCTYPE en-note SYSTEM \"http://xml.evernote.com/pub/enml2.dtd\">"
        nBody += "<en-note>" + noteBody +  "</en-note>"
        print(nBody)
        ## Create note object
        ourNote = Types.Note()
        ourNote.title = noteTitle
        ourNote.content = nBody

        if resources:
            ourNote.resources = resources

        if sourceUrl:
            note_attrs = Types.NoteAttributes()
            note_attrs.sourceURL = sourceUrl
            ourNote.attributes = note_attrs

        ## parentNotebook is optional; if omitted, default notebook is used
        if parentNotebook and hasattr(parentNotebook, 'guid'):
            ourNote.notebookGuid = parentNotebook.guid

        ## Attempt to create note in Evernote account
        note = noteStore.createNote(ourNote)
            ## Something was wrong with the note data
            ## See EDAMErrorCode enumeration for error code explanation
            ## http://dev.evernote.com/documentation/reference/Errors.html#Enum_EDAMErrorCode
            ## Parent Notebook GUID doesn't correspond to an actual notebook
        ## Return created note object
        return note

    @staticmethod
    def getNoteStore(token):

        client = EvernoteClient(token=token, sandbox=False)
        client.service_host = 'app.yinxiang.com'
        noteStore = client.get_note_store()
        return noteStore


    @staticmethod
    def getRemoteRes(url_list):
        ressource_list = []
        for url in url_list:
            res = requests.get(url)
            content = res.content
            md5 = hashlib.md5()
            md5.update(content)
            hash = md5.digest()

            data = Types.Data()
            data.size = len(content)
            data.bodyHash = hash
            data.body = content

            resource = Types.Resource()
            resource.mime = res.headers['Content-Type'].split(';')[0]
            resource.data = data

            ressource_list.append(resource)

        return ressource_list


        # pool = Pool(8)
        # results = pool.map(requests.get, url_list)
        # for res in results:
        #     content = res.content
        #     md5 = hashlib.md5()
        #     md5.update(content)
        #     hash = md5.digest()
        #
        #     data = Types.Data()
        #     data.size = len(content)
        #     data.bodyHash = hash
        #     data.body = content
        #
        #     resource = Types.Resource()
        #     resource.mime = res.headers['Content-Type'].split(';')[0]
        #     resource.data = data
        #
        #     ressource_list.append(resource)

