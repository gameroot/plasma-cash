import pytest
from mockito import mock, verify, when

from plasma_cash.client.child_chain_client import ChildChainClient
from plasma_cash.client.exceptions import RequestFailedException
from unit_tests.unstub_mixin import UnstubMixin


class TestChildChainClient(UnstubMixin):
    BASE_URL = 'https://dummy-plasma-cash'

    @pytest.fixture(scope='function')
    def client(self):
        return ChildChainClient(self.BASE_URL)

    def test_constructor(self):
        DUMMY_BASE_URL = 'base url'
        DUMMY_VERIFY = True
        DUMMY_TIME_OUT = 100

        c = ChildChainClient(DUMMY_BASE_URL, DUMMY_VERIFY, DUMMY_TIME_OUT)
        assert c.base_url == DUMMY_BASE_URL
        assert c.verify == DUMMY_VERIFY
        assert c.timeout == DUMMY_TIME_OUT

    def test_request_success(self, client):
        DUMMY_END_POINT = '/end-point'
        DUMMY_METHOD = 'post'
        DUMMY_PARAMS = 'parmas'
        DUMMY_DATA = {'data': 'dummy'}
        DUMMY_HEADERS = 'headers'

        URL = self.BASE_URL + DUMMY_END_POINT

        MOCK_RESPONSE = mock({'ok': True})

        (when('plasma_cash.client.child_chain_client.requests')
            .request(
                method=DUMMY_METHOD,
                url=URL,
                params=DUMMY_PARAMS,
                data=DUMMY_DATA,
                headers=DUMMY_HEADERS,
                verify=client.verify,
                timeout=client.timeout
            ).thenReturn(MOCK_RESPONSE))

        resp = client.request(
            DUMMY_END_POINT,
            DUMMY_METHOD,
            DUMMY_PARAMS,
            DUMMY_DATA,
            DUMMY_HEADERS
        )

        assert resp == MOCK_RESPONSE

    def test_request_failed(self, client):
        DUMMY_END_POINT = '/end-point'
        DUMMY_METHOD = 'post'
        DUMMY_PARAMS = 'parmas'
        DUMMY_DATA = {'data': 'dummy'}
        DUMMY_HEADERS = 'headers'

        URL = self.BASE_URL + DUMMY_END_POINT

        MOCK_RESPONSE = mock({'ok': False})

        (when('plasma_cash.client.child_chain_client.requests')
            .request(
                method=DUMMY_METHOD,
                url=URL,
                params=DUMMY_PARAMS,
                data=DUMMY_DATA,
                headers=DUMMY_HEADERS,
                verify=client.verify,
                timeout=client.timeout
            ).thenReturn(MOCK_RESPONSE))

        with pytest.raises(RequestFailedException):
            client.request(
                DUMMY_END_POINT,
                DUMMY_METHOD,
                DUMMY_PARAMS,
                DUMMY_DATA,
                DUMMY_HEADERS
            )

    def test_get_current_block(self, client):
        RESP_TEXT = 'response text'
        MOCK_RESP = mock({'text': RESP_TEXT})

        when(client).request('/block', 'GET').thenReturn(MOCK_RESP)
        resp = client.get_current_block()
        assert resp == RESP_TEXT

    def test_get_block(self, client):
        RESP_TEXT = 'response text'
        MOCK_RESP = mock({'text': RESP_TEXT})
        DUMMY_BLK_NUM = 1

        when(client).request('/block/{}'.format(DUMMY_BLK_NUM), 'GET').thenReturn(MOCK_RESP)
        resp = client.get_block(DUMMY_BLK_NUM)
        assert resp == RESP_TEXT

    def test_get_proof(self, client):
        RESP_TEXT = 'response text'
        MOCK_RESP = mock({'text': RESP_TEXT})
        DUMMY_BLK_NUM = 1
        DUMMY_UID = 1

        params = {'blknum': DUMMY_BLK_NUM, 'uid': DUMMY_UID}
        when(client).request('/proof', 'GET', params=params).thenReturn(MOCK_RESP)
        resp = client.get_proof(DUMMY_BLK_NUM, DUMMY_UID)
        assert resp == RESP_TEXT

    def test_submit_block(self, client):
        DUMMY_SIG = 'sig'
        when(client).request(any, any, data=any).thenReturn(None)
        client.submit_block(DUMMY_SIG)
        verify(client).request(
            '/submit_block',
            'POST',
            data={'sig': DUMMY_SIG}
        )

    def test_send_transaction(self, client):
        DUMMY_TX = 'tx'
        when(client).request(any, any, data=any).thenReturn(None)
        client.send_transaction(DUMMY_TX)
        verify(client).request(
            '/send_tx',
            'POST',
            data={'tx': DUMMY_TX}
        )
