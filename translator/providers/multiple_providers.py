import sys
sys.path.insert(0, r'./')
from typing import Union, List
import translators as ts
from .base_provider import Provider


class MultipleProviders(Provider):
    def __init__(self, cache: bool=False):
        self.translator = ts
        self.config = {
            "translator": "bing",
            "timeout": 5.0,
        }
        if cache:
            _ = self.translator.preaccelerate_and_speedtest()  # Optional. Caching sessions in advance, which can help improve access speed.

    def _do_translate(self, input_data: Union[str, List[str]], src: str, dest: str) -> Union[str, List[str]]:
        """
        translate_text(query_text: str, translator: str = 'bing', from_language: str = 'auto', to_language: str = 'en', **kwargs) -> Union[str, dict]
            :param query_text: str, must.
            :param translator: str, default 'bing'.
            :param from_language: str, default 'auto'.
            :param to_language: str, default 'en'.
            :param if_use_preacceleration: bool, default False.
            :param **kwargs:
                    :param is_detail_result: bool, default False.
                    :param professional_field: str, default None. Support alibaba(), baidu(), caiyun(), cloudTranslation(), elia(), sysTran(), youdao(), volcEngine() only.
                    :param timeout: float, default None.
                    :param proxies: dict, default None.
                    :param sleep_seconds: float, default 0.
                    :param update_session_after_freq: int, default 1000.
                    :param update_session_after_seconds: float, default 1500.
                    :param if_use_cn_host: bool, default False. Support google(), bing() only.
                    :param reset_host_url: str, default None. Support google(), yandex() only.
                    :param if_check_reset_host_url: bool, default True. Support google(), yandex() only.
                    :param if_ignore_empty_query: bool, default False.
                    :param limit_of_length: int, default 20000.
                    :param if_ignore_limit_of_length: bool, default False.
                    :param if_show_time_stat: bool, default False.
                    :param show_time_stat_precision: int, default 2.
                    :param if_print_warning: bool, default True.
                    :param lingvanex_mode: str, default 'B2C', choose from ("B2C", "B2B").
                    :param myMemory_mode: str, default "web", choose from ("web", "api").
            :return: str or dict
        """

        return self.translator.translate_text(input_data, from_language=src, to_language=dest, **self.config)


if __name__ == '__main__':
    test = MultipleProviders()
    print(test.translate("Hello", src="en", dest="vi").text)