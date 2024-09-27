import unittest
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

class TestYouTubeTranscriptApi(unittest.TestCase):
    def setUp(self):
        # 设置代理
        self.proxies = {"https": "http://127.0.0.1:1087"}  # 替换为你的代理

    def test_get_transcript(self):
        # 测试视频ID列表
        video_ids = [
            "wWe-gL9B5PU",
            "crwZsfASaDY",
            "pQSd3N-DSbk",  # 应该有字幕的视频
            "gLss-OlSJMg",  # 字幕被禁用的视频
            "dQw4w9WgXcQ"   # 一个流行的视频，很可能有字幕
        ]

        for video_id in video_ids:
            with self.subTest(video_id=video_id):
                try:
                    # 尝试获取简体中文的字幕
                    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['zh-Hans'], proxies=self.proxies)
                    # 下载字幕，不包含时间信息
                    with open(f"{video_id}_zh-Hans.txt", "w", encoding="utf-8") as f:
                        for entry in transcript:
                            f.write(f"{entry['text']}\n")  # 去掉时间信息
                    self.assertIsInstance(transcript, list)
                    self.assertTrue(len(transcript) > 0)
                    print(f"视频 {video_id} 成功获取到简体中文字幕，字幕长度：{len(transcript)}")
                except NoTranscriptFound:
                    print(f"视频 {video_id} 没有找到简体中文字幕，尝试获取繁体中文字幕")
                    try:
                        # 尝试获取繁体中文的字幕
                        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['zh-Hant'], proxies=self.proxies)
                        # 下载字幕，不包含时间信息
                        with open(f"{video_id}_zh-Hant.txt", "w", encoding="utf-8") as f:
                            for entry in transcript:
                                f.write(f"{entry['text']}\n")  # 去掉时间信息
                        self.assertIsInstance(transcript, list)
                        self.assertTrue(len(transcript) > 0)
                        print(f"视频 {video_id} 成功获取到繁体中文字幕，字幕长度：{len(transcript)}")
                    except NoTranscriptFound:
                        print(f"视频 {video_id} 没有找到繁体中文字幕")
                except TranscriptsDisabled:
                    print(f"视频 {video_id} 的字幕已被禁用")
                except Exception as e:
                    self.fail(f"获取视频 {video_id} 的字幕时发生意外错误: {str(e)}")

if __name__ == '__main__':
    unittest.main()
