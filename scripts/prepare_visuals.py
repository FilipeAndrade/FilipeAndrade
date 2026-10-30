"""Keep the animated calendar from the pinned 3D generator, without its charts."""

from copy import deepcopy
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET


SVG = "http://www.w3.org/2000/svg"
NS = {"svg": SVG}
ET.register_namespace("", SVG)


def add_text(parent, text, **attributes):
    element = ET.SubElement(parent, f"{{{SVG}}}text", attributes)
    element.text = text
    return element


def prepare_calendar(source, destination, background):
    original = ET.parse(source).getroot()
    groups = original.findall("svg:g", NS)
    # A calendar contains one group per day, each with the three faces of a bar.
    calendars = [
        group for group in groups
        if len(group) > 0 and all(
            day.tag == f"{{{SVG}}}g" and len(day.findall("svg:rect", NS)) == 3
            for day in group
        )
    ]
    summaries = [
        group for group in groups
        if any(text.text == "contributions" for text in group.findall("svg:text", NS))
    ]
    if len(calendars) != 1 or len(summaries) != 1:
        raise ValueError(f"{source}: unexpected generator layout; refusing to publish")

    summary = summaries[0]
    count = summary.find("svg:text[@class='fill-strong']", NS)
    periods = [
        text for text in summary.findall("svg:text", NS)
        if re.fullmatch(r"\d{4}-\d{2}-\d{2} / \d{4}-\d{2}-\d{2}", text.text or "")
    ]
    style = original.find("svg:style", NS)
    if count is None or not re.fullmatch(r"[\d,]+", count.text or "") or len(periods) != 1 or style is None:
        raise ValueError(f"{source}: missing contribution count, dates, or styles")

    svg = ET.Element(f"{{{SVG}}}svg", {
        "width": "1280", "height": "620", "viewBox": "0 0 1280 620",
        "role": "img", "aria-labelledby": "calendar-title calendar-description",
    })
    ET.SubElement(svg, f"{{{SVG}}}title", {"id": "calendar-title"}).text = "Filipe Andrade's GitHub activity"
    ET.SubElement(svg, f"{{{SVG}}}desc", {"id": "calendar-description"}).text = (
        f"Animated contribution calendar, {periods[0].text}. {count.text} contributions."
    )
    svg.append(deepcopy(style))
    ET.SubElement(svg, f"{{{SVG}}}rect", {
        "width": "1280", "height": "620", "rx": "24", "fill": background,
    })
    add_text(svg, "GitHub activity", x="40", y="56", **{
        "class": "fill-fg", "font-size": "26", "font-weight": "600",
    })
    add_text(svg, periods[0].text, x="1240", y="56", **{
        "class": "fill-weak", "font-size": "20", "text-anchor": "end",
    })

    # Preserve every daily bar and its native animation; only flatten the perspective.
    calendar = deepcopy(calendars[0])
    calendar.set("id", "contribution-calendar")
    calendar.set("transform", "translate(0, 15) scale(1, 0.65)")
    svg.append(calendar)
    add_text(svg, f"{count.text} contributions", x="40", y="585", **{
        "class": "fill-fg", "font-size": "28", "font-weight": "600",
    })

    destination.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(svg).write(destination, encoding="utf-8", xml_declaration=False)
    print(f"Prepared {destination.name}: {len(calendar)} daily bars; no radar or language chart")


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Usage: prepare_visuals.py SOURCE_DIRECTORY OUTPUT_DIRECTORY")
    source, destination = map(Path, sys.argv[1:])
    prepare_calendar(source / "profile-south-season-animate.svg", destination / "profile-3d.svg", "#f6f8fa")
    prepare_calendar(source / "profile-night-rainbow.svg", destination / "profile-3d-dark.svg", "#0d1117")


if __name__ == "__main__":
    main()
