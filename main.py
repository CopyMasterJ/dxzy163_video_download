import asyncio
import os
import re
import shutil
import subprocess
import time
import httpx
import m3u8
import requests
from util.ColorLogUtil import logger


class FileDownloader:
    def __init__(self, client, nested_m3u8_url, output_dir, index, ts_file, semaphore, video_index):
        self.client = client
        self.nested_m3u8_url = nested_m3u8_url
        self.output_dir = output_dir
        self.index = index
        self.ts_file = ts_file
        self.semaphore = semaphore
        self.video_index = video_index

    async def __call__(self):
        ts_url = f'{self.nested_m3u8_url.rsplit("/", 1)[0]}/{self.ts_file.uri}'
        # 最大重试链接次数
        max_retries = 30
        async with self.semaphore:
            retries = 1
            # 在请求失败时重新请求
            while retries < max_retries:
                try:
                    response = await self.client.get(ts_url)
                    response.raise_for_status()
                    content = response.content
                    file_path = os.path.join(self.output_dir, f'{self.index}.ts')

                    with open(file_path, 'wb') as f:
                        f.write(content)
                    if retries > 1:
                        logger.info(f' 第{self.video_index}集-({self.index}.ts)号数据流第{retries}次请求成功:')
                    logger.info(f"第{self.video_index}集-第({self.index}.ts)号数据流文件:{ts_url} 下载完成!")
                    break  # 成功获取响应，跳出循环
                except Exception as e:
                    logger.warning(f"An error occurred: {e}")
                    # 判断请求次数是否大于最大重试链接次数
                    if retries < max_retries:
                        logger.warning(
                            f" 对方服务器响应失败 第{self.video_index}集-({self.index}.ts)号数据流第({retries}/{max_retries})尝试重新请求...")
                        retries += 1
                        # await asyncio.sleep(1)  # 可以根据需要调整重试之间的等待时间
                    else:
                        logger.error(
                            f" 达到最大重试次数,当前第{self.video_index}集-第{self.index}.ts下载失败:{self.nested_m3u8_url}")
                        break  # 达到最大重试次数，跳出循环


async def download_video(url, output_dir, output_filename, video_index):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        time.sleep(1)
    os.makedirs(output_dir)

    requests.packages.urllib3.disable_warnings()
    m3u8_content = requests.get(url, verify=False).text
    m3u8_obj = m3u8.loads(m3u8_content)

    nested_m3u8_url = f'{url.rsplit("/", 1)[0]}/{m3u8_obj.playlists[0].uri}'
    nested_m3u8_content = requests.get(nested_m3u8_url, verify=False).text
    nested_m3u8_obj = m3u8.loads(nested_m3u8_content)
    num_segments = len(nested_m3u8_obj.segments)
    logger.info(f"{output_filename}中共有{num_segments}段文件正在下载:")

    semaphore = asyncio.Semaphore(30)

    async with httpx.AsyncClient(verify=False, timeout=60) as client:
        tasks = []
        for i, ts_file in enumerate(nested_m3u8_obj.segments):
            downloader = FileDownloader(client, nested_m3u8_url, output_dir, i, ts_file, semaphore, video_index)
            tasks.append(downloader())

        await asyncio.gather(*tasks, return_exceptions=True)

    output_path = os.path.join('E:\\video\\', output_filename)

    with open(os.path.join(output_dir, 'filelist.txt'), 'w', encoding='utf-8') as filelist:
        for i in range(num_segments):
            ts_path = os.path.join(output_dir, f'{i}.ts')
            filelist.write(f"file '{ts_path}'\n")

    ffmpeg_path = r'E:\\config\\ffmpeg-n6.1.1-win64-lgpl-6.1\\bin\\ffmpeg.exe'
    filelist_path = f'{output_dir}\\filelist.txt'
    cmd = f'{ffmpeg_path} -f concat -safe 0 -i {filelist_path} -c copy {output_path}.mp4'
    subprocess.call(cmd, shell=True)
    # 删除临时文件
    shutil.rmtree(output_dir)
    logger.info(f"第{video_index}集下载完成!")


async def main():
    output_dir = 'E:\\video\\wlsj'

    requests.packages.urllib3.disable_warnings()
    m3u8_content = requests.get('https://www.dxzy163.com/playdata/8/4360.js?52888.01', verify=False).text

    pattern = r'\$(https://[^$]+)'
    video_links = re.findall(pattern, m3u8_content)

    for index, video_link in enumerate(video_links, start=1):
        if index >= 110:
            logger.info(f"Video {index}: {video_link}\n")
            logger.info(f"开始下载第{index}集.\n")
            await download_video(video_link, f'{output_dir}_{index}', f'净空法师《大乘无量寿经》视频讲座_第{index}集',
                                 index)


if __name__ == "__main__":
    asyncio.run(main())
