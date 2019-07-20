import asyncio
import youtube_dl
import typing
import click
from tqdm import tqdm


class CustomLogger:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def debug(self, msg):
        if self.verbose:
            print('DEBUG', msg)

    def warning(self, msg):
        if self.verbose:
            print('WARNING', msg)

    def error(self, msg):
        print('ERROR', msg)


def get_playlist(playlist_file: typing.IO) -> str:
    for url in playlist_file:
        url = url.strip()
        if url:
            yield url


def download_video(url: str, options: dict = None):
    tqdm.write(f'Downloading {url}')
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

    for future in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
        await future


@click.command()
@click.argument('playlist_file', type=click.File('r'))
def main(playlist_file):
    asyncio.run(async_main(playlist_file))


if __name__ == '__main__':
    main()
