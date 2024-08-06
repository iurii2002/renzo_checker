import json
import requests

from loguru import logger
from eth_account.account import ChecksumAddress

from modules.helpful_scripts import MakePause
from modules.requestor import Requestor

headers = {
    'Origin': 'https://app.renzoprotocol.com',
    'Referer': 'https://app.renzoprotocol.com/',
}


class RenzoSDK(Requestor):
    def __init__(self, address: ChecksumAddress | str):
        super().__init__(_headers=headers)
        self.endpoint = 'https://app.renzoprotocol.com/api/'
        self.address = address

    def get_wallet_points(self) -> dict:
        """
        Returns the amount of points got by wallet, e.g -
        {"renzoPoints": 0,"eigenLayerPoints": 0, "mellowPoints": 0, "symbioticPoints": 0},
        """
        full_data = self.get_request(url=self.endpoint + f'points/{self.address}')
        return full_data['data']['totals']

    def get_airdrop_season2_data(self) -> dict:
        """
        Returns the season 2 airdrop data, e.g. - {"success":true,"data":{"eligible":false,"boost":0,"rezTokens":0}}
        """
        return self.get_request(url=f'https://claim.renzoprotocol.com/api/eligibility-checker/{self.address}')

    def check_airdrop_season_2(self) -> None:
        """
        Logs data from season 2 airdrop, e.g. - <wallet>, <Renzo point>, <Airdrop Amount>
        :return: None
        """
        renzo_points = int(self.get_wallet_points()['renzoPoints'])

        airdrop_full_data = self.get_airdrop_season2_data()
        if airdrop_full_data['success']:
            airdrop_data = airdrop_full_data['data']
            if airdrop_data['eligible']:
                logger.opt(ansi=True).success(f'{self.address}, Renzo Points: {renzo_points}'
                                              f', <green> Airdrop: {airdrop_data["rezTokens"]} </green>')
            else:
                logger.opt(ansi=True).info(f'{self.address}, Renzo Points: {renzo_points}'
                                           f', <red> Airdrop: Not eligible</red> ')
            return
        raise ConnectionError()
