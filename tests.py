#!/usr/bin python3
import unittest

from main import Color
from main import highest_color
from main import lowest_color
from main import mix_color
from main import mix_saturate_color


class TestsColors(unittest.TestCase):
    def test_white(self):
        rgb = Color(red=255, green=255, blue=255)
        rgba = Color(red=255, green=255, blue=255, alpha=255)
        hsl = Color(hue=0, saturation=0, lightness=1)
        hsla = Color(hue=0, saturation=0, lightness=1, alpha=255)

        self.assertEqual(rgb, rgba)
        self.assertEqual(rgb, hsl)
        self.assertEqual(rgb, hsla)

    def test_incorrect_red(self):
        with self.assertRaises(ValueError):  # ValueError expected for invalid color number
            Color(text="fgffff")

        with self.assertRaises(ValueError):
            Color(red=256, green=255, blue=255)

    def test_some_color(self):
        rgba = Color(red=160, green=140, blue=178, alpha=150)
        hsla = Color(hue=271.579, saturation=0.198, lightness=0.624, alpha=150)
        text_rgba = Color(text="a08cb296")
        text_dec = Color(text="160, 140, 178, 150")
        self.assertEqual(rgba.red, hsla.red)
        self.assertEqual(rgba.green, hsla.green)
        self.assertEqual(rgba.blue, hsla.blue)
        self.assertEqual(rgba.hex, hsla.hex)
        self.assertAlmostEqual(rgba.hue, hsla.hue, 2)
        self.assertAlmostEqual(rgba.saturation, hsla.saturation, 2)
        self.assertAlmostEqual(rgba.lightness, hsla.lightness, 2)
        self.assertEqual(rgba.text, hsla.text)
        self.assertEqual(text_rgba.red, text_dec.red)
        self.assertEqual(text_rgba.green, text_dec.green)
        self.assertEqual(text_rgba.blue, text_dec.blue)
        self.assertEqual(text_rgba.hex, text_dec.hex)
        self.assertEqual(text_rgba.hue, text_dec.hue)
        self.assertEqual(text_rgba.saturation, text_dec.saturation)
        self.assertEqual(text_rgba.lightness, text_dec.lightness)

    def test_black(self):
        rgb = Color(red=0, green=0, blue=0)
        rgba = Color(red=0, green=0, blue=0, alpha=255)
        hsl = Color(hue=0, saturation=0, lightness=0)
        hsla = Color(hue=0, saturation=0, lightness=0, alpha=255)

        self.assertEqual(rgb, rgba)
        self.assertEqual(rgb, hsl)
        self.assertEqual(rgb, hsla)

    def test_lowest_mode(self):
        c1 = Color(text="ff00ff00")
        c2 = Color(text="00ff00ff")
        c3 = Color(text="80808080")
        colors = [c1, c2, c3]
        result = lowest_color(colors)
        ref = Color(text="00000000")
        self.assertEqual(result.red, ref.red)
        self.assertEqual(result.green, ref.green)
        self.assertEqual(result.blue, ref.blue)
        self.assertEqual(result.hex, ref.hex)
        self.assertEqual(result.hue, ref.hue)
        self.assertEqual(result.saturation, ref.saturation)
        self.assertEqual(result.lightness, ref.lightness)

    def test_highest_mode(self):
        c1 = Color(text="ff00ff00")
        c2 = Color(text="00ff00ff")
        c3 = Color(text="80808080")
        colors = [c1, c2, c3]
        result = highest_color(colors)
        ref = Color(text="ffffffff")
        self.assertEqual(result.red, ref.red)
        self.assertEqual(result.green, ref.green)
        self.assertEqual(result.blue, ref.blue)
        self.assertEqual(result.hex, ref.hex)
        self.assertEqual(result.hue, ref.hue)
        self.assertEqual(result.saturation, ref.saturation)
        self.assertEqual(result.lightness, ref.lightness)

    def test_mix_mode(self):
        c1 = Color(text="ff00ff00")
        c2 = Color(text="00ff00ff")
        c3 = Color(text="80808080")
        colors = [c1, c2, c3]
        result = mix_color(colors)
        ref = Color(text="80808080")
        self.assertEqual(result.red, ref.red)
        self.assertEqual(result.green, ref.green)
        self.assertEqual(result.blue, ref.blue)
        self.assertEqual(result.hex, ref.hex)
        self.assertEqual(result.hue, ref.hue)
        self.assertEqual(result.saturation, ref.saturation)
        self.assertEqual(result.lightness, ref.lightness)

    def test_mix_saturate_mode(self):
        c1 = Color(text="FF0000ff")
        c2 = Color(text="808080ff")
        c3 = Color(text="CC3333ff")
        colors = [c1, c2, c3]
        result = mix_saturate_color(colors)
        ref = Color(text="bf4040ff")
        self.assertEqual(result.red, ref.red)
        self.assertEqual(result.green, ref.green)
        self.assertEqual(result.blue, ref.blue)
        self.assertEqual(result.hex, ref.hex)
        self.assertAlmostEqual(result.hue, ref.hue, 2)
        self.assertAlmostEqual(result.saturation, ref.saturation, 2)
        self.assertAlmostEqual(result.lightness, ref.lightness, 2)

    def test_mix_saturate_mode_too_few_data(self):
        c1 = Color(text="FF0000ff")
        c2 = Color(text="808080ff")
        colors = [c1]
        with self.assertRaises(ValueError):  # ValueError expected for invalid color number
            mix_saturate_color(colors)


if __name__ == "__main__":
    unittest.main()
