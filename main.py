#!/usr/bin/python3

import re
import sys
from dataclasses import dataclass


@dataclass
class Color:
    text: str = None
    red: int = None
    green: int = None
    blue: int = None
    hex: str = None
    hue: float = None
    saturation: float = None
    lightness: float = None
    alpha: int = 255

    def __post_init__(self):
        if self.text is not None:
            hex_format = re.search("^([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3})$", self.text)
            decimal_format = re.search(
                "^(0,\s?|[0-9]{1,2},\s?|1[0-9]{1,2},\s?|25[0-5]{1},\s?|2[0-4]{1}[0-9]{1},\s?){2,3}(0|[0-9]{1,2}|1[0-9]{1,2}|25[0-5]{1}|2[0-4]{1}[0-9]{1})$",
                self.text,
            )
            if hex_format:
                if len(self.text) == 6:
                    self.hex = self.text + "ff"
                elif len(self.text) == 3:
                    self.hex = (
                        self.text[0] + self.text[0] + self.text[1] + self.text[1] + self.text[2] + self.text[2] + "ff"
                    )
                else:
                    self.hex = self.text
                self.hex_to_rgb()
                self.rgb_to_hsl()
            elif decimal_format:
                color = self.text.split(",")
                self.red = int(color[0])
                self.green = int(color[1])
                self.blue = int(color[2])
                if len(color) == 4:
                    self.alpha = int(color[3])
                self.rgb_to_hsl()
                self.rgb_to_hex()
            else:
                raise ValueError(f"Invalid input data: {self.text} is not a valid color number - check input data \n")
        elif self.red is None and self.green is None and self.blue is None:
            if (
                self.hue >= 0
                and self.hue <= 360
                and self.saturation >= 0
                and self.saturation <= 1
                and self.lightness >= 0
                and self.saturation <= 1
            ):
                self.hsl_to_rgb()
            else:
                raise ValueError(
                    f"Invalid input data: [hue saturation lightness] = [{self.hue} {self.saturation} {self.lightness}] \n"
                )
        elif self.hue is None and self.saturation is None and self.lightness is None:
            if (
                self.red >= 0
                and self.red <= 255
                and self.green >= 0
                and self.green <= 255
                and self.blue >= 0
                and self.blue <= 255
            ):
                self.rgb_to_hsl()
            else:
                raise ValueError(f"Invalid input data: [red green blue] = [{self.red} {self.green} {self.blue}] \n")
        else:
            raise ValueError(
                f"Incomplete input data: either HEX or [red green blue] or [hue saturation lightness] should be provided \n"
            )
        if self.hex is None:
            self.rgb_to_hex()

    def hex_to_rgb(self):
        color_hex = [self.hex[i : i + 2] for i in range(0, len(self.hex), 2)]
        color_decimal = [int(k, 16) for k in color_hex]
        self.red = color_decimal[0]
        self.green = color_decimal[1]
        self.blue = color_decimal[2]
        self.alpha = color_decimal[3]

    def rgb_to_hex(self):
        color_hex = [hex(self.red), hex(self.green), hex(self.blue), hex(self.alpha)]
        # remove '0x' from hex values and pad with zeros if necessary
        color_hex = [(h[2:]).zfill(2) for h in color_hex]
        self.hex = "".join(color_hex)

    def hsl_to_rgb(self):
        c = (1 - abs(2 * self.lightness - 1)) * self.saturation
        x = c * (1 - abs(self.hue / 60 % 2 - 1))
        m = self.lightness - c / 2
        if self.hue < 60:
            red = c
            green = x
            blue = 0
        elif self.hue < 120:
            red = x
            green = c
            blue = 0
        elif self.hue < 180:
            red = 0
            green = c
            blue = x
        elif self.hue < 240:
            red = 0
            green = x
            blue = c
        elif self.hue < 300:
            red = x
            green = 0
            blue = c
        elif self.hue < 360:
            red = c
            green = 0
            blue = x
        self.red = round((red + m) * 255)
        self.green = round((green + m) * 255)
        self.blue = round((blue + m) * 255)
        self.rgb_to_hex()

    def rgb_to_hsl(self):
        r_norm = self.red / 255
        g_norm = self.green / 255
        b_norm = self.blue / 255
        c_max = max([r_norm, g_norm, b_norm])
        c_min = min([r_norm, g_norm, b_norm])
        # lightness
        self.lightness = 0.5 * (c_max + c_min)

        # saturation

        delta = c_max - c_min
        if delta != 0:
            saturation = delta / (1 - abs(2 * self.lightness - 1))
        elif delta == 0:
            saturation = 0

        self.saturation = saturation

        # hue
        if delta == 0:
            hue = 0
        elif c_max == r_norm:
            hue = 60 * (((g_norm - b_norm) / delta) % 6)
        elif c_max == g_norm:
            hue = 60 * (((b_norm - r_norm) / delta) + 2)
        elif c_max == b_norm:
            hue = 60 * (((r_norm - g_norm) / delta) + 4)
        self.hue = hue

    def __str__(self):
        return (
            f"    R:          {self.red}\n"
            f"    G:          {self.green}\n"
            f"    B:          {self.blue}\n"
            f"    alpha:      {self.alpha}\n"
            f"    hex:        #{self.hex}\n"
            f"    hue:        {round(self.hue,3)}\n"
            f"    saturation: {round(self.saturation,3)}\n"
            f"    lightness:  {round(self.lightness,3)}\n"
        )


