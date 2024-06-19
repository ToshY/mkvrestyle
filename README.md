<h1 align="center"> 📺 MKVrestyle </h1>

<div align="center">
    <img src="https://img.shields.io/github/v/release/toshy/mkvrestyle?label=Release&sort=semver" alt="Current bundle version" />
    <img src="https://img.shields.io/github/actions/workflow/status/toshy/mkvrestyle/codestyle.yml?branch=main&label=Ruff" alt="Ruff">
    <img src="https://img.shields.io/github/actions/workflow/status/toshy/mkvrestyle/statictyping.yml?branch=main&label=Mypy" alt="Mypy">
    <img src="https://img.shields.io/github/actions/workflow/status/toshy/mkvrestyle/security.yml?branch=main&label=Security%20check" alt="Security check" />
    <br /><br />
</div>

## 📝 Quickstart

A command-line utility for basic restyling of an embedded ASS file with a new user-defined font and styling.

## 🧰 Requirements

* 🐋 [Docker](https://docs.docker.com/get-docker/)

## 🎬 Usage

MKVrestyle requires 2 volumes to be mounted: `/app/input` and `/app/output`; the other directorys (`/app/preset` is optional).

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

> [!NOTE]
> The `/app/preset` volume mount is optional.

> [!TIP]
> You can add additional JSON presets by mounting the files to the preset directory.
> ```shell
> ./preset/custom.json:/app/preset/custom.json
> ```

> > [!TIP]
> In order to use fonts for the new styling, you can mount your own fonts directory to `/usr/local/share/fonts`.
> ```shell
> # Mount local fonts directory
> ./fonts:/usr/local/share/fonts:ro
> # Mount system-wide fonts directory
> /usr/share/fonts:/usr/local/share/fonts:ro
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

## ❕ License

This repository comes with a [MIT license](./LICENSE).
