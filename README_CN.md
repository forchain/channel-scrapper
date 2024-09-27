# YouTube频道字幕下载器

这个Python程序可以输入YouTube的频道地址，然后下载该频道所有视频的字幕。

[English README](README.md)

## 功能

- 从输入的YouTube频道URL获取所有视频ID
- 下载每个视频的字幕（如果可用）
- 将字幕保存为文本文件，每个视频一个文件

## 安装

1. 克隆此仓库或下载源代码。
2. 安装所需的依赖项：

   ```
   pip install -r requirements.txt
   ```

3. 获取YouTube API密钥：
   a. 访问 [Google Developers Console](https://console.developers.google.com/)
   b. 创建一个新项目或选择现有项目
   c. 在左侧菜单中，点击"API和服务" > "库"
   d. 搜索并启用 "YouTube Data API v3"
   e. 在左侧菜单中，点击"凭据"
   f. 点击"创建凭据" > "API密钥"
   g. 复制生成的API密钥

4. 将 `config.example.py` 复制为 `config.py`，并在其中填入你的YouTube API密钥：
   ```python
   API_KEY = "你的API密钥"
   ```

## 使用方法

1. 运行 `main.py` 文件：

   ```
   python main.py
   ```

2. 如果在 `config.py` 中没有设置默认频道，程序会提示你输入YouTube频道的URL。
3. 程序将开始下载字幕，并将它们保存在 `subtitles` 目录中。

## 注意事项

- 你需要一个有效的YouTube API密钥才能使用此程序。
- 请注意YouTube API的使用配额限制。
- 某些视频可能没有字幕或字幕不可用，程序会跳过这些视频。

## 许可

此项目采用 MIT 许可证。详情请参阅 LICENSE 文件。