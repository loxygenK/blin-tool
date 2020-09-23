import sys

from lib.args import ArgParser, FlagArgs, OptionContentArgs, PositionalArgs

NORMAL = 0b00
BOLD = 0b01
ITALIC = 0b10

chartable = "".join(
    [chr(x) for x in range(ord("A"), ord("Z") + 1)] +
    [chr(x) for x in range(ord("a"), ord("z") + 1)],
)

char_heads = {
    "sans": {
        BOLD: ord("𝗔"),
        BOLD | ITALIC: ord("𝘼"),
    },
    "serif": {
        ITALIC: ord("𝐴"),
        BOLD | ITALIC: ord("𝑨"),
    },
    "mincho": {
        NORMAL: ord("𝙰"),
        BOLD: ord("𝐀"),
    },
    "write": {
        NORMAL: ord("𝒶"),
        BOLD: ord("𝓪"),
    },
    "flower": {
        NORMAL: ord("𝒜"),
        BOLD: ord("𝓐"),
    }
}

DEFAULT_CHAR_TYPE = "sans"

arguments = [
    FlagArgs("bold", "make character bold"),
    FlagArgs("italic", "make character italic"),
    OptionContentArgs("type", "type of characters, default is sans"),
    PositionalArgs(
        "content", "Content to convert character forms.", required=False, limitted=False)
]


def char_form_flag_to_str(flag):
    if flag == 0b00:
        return " Normal"
    return (" Bold (-b)" * (BOLD & flag != 0)) + (" Italic (-i)" * (ITALIC & flag != 0))


def main():
    parser = ArgParser("chartype", arguments)
    char_type = parser.get_or("type", DEFAULT_CHAR_TYPE)
    char_form = (BOLD * parser["bold"]) | (ITALIC * parser["italic"])

    if char_type not in char_heads:
        print("No such char type: {}".format(char_type))
        print("Available types:\n  {}".format("\n  ".join(char_heads.keys())))
        return

    if char_form not in char_heads[char_type]:
        print("Unavailable form:{}".format(char_form_flag_to_str(char_form)))
        print("Available forms: \n{}".format("\n".join(
            [char_form_flag_to_str(x) for x in char_heads[char_type].keys()]
        )))
        return

    content = " ".join(parser["content"])
    if content == "":
        content = "".join(sys.stdin.readlines())
        content = content.rstrip("\n")

    print("".join(
        [
            chr(chartable.index(x) +
                char_heads[char_type][char_form]) if x in chartable else x
            for x in content]
    ))


if __name__ == '__main__':
    main()
