import gkeepapi
from logger.logger import logger


class googleKeepHelper:

    def __init__(self, mail, password):
        self.client = gkeepapi.Keep()
        successful_login = self.client.login(mail, password)
        if(successful_login):
            logger.info('Google Keep login was succesful.')
        else:
            logger.error('Google Keep login failed.')

    def get_items_on_note_by_note_id(self, note_id, only_unchecked): 
        note = self.client.get(note_id)
        items = []

        if isinstance(note, gkeepapi.node.List):
            for item in note.items:
                if not only_unchecked or not item.checked:
                    items.append(item.text)

            logger.info('Data collection from Google Keep is done.')
            return True, items
        # assuming it is a simple text note
        else:
            return False, note.text
        

    def search_note_id(self, name):
        notes = self.client.all()
        for note in notes:
            # google sometimes stores the titles with leading spaces
            if note.title.strip() == name:
                return note.id
        return None

    def search_note_id_by_name(self, name, only_unchecked):
        noteId = self.search_note_id(name)
        if not noteId:
            logger.error(f"Note not found with name: {name}")
        else:
            return self.get_items_on_note_by_note_id(noteId, only_unchecked)
