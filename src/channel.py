import json
import os
from googleapiclient.discovery import build


class Channel:
    """
    Класс для ютуб-канала
    """
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """
        Через экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API.
        """
        self.__channel_id = channel_id

    def print_info(self):
        """
        Выводит в консоль информацию о канале.
        """
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()["items"]
        eventual_print = json.dumps(channel, indent=2, ensure_ascii=False)
        return channel, eventual_print

    @property
    def channel_id(self):
        return self.__channel_id

    @property
    def title(self):
        """
        получаем название канала
        """
        title_ = [tt["snippet"]["title"] for tt in self.print_info()[0]]
        return title_[0]

    @property
    def description(self):
        """
        описание канала
        """
        description = [dsc["snippet"]["description"] for dsc in self.print_info()[0]]
        return description[0]

    @property
    def url(self):
        """
        ссылка на канал
        """
        return f'https://www.youtube.com/channel/{self.__channel_id}'

    @property
    def subscribers_count(self):
        """
        количество подписчиков
        """
        subscribers_count = [sbc["statistics"]["subscriberCount"] for sbc in self.print_info()[0]]
        return subscribers_count[0]

    @property
    def video_count(self):
        """
        количество видео
        """
        video_count = [vd["statistics"]["videoCount"] for vd in self.print_info()[0]]
        return video_count[0]

    @property
    def overall_views_count(self):
        """

        общее количество просмотров
        """
        views_count = [vd["statistics"]["viewCount"] for vd in self.print_info()[0]]
        return views_count[0]

    @classmethod
    def get_service(cls):
        """
        возвращает объект для работы с YouTube API
        """
        return cls.youtube

    def to_json(self, jsn_file):
        """
        сохраняет в файл значения атрибутов экземпляра Channel
        """
        python_dict = dict(id=self.channel_id, title=self.title, description=self.description, url=self.url,
                           subscribers_number=self.subscribers_count, videos=self.video_count,
                           overall_views=self.overall_views_count)
        jsn_list = json.dumps(python_dict, indent=3, ensure_ascii=False)
        with open(jsn_file, "wt", encoding="utf-8") as file:
            file.write(jsn_list)

    def __add__(self, other):
        """
        метод сложения
        """
        return int(self.subscribers_count) + int(other.subscribers_count)

    def __sub__(self, other):
        """
        метод вычитания
        """
        return int(self.subscribers_count) - int(other.subscribers_count)

    def __lt__(self, other):
        """
        метод если self меньше other
        """
        return int(self.subscribers_count) < int(other.subscribers_count)

    def __le__(self, other):
        """
        метод если self меньше или равно other
        """
        return int(self.subscribers_count) <= int(other.subscribers_count)

    def __gt__(self, other):
        """
        метод если self больше other
        """
        return int(self.subscribers_count) > int(other.subscribers_count)

    def __ge__(self, other):
        """
        метод если self больше или равно other
        """
        return int(self.subscribers_count) >= int(other.subscribers_count)

    def __str__(self):
        return f"{self.title} ({self.url})"
