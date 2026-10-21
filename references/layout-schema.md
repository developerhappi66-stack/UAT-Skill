# Renderer input

Run with Python containing reportlab and Pillow:

```sh
python3 /absolute/skill/scripts/build_flow_pdf.py /absolute/task/flow.json /absolute/task/output.pdf
```

Paths in `screens`, `font_regular` and `font_bold` are relative to the manifest directory or absolute. The script embeds source images at their original aspect ratio without cropping or resizing the source pixels. PNG input preserves lossless detail; quality-94 JPEG without chroma subsampling was used in the approved reference to reduce size. Do not downsample long screens.

Default fonts are macOS Arial. Override font paths when unavailable or when the document needs another writing system. The template's word wrapping is space-based; inspect and adapt for CJK labels rather than accepting broken wrapping. Do not silently use a font missing required glyphs.

Minimal manifest (example paths refer to new task captures):

```json
{
  "title": "Product - UAT UI Flow Review",
  "brand": "HAPPI / PRODUCT",
  "review_label": "UAT UI REVIEW | 01 OCT 2026 | V1.0",
  "evidence_note": "Actual local UI with illustrative data; not evidence of completed live UAT.",
  "screens": {"entry": "captures/entry.png", "review": "captures/review.png"},
  "pages": [{
    "flow": "F01",
    "title": "Quotation request",
    "subtitle": "Complete the details, then review the returned quotation.",
    "rows": [[["entry", 1, "Enter details", "Tap Continue"], ["review", 2, "Review quotation", "Check all premium details"]]],
    "max_width": 285,
    "note": "Review all fields and the full premium breakdown."
  }]
}
```

`rows` contains arrays of screen tuples `[screen_id, step_number_or_string, title, action]`. Multiple rows snake in reading order; action labels sit above screens and red arrows connect consecutive screens. Maximum width is a cap: the renderer proportionally fits row heights into the page. It cannot guarantee readable size for arbitrarily many screens. Split the SAME flow into two page objects when needed, repeat its flow ID, and put `next_step` on the first page. Each page object always begins a new PDF page; different flows must use different IDs. Parts and total pages are calculated automatically.

Keep titles short (normally two lines max), action labels two lines max, and footnotes brief. For uncommon very long labels or unusually wide headers, adjust the local renderer copy and verify visually.

## Branch pages

Instead of `rows`, use explicit `nodes` and `arrows` to match approved pages 5–6. Coordinates are points measured from the page's TOP LEFT. Page dimensions are 1190.55 × 1683.78. Header ends at y=133; content normally starts at y=160–175; reserve the area below y=1530 for the footer/continuation.

```json
{
  "flow": "F02", "title": "Review outcome", "subtitle": "Follow the returned outcome.",
  "nodes": [
    {"id":"pending","x":55,"y":175,"w":208,"num":1,"title":"Under review","action":"Refresh status"},
    {"id":"approved","x":344,"y":175,"w":208,"num":2,"title":"Approved","action":"Review quotation"}
  ],
  "arrows": [
    {"points":[[270,320],[332,320]],"label":"Approved","label_pos":[272,298]}
  ],
  "text_blocks": [{"x":633,"y":230,"s":"Continue to the quotation flow.","width":260,"size":14}],
  "note":"Pending alone is not approval."
}
```

A node's `y` is its LABEL top. The phone begins at `y+72`; its total height is `w * source_height/source_width + 25`. Use those measured bounds to route arrows without crossing a screen. Polyline arrows accept multiple `[x,y]` points and optional `dashed`. Labels are red on white and wrap to 160pt. Add a separate node and labeled connector for each real branch; the example only demonstrates syntax. Reference page 5 shows approval/rejection and page 6 shows pending/failure/cancellation. Cross-page destinations can be included in action captions or separate red-arrow text blocks.

The renderer creates `output.layout.json` with each screenshot's page, position, size and source dimensions. It asserts maximum two consecutive pages per flow, explicit continuation step, in-page screenshot bounds and preserved aspect ratios. These checks do not prove UI completeness, label fit, arrow correctness or source authenticity: run the visual/evidence checks in `capture-and-qa.md`.
