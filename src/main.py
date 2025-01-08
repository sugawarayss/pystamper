from typer import Typer, echo, run, Option
from typing import Annotated
from PIL import Image, ImageFont, ImageDraw
from pathlib import Path
import os

from typing import Final

from enumrates import TextColor, TextColorCodes

base_path: Path = Path(os.path.abspath(__file__)).parent
pwd: Path = Path(os.getcwd())

app: Typer = Typer(help="image file generator of emoji stamp for chat tool")

width: Final[int] = 128
height: Final[int] = 128

def parse_text(text: str) -> list[str]:
    """
    空白文字で分割した文字列のリストを返す
    :param text: 分割する文字列
    :return: 半角空白で分割された文字列のリスト
    """
    # TODO: 空白がない場合でも文字数に応じて分割する
    # TODO: 1行には最大3文字まで
    # TODO: 最大2行まで
    return text.split()
def prepare_font(size: int = 55) -> ImageFont:
    """
    フォントオブジェクトを準備する
    """
    # 最大文字数の行に応じてフォントサイズを変更する
    result: ImageFont = ImageFont.truetype(base_path / "fonts/CherryBombOne-Regular.ttf", size)
    return result

def prepare_image_file() -> Image:
    """
    128 * 128の背景が半透明な画像を生成する
    :return: 128 * 128の背景が半透明なImageオブジェクト
    """
    result: Image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    return result

def draw_text_on_image(
    image: Image, text: list[str], font: ImageFont, color: TextColor,
) -> None:
    """
    画像オブジェクトに文字列を描画する
    """
    joined_text: str = "\n".join(text) if len(text) > 1 else text[0]
    draw: ImageDraw = ImageDraw.Draw(image)
    if "\n" in joined_text:
        # 複数行
        bbox = draw.textbbox((0, 0), joined_text, font=font, anchor="la", spacing=40)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        # 中心に配置するための描画位置を計算
        position_x = (width - text_width) / 2
        position_y = (height - text_height) / 2
        draw.multiline_text(
            (position_x, position_y),
            joined_text,
            fill=TextColorCodes[color].value,
            font=font,
            align="center",  # 中央揃え
            anchor="la",  # ベースラインの基準
            spacing=-12,
        )
    else:
        # 1行
        bbox = draw.textbbox((0, 0), joined_text, font=font, anchor="la")
        text_width = bbox[2] - bbox[0]  # テキストの幅
        text_height = bbox[3] - bbox[1]  # テキストの高さ
        x = (width - text_width) / 2  # 横方向の中心
        y = ((height - text_height) / 2) - 15  # 縦方向の中心
        draw.text((x, y), joined_text, color, font=font, align="center")


@app.command()
def main(
    text: str,
    color: TextColor = TextColor.yellow,
) -> None:
    """
    引数で指定した文字列を128 * 128の画像にプロットしてファイル出力する
    """
    parsed_text: list[str] = parse_text(text)
    max_charactors: int = max([len(x) for x in parsed_text])
    print(max_charactors)
    output_file_name: str = "".join(parsed_text) + ".png"
    out: Image = prepare_image_file()
    font: ImageFont = prepare_font(55 if max_charactors == 3 else 65)
    draw_text_on_image(out, parsed_text, font, color)
    out.save(pwd / output_file_name)
    echo(pwd / output_file_name)

if __name__ == "__main__":
    run(main)
