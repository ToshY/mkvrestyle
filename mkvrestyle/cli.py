import itertools
import json
import os
import re
import shutil
from collections import Counter
from pathlib import Path

import click
from loguru import logger  # noqa
from rich.prompt import IntPrompt
from mkvrestyle.args import (
    InputPathChecker,
    OutputPathChecker,
    PresetPathChecker,
    OptionalValueChecker,
    ClickUnionType,
)
from mkvrestyle.exception import (
    FontNotFoundError,
    InvalidFontNameError,
    InvalidSubtitleFormatLines,
    SubtitleNotFoundError,
)
from mkvrestyle.fonts import FontFinder
from mkvrestyle.helper import (
    read_file,
    combine_arguments_by_batch,
    get_subtitle_extension_from_codec_id,
)
from mkvrestyle.process import ProcessCommand
from mkvrestyle.table import table_print_stream_options


def get_lines_per_type(my_lines, split_at=["Format: "]):
    return [
        (i, [x for x in re.split("|".join(split_at) + "|,[\s]?", s) if x])
        for i, s in enumerate(my_lines)
        if any(s.startswith(xs) for xs in split_at)
    ]


def get_format_lines(my_lines):
    rgx_style = (
        r"^([Format]+):\s(\w+),[\s]?(\w+),[\s]?(\w+),[\s]?(\w+),[\s]?(\w+),[\s]?(\w+),[\s]?(\w+),[\s]?(\w+),"
        r"[\s]?(\w+),[\s]?(\w+),[\s]?(\w+),[\s]?(\w+),[\s]?(\w+),[\s]?(\w+),[\s]?(\w+),[\s]?(\w+),"
        r"[\s]?(\w+),[\s]?(\w+),[\s]?(\w+),[\s]?(\w+),[\s]?(\w+),[\s]?(\w+),[\s]?(\w+)$"
    )
    rgx_dialogue = (
        r"^([Format]+):\s(\w+),[\s]?(\w+),[\s]?(\w+),[\s]?(\w+),[\s]?(\w+),[\s]?(\w+),[\s]?(\w+),"
        r"[\s]?(\w+),[\s]?(\w+),[\s]?(\w+)$"
    )
    format_line_style = [
        (i, list(re.findall(rgx_style, x)[0]))
        for i, x in enumerate(my_lines)
        if any(x.startswith(xs) for xs in ["Format: Name"])
    ]
    format_line_dialogue = [
        (i, list(re.findall(rgx_dialogue, x)[0]))
        for i, x in enumerate(my_lines)
        if any(x.startswith(xs) for xs in ["Format: Layer"])
    ]
    format_lines = format_line_style + format_line_dialogue
    if len(format_lines) > 2:
        raise InvalidSubtitleFormatLines(len(format_lines))

    return {"style": format_lines[0], "dialogue": format_lines[1]}


def get_dialogue_lines(my_lines, keys):
    rgx = (
        r"^^([Dialogue]+|[Comment]+):\s(\d{1,}),(\d{1}:\d{2}:\d{2}.\d{2}),(\d{1}:\d{2}:\d{2}.\d{2}),(.*?),(.*?),"
        r"([0-9.]{1,4}),([0-9.]{1,4}),([0-9.]{1,4}),([$^,]?|[^,]+?)?,(.*?)$"
    )
    dialogue_lines = [
        (i, dict(zip(keys, list(re.findall(rgx, x)[0]))))
        for i, x in enumerate(my_lines)
        if any(x.startswith(xs) for xs in ["Dialogue", "Comment"])
    ]
    return dialogue_lines


def get_style_lines(my_lines, keys):
    rgx = (
        r"^([Style]+):\s(.*?),(.*?),([0-9.]{1,}),(&H[a-fA-F0-9]{8}),(&H[a-fA-F0-9]{8}),(&H[a-fA-F0-9]{8}),"
        r"(&H[a-fA-F0-9]{8}),(0|-1),(0|-1),(0|-1),(0|-1),([0-9.]{1,}),([0-9.]{1,}),([0-9.]{1,}),([0-9.]{1,}),"
        r"(1|3),([0-9.]{1,}),([0-9.]{1,}),([1-9]),([0-9.]{1,4}),([0-9.]{1,4}),([0-9.]{1,4}),(\d{1,3})$"
    )
    style_lines = [
        (i, dict(zip(keys, list(re.findall(rgx, x)[0]))))
        for i, x in enumerate(my_lines)
        if any(x.startswith(xs) for xs in ["Style"])
    ]
    return style_lines


