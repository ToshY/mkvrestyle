from pathlib import Path
from contextlib import redirect_stderr as rs
from matplotlib import font_manager
from fontTools.ttLib import TTFont as ttfo  # type: ignore
import os

os.environ["MPLCONFIGDIR"] = "/tmp"


class FontFinder:
    """
    The FontFinder; finding unique fonts on the current platform.

    Attributes
    ----------
    lang_ids : list
        Language IDs used at font finding. The default is [0, 1033, 1041]

    """

    lang_ids = [0, 1033, 1041]

    def __init__(self, exclude_extension: list = [".ttc"], rebuild: bool = False):
        """
        Constructor.

        Parameters
        ----------
        exclude_extension : list, optional
            Extension to exclude for getting font info. The default is ['.ttc'].
        rebuild : bool, optional
            Rebuilding font cache. The default is False.

        Returns
        -------
        None.

        """
        self.excl = exclude_extension
        if rebuild:
            self._rebuild_font_cache()
        self.fonts = self._get_available_fonts()

    def check_font_installed(self, user_font: str, dict_key: str = "name") -> list:
        """
        Check if the user defined font is installed.

        Parameters
        ----------
        user_font : str
            The path, name or other definition of the font to search for.
        dict_key : str, optional
            The dictionary key to find the sepcified value in. The default is 'name'.

        Returns
        -------
        list
            Returns a list of the user defined font(s).

        """
        return list(
            filter(lambda x: x[dict_key].lower() == user_font.lower(), self.fonts)
        )

    @staticmethod
    def mimetype_by_extension(file_extension: str) -> str:
        """
        Get appropriate mimetype; mimetype library cannot guess font mimes.

        Parameters
        ----------
        file_extension : str
            The specified font file.

        Returns
        -------
        str
            The mimetype for the corresponding file extension.

        """

        mimes = {
            "ttf": "application/x-truetype-font",
            "otf": "application/vnd.ms-opentype",
            "eot": "application/vnd.ms-fontobject",
        }

        return mimes[file_extension.lower().lstrip(".")]

    @staticmethod
    def _rebuild_font_cache() -> None:
        """
        Rebuild MatPlotLib font cache.

        Returns
        -------
        None

        """
        font_manager._load_fontmanager(try_read_cache=False)  # type: ignore[attr-defined]

    def _get_available_fonts(self) -> list:
        """
        Get all the unique available fonts on the current system.

        Returns
        -------
        list
            Contains font entries as dictionaries with keys 'file_path', 'file_name',
            'font_name', 'font_family', 'font_style.

        """
        initial_fonts = []
        for current_font in self._fonts_on_system():
            pfont = Path(current_font)
            if pfont.suffix.lower() in self.excl:
                continue

            file_path = pfont.resolve()
            file_name = pfont.name

            initial_fonts.append(
                {
                    **{"file_path": file_path, "file_name": file_name},
                    **self.font_info_by_file(file_path),
                }
            )

        unique_font_list = self._unique_list_of_dicts_by_key(initial_fonts, "font_name")
        self.fonts = self._sort_list_of_dicts_by_key(unique_font_list, "font_name")

        return self.fonts

    def font_info_by_file(self, file_path: Path) -> dict:
        """
        Get font info by file.

        Parameters
        ----------
        file_path : pt
            The font file specified as Path object.

        Returns
        -------
        dict
            Contains keys 'font_name', 'font_family' and 'font_style' for the specified font file.

        """

        try:
            font = ttfo(str(file_path), fontNumber=-1, ignoreDecompileErrors=True)
        except Exception:
            font = ttfo(str(file_path), fontNumber=0, ignoreDecompileErrors=True)

        with rs(None):
            names = font["name"].names

        details = {}
        for name in names:
            if name.langID in self.lang_ids:
                try:
                    details[name.nameID] = name.toUnicode()
                except UnicodeDecodeError:
                    details[name.nameID] = name.string.decode(errors="ignore")
                continue

        if details:
            return {
                "font_name": details[4],
                "font_family": details[1],
                "font_style": details[2],
            }

        return details

    @staticmethod
    def _fonts_on_system() -> list:
        """
        Finds the fonts on the current system using MatPlotLib's font_manager.

        Returns
        -------
        list
            Returns a list of (possible) duplicate fonts.

        """
        return font_manager.findSystemFonts()

    @staticmethod
    def _unique_list_of_dicts_by_key(
        user_list: list, dict_key: str = "font_name"
    ) -> list:
        """
        Get an unique list of dictionaries by specified dictionary key.

        Parameters
        ----------
        user_list : list
            The list containing (possible) duplicate fonts.
        dict_key : str, optional
            The dictionary key to filter upon. The default is 'font_name'.

        Returns
        -------
        list
            An unique representation of the input list.

        """
        return list({v[dict_key]: v for v in user_list}.values())

    @staticmethod
    def _sort_list_of_dicts_by_key(
        user_list: list, dict_key: str = "font_name"
    ) -> list:
        """
        Sort a list of dictionaries by specified dictionary key.

        Parameters
        ----------
        user_list : list
            Unsorted input list of fonts.
        dict_key : str, optional
            The dictionary key to sort upon. The default is 'font_name'.

        Returns
        -------
        list
            A sorted representation of the input list.

        """
        return sorted(user_list, key=lambda k: k[dict_key])
