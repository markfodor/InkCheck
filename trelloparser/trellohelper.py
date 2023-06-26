from trello import TrelloClient
from logger.logger import logger


class TrelloHelper:

    def __init__(self, api_key, token):
        self.client = TrelloClient(api_key, None, token, None)

    def get_data(self, board_name, list_name):
        boards = self.client.search(board_name, True, ['boards'])

        if not boards:
            logger.error(f"No match found for board name: {board_name}")
            return []
        if len(boards) > 1:
            logger.error(f"More than one match found for board name: {board_name}")
            return [] 

        # "There can be only one"
        selected_board = boards[0]

        # these are a columns on the board
        lists = selected_board.all_lists()
        for trello_list in lists:
            if list_name == trello_list.name:
                selected_list = trello_list

        # cards in the column
        cards = selected_list.list_cards()
        cards_names = []
        for card in cards:
            cards_names.append(card.name)

        logger.info('Data collection from Trello is done.')
        return cards_names