def prepare_track_info(file, index, codec, lang):
    return (
        file.stem
        + "_track"
        + str(index)
        + "_"
        + lang
        + f".{get_subtitle_extension_from_codec_id(codec)}"
    )


def extract_subtitles_and_fonts(
    input_file, attachments_folder, stream_select: str | int | None = None
):
    """
    Extracts subtitles and fonts from the input file.

    Parameters:
        input_file (Path): The input file from which to extract subtitles and fonts.
        attachments_folder (Path): The folder where the attachments are stored.
        stream_select (str | int | None, optional): Optional parameter to select a specific stream for subtitles. The default is None.

    Returns:
        list: A list containing the extracted subtitle file, the path to the associated attachments, and available fonts.
    """

    input_file_string = str(input_file)

    mkvmerge_identify_command = [
        "mkvmerge",
        "--identify",
        "--identification-format",
        "json",
        input_file_string,
    ]

    # MKV identify
    process = ProcessCommand(logger)
    result = process.run("MKVmerge identify", mkvmerge_identify_command)

    # Json output
    mkvmerge_identify_command_output = json.loads(result.stdout)

    # Get attachments
    attachments = mkvmerge_identify_command_output["attachments"]
    tracks = mkvmerge_identify_command_output["tracks"]

    subtitle = [
        {
            "index": sub["id"],
            "codec": sub["properties"]["codec_id"],
            "language": (
                sub["properties"]["language"] if "language" in sub["properties"] else ""
            ),
            "title": (
                sub["properties"]["track_name"]
                if "track_name" in sub["properties"]
                else ""
            ),
            "save_file": prepare_track_info(
                input_file,
                sub["id"],
                sub["properties"]["codec_id"],
                sub["properties"]["language"],
            ),
        }
        for sub in tracks
        if sub["type"] == "subtitles"
    ]

    if not subtitle:
        raise SubtitleNotFoundError(input_file_string)

    # No user input provided, so identify streams and ask for input
    if stream_select is None:
        selected_subs = subtitle[0]["index"]
        # Request user input for stream type
        if len(subtitle) > 1:
            logger.info("Multiple `subtitle` streams detected")

            table_print_stream_options(subtitle)
            allowed = [str(sub["index"]) for sub in subtitle]

            # Request user input
            selected_subs = IntPrompt.ask(
                "# Please specify the subtitle index to use: ",
                choices=allowed,
                default=selected_subs,
                show_choices=True,
                show_default=True,
            )
            logger.info(f"Selected subtitle stream index: {selected_subs}")
    else:
        if (isinstance(stream_select, int)) or stream_select.isnumeric():
            selected_subs = stream_select
        else:
            selected_subs = next(
                sub["index"] for sub in subtitle if sub["language"] == stream_select
            )

    selected_subs = next(
        sub for sub in subtitle if int(sub["index"]) == int(selected_subs)
    )
    ass_track_path = Path(
        os.path.join(attachments_folder.parent, selected_subs["save_file"])
    )

    mkvextract_subtitles_command = [
        "mkvextract",
        "tracks",
        input_file_string,
        f'{selected_subs["index"]}:{ass_track_path}',
    ]

    process = ProcessCommand(logger)
    process.run("MKVextract subtitle", mkvextract_subtitles_command)

    font_finder = FontFinder()
    available_fonts = font_finder.fonts

    if attachments:
        font_files, font_files_extract = export_fonts_list(
            attachments, attachments_folder
        )

        mkvextract_attachments_cmd = [
            "mkvextract",
            "attachments",
            input_file_string,
        ] + font_files_extract

        process = ProcessCommand(logger)
        process.run("MKVextract attachments", mkvextract_attachments_cmd)

        # Get current fonts
        font_info = [
            {**{"file_path": Path(element)}, **font_finder.font_info_by_file(element)}
            for element in font_files
        ]

        return (
            [selected_subs["save_file"], ass_track_path, available_fonts],
            font_info,
        )

    return [selected_subs["save_file"], ass_track_path, available_fonts], []


def find_available_fonts(fonts_list: dict, font_names_list: list) -> dict:
    fonts_available = {}
    for font in font_names_list:
        fonts_available[font] = next(
            (item for item in fonts_list if item["font_name"].lower() == font.lower()),
            False,
        )

    return fonts_available


