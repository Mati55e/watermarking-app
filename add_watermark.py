from PIL import Image, ImageDraw, ImageFont
from PIL.ImageTk import PhotoImage


class WatermarkEngine():
    def __init__(self, path):
        self.text = "Sample Text"
        self.path = path
        self.base_image = Image.open(self.path, mode="r")
        self.tk_image = PhotoImage(self.base_image.convert("RGB"))
        self.w, self.h = self.base_image.size

    def text_watermark(self):
        try:
            text_img = Image.new("RGBA", (self.w, self.h), (255, 255, 255, 0))
            draw = ImageDraw.Draw(text_img)
            font = ImageFont.truetype('fonts/Roboto/Roboto-Bold.ttf', 36)

            ascent, descent = font.getmetrics()
            text_w = font.getmask(self.text).getbbox()[2]
            text_h = font.getmask(self.text).getbbox()[3] + descent

            margin = 15
            x = self.w - text_w - margin
            y = self.h - text_h - margin

            draw.text((x, y), text=self.text, font=font, fill=(255, 255, 255, 80))
            self.output = Image.alpha_composite(self.base_image.convert(mode="RGBA"), text_img)
            self.tk_image = PhotoImage(self.output.convert(mode="RGB"))

        except OSError:
            print("Could not open image. Check image extension.")

    def img_watermark(self):
        watermark = Image.open("./watermark_images/watermark.png", mode="r")
        wm_w, wm_h = watermark.size
        coef = self.w / wm_w
        watermark = watermark.resize((self.w, int(wm_h * coef)))
        watermark.putalpha(90)
        base_watermark = Image.new(mode="RGBA", color=(0,0,0,0), size=(self.w, self.h))
        y_pos = int((self.h / 2) - ((wm_h) / 2 * coef))
        base_watermark.paste(watermark, (0, y_pos))
        self.output = Image.alpha_composite(self.base_image.convert(mode="RGBA"), base_watermark)
        self.tk_image = PhotoImage(self.output.convert(mode="RGB"))

    def save(self, path):
        try:
            self.output = self.output.convert(mode="RGB")
            self.output.save(fp=f"{path}.png")
        except (ValueError, AttributeError):
            print("Save image exited")
            return