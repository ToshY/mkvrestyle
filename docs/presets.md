## Usage

The following section shows the basic presets that are already available. You
can add your custom presets by mounting files to the `/app/preset` directory.

---

### 🐋 Docker

```sh
docker run -it --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/input:/app/input \
  -v ${PWD}/output:/app/output \
  -v ${PWD}/preset/style-custom.json:/app/preset/style-custom.json \
  ghcr.io/toshy/mkvrestyle:latest
```

### 🐳 Compose

```yaml
services:
  mkvrestyle:
    image: ghcr.io/toshy/mkvrestyle:latest
    volumes:
      - ./input:/app/input
      - ./output:/app/output
      - ./preset/style-custom.json:/app/preset/style-custom.json
```

## Style

Argument: `--preset` / `-p`.

---

### Default

???+ example "`default.json`"

    ```json
    {
        "Fontsize": {
            "factor": 0.95,
            "round": 0
        },
        "ScaleX": {
            "factor": 1,
            "round": 0
        },
        "ScaleY": {
            "factor": 1,
            "round": 0
        },
        "Spacing": {
            "factor": 1,
            "round": 0
        },
        "Outline": {
            "factor": 0.646,
            "round": 2
        },
        "Shadow": {
            "factor": 0,
            "round": 0
        },
        "MarginL": {
            "factor": 0,
            "round": 0
        },
        "MarginR": {
            "factor": 0,
            "round": 0
        },
        "MarginV": {
            "factor": 0.81,
            "round": 0
        }
    }
    ```

### Custom

Additionally, you can add the `FontName` key to supply a font face as replacement for existing styles.

Replacing the font face requires mounting the `/app/fonts` directory with the font you want to use.

#### All styles

Supply `all` for the `substitute` option to replace all styles (dialogue, signs, etc.).

```json
{
    "FontName": {
        "name": "Open Sans Semibold",
        "substitute": "all"
    }
}
```

#### Dialogue style

Supply `custom` for the `substitute` option to replace the dialogue styling for specified styles.

##### Automatic dialogue style detection

If no `style` key is given, a single dialogue style will be determined automatically based on occurrence.

```json
{
    "FontName": {
        "name": "Open Sans Semibold",
        "substitute": "custom"
    }
}
```

##### User-defined dialogue style

Supply one or multiple (dialogue) styles to more accurately restyle the given lines.

```json
{
    "FontName": {
        "name": "Open Sans Semibold",
        "substitute": "custom",
        "style": [
            "Default",
            "DefaultItalics",
            "Flashback",
            "FlashbackItalics"
        ]
    }
}
```

!!! warning

    No additional validation is performed to check if the given style(s) actually exist.
