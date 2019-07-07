import json
import aiohttp

from linebot import LineBotApi, __version__ as linebotapi_version
from linebot.http_client import HttpClient
from linebot.models import (
    Error, Profile, MemberIds, Content, RichMenuResponse, MessageQuotaResponse,
    MessageQuotaConsumptionResponse, IssueLinkTokenResponse, IssueChannelTokenResponse,
    MessageDeliveryBroadcastResponse, MessageDeliveryMulticastResponse,
    MessageDeliveryPushResponse, MessageDeliveryReplyResponse,
)
from linebot.exceptions import LineBotApiError

__version__ = '0.2'


class AioLineBotApi(LineBotApi):
    """AioLineBotApi provides asynchronous interface for LINE messaging API."""

    def __init__(self, channel_access_token, endpoint=LineBotApi.DEFAULT_API_ENDPOINT,
                 timeout=HttpClient.DEFAULT_TIMEOUT, http_client=aiohttp.ClientSession):
        """__init__ method.

        :param str channel_access_token: Your channel access token
        :param str endpoint: (optional) Default is https://api.line.me
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is linebot.http_client.HttpClient.DEFAULT_TIMEOUT
        :type timeout: float | tuple(float, float)
        :param http_client: (optional) Default is
            :py:class:`aiohttp.ClientSession`
        :type http_client: T <= :py:class:`aiohttp.ClientSession`
        """
        self.endpoint = endpoint
        self.headers = {
            'Authorization': 'Bearer ' + channel_access_token,
            'User-Agent': 'line-bot-sdk-python/' + linebotapi_version
        }
        self.timeout = timeout
        self.http_client = http_client

    async def reply_message(self, reply_token, messages, notification_disabled=False, timeout=None):
        """Call reply message API.

        https://developers.line.biz/en/reference/messaging-api/#send-reply-message

        Respond to events from users, groups, and rooms.

        Webhooks are used to notify you when an event occurs.
        For events that you can respond to, a replyToken is issued for replying to messages.

        Because the replyToken becomes invalid after a certain period of time,
        responses should be sent as soon as a message is received.

        Reply tokens can only be used once.

        :param str reply_token: replyToken received via webhook
        :param messages: Messages.
            Max: 5
        :type messages: T <= :py:class:`linebot.models.send_messages.SendMessage` |
            list[T <= :py:class:`linebot.models.send_messages.SendMessage`]
        :param bool notification_disabled: (optional) True to disable push notification
            when the message is sent. The default value is False.
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        if not isinstance(messages, (list, tuple)):
            messages = [messages]

        data = {
            'replyToken': reply_token,
            'messages': [message.as_json_dict() for message in messages],
            'notificationDisabled': notification_disabled,
        }

        await self._post(
            '/v2/bot/message/reply', data=json.dumps(data), timeout=timeout
        )

    async def push_message(self, to, messages, notification_disabled=False, timeout=None):
        """Call push message API.

        https://developers.line.biz/en/reference/messaging-api/#send-push-message

        Send messages to users, groups, and rooms at any time.

        :param str to: ID of the receiver
        :param messages: Messages.
            Max: 5
        :type messages: T <= :py:class:`linebot.models.send_messages.SendMessage` |
            list[T <= :py:class:`linebot.models.send_messages.SendMessage`]
        :param bool notification_disabled: (optional) True to disable push notification
            when the message is sent. The default value is False.
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        if not isinstance(messages, (list, tuple)):
            messages = [messages]

        data = {
            'to': to,
            'messages': [message.as_json_dict() for message in messages],
            'notificationDisabled': notification_disabled,
        }

        await self._post(
            '/v2/bot/message/push', data=json.dumps(data), timeout=timeout
        )

    async def multicast(self, to, messages, notification_disabled=False, timeout=None):
        """Call multicast API.

        https://developers.line.biz/en/reference/messaging-api/#send-multicast-message

        Send messages to multiple users at any time.

        :param to: IDs of the receivers
            Max: 150 users
        :type to: list[str]
        :param messages: Messages.
            Max: 5
        :type messages: T <= :py:class:`linebot.models.send_messages.SendMessage` |
            list[T <= :py:class:`linebot.models.send_messages.SendMessage`]
        :param bool notification_disabled: (optional) True to disable push notification
            when the message is sent. The default value is False.
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        if not isinstance(messages, (list, tuple)):
            messages = [messages]

        data = {
            'to': to,
            'messages': [message.as_json_dict() for message in messages],
            'notificationDisabled': notification_disabled,
        }

        await self._post(
            '/v2/bot/message/multicast', data=json.dumps(data), timeout=timeout
        )

    async def broadcast(self, messages, notification_disabled=False, timeout=None):
        """Call broadcast API.

        https://developers.line.biz/en/reference/messaging-api/#send-broadcast-message

        Send messages to multiple users at any time.

        :param messages: Messages.
            Max: 5
        :type messages: T <= :py:class:`linebot.models.send_messages.SendMessage` |
            list[T <= :py:class:`linebot.models.send_messages.SendMessage`]
        :param bool notification_disabled: (optional) True to disable push notification
            when the message is sent. The default value is False.
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        if not isinstance(messages, (list, tuple)):
            messages = [messages]

        data = {
            'messages': [message.as_json_dict() for message in messages],
            'notificationDisabled': notification_disabled,
        }

        await self._post(
            '/v2/bot/message/broadcast', data=json.dumps(data), timeout=timeout
        )

    async def get_message_delivery_broadcast(self, date, timeout=None):
        """Get number of sent broadcast messages.

        https://developers.line.biz/en/reference/messaging-api/#get-number-of-broadcast-messages

        Gets the number of messages sent with the /bot/message/broadcast endpoint.

        :param str date: Date the messages were sent. The format is `yyyyMMdd` (Timezone is UTC+9).
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        response = await self._get(
            '/v2/bot/message/delivery/broadcast?date={date}'.format(date=date),
            timeout=timeout
        )

        return MessageDeliveryBroadcastResponse.new_from_json_dict(response.json)

    async def get_message_delivery_reply(self, date, timeout=None):
        """Get number of sent reply messages.

        https://developers.line.biz/en/reference/messaging-api/#get-number-of-reply-messages

        Gets the number of messages sent with the /bot/message/reply endpoint.

        :param str date: Date the messages were sent. The format is `yyyyMMdd` (Timezone is UTC+9).
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        response = await self._get(
            '/v2/bot/message/delivery/reply?date={date}'.format(date=date),
            timeout=timeout
        )

        return MessageDeliveryReplyResponse.new_from_json_dict(response.json)

    async def get_message_delivery_push(self, date, timeout=None):
        """Get number of sent push messages.

        https://developers.line.biz/en/reference/messaging-api/#get-number-of-push-messages

        Gets the number of messages sent with the /bot/message/push endpoint.

        :param str date: Date the messages were sent. The format is `yyyyMMdd` (Timezone is UTC+9).
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        response = await self._get(
            '/v2/bot/message/delivery/push?date={date}'.format(date=date),
            timeout=timeout
        )

        return MessageDeliveryPushResponse.new_from_json_dict(response.json)

    async def get_message_delivery_multicast(self, date, timeout=None):
        """Get number of sent multicast messages.

        https://developers.line.biz/en/reference/messaging-api/#get-number-of-multicast-messages

        Gets the number of messages sent with the /bot/message/multicast endpoint.

        :param str date: Date the messages were sent. The format is `yyyyMMdd` (Timezone is UTC+9).
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        response = await self._get(
            '/v2/bot/message/delivery/multicast?date={date}'.format(date=date),
            timeout=timeout
        )

        return MessageDeliveryMulticastResponse.new_from_json_dict(response.json)

    async def get_profile(self, user_id, timeout=None):
        """Call get profile API.

        https://developers.line.biz/en/reference/messaging-api/#get-profile

        Get user profile information.

        :param str user_id: User ID
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.Profile`
        :return: Profile instance
        """
        response = await self._get(
            '/v2/bot/profile/{user_id}'.format(user_id=user_id),
            timeout=timeout
        )

        return Profile.new_from_json_dict(response.json)

    async def get_group_member_profile(self, group_id, user_id, timeout=None):
        """Call get group member profile API.

        https://developers.line.biz/en/reference/messaging-api/#get-group-member-profile

        Gets the user profile of a member of a group that
        the bot is in. This can be the user ID of a user who has
        not added the bot as a friend or has blocked the bot.

        :param str group_id: Group ID
        :param str user_id: User ID
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.Profile`
        :return: Profile instance
        """
        response = await self._get(
            '/v2/bot/group/{group_id}/member/{user_id}'.format(group_id=group_id, user_id=user_id),
            timeout=timeout
        )

        return Profile.new_from_json_dict(response.json)

    async def get_room_member_profile(self, room_id, user_id, timeout=None):
        """Call get room member profile API.

        https://developers.line.biz/en/reference/messaging-api/#get-room-member-profile

        Gets the user profile of a member of a room that
        the bot is in. This can be the user ID of a user who has
        not added the bot as a friend or has blocked the bot.

        :param str room_id: Room ID
        :param str user_id: User ID
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.Profile`
        :return: Profile instance
        """
        response = await self._get(
            '/v2/bot/room/{room_id}/member/{user_id}'.format(room_id=room_id, user_id=user_id),
            timeout=timeout
        )

        return Profile.new_from_json_dict(response.json)

    async def get_group_member_ids(self, group_id, start=None, timeout=None):
        """Call get group member IDs API.

        https://developers.line.biz/en/reference/messaging-api/#get-group-member-ids

        Gets the user IDs of the members of a group that the bot is in.
        This includes the user IDs of users who have not added the bot as a friend
        or has blocked the bot.

        :param str group_id: Group ID
        :param str start: continuationToken
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.MemberIds`
        :return: MemberIds instance
        """
        params = None if start is None else {'start': start}

        response = await self._get(
            '/v2/bot/group/{group_id}/members/ids'.format(group_id=group_id),
            params=params,
            timeout=timeout
        )

        return MemberIds.new_from_json_dict(response.json)

    async def get_room_member_ids(self, room_id, start=None, timeout=None):
        """Call get room member IDs API.

        https://developers.line.biz/en/reference/messaging-api/#get-room-member-ids

        Gets the user IDs of the members of a group that the bot is in.
        This includes the user IDs of users who have not added the bot as a friend
        or has blocked the bot.

        :param str room_id: Room ID
        :param str start: continuationToken
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.MemberIds`
        :return: MemberIds instance
        """
        params = None if start is None else {'start': start}

        response = await self._get(
            '/v2/bot/room/{room_id}/members/ids'.format(room_id=room_id),
            params=params,
            timeout=timeout
        )

        return MemberIds.new_from_json_dict(response.json)

    def get_message_content(self, message_id, timeout=None):
        """Call get content API.

        https://developers.line.biz/en/reference/messaging-api/#get-content

        Retrieve image, video, and audio data sent by users.

        :param str message_id: Message ID
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`AioContent`
        :return: Content instance
        """
        url = self.endpoint + '/v2/bot/message/{message_id}/content'.format(message_id=message_id)

        client_session = self.http_client()
        resp_coro = client_session.get(url, headers=self.headers, timeout=timeout or self.timeout)
        close_func = client_session.close

        return AioContent(resp_coro, close_func)

    async def leave_group(self, group_id, timeout=None):
        """Call leave group API.

        https://developers.line.biz/en/reference/messaging-api/#leave-group

        Leave a group.

        :param str group_id: Group ID
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        await self._post(
            '/v2/bot/group/{group_id}/leave'.format(group_id=group_id),
            timeout=timeout
        )

    async def leave_room(self, room_id, timeout=None):
        """Call leave room API.

        https://developers.line.biz/en/reference/messaging-api/#leave-room

        Leave a room.

        :param str room_id: Room ID
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        await self._post(
            '/v2/bot/room/{room_id}/leave'.format(room_id=room_id),
            timeout=timeout
        )

    async def get_rich_menu(self, rich_menu_id, timeout=None):
        """Call get rich menu API.

        https://developers.line.me/en/docs/messaging-api/reference/#get-rich-menu

        :param str rich_menu_id: ID of the rich menu
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.RichMenuResponse`
        :return: RichMenuResponse instance
        """
        response = await self._get(
            '/v2/bot/richmenu/{rich_menu_id}'.format(rich_menu_id=rich_menu_id),
            timeout=timeout
        )

        return RichMenuResponse.new_from_json_dict(response.json)

    async def create_rich_menu(self, rich_menu, timeout=None):
        """Call create rich menu API.

        https://developers.line.me/en/docs/messaging-api/reference/#create-rich-menu

        :param rich_menu: Inquired to create a rich menu object.
        :type rich_menu: T <= :py:class:`linebot.models.rich_menu.RichMenu`
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: str
        :return: rich menu id
        """
        response = await self._post(
            '/v2/bot/richmenu', data=rich_menu.as_json_string(), timeout=timeout
        )

        return response.json.get('richMenuId')

    async def delete_rich_menu(self, rich_menu_id, timeout=None):
        """Call delete rich menu API.

        https://developers.line.me/en/docs/messaging-api/reference/#delete-rich-menu

        :param str rich_menu_id: ID of an uploaded rich menu
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        await self._delete(
            '/v2/bot/richmenu/{rich_menu_id}'.format(rich_menu_id=rich_menu_id),
            timeout=timeout
        )

    async def get_rich_menu_id_of_user(self, user_id, timeout=None):
        """Call get rich menu ID of user API.

        https://developers.line.me/en/docs/messaging-api/reference/#get-rich-menu-id-of-user

        :param str user_id: IDs of the user
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: str
        :return: rich menu id
        """
        response = await self._get(
            '/v2/bot/user/{user_id}/richmenu'.format(user_id=user_id),
            timeout=timeout
        )

        return response.json.get('richMenuId')

    async def link_rich_menu_to_user(self, user_id, rich_menu_id, timeout=None):
        """Call link rich menu to user API.

        https://developers.line.me/en/docs/messaging-api/reference/#link-rich-menu-to-user

        :param str user_id: ID of the user
        :param str rich_menu_id: ID of an uploaded rich menu
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        await self._post(
            '/v2/bot/user/{user_id}/richmenu/{rich_menu_id}'.format(
                user_id=user_id,
                rich_menu_id=rich_menu_id
            ),
            timeout=timeout
        )

    async def link_rich_menu_to_users(self, user_ids, rich_menu_id, timeout=None):
        """Links a rich menu to multiple users.

        https://developers.line.biz/en/reference/messaging-api/#link-rich-menu-to-users

        :param user_ids: user IDs
            Max: 150 users
        :type user_ids: list[str]
        :param str rich_menu_id: ID of an uploaded rich menu
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        await self._post(
            '/v2/bot/richmenu/bulk/link',
            data=json.dumps({
                'userIds': user_ids,
                'richMenuId': rich_menu_id,
            }),
            timeout=timeout
        )

    async def unlink_rich_menu_from_user(self, user_id, timeout=None):
        """Call unlink rich menu from user API.

        https://developers.line.me/en/docs/messaging-api/reference/#unlink-rich-menu-from-user

        :param str user_id: ID of the user
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        await self._delete(
            '/v2/bot/user/{user_id}/richmenu'.format(user_id=user_id),
            timeout=timeout
        )

    async def unlink_rich_menu_from_users(self, user_ids, timeout=None):
        """Unlinks rich menus from multiple users.

        https://developers.line.biz/en/reference/messaging-api/#unlink-rich-menu-from-users

        :param user_ids: user IDs
            Max: 150 users
        :type user_ids: list[str]
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        await self._post(
            '/v2/bot/richmenu/bulk/unlink',
            data=json.dumps({
                'userIds': user_ids,
            }),
            timeout=timeout
        )

    def get_rich_menu_image(self, rich_menu_id, timeout=None):
        """Call download rich menu image API.

        https://developers.line.me/en/docs/messaging-api/reference/#download-rich-menu-image

        :param str rich_menu_id: ID of the rich menu with the image to be downloaded
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`AioContent`
        :return: Content instance
        """
        url = self.endpoint + '/v2/bot/richmenu/{rich_menu_id}/content'.format(rich_menu_id=rich_menu_id)

        client_session = self.http_client()
        resp_coro = client_session.get(url, headers=self.headers, timeout=timeout or self.timeout)
        close_func = client_session.close

        return AioContent(resp_coro, close_func)

    async def set_rich_menu_image(self, rich_menu_id, content_type, content, timeout=None):
        """Call upload rich menu image API.

        https://developers.line.me/en/docs/messaging-api/reference/#upload-rich-menu-image

        Uploads and attaches an image to a rich menu.

        :param str rich_menu_id: IDs of the richmenu
        :param str content_type: image/jpeg or image/png
        :param content: image content as bytes, or file-like object
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        await self._post(
            '/v2/bot/richmenu/{rich_menu_id}/content'.format(rich_menu_id=rich_menu_id),
            data=content,
            headers={'Content-Type': content_type},
            timeout=timeout
        )

    async def get_rich_menu_list(self, timeout=None):
        """Call get rich menu list API.

        https://developers.line.me/en/docs/messaging-api/reference/#get-rich-menu-list

        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: list(T <= :py:class:`linebot.models.responses.RichMenuResponse`)
        :return: list[RichMenuResponse] instance
        """
        response = await self._get(
            '/v2/bot/richmenu/list',
            timeout=timeout
        )

        result = []
        for richmenu in response.json['richmenus']:
            result.append(RichMenuResponse.new_from_json_dict(richmenu))

        return result

    async def set_default_rich_menu(self, rich_menu_id, timeout=None):
        """Set the default rich menu.

        https://developers.line.biz/en/reference/messaging-api/#set-default-rich-menu

        :param str rich_menu_id: ID of an uploaded rich menu
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        await self._post(
            '/v2/bot/user/all/richmenu/{rich_menu_id}'.format(
                rich_menu_id=rich_menu_id,
            ),
            timeout=timeout
        )

    async def get_default_rich_menu(self, timeout=None):
        """Get the ID of the default rich menu set with the Messaging API.

        https://developers.line.biz/en/reference/messaging-api/#get-default-rich-menu-id

        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        response = await self._get(
            '/v2/bot/user/all/richmenu',
            timeout=timeout
        )

        return response.json.get('richMenuId')

    async def cancel_default_rich_menu(self, timeout=None):
        """Cancel the default rich menu set with the Messaging API.

        https://developers.line.biz/en/reference/messaging-api/#cancel-default-rich-menu

        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        await self._delete(
            '/v2/bot/user/all/richmenu',
            timeout=timeout
        )

    async def get_message_quota(self, timeout=None):
        """Call Get the target limit for additional messages.

        https://developers.line.biz/en/reference/messaging-api/#get-quota

        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.MessageQuotaResponse`
        :return: MessageQuotaResponse instance
        """
        response = await self._get(
            '/v2/bot/message/quota',
            timeout=timeout
        )

        return MessageQuotaResponse.new_from_json_dict(response.json)

    async def get_message_quota_consumption(self, timeout=None):
        """Get number of messages sent this month.

        https://developers.line.biz/en/reference/messaging-api/#get-consumption

        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.MessageQuotaConsumptionResponse`
        :return: MessageQuotaConsumptionResponse instance
        """
        response = await self._get(
            '/v2/bot/message/quota/consumption',
            timeout=timeout
        )

        return MessageQuotaConsumptionResponse.new_from_json_dict(response.json)

    async def issue_link_token(self, user_id, timeout=None):
        """Issues a link token used for the account link feature.

        https://developers.line.biz/en/reference/messaging-api/#issue-link-token

        :param str user_id: User ID for the LINE account to be linked
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.IssueLinkTokenResponse`
        :return: IssueLinkTokenResponse instance
        """
        response = await self._post(
            '/v2/bot/user/{user_id}/linkToken'.format(
                user_id=user_id
            ),
            timeout=timeout
        )

        return IssueLinkTokenResponse.new_from_json_dict(response.json)

    async def issue_channel_token(self, client_id, client_secret,
                            grant_type='client_credentials', timeout=None):
        """Issues a short-lived channel access token.

        https://developers.line.biz/en/reference/messaging-api/#issue-channel-access-token

        :param str client_id: Channel ID.
        :param str client_secret: Channel secret.
        :param str grant_type: `client_credentials`
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        :rtype: :py:class:`linebot.models.responses.IssueChannelTokenResponse`
        :return: IssueChannelTokenResponse instance
        """
        response = await self._post(
            '/v2/oauth/accessToken',
            data={
                'client_id': client_id,
                'client_secret': client_secret,
                'grant_type': grant_type,
            },
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=timeout
        )

        return IssueChannelTokenResponse.new_from_json_dict(response.json)

    async def revoke_channel_token(self, access_token, timeout=None):
        """Revokes a channel access token.

        https://developers.line.biz/en/reference/messaging-api/#revoke-channel-access-token

        :param str access_token: Channel access token.
        :param timeout: (optional) How long to wait for the server
            to send data before giving up, as a float,
            or a (connect timeout, read timeout) float tuple.
            Default is self.http_client.timeout
        :type timeout: float | tuple(float, float)
        """
        await self._post(
            '/v2/oauth/revoke',
            data={'access_token': access_token},
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=timeout
        )

    async def _get(self, path, params=None, headers=None, stream=False, timeout=None):
        url = self.endpoint + path

        if headers is None:
            headers = {}
        headers.update(self.headers)

        async with self.http_client() as client_session:
            async with client_session.get(
                url, headers=headers, params=params, timeout=timeout or self.timeout
            ) as resp:
                response = AioHttpResponse(resp.status, resp.headers)
                if resp.content_type == "application/json":
                    response.json = await resp.json()
                else:
                    response.content = await resp.content.read()

        self.__check_error(response)
        return response

    async def _post(self, path, data=None, headers=None, timeout=None):
        url = self.endpoint + path

        if headers is None:
            headers = {'Content-Type': 'application/json'}
        headers.update(self.headers)

        async with self.http_client() as client_session:
            async with client_session.post(
                url, headers=headers, data=data, timeout=timeout or self.timeout
            ) as resp:
                response = AioHttpResponse(resp.status, resp.headers)
                if resp.content_type == "application/json":
                    response.json = await resp.json()

        self.__check_error(response)
        return response

    async def _delete(self, path, data=None, headers=None, timeout=None):
        url = self.endpoint + path

        if headers is None:
            headers = {}
        headers.update(self.headers)

        async with self.http_client() as client_session:
            async with client_session.delete(
                url, headers=headers, data=data, timeout=timeout or self.timeout
            ) as resp:
                response = AioHttpResponse(resp.status, resp.headers)
                if resp.content_type == "application/json":
                    response.json = await resp.json()

        self.__check_error(response)
        return response

    @staticmethod
    def __check_error(response):
        if 200 <= response.status_code < 300:
            pass
        else:
            error = Error.new_from_json_dict(response.json)
            raise LineBotApiError(response.status_code, error)


class AioHttpResponse:
    """Response with minumum properties for linebot api"""

    def __init__(self, status_code, headers, json=None, content=None):
        """__init__ method.

        :param int status_code: status code
        :param dict headers: Response headers
        :param dict json: Response data as JSON
        :param list content: Response data as list of bytes
        """
        self.status_code = status_code
        self.headers = headers
        self.json = json
        self.content = content


class AioContent:
    """MessageContent using aiohttp.

    https://devdocs.line.me/ja/#get-content
    """

    def __init__(self, coro_response, close_func):
        """__init__ method.

        :param coroutine coro_response: Response coroutine
        :param method close_func: function to close http connection
        :rtype: :py:class:`AioContent`
        :return: AioContent instance
        """
        self._coro_response = coro_response
        self.close = close_func
        self.response = None

    @property
    def content_type(self):
        """Get Content-type header value.

        :rtype: str
        :return: content-type header value
        """
        return self.response.content_type

    @property
    async def content(self):
        """Get content.

        If content size is large, should use iter_content.

        :rtype: binary
        """
        return await self.response.content.read()

    def iter_content(self, chunk_size=1024):
        """Get content as iterator (stream).

        If content size is large, should use this.

        :param chunk_size: Chunk size
        :rtype: iterator
        :return:
        """
        return self.response.content.iter_chunked(n=chunk_size)

    async def __aenter__(self):
        try:
            self.response = await self._coro_response
            if 200 <= self.response.status < 300:
                pass
            else:
                error = Error.new_from_json_dict(await self.response.json())
                raise LineBotApiError(self.response.status, error)

        except Exception as ex:
            await self.close()
            raise ex

        return self

    async def __aexit__(self, exc_type=None, exc_value=None, tb=None):
        await self.close()
