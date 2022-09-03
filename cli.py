import click
from img2txt import generate_txt_from_image


@click.command()
@click.argument("source_file", type=click.Path(exists=True))
@click.argument("destination_file", type=click.Path(), required=False)
@click.option("-s", "--scale")
@click.option("-m", "--max-resolution", type=(int, int))
@click.option("-q", "--quiet", is_flag=True)
def generate_txt_from_image_cli_wrapper(
    source_file, destination_file, scale, max_resolution, quiet
):
    generate_txt_from_image(
        source_img_path=source_file,
        destination_img_path=destination_file,
        scale=scale,
        max_resolution=max_resolution,
        quiet=quiet,
    )


if __name__ == "__main__":
    generate_txt_from_image_cli_wrapper()
