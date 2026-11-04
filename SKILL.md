---
name: create-gemscript-collage
description: Turn a raster photo into a V6 GemScript collage with a small tightly cropped high-contrast vintage black-and-white film print, generous negative space, a high-lightness low-saturation Morandi paper background, multicolor flat-back rhinestone calligraphy using exact custom text, controlled mixed-shape accents, organic stroke extensions, nonlinear loose-gem clusters, a source-responsive layout, and an optional automatic 3:4 composite that stacks the effect above the untouched original. Use for GemScript, rhinestone-script, Y2K jewel-sticker, vintage-film collage, custom English word or name, effect-only, and effect-plus-original image requests.
---

# Create GemScript Collage

Create a 3:2 GemScript effect image. Preserve the V6 spatial system: small film, tight crop, compact film-and-lettering relationship, and large calm margins. When requested, deterministically stack the accepted effect above the real source photo in a 3:4 final PNG. Never ask the image model to redraw the lower half.

## Generation budget and stop conditions

These are hard safety limits:

- A non-batch user request authorizes at most one image-generation or image-edit call. After that call, deliver the result or report the failure and end the turn.
- An explicit batch authorizes at most one call per named source image, with no more than three generation/edit calls in one task. Before a fourth call, stop and ask the user to continue in a fresh task with a compact text handoff and only the current source path. Do not create that task unless the user asks.
- An error, timeout, oversized response, missing result, wrong text, or failed validation consumes the authorized call. Never retry, rephrase and resubmit, regenerate, or edit automatically in the same turn.
- After an error, timeout, oversized response, or missing result, do not call the image tool again in the same task. Report the failure and require a fresh task for any retry.
- Never auto-resume a failed generation when a task is reopened.
- Use only the source image explicitly named in the current request plus the material references required by this skill. When local paths exist, pass those exact paths and do not include recent conversation images. Never copy or preserve base64 image data in prompts, messages, logs, handoffs, or output files.

## Workflow

1. Inspect the source photo with the available image viewer.
2. Resolve the lettering:
   - Reproduce user-provided English text verbatim, including capitalization and spaces.
   - If none is provided, choose one short English word, or at most two short words, that fit the photo.
3. Choose a restrained background hue derived from or complementary to the source. Keep it high-lightness, low-saturation, and slightly gray.
4. Analyze the source crop, subject orientation, dominant visual direction, and negative space. Choose one source-responsive relationship instead of a fixed template:
   - film left, lettering right;
   - lettering left, film right;
   - film above, lettering directly below and touching;
   - lettering above, film directly below and touching.
   For a batch, vary the relationship unless the sources clearly call for the same solution.
   For consecutive single-image tests in the same task, avoid reusing the immediately previous relationship when another mode fits the source; repeat a mode only when source geometry or readability clearly requires it. Track the last used mode in the current context.
