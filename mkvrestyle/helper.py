import collections
import json
import re
from pathlib import Path

from mkvrestyle.exception import SubtitleCodecError


def files_in_dir(path: Path, file_types=["*.mkv"]):
    """
    Returns a list of files in the given directory that match the specified file types.

    Parameters:
        path (Path): The path to the directory.
        file_types (List[str], optional): A list of file types to match. Defaults to ["*.mkv"].

    Returns:
        List[Path]: A list of paths to the files in the directory that match the specified file types.
    """

    file_list = [f for f_ in [path.rglob(e) for e in file_types] for f in f_]

    return file_list


def read_json(path: Path) -> dict:
    """
    Reads a JSON file from the given path and returns its contents as a dictionary.

    Parameters:
        path (Path): The path to the JSON file.

    Returns:
        dict: The contents of the JSON file as a dictionary.
    """

    with path.open("r") as file:
        data = json.load(file)

    return data


def read_file(
    input_file: str, split_lines: bool = True, custom_encoding: str = "latin-1"
) -> dict:
    """
    Read a file and return its content as a list.

    Parameters:
        input_file (str): The path to the file to read.
        split_lines (bool, optional): Whether to split the content into lines. Defaults to True.
        custom_encoding (str, optional): The encoding to use. Defaults to "latin-1".

    Returns:
        list: The content of the file as a list.
    """

    input_file_read = open(str(input_file), mode="r", encoding=custom_encoding).read()

    if split_lines:
        return {"content": input_file_read.splitlines(), "encoding": custom_encoding}

    return {"content": input_file_read, "encoding": custom_encoding}


def find_in_dict(input_list: list, key: str, value: str):
    """
    Find the index of the first occurrence of a dictionary with a specific key-value pair in a list of dictionaries.

    Parameters:
        input_list (list): A list of dictionaries.
        key (str): The key to search for in the dictionaries.
        value (str): The value to match with the key.

    Returns:
        int or bool: The index of the first occurrence of the dictionary with the specified key-value pair,
        or False if no match is found.
    """

    for i, dic in enumerate(input_list):
        if dic[key] == value:
            return i

    return False


def split_list_of_dicts_by_key(
    list_of_dicts: list, key: str = "codec_type"
) -> tuple[list[list], list]:
    """
    Splits a list of dictionaries into sublists based on a specified key.

    Parameters:
        list_of_dicts (list): A list of dictionaries to be split.
        key (str, optional): The key to use for splitting. Defaults to "codec_type".

    Returns:
        list: A list of sublists, where each sublist contains dictionaries with the same value for the specified key.
        list: A list of unique values for the specified key.

    """

    result = collections.defaultdict(list)
    keys = []
    for d in list_of_dicts:
        result[d[key]].append(d)
        if d[key] not in keys:
            keys.append(d[key])

    return list(result.values()), keys


def replace_conflicting_characters_in_filename(file_path: Path) -> Path:
    """
    Replaces single and double quotes in filenames for FFmpeg/FFprobe.

    Parameters:
        file_path (Path): The Path object representing the file path.

    Returns:
        Path: The new file path after replacing conflicting characters.
    """

    new_filename = re.sub(r"[\"']", "", file_path.name)
    new_file_path = file_path.with_name(new_filename)
    file_path.rename(new_file_path)

    return new_file_path


def combine_arguments_by_batch(*lists):
    """
    Combine arguments from multiple lists into batches based on the 'batch' key in each item.

    Parameters:
        *lists: Variable number of lists containing dictionaries with a 'batch' key.

    Returns:
        list: A list of dictionaries containing combined items grouped by their 'batch' key.
    """

    combined = collections.defaultdict(dict)

    for lst in lists:
        for item in lst:
            batch = item["batch"]
            combined[batch].update(item)

    result = [value for key, value in combined.items()]

    return result


def get_subtitle_extension_from_codec_id(codec_id: str) -> str:
    match codec_id:
        case "S_TEXT/ASS" | "S_TEXT/SSA":
            return "ass"
        case "S_TEXT/UTF8":
            return "srt"
        case "S_TEXT/PGS":
            return "sup"
        case "S_VOBSUB":
            return "sub"
        case "S_HDMV/USF":
            return "usf"
        case _:
            raise SubtitleCodecError(codec_id)