def get_fonts(ass, font_names_kept, fonts) -> list:
    fonts_filesystem = find_available_fonts(ass[2], font_names_kept)
    fonts_embed = find_available_fonts(fonts, font_names_kept)
    main_fonts_ass = []
    for (font_name, filesystem_font), (_, embed_font) in zip(
        fonts_filesystem.items(), fonts_embed.items()
    ):
        main_fonts_ass.append(
            check_available_fonts(
                {font_name: filesystem_font}, {font_name: embed_font}, font_name
            )
        )
    return main_fonts_ass


def check_available_fonts(filesystem_fonts: dict, embedded_fonts: dict, key: str):
    if (filesystem_fonts[key] is False) & (embedded_fonts[key] is False):
        raise FontNotFoundError(key)
    elif (filesystem_fonts[key] is False) and (embedded_fonts[key] is not False):
        main_font = embedded_fonts[key]
    elif (filesystem_fonts[key] is not False) and (embedded_fonts[key] is False):
        main_font = filesystem_fonts[key]
    else:
        main_font = embedded_fonts[key]

    return main_font


def export_fonts_list(attachments, save_loc):
    font_files = []
    font_files_extract = []
    for el in attachments:
        fl = os.path.join(save_loc, el["file_name"])
        font_files.append(fl)
        font_files_extract.append("{}:{}".format(el["id"], fl))

    return font_files, font_files_extract


def resample_mean(dimensions_list_one, dimensions_list_two):
    mean_factor = (
        (int(dimensions_list_one[0]) / int(dimensions_list_two[0]))
        + (int(dimensions_list_one[1]) / int(dimensions_list_two[1]))
    ) / 2

    return mean_factor


