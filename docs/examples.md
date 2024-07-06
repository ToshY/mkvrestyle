# Examples

## Basic

Add your files to the input directory of the mounted container.

```shell
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  ghcr.io/toshy/mkvrestyle:latest
```

By default, it will find all files from the `/app/input` directory (recursively) and write the output to the `/app/output`
directory. If no presets are provided, it will automatically use the [`preset/default.json`](presets.md#default)

## Specific file

Restyling subtitles for a specific file and writing output to `/app/output` (default).

```shell
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  ghcr.io/toshy/mkvrestyle:latest \
  -i "input/rick-astley-never-gonna-give-you-up.mkv"
```

## Single file with output subdirectory

Restyling subtitles for a specific file and writing output to `/app/output/hits`.

```shell
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  ghcr.io/toshy/mkvrestyle:latest \
  -i "input/rick-astley-never-gonna-give-you-up.mkv" \
  -o "output/hits"
```

## Specific subdirectory

Restyling subtitles for a files in specific subdirectory and writing output to `/app/output/hits`.

```shell
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  ghcr.io/toshy/mkvrestyle:latest \
  -i "input/hits" \
  -o "output/hits"
```

## Multiple inputs

Restyling subtitles for files in multiple input subdirectories and writing output to `/app/output` (default).

```shell
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  ghcr.io/toshy/mkvrestyle:latest \
  -i "input/dir1" \
  -i "input/dir2" \
  -i "input/dir3" \
  -i "input/dir4" \
  -i "input/dir5"
```

## Multiple inputs and outputs

Restyling subtitles for files in multiple input subdirectories and writing output to specific output subdirectories
respectively.

```shell
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  ghcr.io/toshy/mkvrestyle:latest \
  -i "input/dir1" \
  -i "input/dir2" \
  -i "input/dir3" \
  -i "input/dir4" \
  -i "input/dir5" \
  -o "output/dir1" \
  -o "output/dir2" \
  -o "output/dir3" \
  -o "output/dir4" \
  -o "output/dir5"
```

## Multiple inputs, outputs and single preset

Restyling subtitles for files in multiple input subdirectories, with single video and audio preset, and writing output
to specific output subdirectories respectively.

```shell
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  ghcr.io/toshy/mkvrestyle:latest \
  -i "input/dir1" \
  -i "input/dir2" \
  -i "input/dir3" \
  -i "input/dir4" \
  -i "input/dir5" \
  -p "preset/style-custom.json" \
  -o "output/dir1" \
  -o "output/dir2" \
  -o "output/dir3" \
  -o "output/dir4" \
  -o "output/dir5"
```

## Multiple inputs, outputs and presets

Restyling subtitles for files in multiple input subdirectories, with different presets, and writing output to specific
output subdirectories respectively.

```shell
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  -v ${PWD}/preset/video-custom.json:/app/preset/video-custom.json \
  -v ${PWD}/preset/audio-custom.json:/app/preset/audio-custom.json \
  ghcr.io/toshy/mkvrestyle:latest \
  -i "input/dir1" \
  -i "input/dir2" \
  -i "input/dir3" \
  -i "input/dir4" \
  -i "input/dir5" \
  -p "preset/style-custom.json" \
  -p "preset/style-custom-two.json" \
  -p "preset/style-custom-three.json" \
  -p "preset/style-custom-four.json" \
  -p "preset/style-custom.json" \
  -o "output/dir1" \
  -o "output/dir2" \
  -o "output/dir3" \
  -o "output/dir4" \
  -o "output/dir5"
```
