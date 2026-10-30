"""Validate README image paths and generated SVGs before publishing them."""

import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path


class ReadmeImages(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = set()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "img":
            assert attributes.get("alt"), "README images need descriptive alt text"
            self.paths.add(attributes["src"])
        elif tag == "source":
            self.paths.add(attributes["srcset"])


root = Path(__file__).resolve().parents[1]
image_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "assets"
images = ReadmeImages()
images.feed((root / "README.md").read_text(encoding="utf-8"))
expected = {"profile-3d.svg", "profile-3d-dark.svg", "snake.svg", "snake-dark.svg"}
assert images.paths == {f"./assets/{name}" for name in expected}, "Unexpected README image references"
assert {path.name for path in image_dir.glob("*.svg")} == expected, "Missing or unexpected SVGs"

for name in sorted(expected):
    path = image_dir / name
    content = path.read_text(encoding="utf-8")
    svg = ET.fromstring(content)
    assert svg.tag == "{http://www.w3.org/2000/svg}svg", f"{name}: not an SVG document"
    assert svg.get("viewBox"), f"{name}: missing scalable viewBox"
    assert re.search(r"@keyframes|<animate(?:Transform)?\b", content), f"{name}: no animation"
    assert len(list(svg.iter())) > 10, f"{name}: empty or incomplete drawing"
    if name.startswith("profile-3d"):
        calendar = svg.find("{http://www.w3.org/2000/svg}g[@id='contribution-calendar']")
        assert calendar is not None and len(calendar) > 0, f"{name}: missing contribution calendar"
        assert svg.findall("{http://www.w3.org/2000/svg}g") == [calendar], f"{name}: unexpected secondary chart"
        assert not list(calendar.iter("{http://www.w3.org/2000/svg}text")), f"{name}: unexpected chart labels"
    for element in svg.iter():
        assert element.tag.split("}")[-1] not in {"script", "foreignObject"}, f"{name}: unsafe element"
        for key, value in element.attrib.items():
            assert not key.lower().startswith("on"), f"{name}: script event handler"
            if key.split("}")[-1] == "href":
                assert value.startswith("#"), f"{name}: external resource"
    print(f"OK: {name} ({path.stat().st_size:,} bytes, valid animated SVG)")

print("All README images resolve to validated local assets.")
