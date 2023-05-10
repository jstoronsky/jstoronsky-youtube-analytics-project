import os
from googleapiclient.discovery import build
import isodate
import datetime


class PlayList:
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id

    def print_info(self):
        """
        Выводит в консоль информацию о плейлисте.
        """
        data_in_dict = self.youtube.playlists().list(id=self.playlist_id, part='snippet').execute()
        return data_in_dict

    @property
    def title(self):
        """
        Получаем из ранее полученной информации название плейлиста
        """
        title_ = [tl["snippet"]["title"] for tl in self.print_info()["items"]]
        return title_[0]

    @property
    def url(self):
        """
        Формируем ссылку на плейлист
        """
        return f'https://www.youtube.com/playlist?list={self.playlist_id}'

    @property
    def total_duration(self):
        """
        получаем длительность всех видео в плейлисте
        сначала достаём айди каждого видео в плейлисте, затем по айди вытаскиваем длительность
        переводим длительность в человеческий формат при помощи isodate.parse_duration
        затем переводим в общее количество часов при помощи datetime.timedelta
        """
        content = self.youtube.playlistItems().list(playlistId=self.playlist_id, part='contentDetails').execute()
        video_ids_list = [id_["contentDetails"]["videoId"] for id_ in content["items"]]
        video_info = self.youtube.videos().list(id=video_ids_list, part='contentDetails, statistics').execute()
        durations = [dr["contentDetails"]["duration"] for dr in video_info["items"]]
        edited_durations = [isodate.parse_duration(length).total_seconds() for length in durations]
        total_hours = datetime.timedelta(seconds=sum(edited_durations))
        return total_hours

    def show_best_video(self):
        """
        получаем видео с наибольшим количеством лайков
        достаём айди всех видео, по ним получаем лайки у каждого видоса
        затем получаем индекс видео с самым высоким количеством лайков и формируем ссылку
        """
        content = self.youtube.playlistItems().list(playlistId=self.playlist_id, part='contentDetails').execute()
        video_ids_list = [id_["contentDetails"]["videoId"] for id_ in content["items"]]
        video_info = self.youtube.videos().list(id=video_ids_list, part='statistics').execute()
        likes_number = [int(like["statistics"]["likeCount"]) for like in video_info["items"]]
        best_video_id = video_ids_list[likes_number.index(max(likes_number))]
        return f'https://youtu.be/{best_video_id}'
