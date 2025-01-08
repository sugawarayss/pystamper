from typer import Typer, echo, run, Option
from typing_extensions import Annotated

from src.enumrates import FontColor

app: Typer = Typer()

@app.command("pystamper")
def main():

    echo("Hello")


if __name__ == '__main__':
    run(main)
