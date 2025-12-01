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
AZURE_OPENAI_API_VERSION=2025-01-01-preview
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