import requests

from tests.constants import (
    BASE_WALLETS_URL,
    WALLET_DATA,
    WALLET_DATA_AFTER_PUT,
    WALLET_OPERATION_DEPOSIT_DATA,
)


class TestWallets:
    """Тестирует эндпоинты для wallets"""

    url = BASE_WALLETS_URL
    wallet_id = None

    @classmethod
    def test_get_all_wallets(cls):
        response = requests.get(url=cls.url)
        result = response.json()

        assert response.status_code == 200
        assert isinstance(result, list)

    @classmethod
    def test_post_wallet(cls):
        response = requests.post(
            url=cls.url,
            json=WALLET_DATA,
        )
        result = response.json()

        assert response.status_code == 201
        assert isinstance(result, dict)
        assert result["title"] == WALLET_DATA["title"]
        assert result["description"] == WALLET_DATA["description"]

        # Задаем id тестового кошелька и его url
        cls.wallet_id = result["id"]
        cls.url_by_id = f"{cls.url}{cls.wallet_id}/"

    @classmethod
    def test_get_wallet_by_id(cls):
        response = requests.get(url=cls.url_by_id)
        wallet = response.json()

        assert response.status_code == 200
        assert isinstance(wallet, dict)
        assert wallet["title"] == "test_wallet_1"
        assert wallet["description"] == "test_description_1"

    @classmethod
    def test_put_wallet_by_id(cls):
        response = requests.get(url=cls.url_by_id)
        result = response.json()
        assert result["title"] == "test_wallet_1"
        assert result["description"] == "test_description_1"

        response_after_put = requests.put(
            url=cls.url_by_id,
            json=WALLET_DATA_AFTER_PUT,
        )
        result_after_put = response_after_put.json()

        assert response.status_code == 200
        assert result_after_put == "Кошелёк успешно изменён"

    @classmethod
    def test_wallet_operation_by_id(cls):
        wallet = requests.get(url=cls.url_by_id)
        assert wallet.json()["balance"] == "0.00"

        url = f"{cls.url_by_id}operation/"
        operation = requests.post(
            url=url,
            json=WALLET_OPERATION_DEPOSIT_DATA,
        )
        assert operation.status_code == 200
        assert operation.json() == "Транзакция прошла успешно!"

        wallet_after_operation = requests.get(url=cls.url_by_id)
        assert wallet_after_operation.json()["balance"] == "100.00"
