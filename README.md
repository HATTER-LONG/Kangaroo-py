# Kangaroo-py

## whisper api client

- 基于 `[whisper-asr-webservice](https://github.com/ahmetoner/whisper-asr-webservice)` 服务端提供端 api 实现脚本客户端功能：
  1. 自动分离视频中音频。
  2. 上传到 `whisper-asr-webservice` 中进行识别。
  3. 通过 `google-translate` 进行翻译生成 srt 字幕。
  4. 支持客户端录制音频实时上传翻译。