def parse_cli_args():
    # it it assumed that the first parameters are the ones with '-' or '--'
    # and color values go at the end
    # any option other that '-m' or '--mode' is ignored

    mode = "mix"  # defualt mode
    valid_modes = ["mix", "lowest", "highest", "mix-saturate"]
    opts = [opt for opt in sys.argv[1:] if (opt.startswith("-"))]
    args = [arg for arg in sys.argv[1:] if (not arg.startswith("-"))]

    colors_cli = args[len(opts) :]
    args = args[: len(opts)]

    if opts:
        if "-m" in opts:
            arg = args[opts.index("-m")]
            if arg in valid_modes:
                mode = arg
            else:
                print(f"Invalid argument -m {arg}: default mode chosen \n")
                mode = "mix"
        elif "--mode" in opts:
            arg = args[opts.index("--mode")]
            if arg in valid_modes:
                mode = arg
            else:
                print(f"Invalid argument --mode {arg}: default mode chosen \n")
        else:
            print(
                f"Invalid arguments: default mode chosen \n Usage: {sys.argv[0]} (-m | --mode) <MODE>  \n   possible MODES: mix lowest highest mix-saturate \n"
            )
    else:
        print("No arguments: default mode chosen \n")
    return mode, colors_cli


def mix_color(colors):
    n = len(colors)
    if n == 1:
        mixed_color = colors[0]
    else:
        red = 0
        green = 0
        blue = 0
        alpha = 0
        for color in colors:
            red += color.red / n
            green += color.green / n
            blue += color.blue / n
            alpha += color.alpha / n

        mixed_color = Color(red=round(red), green=round(green), blue=round(blue), alpha=round(alpha))

    return mixed_color


def lowest_color(colors):
    n = len(colors)
    if n == 1:
        lowest_color = colors[0]
    else:
        red = 255
        green = 255
        blue = 255
        alpha = 255
        for color in colors:
            red = min(red, color.red)
            green = min(green, color.green)
            blue = min(blue, color.blue)
            alpha = min(alpha, color.alpha)

        lowest_color = Color(red=red, green=green, blue=blue, alpha=alpha)
        lowest_color.rgb_to_hex()
        lowest_color.rgb_to_hsl()

    return lowest_color


def highest_color(colors):
    n = len(colors)
    if n == 1:
        highest_color = colors[0]
    else:
        red = 0
        green = 0
        blue = 0
        alpha = 0
        for color in colors:
            red = max(red, color.red)
            green = max(green, color.green)
            blue = max(blue, color.blue)
            alpha = max(alpha, color.alpha)

        highest_color = Color(red=red, green=green, blue=blue, alpha=alpha)
        highest_color.rgb_to_hex()
        highest_color.rgb_to_hsl()

    return highest_color


def mix_saturate_color(colors):
    n = len(colors)
    if n == 1:
        raise ValueError("Too few colors to calculate mix-saturate color - at least 2 colors needed \n")
    else:
        saturation = 0
        for color in colors[:-1]:
            saturation += color.saturation / (n - 1)
        alpha = colors[-1].alpha
        hue = colors[-1].hue
        lightness = colors[-1].lightness

        # calculate RGB for HSL
        mix_saturate_color = Color(hue=hue, alpha=alpha, lightness=lightness, saturation=saturation)
        mix_saturate_color.hsl_to_rgb()

    return mix_saturate_color


filename = "colors.txt"


# read file with data
try:
    with open(filename) as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
except IOError:
    print(f"Could not read file {filename}")
    lines = []


# parse CLI arguments
try:
    mode, colors_cli = parse_cli_args()
except ValueError as e:
    sys.exit(e)


# analyse input data from file and from CLI
input_data = lines + colors_cli
colors = []
for item in input_data:
    try:
        c = Color(text=item)
        colors.append(c)
    except ValueError as e:
        print(e)


if mode == "mix-saturate":
    try:
        new_color = mix_saturate_color(colors)
        print(f"New color (MODE {mode}): ")
        print(new_color)
    except ValueError as e:
        print(e)
elif mode == "mix":
    new_color = mix_color(colors)
    print(f"New color (MODE {mode}): ")
    print(new_color)
elif mode == "lowest":
    new_color = lowest_color(colors)
    print(f"New color (MODE {mode}): ")
    print(new_color)
elif mode == "highest":
    new_color = highest_color(colors)
    print(f"New color (MODE {mode}): ")
    print(new_color)
