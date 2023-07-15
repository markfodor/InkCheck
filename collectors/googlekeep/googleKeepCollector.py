import pathlib
import gkeepapi
from logger.logger import logger
from model.columnData import ColumnData
from util.configHelper import read_config
from collectors.abstractBaseCollector import AbstractBaseCollector


class GoogleKeepCollector(AbstractBaseCollector):

    def __init__(self):
        config = read_config(str(pathlib.Path(__file__).parent.absolute()))

        if config:
            self.username = config['username']
            self.password = config['password']
            self.node_name = config['nodeName']
            self.only_unchecked_items = config['onlyUncheckedItems']

            logger.info('Google Keep config is set.')
        else:
            logger.error('Error occured while setting Google Keep config.')
            return 

        self.client = gkeepapi.Keep()
        successful_login = self.client.login(self.username, self.password)
        if(successful_login):
            logger.info('Google Keep login was succesful.')
        else:
            logger.error('Google Keep login failed.')

    def _get_items_on_node_by_node_id(self, node_id):
        node = self.client.get(node_id)

        if isinstance(node, gkeepapi.node.List):
            data: ColumnData = ColumnData(title=self.node_name, is_list=True)
            for item in node.items:
                if not self.only_unchecked_items or not item.checked:
                    data.items.append(item.text)

            logger.info('Data collection from Google Keep is done.')
            return data
        # assuming it is a simple text node
        else:
            data: ColumnData = ColumnData(title=self.node_name, is_list=False)
            data.text = node.text
            return data
        

    def _search_node_id(self, name):
        nodes = self.client.all()
        for node in nodes:
            # Google sometimes stores the titles with leading spaces
            if node.title.strip() == name:
                return node.id
        return None

    def get_data(self) -> ColumnData:
        nodeId = self._search_node_id(self.node_name)
        if not nodeId:
            logger.error(f"node not found with name: {self.node_name}")
            return None
        else:
            return self._get_items_on_node_by_node_id(nodeId)
