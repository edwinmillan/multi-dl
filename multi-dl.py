import asyncio
import youtube_dl
import typing
import click


class CustomLogger:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def debug(self, msg):
        if self.verbose:
            print('DEBUG', msg)

    def warning(self, msg):
        print('WARNING', msg)

    def error(self, msg):
        print('ERROR', msg)


class FileProgress:
    def __init__(self, filename, downloaded_bytes, total_bytes, done):
        self.filename: filename
        self.downloaded_bytes: downloaded_bytes
        self.total_bytes: total_bytes
        self.done: done


class Coordinator:
    def __init__(self, **kwargs):
        pass


def get_playlist(playlist_file: typing.IO) -> str:
    for url in playlist_file:
        url = url.strip()
        if url:
            yield url


def download_video(url: str, options: dict = None):
    ydl_opts = options or {
        'logger': CustomLogger(verbose=False),
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


async def run_in_executor(sync_func, *params):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, sync_func, *params)


async def async_main(playlist_file):
    urls = []

    if playlist_file:
        urls.extend(get_playlist(playlist_file))

    tasks = [run_in_executor(download_video, url) for url in urls]

    await asyncio.gather(*tasks)


@click.command()
@click.argument('playlist_file', type=click.File('r'))
def main(playlist_file):
    asyncio.run(async_main(playlist_file))


if __name__ == '__main__':
    main()
