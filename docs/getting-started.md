## Requirements

- 🐋 [Docker](https://docs.docker.com/get-docker/)

## Pull image

```shell
docker pull ghcr.io/toshy/mkvrestyle:latest
```

## Run container

### 🐋 Docker

Run with `docker`.

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
      - ./input:/app/input
      - ./output:/app/output
```

Run with `docker compose`.

```shell
docker compose run -u $(id -u):$(id -g) --rm mkvrestyle -h
```

## Volumes

The following volume mounts are **required**: 

- `/app/input`
- `/app/output`

The following volume mounts are **optional**: 

- `/app/preset`
- `/app/fonts`

!!! tip

    Sometimes MKV files are missing embedded fonts, which can lead to incorrectly styled subtitles. One way to prevent this
    from happening, is to mount an additional (system-wide) fonts directory to `/app/fonts`.
    ```yaml
    # Mount local fonts directory
    ./fonts:/app/fonts:ro
    # Mount system-wide fonts directory
    /usr/share/fonts:/app/fonts:ro
    ```