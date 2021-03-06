import abc
import json
from typing import Callable

from src.CoAP.constants import *


class Command(metaclass=abc.ABCMeta):
    """
        Clasa abstracta utilizata pentru notiunea de comanda generata de utilizator.
        In functie de tipul comenzii , va fi creata o clasa specifica.
        ( din cele care mostenesc aceasta clasa )
    """

    def __init__(self,call_fct:Callable=None):
        """
           Pentru fiecare din clasele descendent se va atasa o functie de callback ,
           necesara sincronizarii raspunsurilor cu interfata aplicatiei.

           In functie de tipul comenzii, vor mai fi initializate atribute specifice.

            :param call_fct: functie de callback
        """
        self.call_fct=call_fct


    @abc.abstractmethod
    def get_class(self):
        pass


    @abc.abstractmethod
    def get_code(self):
        pass


    @abc.abstractmethod
    def response_needed(self):
        pass


    @abc.abstractmethod
    def payload(self):
        pass

    @abc.abstractmethod
    def parse_response(self, data_from_server):
        """
            Se apeleaza functia de callback atasata cu parametrii corespunzatori
            :param data_from_server: raspunsul ce urmeaza sa fie parsat , pentru actualizarea interfetei
        """
        pass


class detailsCommand(Command):
    """
       Comanda pentru listarea tipului, dimensiunii , caii absolute pentru un fisier/director.
    """

    def __init__(self, pathName: str, call_fct: Callable=None):
        super().__init__(call_fct)
        self.pathName=pathName
        self.mType=TYPE_NON_CON_MSG



    def get_class(self):
        return CLASS_METHOD


    def get_code(self):
        return CODE_GET


    def response_needed(self):
        return True


    def payload(self):
        p={
            "cmd":"details",
            "path":self.pathName
        }

        return json.dumps(p)

    def parse_response(self, data_from_server):
        if self.call_fct:
            self.call_fct(data_from_server)




class createCommand(Command):
    """
        Comanda pentru crearea unui fisier/director.
    """

    def __init__(self, pathName: str, type: str, call_fct: Callable=None):
        super().__init__(call_fct)
        self.pathName=pathName
        self.type=type #file or folder
        self.mType=TYPE_NON_CON_MSG


    def get_class(self):
        return CLASS_METHOD


    def get_code(self):
        return CODE_POST


    def response_needed(self):
        return False


    def payload(self):
        p={
            "cmd":"create",
            "path":self.pathName,
            "type":self.type
        }

        return json.dumps(p)

    def parse_response(self, data_from_server):
        if data_from_server != '':
            status=data_from_server['status']
            if status != 'exists' and status != 'existed':
                if self.call_fct:
                    self.call_fct()



class openCommand(Command):
    """
       Comanda pentru listarea continutului unui fisier/director.

       In cazul in care se executa aceasta comanda pentru un director, browser-ul isi
       va stabili 'current_path' drept calea absoluta a acestuia.
    """

    def __init__(self, openedPathName: str, call_fct: Callable=None):
        super().__init__(call_fct)
        self.openedPathName=openedPathName
        self.mType=TYPE_NON_CON_MSG


    def get_class(self):
        return CLASS_METHOD


    def get_code(self):
        return CODE_GET


    def response_needed(self):
        return True

    def payload(self):
        p={
            "cmd":"open",
            "path":self.openedPathName,
        }

        return json.dumps(p)

    def parse_response(self, data_from_server):
        data_to_parse=data_from_server["response"]
        item_type=data_from_server["type"]
        if self.call_fct:
            self.call_fct(data_to_parse,item_type)


class saveCommand(Command):
    """
       Comanda pentru salvarea continutului unui fisier.
    """

    def __init__(self, savedPathName: str, savedContent: str, call_fct: Callable=None):
        super().__init__(call_fct)
        self.savedPathName=savedPathName
        self.savedContent=savedContent
        self.mType=TYPE_CON_MSG


    def get_class(self):
        return CLASS_METHOD


    def get_code(self):
        return CODE_POST


    def response_needed(self):
        return False

    def payload(self):
        p={
            "cmd":"save",
            "path":self.savedPathName,
            "content":self.savedContent
        }

        return json.dumps(p)

    def parse_response(self, data_from_server):
        if self.call_fct:
            self.call_fct()


class deleteCommand(Command):
    """
       Comanda pentru stergerea unui fisier/director din sistemul de fisiere.
    """

    def __init__(self, deletedPathName: str, call_fct: Callable=None):
        super().__init__(call_fct)
        self.deletedPathName=deletedPathName
        self.mType=TYPE_NON_CON_MSG


    def get_class(self):
        return CLASS_METHOD


    def get_code(self):
        return CODE_POST


    def response_needed(self):
        return False

    def payload(self):
        p={
            "cmd":"delete",
            "path":self.deletedPathName,
        }

        return json.dumps(p)

    def parse_response(self, data_from_server):
        if self.call_fct:
            self.call_fct()


class renameCommand(Command):
    """
       Comanda pentru redenumirea unui fisier/director.
    """

    def __init__(self, path: str, name: str, call_fct: Callable=None):
        super().__init__(call_fct)
        self.path=path
        self.name=name
        self.mType=TYPE_NON_CON_MSG


    def get_class(self):
        return CLASS_METHOD


    def get_code(self):
        return CODE_POST


    def response_needed(self):
        return False

    def payload(self):
        p={
            "cmd":"rename",
            "path":self.path,
            "name":self.name
        }

        return json.dumps(p)

    def parse_response(self, data_from_server):
        if self.call_fct:
            self.call_fct()


class moveCommand(Command):
    """
        Comanda pentru mutarea unui fisier/director intr-o locatie diferita in cadrul FS.
    """

    def __init__(self, sourcePath: str, destinationPath: str, call_fct: Callable=None):
        super().__init__(call_fct)
        self.sourcePath=sourcePath
        self.destinationPath=destinationPath
        self.mType=TYPE_NON_CON_MSG


    def get_class(self):
        return CLASS_METHOD


    def get_code(self):
        return CODE_POST


    def response_needed(self):
        return False

    def payload(self):
        p={
            "cmd":"move",
            "path":self.sourcePath,
            "new_path":self.destinationPath
        }

        return json.dumps(p)

    def parse_response(self, data_from_server):
        if self.call_fct:
            self.call_fct()



class searchCommand(Command):
    """
       Comanda pentru cautarea dupa nume/nume_partial a unui element din FS.
    """

    def __init__(self, searchedPathName: str, targetName: str, call_fct: Callable=None):
        super().__init__(call_fct)
        self.searchedPathName=searchedPathName  #va fi mereu current_path
        self.targetName=targetName
        self.mType=TYPE_NON_CON_MSG


    def get_class(self):
        return CLASS_METHOD


    def get_code(self):
        return CODE_SEARCH


    def response_needed(self):
        return True

    def payload(self):
        p={
            "cmd":"search",
            "path":self.searchedPathName,
            "target_name_regex":self.targetName

        }

        return json.dumps(p)

    def parse_response(self, data_from_server):
        results=data_from_server["results"]
        print(results)
        if self.call_fct:
            self.call_fct(results)