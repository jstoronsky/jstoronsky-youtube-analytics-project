import json
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Video:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id: str) -> None:
        """
        Через экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API.
        """
        self.__video_id = video_id

    def print_info(self):
        """
        Выводит в консоль информацию о видосе.
        """
        video_ = self.youtube.videos().list(id=self.__video_id, part='snippet,statistics').execute()["items"]
        eventual_print = json.dumps(video_, indent=2, ensure_ascii=False)
        return video_, eventual_print

    @property
    def video_id(self):
        """
        получаем id видео
        """
        return self.__video_id

    @property
    def video_title(self):
        """
        получаем название видео
        """
        title = [tt["snippet"]["title"] for tt in self.print_info()[0]]
        try:
            title[0]
        except HttpError:
            return None
        except IndexError:
            return None
        else:
            return title[0]

    @property
    def video_url(self):
        """
        ссылка на видео
        """
        return f'https://www.youtube.com/watch?v={self.__video_id}'

    @property
    def video_views_count(self):
        """
        количество просмотров у видео
        """
        views_count = [vd["statistics"]["viewCount"] for vd in self.print_info()[0]]
        try:
            views_count[0]
        except HttpError:
            return None
        except IndexError:
            return None
        else:
            return views_count[0]

    @property
    def video_likes_count(self):
        """
        количество лайков у видео
        """
        likes_count = [lk["statistics"]["likeCount"] for lk in self.print_info()[0]]
        try:
            likes_count[0]
        except HttpError:
            return None
        except IndexError:
            return None
        else:
            return likes_count[0]

    def __str__(self):
        if self.video_title is None:
            return "None"
        return self.video_title


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def check_playlist_id(self):
        """
        Выводит в консоль id плейлиста, либо ошибку если id видео и плейлиста не совпадают
        """
        playlist_items = self.youtube.playlistItems().list(playlistId=self.playlist_id, part='snippet').execute()
        playlist_id_info = [data["snippet"]["playlistId"] for data in list(playlist_items.values())[3]
                            if self.video_id == data["snippet"]["resourceId"]["videoId"]]
        if len(playlist_id_info) == 0:
            raise ValueError("video id and playlist id do not match")
        else:
            return playlist_id_info[0]

    @property
    def link_to_video_in_playlist(self):
        """
        возвращает ссылку на видео в плейлисте
        """
        return f"https://www.youtube.com/watch?v={self.video_id}&list={self.check_playlist_id()}"