@logger.catch
@click.command(
    context_settings={"help_option_names": ["-h", "--help"]},
    epilog="Repository: https://github.com/ToshY/mkvrestyle",
)
@click.option(
    "--input-path",
    "-i",
    type=click.Path(exists=True, dir_okay=True, file_okay=True, resolve_path=True),
    required=True,
    multiple=True,
    callback=InputPathChecker(),
    help="Path to input file or directory",
)
@click.option(
    "--output-path",
    "-o",
    type=click.Path(dir_okay=True, file_okay=True, resolve_path=True),
    required=True,
    multiple=True,
    callback=OutputPathChecker(),
    help="Path to output file or directory",
)
@click.option(
    "--preset",
    "-p",
    type=click.Path(exists=True, dir_okay=False, file_okay=True, resolve_path=True),
    required=False,
    multiple=True,
    callback=PresetPathChecker(),
    show_default=True,
    default=["./preset/default.json"],
    help="Path to JSON file with ASS video preset options",
)
@click.option(
    "--stream",
    "-s",
    type=ClickUnionType([click.INT, click.STRING]),
    required=False,
    multiple=True,
    callback=OptionalValueChecker(),
    show_default=True,
    default=[None],
    help="Stream ID or ISO 639-3 language code of the subtitle track",
)
def cli(input_path, output_path, preset, stream):
    combined_result = combine_arguments_by_batch(
        input_path, output_path, preset, stream
    )

    for item in combined_result:
        # current_batch = item.get("batch")
        current_stream = item.get("stream")
        current_preset = item.get("preset")
        current_output = item.get("output").get("resolved")
        # current_input_original_batch_name = item.get("input").get("given")
        current_input_files = item.get("input").get("resolved")
        # total_current_input_files = len(current_input_files)

        for current_file_path_index, current_file_path in enumerate(
            current_input_files
        ):
            file_attachments_output_folder_for_current_file_path = (
                current_output.with_suffix("").joinpath("attachments")
            )
            file_attachments_output_folder_for_current_file_path.mkdir(
                parents=True, exist_ok=True
            )

            # Extract subtitles and fonts
            ass, fonts = extract_subtitles_and_fonts(
                current_file_path,
                file_attachments_output_folder_for_current_file_path,
                current_stream,
            )

            # Read subtitle file contents
            read_file_content = read_file(ass[1], True)
            lines = read_file_content["content"]

            # Get Resolution/Format/Styles/Dialogues indices
            ass_resolution = {
                "PlayResX": get_lines_per_type(lines, ["PlayResX: "])[0],
                "PlayResY": get_lines_per_type(lines, ["PlayResY: "])[0],
            }
            format_lines = get_format_lines(lines)
            style_lines = get_style_lines(lines, format_lines["style"][1])
            dialogue_lines = get_dialogue_lines(lines, format_lines["dialogue"][1])

            # Style names from dialogue
            style_names_dialogue_all = [el[-1]["Style"] for el in dialogue_lines]
            style_names_dialogue = list(set(style_names_dialogue_all))

            # Find the dialogue styles which exist and which are not in Styles
            style_lines_kept = [
                el for el in style_lines if el[-1]["Name"] in style_names_dialogue
            ]
            style_lines_remove = [
                el for el in style_lines if el[-1]["Name"] not in style_names_dialogue
            ]

            ffprobe_select_streams_command = [
                "ffprobe",
                "-v",
                "error",
                "-select_streams",
                "v",
                "-show_entries",
                "stream={}".format(",".join(["width", "height"])),
                "-of",
                "json",
                str(current_file_path),
            ]

            process = ProcessCommand(logger)
            ffprobe_select_streams_output = process.run(
                "FFprobe", ffprobe_select_streams_command
            )

            ffprobe_stream_output = json.loads(ffprobe_select_streams_output.stdout)[
                "streams"
            ][0]
            ffprobe_stream_output["PlayResX"] = ffprobe_stream_output.pop("width")
            ffprobe_stream_output["PlayResY"] = ffprobe_stream_output.pop("height")

            # Calculate resample mean between video dimensions and preset
            ass_resample_mean = resample_mean(
                [ffprobe_stream_output["PlayResX"], ffprobe_stream_output["PlayResY"]],
                [ass_resolution["PlayResX"][-1][0], ass_resolution["PlayResY"][-1][0]],
            )

            # Resample ASS to video dimensions and user preset
            for ids, (line, style) in enumerate(style_lines_kept):
                for key in style:
                    if key in [
                        "Fontsize",
                        "ScaleX",
                        "ScaleY",
                        "Spacing",
                        "Outline",
                        "Shadow",
                        "MarginL",
                        "MarginR",
                        "MarginV",
                    ]:
                        if int(style[key]) != 0:
                            if key not in ["ScaleX", "ScaleY"]:
                                style[key] = round(
                                    float(style[key]) * ass_resample_mean, 2
                                )
                            preset_key_dict = current_preset[key]
                            if preset_key_dict:
                                resampled_value = round(
                                    float(style[key])
                                    * float(preset_key_dict["factor"]),
                                    preset_key_dict["round"],
                                )
                                if preset_key_dict["round"] == 0:
                                    resampled_value = int(resampled_value)
                                style[key] = str(resampled_value)

                # Change original line to resampled line
                format_type = dict(itertools.islice(style.items(), 1))["Format"]
                format_values = list(
                    dict(itertools.islice(style.items(), 1, None)).values()
                )
                lines[line] = "{}: {}".format(format_type, ",".join(format_values))

            # Resample dialogue margins
            for idd, (line, dialogue) in enumerate(dialogue_lines):
                for key in dialogue:
                    if key in ["MarginL", "MarginR", "MarginV"]:
                        if int(dialogue[key]) != 0:
                            dialogue[key] = round(
                                float(dialogue[key]) * ass_resample_mean, 2
                            )
                            preset_key_dict = current_preset[key]
                            if preset_key_dict:
                                resampled_value = round(
                                    float(dialogue[key])
                                    * float(preset_key_dict["factor"]),
                                    preset_key_dict["round"],
                                )
                                if preset_key_dict["round"] == 0:
                                    resampled_value = int(resampled_value)
                                dialogue[key] = str(resampled_value)

                # Change original line to resampled line
                format_type = dict(itertools.islice(dialogue.items(), 1))["Format"]
                format_values = list(
                    dict(itertools.islice(dialogue.items(), 1, None)).values()
                )
                lines[line] = "{}: {}".format(format_type, ",".join(format_values))

            # Style font replacement (from ASS styles)
            font_names_kept = [*{*[el[-1]["Fontname"] for el in style_lines_kept]}]

            # Check font preset options
            font_settings = current_preset.get("FontName")
            font_option = font_settings.get("substitute", None)
            font_name = font_settings.get("name", None)
            if (not isinstance(font_name, str)) or (
                not (font_name and font_name.strip())
            ):
                raise InvalidFontNameError(font_name)

            main_fonts_ass = []
            main_font_preset = None
            if font_option == "all":
                # Preset font availability
                fonts_filesystem = find_available_fonts(ass[2], [font_name])
                fonts_embed = find_available_fonts(fonts, [font_name])

                main_font_preset = check_available_fonts(
                    fonts_filesystem, fonts_embed, font_name
                )

                # Replacement of every existing style
                style_lines = get_style_lines(lines, format_lines["style"][1])
                for line, style in style_lines:
                    for key in style:
                        if key == "Fontname":
                            style[key] = main_font_preset["font_name"]

                    # Change original line to resampled line
                    format_type = dict(itertools.islice(style.items(), 1))["Format"]
                    format_values = list(
                        dict(itertools.islice(style.items(), 1, None)).values()
                    )
                    lines[line] = "{}: {}".format(format_type, ",".join(format_values))
            elif font_option == "main":
                # Preset font availability
                fonts_filesystem = find_available_fonts(ass[2], [font_name])
                fonts_embed = find_available_fonts(fonts, [font_name])

                main_font_preset = check_available_fonts(
                    fonts_filesystem, fonts_embed, font_name
                )

                main_fonts_ass = get_fonts(ass, font_names_kept, fonts)

                # Get most occurring style name
                style_occurrence = Counter(style_names_dialogue_all)
                max_occurring_style_name = max(
                    style_occurrence, key=style_occurrence.get
                )

                # Get corresponding font for style to replace
                max_occurring_style = next(
                    (
                        item
                        for item in style_lines_kept
                        if item[1]["Name"] == max_occurring_style_name
                    ),
                    False,
                )
                max_occurring_font = max_occurring_style[1]["Fontname"]

                # Replacement of most occurring font (e.g. in main/top/italic) by preset font
                style_lines = get_style_lines(lines, format_lines["style"][1])
                for line, style in style_lines:
                    for key in style:
                        if (key == "Fontname") & (style[key] == max_occurring_font):
                            style[key] = main_font_preset["font_name"]

                    # Change original line to resampled line
                    format_type = dict(itertools.islice(style.items(), 1))["Format"]
                    format_values = list(
                        dict(itertools.islice(style.items(), 1, None)).values()
                    )
                    lines[line] = "{}: {}".format(format_type, ",".join(format_values))
            else:
                main_fonts_ass = get_fonts(ass, font_names_kept, fonts)

            # Replace PlayRes by video dimension
            for direction, (line, _) in ass_resolution.items():
                lines[line] = f"{direction}: {ffprobe_stream_output[direction]}"

            # Remove unnecessary styles
            lines = [
                el
                for idx, el in enumerate(lines)
                if idx not in [idy for idy, style in style_lines_remove]
            ]

            # Overwrite ASS
            with open(ass[1], "w", encoding=read_file_content["encoding"]) as f:
                f.write("\n".join(item for item in lines))

            # For replacement of all styles with single font, clean-up the attachments directory prior to copying
            if font_option == "all":
                for path in Path(
                    file_attachments_output_folder_for_current_file_path
                ).glob("**/*"):
                    if not path.is_file():
                        continue
                    path.unlink()
            elif font_option == "main":
                # The font that was originally used and extracted from the input file can be removed from attachments
                font_files_to_be_deleted = [
                    font for font in fonts if font["font_family"] == max_occurring_font
                ]
                for font_entry_to_be_deleted in font_files_to_be_deleted:
                    font_filepath_to_be_deleted = font_entry_to_be_deleted.get(
                        "file_path"
                    )
                    if not font_filepath_to_be_deleted.exists():
                        continue
                    font_filepath_to_be_deleted.unlink()

            # If preset font was used, copy it
            if main_font_preset is not None:
                if (
                    main_font_preset["file_path"].parent
                    == file_attachments_output_folder_for_current_file_path
                ):
                    continue

                shutil.copy(
                    main_font_preset["file_path"],
                    file_attachments_output_folder_for_current_file_path.joinpath(
                        main_font_preset["file_name"]
                    ),
                )

            # Get entire family for replacement font making sure it has other variants (e.g. bold/italics/etc)
            if font_option == "all" or font_option == "main":
                main_fonts_ass = [
                    font
                    for font in ass[2]
                    if font["font_family"] == main_font_preset.get("font_family")
                ]

            # Copy other fonts into attachment folder
            for font in main_fonts_ass:
                if (
                    font["file_path"].parent
                    == file_attachments_output_folder_for_current_file_path
                ):
                    continue

                shutil.copy(
                    font["file_path"],
                    file_attachments_output_folder_for_current_file_path.joinpath(
                        font["file_name"]
                    ),
                )
