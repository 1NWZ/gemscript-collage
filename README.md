# GemScript Collage

A photo collage skill combining a small vintage black-and-white film print, rhinestone lettering, and a muted paper background.

## Source and version

Prepared from gemscript-collage 1.6.0 distributed through RedSkill. This repository layout restores the scripts/ and references/ paths referenced by SKILL.md. Original skill and script contents are preserved. Local installation metadata is omitted.

## Contents

- SKILL.md: agent workflow and visual requirements.
- references/v6-prompt.md: image-generation prompt template.
- references/v6-approved-examples.md: description of visual benchmarks.
- scripts/compose_vertical.py: Pillow compositor for stacking an effect above an original photograph.

## Known limitations

The RedSkill package did not include assets/v5-rhinestone-references/ or assets/v6-approved-examples/. Those image references remain unavailable; the full prescribed reference-based workflow cannot be reproduced from this package alone.

## Compositor

Install Python 3.10+ and Pillow, then run:

```sh
python -m pip install Pillow
python scripts/compose_vertical.py --effect effect.png --original original.jpg --output final.png
```

The default output is a 1536 × 2048 PNG. Image generation requires a separate compatible image-generation tool.

## License

Released under the MIT License; see LICENSE. The publisher has confirmed authorization to release this distribution as open source. The downloaded RedSkill package did not include an original license or author attribution.
