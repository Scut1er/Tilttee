import validators
from yt_dlp import YoutubeDL
from config import YDL_OPT


class Track:
    """
    Представляет трек с URL источника и названием.

    Атрибуты:
    - source: URL трека.
    - title: Название трека.
    - playlist: Плейлист, к которому принадлежит трек (по умолчанию None).
    """

    def __init__(self, source: str, title: str, playlist=None):
        self.source = source
        self.title = title
        self.playlist = playlist

    def __repr__(self):
        return f"{self.title}"


async def search_track(player, query):
    """
    Выполняет поиск трека на YouTube.

    Parameters:
    - player: объект плеера
    - query: строка запроса или ссылка на видео

    Returns:
    - Объект Track с URL источника и названием, или None, если результат не найден.
    """
    with YoutubeDL(YDL_OPT) as ytdl:
        # Если это не ссылка, использовать ytsearch
        if not validators.url(query):
            query = f"ytsearch1:{query}"

        info = await player.bot.loop.run_in_executor(None, lambda: ytdl.extract_info(query, download=False))

        # ytsearch возвращает 'entries', URL — обычный возврат
        if "entries" in info and info["entries"]:
            info = info["entries"][0]

        if not info:
            return None

        return Track(source=info.get('url'), title=info.get('title'))


async def search_playlist(player, query):
    """
    Выполняет поиск плейлиста на YouTube и возвращает его треки.

    Parameters:
    - query: Запрос для поиска или URL плейлиста.

    Returns:
    - Список объектов Track, или None, если результаты не найдены.
    """
    with YoutubeDL(YDL_OPT) as ytdl:
        info = await player.bot.loop.run_in_executor(None, lambda: ytdl.extract_info(query, download=False))
        if not info:
            return None
        tracks = [Track(source=entry['url'], title=entry['title'], playlist=query) for entry in info['entries'] if
                  entry]
        unavailable = len(info['entries']) - len(tracks)
        if unavailable > 0:
            await player.ctx.send(f"```⚠️ {unavailable} трек(ов) были недоступны и пропущены.```")
        return tracks


async def get_first_track_from_playlist(player, query) -> Track | None:
    """
    Получает первый трек из плейлиста.

    Parameters:
    - query: URL или строка запроса плейлиста.

    Returns:
    - Track или None, если не найдено ни одного трека.
    """
    ytdl_params = YDL_OPT.copy()
    ytdl_params['playlistend'] = 1  # Скачиваем только первый трек

    with YoutubeDL(ytdl_params) as ytdl:
        try:
            info = await player.bot.loop.run_in_executor(
                None, lambda: ytdl.extract_info(query, download=False)
            )

            entries = info.get('entries')
            if entries and len(entries) > 0:
                first = entries[0]
                return Track(source=first['url'], title=first['title'], playlist=query)
            return None
        except Exception as e:
            print(f"Ошибка при получении первого трека: {e}")
            return None
