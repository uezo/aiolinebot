"""aiolinebot.api module."""

import json

from linebot.api import LineBotApi
from linebot.http_client import HttpClient, RequestsHttpClient
from linebot.models import (
    Profile, MemberIds, Content, RichMenuResponse, MessageQuotaResponse,
    MessageQuotaConsumptionResponse, IssueLinkTokenResponse, IssueChannelTokenResponse,
    MessageDeliveryBroadcastResponse, MessageDeliveryMulticastResponse,
    MessageDeliveryPushResponse, MessageDeliveryReplyResponse,
    InsightMessageDeliveryResponse, InsightFollowersResponse, InsightDemographicResponse,
    InsightMessageEventResponse, BroadcastResponse, NarrowcastResponse,
    MessageProgressNarrowcastResponse,
)
from .http_client import AioHttpClient


class AioLineBotApi(LineBotApi):
    """AioLineBotApi provides asynchronous interface for LINE messaging API."""

    LINE_BOT_API_VERSION = 'LINE_BOT_API_VERSION'

    def __init__(self, channel_access_token,
                 endpoint=LineBotApi.DEFAULT_API_ENDPOINT,
                 data_endpoint=LineBotApi.DEFAULT_API_DATA_ENDPOINT,
                 timeout=HttpClient.DEFAULT_TIMEOUT,
                 http_client=RequestsHttpClient):
        """__init__ method.

        :param str channel_access_token: Your channel access token
        :param str endpoint: (optional) Default is https://api.line.me
        :param str data_endpoint: (optional) Default is https://api-data.line.me
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is linebot.http_client.HttpClient.DEFAULT_TIMEOUT
            If you set tuple, set float or other proper values
            for aiohttp_client.timeout after initialization.
        :type timeout: float | tuple(float, float)
        :param http_client: (optional) Default is
            :py:class:`linebot.http_client.RequestsHttpClient`
        :type http_client: T <= :py:class:`linebot.http_client.HttpClient`
        """
        super().__init__(channel_access_token, endpoint=endpoint, data_endpoint=data_endpoint,
                         timeout=timeout, http_client=http_client)

        self.aiohttp_client = AioHttpClient(timeout=timeout)
