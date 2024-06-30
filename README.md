<h1 align="center"> 📺 MKVrestyle </h1>

<div align="center">
    <img src="https://img.shields.io/github/v/release/toshy/mkvrestyle?label=Release&sort=semver" alt="Current bundle version" />
    <img src="https://img.shields.io/github/actions/workflow/status/toshy/mkvrestyle/codestyle.yml?branch=main&label=Black" alt="Black">
    <img src="https://img.shields.io/github/actions/workflow/status/toshy/mkvrestyle/codequality.yml?branch=main&label=Ruff" alt="Ruff">
    <img src="https://img.shields.io/github/actions/workflow/status/toshy/mkvrestyle/statictyping.yml?branch=main&label=Mypy" alt="Mypy">
    <img src="https://img.shields.io/github/actions/workflow/status/toshy/mkvrestyle/security.yml?branch=main&label=Security%20check" alt="Security check" />
</div>

## 📝 Quickstart

A command-line utility for basic restyling of an embedded ASS file with a new user-defined font and styling.

> [!WARNING]
> Resampling currently only works for the main dialogue font; lines containing tags for inline styling might be broken after resampling!

## 🧰 Requirements

* 🐋 [Docker](https://docs.docker.com/get-docker/)

## 🎬 Usage

MKVrestyle requires 2 volumes to be mounted: `/app/input` and `/app/output`.

### 🐋 Docker

```shell
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  ghcr.io/toshy/mkvrestyle:latest -h
```

### 🐳 Compose

Create a `compose.yaml` file.

```yaml
services:
  mkvrestyle:
    image: ghcr.io/toshy/mkvrestyle:latest
    volumes:
      - ./input:/input
      - ./output:/output
```

Then run it.

```shell
docker compose run -u $(id -u):$(id -g) --rm mkvrestyle -h
```

> [!TIP]
> You can add additional JSON presets by mounting the files to the preset directory:
> ```shell
> ./preset/custom.json:/app/preset/custom.json
> ```

> [!TIP]
> Sometimes MKV files are missing embedded fonts, which can lead to incorrectly styled subtitles. One way to prevent this
> from happening, is to mount an additional (system-wide) fonts directory to `/app/fonts`. FFmpeg (fontconfig) will
> use that directory as a fallback in case an embedded font is missing.
> ```yaml
> # Mount local fonts directory
> ./fonts:/app/fonts:ro
> # Mount system-wide fonts directory
> /usr/share/fonts:/app/fonts:ro
> ```

## 🛠️ Contribute

### Requirements

* ☑️ [Pre-commit](https://pre-commit.com/#installation).
* 🐋 [Docker Compose V2](https://docs.docker.com/compose/install/)
* 📋 [Task 3.37+](https://taskfile.dev/installation/)

### Pre-commit

Setting up `pre-commit` code style & quality checks for local development.

```shell
pre-commit install
```

## 📚 Suite

Check out the other tools:

- [MKVimport](https://github.com/ToshY/mkvimport) - embedding attachments (subtitles, fonts and chapters) to MKV files.
- [MKVexport](https://github.com/ToshY/mkvexport) - extracting attachments (subtitles, fonts and chapters) of MKV files.
- [MKVresort](https://github.com/ToshY/mkvresort) - resorting streams in a user-defined fashion.
- [FFconv](https://github.com/ToshY/ffconv) - hardcoding subtitles into videos by converting MKV to MP4.

## ❕ License

This repository comes with a [MIT license](./LICENSE).
