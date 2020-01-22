from typing import TYPE_CHECKING, Optional, List, Union

if TYPE_CHECKING:
    from yandex_music import Client

from yandex_music import YandexMusicObject, Artist, Album, Track, Playlist, Video


de_json_result = {
    'track': Track.de_list,
    'artist': Artist.de_list,
    'album': Album.de_list,
    'playlist': Playlist.de_list,
    'video': Video.de_list,
}


class SearchResult(YandexMusicObject):
    """Класс, представляющий результат поиска.

        Attributes:
            total (:obj:`int`): Количество результатов.
            per_page (:obj:`int`): Максимальное количество результатов на странице.
            order (:obj:`int`): Номер страницы.
            results (:obj:`list` из :obj:`yandex_music.Track` | :obj:`yandex_music.Artist` | :obj:`yandex_music.Album` \
                | :obj:`yandex_music.Playlist` | :obj:`yandex_music.Video`): Результаты поиска.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Args:
            total (:obj:`int`): Количество результатов.
            per_page (:obj:`int`): Максимальное количество результатов на странице.
            order (:obj:`int`): Номер страницы.
            results (:obj:`list` из :obj:`yandex_music.Track` | :obj:`yandex_music.Artist` | :obj:`yandex_music.Album` \
                | :obj:`yandex_music.Playlist` | :obj:`yandex_music.Video`): Результаты поиска.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.
            **kwargs: Произвольные ключевые аргументы полученные от API.
    """
    
    def __init__(self,
                 total: int,
                 per_page: int,
                 order: int,
                 results: List[Union[Track, Artist, Album, Playlist, Video]],
                 client: Optional['Client'] = None,
                 **kwargs) -> None:
        self.total = total
        self.per_page = per_page
        self.order = order
        self.results = results

        self.client = client
        self._id_attrs = (self.total, self.per_page, self.order, self.results)

    @classmethod
    def de_json(cls, data: dict, client: 'Client', type_: str = None) -> Optional['SearchResult']:
        """Десериализация объекта.

        Args:
            data (:obj:`dict`): Поля и значения десериализуемого объекта.
            client (:obj:`yandex_music.Client`): Объект класса :class:`yandex_music.Client` представляющий клиент Yandex
                Music.

        Returns:
            :obj:`yandex_music.SearchResult`: Объект класса :class:`yandex_music.SearchResult`.
        """
        if not data:
            return None

        data = super(SearchResult, cls).de_json(data, client)
        data['results'] = de_json_result.get(type_)(data.get('results'), client)

        return cls(client=client, **data)