5. Preserve any user-approved layout reference. Treat it as a composition-only reference: retain its breathing room, film scale, crop, and film/lettering relationship while redesigning only the requested subsystem.
6. Read [references/v6-prompt.md](references/v6-prompt.md) completely and replace every placeholder, including `{LAYOUT_MODE}`, before generation.
7. Use 2–3 images from [assets/v5-rhinestone-references](assets/v5-rhinestone-references) as material-only references when the image tool supports multiple references. They define the preferred flat-back craft-sticker material, tiny connective crystals, irregular mixed-shape rhythm, and multicolor distribution. They do not define the subject, word, background hue, film crop, or layout. Explicitly label every image role in the generation prompt.
8. Before generation, write a compact layout spec for this exact image and use it as an acceptance contract, not as a suggestion: canvas `1536×1024`. Define the **core group** as film + lettering + true extensions; loose gems are intentionally excluded from this core bounding box. Every image **must include exactly 7–12 detached loose rhinestones** in the surrounding negative space, arranged as two or three irregular micro-clusters plus one to three isolated pieces; they must stay away from the canvas edge and must not form a second composition. Use the smaller inner target: for a horizontal layout, target a core group of `52–58% W × 50–56% H`, reserve a `2–3% W` gap, keep one short word at `25–32% W` and at most `16% H`, and keep the film at `8–12% W` and at most `22% H`. For a vertical layout, target a core group of `50–58% W × 52–60% H`, reserve a `2–3% H` gap, keep one short word at `25–32% W` and at most `16% H`, and keep the film at `8–12% W` and at most `22% H`. Keep at least `18%` side and `20%` top/bottom breathing room for the core group. The film's visible-bounding-box area should be `25–35%` of the lettering area, with `40%` as a hard maximum. If the source, word, or chosen layout cannot satisfy this spec, change the placement or shrink the film before generation. Do not silently relax the numbers.
9. Check the generation budget above, then use the built-in image-generation workflow. If an `imagegen` skill is available, load and follow it before calling the image tool. Treat the current uploaded photo or its explicit local path as the sole subject reference and generate one independent 3:2 landscape effect image. Do not include earlier conversation images.
10. Inspect the effect and validate:
   - exact text and readable letterforms;
   - every capital passes a skeleton check before material styling: temporarily ignore the gems and verify that the underlying handwriting path still reads as the intended capital;
   - a capital `M` has two clearly visible shoulders, one central valley, two connected main downstrokes, and a continuous handoff into the following lowercase letter; it must not read as a large oval plus a detached stem, a single arch, `A`, `N`, or lowercase `n`;
   - every lowercase letter passes the same skeleton check; in particular `m`, `n`, `u`, and `r` must have only the intended stems, humps, counters, and one natural exit stroke, with no extra branch, repeated stem, spur, loop, hook, or unexplained growth; a terminal flourish may begin only after the final intended stroke and must not alter the letter's skeleton;
   - recognizable subject and appropriate crop;
   - the film crop has one named editorial focal detail occupying roughly 60–80% of the print, with at most one small contextual edge; reject a broad scene crop that includes the full subject plus all major props;
   - high-contrast black-and-white film with only a faint background tint;
   - the film passes a tonal contrast check: near-black shadow areas, near-white highlights, and clearly separated midtones; reject gray veil, milky gray, lifted blacks, flat low contrast, or a tint that obscures the black-and-white structure;
   - high-lightness low-saturation background;
   - measure the **core** visible bounding box, not occupied area alone, and exclude loose gems from this measurement; use the horizontal or vertical core-group range defined before generation;
   - keep at least 18% left/right margins and 20% top/bottom breathing room for the core group; use a 2–3% gap between film and lettering; keep one short word at most 32% of canvas width and no more than 16% of canvas height;
   - for one short word, lettering is the primary element and the film is secondary: the film's visible-bounding-box area should be 25–35% of the lettering's visible-bounding-box area, with 40% as a hard upper limit; if independent size rules conflict with this hierarchy, shrink the film;
   - the film remains small, at most 12% of canvas width and 22% of canvas height, with a tighter crop than the source;
   - the layout follows the source composition and is not automatically lettering-left / film-right;
   - the rhinestone word and film overlap only when a real letter stroke can reach the nearest film edge without changing its natural handwriting tangent; if not, move the film slightly or leave a narrow gap rather than forcing a connection;
   - one, or at most two, rhinestone extensions begin from a real entry stroke, exit stroke, or terminal flourish and continue its tangent naturally; never add a vertical drop, sharp fold-back, hanging cord, or second tail after the word has already visibly finished;
   - exactly 7–12 detached loose gems are visibly present outside the word, arranged as two or three irregular micro-clusters plus one to three isolated pieces, with uneven spacing and no independent dotted line, arc, or diagonal; reject the image if the loose-gem count is below 7 or above 12;
   - no more than three loose gems visually align in one direction;
   - connective strokes use mostly tiny round crystals, while larger geometric cuts are embedded sparingly at structurally meaningful points;
   - at least five shape families appear across the complete design, but only one or two motif families repeat prominently;
   - the gems are shallow flat-back craft stickers with crisp facets and tight contact shadows, never thick glass jewels or cabochons;
   - no extra text, logo, watermark, split screen, or original photo outside the film.
11. Apply a hard pre-delivery gate. The image is accepted only if every numeric and visual check above passes together. In particular, reject any output whose group is too wide/tall, whose film is too large or too close in visual weight to the lettering, or whose film crop is a broad whole-scene crop. “The model may have ignored the prompt” is not an acceptance reason. Do not save, link, or present a failed image as the result.
12. If validation fails, do not make another tool call automatically. Report the defect and stop. Only an explicit later correction request authorizes one targeted image edit, subject to the generation budget. For that edit, reject wrong text, an incorrect capital skeleton, an oversized group, an oversized film, a fixed-template layout, a detached gem trail, a forced film connector, low-diversity all-round gems, or bulky jewel-like material. When the layout is already approved, do not regenerate the whole composition to fix only a letterform, terminal stroke, or rhinestone material. For a failed capital, freeze the photograph, background, remaining letters, loose accents, scale, and layout; redraw only that capital and its two adjacent joins. For a failed terminal interaction, freeze the entire word and composition except the final letter's true exit stroke and the local overlap area; remove any post-word vertical drop or independent connector.
13. Save the accepted effect non-destructively as `<source-stem>-gemscript-effect.png` in the user's working or requested output directory.
14. Choose normalized original-photo crop focus coordinates after inspection: `0.0` is left/top and `1.0` is right/bottom. Default to `0.5,0.5` only when the subject is already centered.
15. Load the bundled workspace dependencies and use the returned Python executable. This avoids assuming the system Python has Pillow. Run the deterministic compositor:

```bash
<workspace-python> <skill-dir>/scripts/compose_vertical.py \
  --effect <effect.png> \
  --original <source-photo> \
  --output <source-stem>-gemscript-final-3x4.png \
  --focus-x <0..1> \
  --focus-y <0..1>
```

16. Inspect the final PNG. Verify a 3:4 canvas, equal 3:2 halves, effect on top, the real source on the bottom, no gap or divider, and no damaged subject crop.
17. Deliver both the effect PNG and the final 3:4 PNG. Lead with the final composite.

## Output Rules

- Default half size: `1536×1024`; final size: `1536×2048`.
- Preserve the source file unchanged.
- Do not overwrite existing outputs; add a version suffix or pass `--force` only when replacement is explicitly requested.
- Skip composition only when the user explicitly asks for the effect image alone.


## V6 approved visual regression references
Use `references/v6-approved-examples.md` and the three PNGs in `assets/v6-approved-examples/` as the approved V6 visual benchmarks for composition, scale, legibility, and rhinestone quality.
