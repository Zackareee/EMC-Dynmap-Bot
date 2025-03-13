import argparse
from dynmap_bot_core.models.spatial.map import Map
from dynmap_bot_core.utils import image, build
from PIL import Image

parser = argparse.ArgumentParser(description="Render towns or nations into an image.")
parser.add_argument("-t", "--towns", nargs="+", help="List of towns to render")
parser.add_argument("-n", "--nations", nargs="+", help="List of nations to render")
parser.add_argument("-o", "--output", default="out.png", help="Output image filename (default: out.png)")
parser.add_argument("-uc", "--uncropped", action="store_true", help="Render uncropped version")


def render_towns(town_names, _output: str, uncropped=False):
    map_obj: Map = build.build_map(town_names=town_names)
    image_obj: Image = build.build_map_image(map_obj)
    if not uncropped:
        image_obj: Image = image.crop_map_and_image(map_obj, image_obj)
    image_obj.save(f"./out/{_output}")


def render_nations(nation_names, _output: str, uncropped=False):
    map_obj: Map = build.build_nations(nation_names=nation_names)
    image_obj: Image = build.build_map_image(map_obj)
    if not uncropped:
        image_obj: Image = image.crop_map_and_image(map_obj, image_obj)
    image_obj.save(f"./out/{_output}")


def main():

    args = parser.parse_args()
    output_ext = args.output.split(".")[-1].lower()

    valid_extensions = {"png", "jpg", "jpeg", "svg"}

    if output_ext not in valid_extensions:
        print(f"Error: Invalid file format '{output_ext}'. Supported formats: {', '.join(valid_extensions)}")
        exit(1)

    print(f"Rendering {'towns' if args.towns else 'nations'}: {args.towns or args.nations}")

    if args.towns:
        render_towns(args.towns, args.output, args.uncropped)
    elif args.nations:
        render_nations(args.nations, args.output, args.uncropped)

    print(f"Saved as: {args.output} (Format: {output_ext})")


if __name__ == "__main__":
    main()
