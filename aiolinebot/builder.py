import inspect
import linebot


class AioLineBotApiBuilder:
    @classmethod
    def build_class(cls, save_as, version):
        # get class base source
        from . import api_base
        base_source = inspect.getsource(api_base)

        # set line-bot-sdk version
        base_source = base_source.replace(
            "'LINE_BOT_API_VERSION'", f"'{version}'")

        # make public methods async and add to base
        for m in inspect.getmembers(linebot.api.LineBotApi):
            if not m[0].startswith("_") and callable(m[1]):
                method_source = inspect.getsource(m[1])
                method_source = method_source.replace(
                    f"def {m[0]}(", f"async def {m[0]}_async(")
                # call private method asynchronously
                method_source = method_source.replace(
                    "self._get", "await self._get_async")
                method_source = method_source.replace(
                    "self._post", "await self._post_async")
                method_source = method_source.replace(
                    "self._delete", "await self._delete_async")
                base_source += "\n" + method_source

        # make get/post/delete private methods async
        for m in ["get", "post", "delete"]:
            method_source = inspect.getsource(getattr(linebot.api.LineBotApi, f"_{m}"))
            method_source = method_source.replace(
                f"def _{m}", f"async def _{m}_async")
            method_source = method_source.replace(
                f"self.http_client.{m}", f"await self.aiohttp_client.{m}")
            method_source = method_source.replace(
                "self.__check_error(response)", "response.check_error()")
            base_source += "\n" + method_source

        # save api module file
        with open(save_as, "w") as f:
            f.write(base_source)
