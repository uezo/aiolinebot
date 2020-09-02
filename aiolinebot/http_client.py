import json
import aiohttp
from linebot.api import LineBotApiError
from linebot.http_client import HttpResponse, HttpClient
from linebot.models import Error


class AioHttpResponse(HttpResponse):
    """HttpResponse implemented by aiohttp lib's response."""

    def __init__(self, status_code, headers, *, content=None, session=None):
        """__init__ method.

        :param int status_code: status code
        :param CIMultiDictProxy headers: headers
        :param bytes content: content data or aiohttp.streams.StreamReader
        :param aiohttp.ClientSession session: client session. must be closed
        """
        self._status_code = status_code
        self._headers = headers
        self._session = session
        self._content = content

    async def close(self):
        """Close connection."""
        await self._session.close()

    @property
    def status_code(self):
        """Get status code."""
        return self._status_code

    @property
    def headers(self):
        """Get headers.

        :rtype :py:class:`CIMultiDictProxy`
        """
        return self._headers

    @property
    def text(self):
        """Get response body as text-decoded."""
        return self._content.decode()

    @property
    def content(self):
        """Get response body as binary."""
        return self._content

    @property
    def json(self):
        """Get response body as json-decoded."""
        return json.loads(self._content.decode())

    def iter_content(self, chunk_size=1024, decode_unicode=False):
        """Get response body as iterator content (stream).

        :param int chunk_size:
        :param bool decode_unicode (not used, ignored):
        """
        return self.content.iter_chunked(n=chunk_size)

    @staticmethod
    def is_success(status_code):
        if 200 <= status_code < 300:
            return True

    def check_error(self):
        if self.is_success(self.status_code):
            pass
        else:
            raise LineBotApiError(
                status_code=self.status_code,
                headers=dict(self.headers.items()),
                request_id=self.headers.get('X-Line-Request-Id'),
                error=Error.new_from_json_dict(self.json)
            )


class AioHttpClient(HttpClient):
    """HttpClient implemented by aiohttp."""

    def __init__(self, timeout=HttpClient.DEFAULT_TIMEOUT):
        """__init__ method.

        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float
            Default is :py:attr:`DEFAULT_TIMEOUT`
        :type timeout: float
        """
        super(AioHttpClient, self).__init__(timeout)

    async def get(self, url, headers=None, params=None, stream=False, timeout=None):
        """GET request.

        :param str url: Request url
        :param dict headers: (optional) Request headers
        :param dict params: (optional) Request query parameter
        :param bool stream: (optional) get content as stream
        :param timeout: (optional), How long to wait for the server
            to send data before giving up, as a float
            Default is :py:attr:`self.timeout`
        :type timeout: float
        :rtype: :py:class:`AioHttpResponse`
        :return: AioHttpResponse instance
        """
        if timeout is None:
            timeout = self.timeout

        if stream is False:
            async with aiohttp.ClientSession() as client_session:
                async with client_session.get(
                    url, headers=headers, params=params, timeout=timeout
                ) as resp:
                    aio_response = AioHttpResponse(
                        resp.status, resp.headers,
                        content=await resp.content.read())
        else:
            client_session = aiohttp.ClientSession()
            resp = await client_session.get(
                url, headers=headers, params=params, timeout=timeout
            )
            if AioHttpResponse.is_success(resp.status):
                aio_response = AioHttpResponse(
                    resp.status, resp.headers,
                    content=resp.content,
                    session=client_session)
            else:
                aio_response = AioHttpResponse(
                    resp.status, resp.headers,
                    content=await resp.content.read())
                client_session.close()

        return aio_response

    async def post(self, url, headers=None, data=None, timeout=None):
        """POST request.

        :param str url: Request url
        :param dict headers: (optional) Request headers
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body
        :param timeout: (optional), How long to wait for the server
            to send data before giving up, as a float
            Default is :py:attr:`self.timeout`
        :type timeout: float
        :rtype: :py:class:`AioHttpResponse`
        :return: AioHttpResponse instance
        """
        if timeout is None:
            timeout = self.timeout

        async with aiohttp.ClientSession() as client_session:
            async with client_session.post(
                url, headers=headers, data=data, timeout=timeout
            ) as resp:
                aio_response = AioHttpResponse(
                    resp.status, resp.headers,
                    content=await resp.content.read())

        return aio_response

    async def delete(self, url, headers=None, data=None, timeout=None):
        """DELETE request.

        :param str url: Request url
        :param dict headers: (optional) Request headers
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body
        :param timeout: (optional), How long to wait for the server
            to send data before giving up, as a float
            Default is :py:attr:`self.timeout`
        :type timeout: float
        :rtype: :py:class:`AioHttpResponse`
        :return: AioHttpResponse instance
        """
        if timeout is None:
            timeout = self.timeout

        async with aiohttp.ClientSession() as client_session:
            async with client_session.delete(
                url, headers=headers, data=data, timeout=timeout
            ) as resp:
                aio_response = AioHttpResponse(
                    resp.status, resp.headers,
                    content=await resp.content.read())

        return aio_response
