# Azure STT Sample

Azure OpenAI の音声認識モデルを比較するサンプルアプリケーションです。

## 対応モデル

以下の4つのモデルを比較します：

- **Whisper** - OpenAI の Whisper モデル
- **gpt-4o-transcribe** - GPT-4o ベースの文字起こしモデル
- **gpt-4o-mini-transcribe** - GPT-4o-mini ベースの軽量文字起こしモデル
- **gpt-4o-transcribe-diarize** - 話者識別機能付きの文字起こしモデル

## 前提条件

- Python 3.12 以上
- [uv](https://docs.astral.sh/uv/) パッケージマネージャー
- Azure OpenAI リソース（上記モデルがデプロイされていること）

## セットアップ

1. リポジトリをクローン

```bash
git clone https://github.com/h-morozumi/azure-stt-sample.git
cd azure-stt-sample
```

2. 環境変数を設定

`.env.example` をコピーして `.env` を作成し、Azure OpenAI の接続情報を設定します。

```bash
cp .env.example .env
```

`.env` ファイルを編集：

```
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_API_VERSION=2025-04-01-preview
```

3. 依存関係をインストール

```bash
uv sync
```

## 使い方

音声ファイルを `audio` フォルダに配置し、以下のコマンドで実行します：

```bash
uv run main.py ./audio/your-audio-file.mp3
```

## response_format について

`main.py` では、各モデルごとに `response_format` を切り替えてリクエストしています。

- 公式ドキュメント上、音声文字起こしの `response_format` は `json` / `text` / `srt` / `verbose_json` / `vtt` が定義されています。
- `timestamp_granularities[]` を使う場合、`response_format` は `verbose_json` である必要があります。
- `gpt-4o-transcribe` / `gpt-4o-transcribe-diarize` / `gpt-4o-mini-transcribe` など一部の音声文字起こしモデルは、ドキュメント上「`json` のみ対応」と記載があります。

参考（公式）:

- https://learn.microsoft.com/en-us/azure/ai-foundry/openai/reference-preview?view=foundry-classic#transcriptions---create
- https://learn.microsoft.com/en-us/azure/ai-foundry/openai/reference-preview-latest?view=foundry-classic#components

### gpt-4o-transcribe-diarize の json / diarized_json

このサンプルでは `gpt-4o-transcribe-diarize` に対して `response_format="diarized_json"` を指定しています。

- `response_format` を `json` に変更すると、出力は通常の JSON 形式になり、話者識別（diarization）に関する情報の有無や構造が変わります。
- `diarized_json` は上記の公式 REST 仕様の列挙値には含まれていないため、利用可否や出力形式は API バージョン/SDK 実装によって変わる可能性があります（動作しない場合は `json` に戻してください）。

### 例

```bash
uv run main.py ./audio/sample.mp3
```

## 対応している音声形式

- MP3
- WAV
- M4A
- WEBM
- その他 Azure OpenAI がサポートする形式

## ライセンス

MIT License