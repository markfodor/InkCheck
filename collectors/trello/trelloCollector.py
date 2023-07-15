import pathlib
from trello import TrelloClient
from logger.logger import logger
from model.columnData import ColumnData
from util.configHelper import read_config
from collectors.abstractBaseCollector import AbstractBaseCollector


class TrelloCollector(AbstractBaseCollector):

    def __init__(self):
        config = read_config(str(pathlib.Path(__file__).parent.absolute()))

        if config:
            self.key = config['key']
            self.token = config['token']
            self.board = config['board']
            self.data_list = config['list']

            logger.info('Trello config is set.')
        else:
            logger.error('Error occured while setting Trello config.')
            return

        self.client = TrelloClient(self.key, None, self.token, None)

    def get_data(self) -> ColumnData:
        boards = self.client.search(self.board, True, ['boards'])

        if not boards:
            logger.error(f"No match found for board name: {self.board}")
            return []
        if len(boards) > 1:
            logger.error(f"More than one match found for board name: {self.board}")
            return [] 

        # "There can be only one" in the result set
        selected_board = boards[0]
        data: ColumnData = ColumnData(title=self.board, is_list=True)

        # these are a columns on the board
        lists = selected_board.all_lists()
        for trello_list in lists:
            if self.data_list == trello_list.name:
                selected_list = trello_list

        # cards in the column
        cards = selected_list.list_cards()
        # cards_names = []
        for card in cards:
            # cards_names.append(card.name)
            data.items.append(card.name)

        logger.info('Data collection from Trello is done.')
        return data
