from pathlib import Path
from PIL import Image, ImageDraw
import argparse


def create_sample_image(path: Path, defect: bool):
    image = Image.new("RGB", (224, 224), color=(200, 200, 200) if not defect else (220, 180, 180))
    draw = ImageDraw.Draw(image)
    draw.rectangle([32, 32, 192, 192], outline=(40, 40, 40), width=4)
    if defect:
        draw.line([80, 80, 144, 144], fill=(200, 20, 20), width=8)
        draw.line([144, 80, 80, 144], fill=(200, 20, 20), width=8)
    else:
        draw.line([80, 112, 144, 112], fill=(40, 160, 40), width=10)
    image.save(path)


def main():
    parser = argparse.ArgumentParser(description="Generate sample defect and non-defect images.")
    parser.add_argument("--output", type=str, default="sample_data/demo", help="Output directory")
    args = parser.parse_args()

    output = Path(args.output)
    normal_dir = output / "normal"
    defective_dir = output / "defective"
    normal_dir.mkdir(parents=True, exist_ok=True)
    defective_dir.mkdir(parents=True, exist_ok=True)

    for index in range(3):
        create_sample_image(normal_dir / f"normal_{index + 1}.png", defect=False)
        create_sample_image(defective_dir / f"defect_{index + 1}.png", defect=True)

    print(f"Generated sample dataset in {output}")


if __name__ == "__main__":
    main()
