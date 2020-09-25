from abc import ABC, abstractmethod
from argparse import ArgumentParser
from typing import List, Optional


class Args(ABC):

    @abstractmethod
    def add_to_parser(parser: ArgumentParser):
        pass


class PositionalArgs(Args):

    def __init__(self, name: str, help: str, required: bool = True, limitted: bool = True):
        self.name = name
        self.help = help
        self.required = required
        self.limitted = limitted

    def add_to_parser(self, parser: ArgumentParser):
        nargs = None
        if not self.limitted:
            nargs = "+"
        if not self.required:
            nargs = "*"
        if (not self.required) and self.limitted:
            nargs = "?"

        parser.add_argument(
            self.name, type=str, help=self.help,
            nargs=nargs
        )

    def __str__(self):
        return "{}".format(self.name.upper())


class OptionArgs(Args, ABC):

    def __init__(
        self,
        name: str,
        help: str,
        required=False,
        dest: Optional[str] = None,
    ):
        self.short_name = "-" + name[0]
        self.long_name = "--" + name
        self.dest = dest if dest is not None else name
        self.required = required
        self.help = help

    @abstractmethod
    def add_to_parser(self, parser: ArgumentParser):
        pass

    def __str__(self):
        return "{}{}{}".format(
            "[" if self.required else "",
            self.long_name,
            "]" if self.required else ""
        )


class OptionContentArgs(OptionArgs):

    def __init__(
        self,
        name: str,
        help: str,
        required: bool = False,
        dest: Optional[str] = None,
    ):
        super().__init__(name, help, required, dest)

    def add_to_parser(self, parser: ArgumentParser):
        parser.add_argument(
            self.short_name, self.long_name, type=str,
            required=self.required,
            dest=self.dest, help=self.help
        )


class FlagArgs(OptionArgs):

    def __init__(
        self,
        name: str,
        help: str,
        required: bool = False,
        dest: Optional[str] = None,
    ):
        super().__init__(name, help, required, dest)

    def add_to_parser(self, parser: ArgumentParser):
        parser.add_argument(
            self.short_name, self.long_name,
            required=self.required,
            help=self.help, dest=self.dest,
            action="store_true"
        )


class ArgParser(dict):

    def __init__(self, name: str, args: List[Args]):
        usage = "Usage: {} [-h] {}".format(
            name,
            " ".join([str(x) for x in args])
        )
        self.parser: ArgumentParser = ArgumentParser(usage=usage)
        for arg in args:
            arg.add_to_parser(self.parser)
        self.parsed_args = self.parser.parse_args()

    def __getitem__(self, k: str) -> str:
        return eval("self.parsed_args." + k)

    def get_or(self, k: str, default) -> str:
        return self[k] if self[k] is not None else default
