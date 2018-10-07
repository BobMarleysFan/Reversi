import configparser
import logging

LOGGER = logging.getLogger("settings")


class Settings:
    def __init__(self, filename="settings.ini"):
        self._config = configparser.ConfigParser()
        LOGGER.info('Reading settings from "{}"'.format(filename))
        self._config.read(filename, encoding="utf8")

        side, mode = self._global()["DefaultGame"].split(',')
        self._default_game = (int(side), mode)

    def _global(self):
        return self._config["GLOBAL"]

    @property
    def default_game(self):
        return self._default_game

    @property
    def savedir(self):
        return self._global()["SaveDir"]

    def picture(self, name):
        return self._config["Pictures"].get(name, "pictures/default.png")
