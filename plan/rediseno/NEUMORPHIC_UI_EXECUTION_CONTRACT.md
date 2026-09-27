# NEUMORPHIC UI EXECUTION CONTRACT

## 0. EXECUTION DIRECTIVE

This document is an implementation contract.

It is not:

- a brainstorming document;
- a design proposal;
- an invitation to reinterpret the target aesthetic;
- a request for alternative visual directions;
- a negotiation.

Execute the specification.

Do not:

- defend the current implementation;
- preserve a visual decision merely because it already exists;
- substitute subjective preference for the reference images;
- generate comparison Markdown files;
- declare success because tests pass;
- declare success because CSS tokens exist;
- declare success because components technically contain `box-shadow`;
- reinterpret visual failure as acceptable variation.

The required result is visual.

---

# 1. AUTHORITY ORDER

Visual authority, highest first:

1. `/home/gusta/Projects/DASHBOARDS/Works/evidencia/IDEAL/Neumorphism_Dashboard_Professional.jpeg`
2. `/home/gusta/Projects/DASHBOARDS/Works/evidencia/IDEAL/Neumorphism_Dashboard_mobile_.jpeg`
3. This execution contract.
4. Previous visual specifications, only where they do not conflict with 1–3.
5. Current implementation: **ANTI-REFERENCE ONLY**.

Functional authority remains the existing application.

Therefore:

```text
FUNCTIONAL BEHAVIOR = PRESERVE
VISUAL IMPLEMENTATION = RECONSTRUCT WHEN REQUIRED
```

Do not change:

- data;
- business rules;
- actions;
- action semantics;
- application flows;
- backend;
- API behavior;
- stored information;
- functional labels unless explicitly instructed elsewhere.

---

# 2. TARGET

The target is not:

> "a UI with soft shadows"

The target is:

> A coherent mobile-first neumorphic material system whose geometry, lighting, surface treatment, rhythm and icon/text relationships belong visibly to the same design family as the IDEAL references.

The current UI must stop looking like:

```text
generic component
+ border-radius
+ box-shadow
= neumorphism
```

The required model is:

```text
MATERIAL
+ LIGHT MODEL
+ GEOMETRIC SYSTEM
+ CONSISTENT ELEVATION
+ ICONOGRAPHIC STRUCTURE
+ SPATIAL RHYTHM
+ INTERACTION STATES
= NEUMORPHIC UI
```

---

# 3. REFERENCE INSPECTION — REQUIRED BEFORE EDITING

Before modifying CSS or markup:

1. Inspect both IDEAL images directly.
2. Inspect the current `componentes-390.png`.
3. Compare them visually side-by-side.
4. Identify the following properties from the references:

```text
REFERENCE_GEOMETRY
REFERENCE_LIGHT_VECTOR
REFERENCE_SHADOW_CHARACTER
REFERENCE_RADIUS_SYSTEM
REFERENCE_ICON_SCALE
REFERENCE_ICON_TEXT_RELATION
REFERENCE_VERTICAL_RHYTHM
REFERENCE_SURFACE_HIERARCHY
REFERENCE_COMPONENT_PROPORTIONS
```

Do not copy:

- textual content;
- application modules;
- business functionality.

Extract only the visual system.

Do not create a user-facing report from this analysis.

Perform the analysis internally and implement.

---

# 4. COORDINATE MODEL

Use the mobile viewport `390px` as the primary calibration environment.

Define normalized coordinates:

```text
u = x / viewport_width
v = y / viewport_height
```

This allows geometry to be compared independently of source-image resolution.

For any family of equivalent controls `C`:

```text
H(C₁) ≈ H(C₂) ≈ ... ≈ H(Cₙ)

R(C₁) / H(C₁)
≈
R(C₂) / H(C₂)
≈
...
≈
R(Cₙ) / H(Cₙ)
```

Where:

```text
H = component height
R = corner radius
```

Equivalent controls must not acquire arbitrary geometry because their labels differ.

---

# 5. GEOMETRIC INVARIANTS

For equivalent action controls:

```text
σ(height) <= 2px
σ(icon_x) <= 2px
σ(text_x) <= 2px
σ(radius) <= 1px
```

Where `σ` represents maximum visual deviation inside the component family.

Vertical gaps:

```text
| gap[n] - gap[n+1] | <= 2px
```

except at explicit section boundaries.

Text must share a common vertical axis.

Icon modules must share a common vertical axis.

Do not independently center each row according to its content.

---

# 6. MOBILE LAYOUT CONSTRAINTS

Primary viewport:

```text
Wv = 390px
```

Hard constraints:

```text
document.scrollWidth <= 390px
```

No visual element may unintentionally force document-level horizontal overflow.

Horizontal page margin target:

```text
12px <= Mpage <= 20px
```

Do not create nested containers whose combined padding compresses the usable action area unnecessarily.

For a container:

```text
Wusable = Wv - 2*Mpage - 2*Pcontainer
```

Before introducing or preserving another wrapper, verify that:

```text
Wusable / Wv >= required visual proportion
```

Do not solve "symmetry" by shrinking the usable width.

---

# 7. SYMMETRY DEFINITION

Symmetry means:

```text
repeatable geometry
+ common axes
+ common proportions
+ controlled spacing
+ consistent material behavior
```

Symmetry does **not** mean:

```text
everything narrow
everything centered
everything inside one box
everything identical regardless of role
```

The current implementation must not use containerization as a substitute for composition.

---

# 8. MATERIAL MODEL

Use one primary neutral material family.

The body, panel and controls must appear constructed from related material.

Avoid:

- white cards floating on gray backgrounds;
- arbitrary colored bodies;
- colored outlines defining component geometry.

Initial neutral base:

```css
--neu-bg: #e7e8eb;
--neu-surface: #e7e8eb;
```

The exact neutral may be tuned slightly after visual comparison.

Constraint:

```text
ΔL(background, primary_surface) ≈ minimal
```

The volume must primarily come from light and shadow, not from large fill-color differences.

---

# 9. LIGHT MODEL

Use one global virtual light source.

Direction:

```text
TOP-LEFT → BOTTOM-RIGHT
```

Approximate light vector:

```text
θ ≈ 315°
```

Therefore:

```text
highlight offset  = (-x, -y)
shadow offset     = (+x, +y)
```

All neumorphic controls must obey the same virtual light source.

FAIL if one component appears illuminated from a different direction.

---

# 10. ELEVATION MODEL

Define elevation as a function:

```text
E = f(offset, blur, shadow-opacity, highlight-opacity, contact-shadow)
```

Do not equate elevation with a border.

Required levels:

```text
E0 = flat
E1 = subtle
E2 = low
E3 = primary raised
E4 = strongly raised
E5 = focal/hero
IN1 = recessed
IN2 = strongly recessed
```

Primary interactive controls should generally occupy:

```text
E3 <= primary_control <= E4
```

The current weak 1–2 appearance is rejected.

E5 is reserved for exceptional visual hierarchy.

Do not apply E5 everywhere.

---

# 11. PRIMARY ELEVATED SHADOW TOKEN

Start calibration at approximately:

```css
--neu-e3:
  -8px -8px 16px rgba(255,255,255,.82),
   8px  8px 18px rgba(153,160,171,.46),
   2px  3px  6px rgba(120,128,140,.12);
```

Interpretation:

```text
shadow 1 = broad upper-left highlight
shadow 2 = broad lower-right ambient shadow
shadow 3 = subtle contact/occlusion shadow
```

This is an initial implementation target, not permission to weaken the result until it disappears.

At `390px`, the elevation must remain clearly visible at 100% zoom.

---

# 12. STRONG ELEVATION TOKEN

For components requiring stronger presence:

```css
--neu-e4:
  -10px -10px 20px rgba(255,255,255,.88),
   10px  10px 22px rgba(150,157,169,.50),
    3px   4px  7px rgba(115,123,136,.14);
```

Do not introduce colored glow merely to simulate depth.

Depth comes from luminosity and occlusion.

---

# 13. RECESSED TOKEN

For fields, tracks and selected recessed surfaces:

```css
--neu-in1:
  inset 5px 5px 10px rgba(151,158,169,.27),
  inset -5px -5px 10px rgba(255,255,255,.72);
```

A recessed component must visually read as:

```text
surface displaced below material plane
```

not:

```text
gray rectangle
```

---

# 14. PRESSED STATE

The physical interaction model is:

```text
RAISED
↓ pointerdown
PRESSED
↓ pointerup
RAISED
```

Pressed state:

```css
transform:
  translateY(1px)
  scale(.99);

box-shadow:
  inset 4px 4px 8px rgba(151,158,169,.28),
  inset -4px -4px 8px rgba(255,255,255,.68);
```

Transition target:

```text
90–140ms press
140–200ms release
```

The control must visibly move from elevated to recessed.

Changing only color is insufficient.

---

# 15. SHADOW QUALITY CONSTRAINTS

For any primary elevated control:

```text
offset_dark > 0
offset_light < 0

blur / |offset| ≈ 1.8–2.5
```

Highlight must remain visible.

Dark shadow must remain visible.

Neither may disappear into the background.

FAIL if:

```text
left/top edge visually disappears
OR
right/bottom shadow looks like a conventional drop shadow only
OR
component appears flat at 390px
```

---

# 16. NO PERSISTENT OUTLINES

For neumorphic raised components:

```css
border: 0;
background-image: none;
```

Do not use persistent:

- blue borders;
- green borders;
- red borders;
- amber borders;

to define the component.

Accessibility focus is an exception:

```css
:focus-visible
```

may display a temporary focus indication.

That indication is state-specific and must not become permanent component geometry.

---

# 17. COLOR STATE MODEL

Color is subordinate to material.

Use:

```text
NEUTRAL MATERIAL
+
SMALL SEMANTIC COLOR ACCENT
```

not:

```text
SEMANTIC COLOR BORDER
=
COMPONENT
```

State mapping:

```text
success   → green icon/accent
error     → red icon/accent
attention → amber icon/accent
processing→ motion/accent
disabled  → reduced contrast/elevation
```

The component body remains neutral.

---

# 18. ICONOGRAPHIC MODEL

The existing tiny circular icon-badge treatment is rejected.

Primary action rows must follow:

```text
[ ICON MODULE ]  [ TEXT MODULE ]
```

not:

```text
[ tiny raised circle containing icon ] [ text ]
```

unless a circular control is functionally justified.

For full action controls:

```text
icon visual box: 24–30px
reserved icon column: 32–40px
icon/text gap: 14–20px
```

All equivalent actions share:

```text
icon_x = constant
text_x = constant
```

---

# 19. ICON STYLE

For the principal dashboard direction:

Do not treat Lucide outline iconography as mandatory.

Target reference characteristics:

- visually substantial;
- simple;
- rounded or solid;
- high recognizability;
- coherent apparent weight;
- capable of being recognized before reading the label.

Preferred visual treatment:

```text
filled / substantial glyph
rather than
thin decorative outline
```

Do not introduce a new external icon dependency unless required.

Inline SVG is acceptable.

If a library is already available, use a filled/rounded family compatible with the references.

---

# 20. ICON SEMANTICS

Do not use state icons as generic action icons.

Examples:

```text
✓ should communicate success/completion
✕ should communicate failure/cancel state
! should communicate attention
spinner should communicate processing
```

Do not place a checkmark on a neutral action merely because an icon is needed.

Use a semantically appropriate action icon.

---

# 21. ACTION FAMILY CONTRACT

The following are one visual family:

```text
C-01
C-02
Processing
Success
Error
Disabled
```

They must share:

```text
material
height family
radius family
light vector
icon column
text axis
base elevation model
```

States may alter:

```text
icon
accent color
opacity
animation
elevation intensity
```

They must not become unrelated component designs.

---

# 22. PROCESSING STATE

Processing must preserve the geometry of the originating action.

Constraint:

```text
W_processing = W_origin
H_processing = H_origin
R_processing = R_origin
```

No layout shift.

Spinner:

- occupies icon module;
- may animate;
- does not require its own raised circular button.

---

# 23. SUCCESS STATE

Use:

```text
neutral body
E3 material
green success glyph
```

Do not use:

```text
green outline
green card border
green component body
```

unless required by functional specification outside this contract.

---

# 24. ERROR STATE

Use:

```text
neutral body
E3 material
red failure glyph
```

Do not use persistent red border as primary shape definition.

---

# 25. DISABLED STATE

Disabled must remain visibly identifiable as the same component.

Use approximately:

```text
opacity/content contrast reduction
+
lower elevation
```

Target:

```text
E1–E2
```

Do not reduce visibility until component geometry disappears.

No interaction shadow transition on press.

---

# 26. C-03 CONTRACT

C-03 must not read as:

```text
generic outlined card
```

Use:

```text
neutral material
controlled E3 elevation
shared light model
shared radius family
```

If it contains secondary text:

```text
title axis = shared text axis
secondary text aligned with title
```

Avoid arbitrary colored border.

---

# 27. C-04 CONTRACT

C-04 remains recessed.

Target:

```text
IN1
```

It must show:

- upper-left internal highlight;
- lower-right internal shadow;
- readable text;
- no heavy conventional border.

On focus:

- functional focus cue may appear;
- underlying recessed material must remain recognizable.

---

# 28. C-05 CONTRACT

C-05 remains a toggle.

Track:

```text
IN1
```

Thumb:

```text
E2–E3
```

Do not enlarge the entire control merely to increase presence.

Increase perceived material depth through:

```text
light
shadow
occlusion
```

not arbitrary size.

---

# 29. C-06 CONTRACT

Segmented control:

```text
container = IN1
inactive option = material plane / recessed context
active option = E2–E3
```

The active element must visually rise from the recessed container.

Maintain common radius and light source.

---

# 30. C-07 CONTRACT

C-07 is explicitly excluded from neumorphic elevation.

It remains:

```text
blue
underlined
flat
```

Do not "fix" it by adding elevation.

---

# 31. C-08 CONTRACT

Modal/overlay:

```text
modal = high elevation layer
label = flat metadata
```

Do not wrap metadata in a chip unless functionally required.

The modal must visually separate from the underlying plane through broad depth, not through a dark conventional border.

---

# 32. C-09 CONTRACT

C-09 is a compact state surface.

Do not implement as:

```text
colored outline pill
```

Use:

```text
neutral neumorphic surface
+
semantic icon accent
```

Compact components may use E2 rather than E4.

---

# 33. C-10 CONTRACT

Functional horizontal scrolling is already validated.

Do not alter its behavior.

Required invariant:

```css
overflow-x: auto;
```

and:

```text
document.scrollWidth <= viewport_width
```

Do not shrink table typography merely to fit all columns.

---

# 34. PROFESSIONAL REFERENCE — STRUCTURAL EXTRACTION

Use `Neumorphism_Dashboard_Professional.jpeg` primarily for:

```text
geometry
symmetry
action-row proportions
icon/text alignment
vertical rhythm
surface cohesion
large-control consistency
```

The critical pattern is:

```text
┌───────────────────────────────┐
│  ICON    ACTION               │
└───────────────────────────────┘

             ↓ constant gap

┌───────────────────────────────┐
│  ICON    ACTION               │
└───────────────────────────────┘
```

The repeated geometry is intentional.

---

# 35. MOBILE REFERENCE — STRUCTURAL EXTRACTION

Use `Neumorphism_Dashboard_mobile_.jpeg` primarily for:

```text
surface material
depth quality
small/large control relationship
shadow softness
panel/control cohesion
icon prominence
```

Do not copy its content.

---

# 36. VISUAL RHYTHM

Define a base spacing quantum:

```text
q = 4px
```

Allowed spacing values should normally belong to:

```text
{2q, 3q, 4q, 5q, 6q, 8q, 10q, 12q}
```

Equivalent action rows should use one repeated gap value.

Do not alternate arbitrary gaps.

---

# 37. CORNER-RADIUS SYSTEM

Radius should be relational.

For large action controls:

```text
R / H ≈ 0.35–0.50
```

For strongly pill-shaped controls:

```text
R >= H/2
```

Do not randomly mix:

```text
10px
14px
17px
22px
27px
```

without semantic reason.

---

# 38. TEXT ALIGNMENT

Action controls:

```text
text-align: left
```

unless the reference role explicitly requires centered content.

Text baseline must align consistently across the family.

Do not independently center icon+label pairs according to label length.

---

# 39. TYPOGRAPHIC ROLE

Typography must support geometry rather than dominate it.

For action rows:

```text
label weight ≈ 600–700
```

Avoid reducing text simply because the label is longer.

If a label does not fit:

first inspect:

```text
component width
padding
icon gap
layout
```

before reducing font size.

---

# 40. STATE MACHINE

Generic interactive control:

```text
REST
 │
 ├─ pointerenter → HOVER
 │
 ├─ pointerdown → PRESSED
 │                  │
 │                  └─ pointerup → REST
 │
 ├─ async-start → PROCESSING
 │                   │
 │                   ├─ resolved → SUCCESS
 │                   └─ rejected → ERROR
 │
 └─ disabled → DISABLED
```

---

# 41. MOTION CONTRACT

Recommended timings:

```text
REST → PRESSED      90–120ms
PRESSED → REST     140–180ms
REST → HOVER       120–160ms
ASYNC → SUCCESS    160–220ms
ASYNC → ERROR      160–220ms
```

Suggested easing:

```css
cubic-bezier(.2,.8,.2,1)
```

Do not animate:

- huge layout dimensions;
- continuous decorative motion.

Prefer:

```text
transform
opacity
shadow transition
```

---

# 42. HOVER

Desktop hover must not redefine the component.

Use only subtle increase in perceived elevation:

```text
E3 → E3.3
```

Do not introduce:

- colored border;
- colored fill;
- unrelated glow.

---

# 43. PROCESSING MOTION

Spinner motion must be local.

Do not animate the entire button continuously.

Button remains geometrically stable.

---

# 44. REFERENCE SIMILARITY IS NOT PIXEL COPYING

Because content differs, do not perform literal pixel-perfect duplication.

Match:

```text
visual grammar
relative geometry
material behavior
lighting
rhythm
icon hierarchy
depth
```

not content.

---

# 45. DOM/GEOMETRY VALIDATION

At `390px`, programmatically inspect equivalent action controls.

Verify:

```javascript
Math.max(...heights) - Math.min(...heights) <= 2
```

Verify icon axes:

```javascript
Math.max(...iconXs) - Math.min(...iconXs) <= 2
```

Verify text axes:

```javascript
Math.max(...textXs) - Math.min(...textXs) <= 2
```

Verify document width:

```javascript
document.documentElement.scrollWidth <= window.innerWidth
```

If any fails:

iteration fails.

---

# 46. COMPUTED STYLE VALIDATION

For every primary elevated control:

```text
background-image == none
```

Persistent border must be:

```text
none
or visually transparent
```

`box-shadow` must contain both:

```text
negative X/Y light component
positive X/Y dark component
```

unless the component is explicitly recessed.

---

# 47. RECESSED STYLE VALIDATION

For C-04, C-05 track and C-06 container:

computed `box-shadow` must include:

```text
inset light
+
inset dark
```

A single inset shadow does not satisfy the material model.

---

# 48. ICON VALIDATION

FAIL if equivalent action icons:

- have inconsistent apparent size;
- use unrelated stroke weights;
- randomly switch between filled and thin-outline styles;
- occupy arbitrary circular containers;
- shift horizontal position between rows.

---

# 49. MATERIAL VALIDATION

FAIL if an elevated control depends primarily on:

```text
border-color
background hue
gradient
```

to communicate elevation.

Elevation must remain apparent in grayscale.

This is a hard requirement.

---

# 50. GRAYSCALE TEST

Temporarily inspect the screenshot in grayscale.

The following must still be distinguishable:

- elevated controls;
- recessed fields;
- panel;
- modal;
- disabled state;
- active segmented control.

If the hierarchy collapses without semantic colors:

FAIL.

---

# 51. 100% SCALE TEST

Evaluate mobile screenshot at normal scale.

Do not use zoom as evidence that a shadow exists.

If elevation is only visible after zooming:

FAIL.

---

# 52. NO SELF-APPROVAL DOCUMENTS

Do not create:

```text
comparacion-T1*.md
visual-analysis*.md
compliance-report*.md
```

unless explicitly requested.

No internal rubric output is needed.

Use the rubric to improve the implementation.

---

# 53. OUTPUT REQUIRED

After implementation provide only:

1. modified code;
2. fresh `390px` screenshot;
3. desktop screenshot if relevant;
4. concise list of actual files modified;
5. test result summary.

Do not produce a long defense of the design.

---

# 54. HARD FAIL CONDITIONS

The iteration automatically fails if any of the following occurs:

```text
F01: Primary actions visually remain E1–E2.
F02: Colored outlines define Success/Error/Attention.
F03: C-03 becomes an outlined generic card.
F04: Icons remain tiny decorative bubbles.
F05: Equivalent action text axes differ > 2px.
F06: Equivalent icon axes differ > 2px.
F07: Equivalent control heights differ > 2px.
F08: Global document width exceeds viewport.
F09: Control geometry disappears in disabled state.
F10: Component elevation disappears at 390px / 100% scale.
F11: Components use conflicting light directions.
F12: Surface family breaks into unrelated colors.
F13: Symmetry is achieved by excessive compression.
F14: Another analysis report is produced instead of fixing UI.
F15: Current implementation is defended against the IDEAL references.
```

Any hard fail means:

```text
DO NOT DECLARE COMPLETION.
```

---

# 55. ACCEPTANCE VECTOR

Evaluate the iteration internally using:

```text
V = [
  geometry,
  material,
  elevation,
  iconography,
  rhythm,
  alignment,
  interaction,
  reference-cohesion
]
```

Each dimension:

```text
0.0 – 1.0
```

Minimum:

```text
min(V) >= 0.85
```

Overall mean:

```text
mean(V) >= 0.90
```

Hard-fail conditions override the score.

---

# 56. WEIGHTED VISUAL OBJECTIVE

Use internally:

```text
Score =
  0.20 * Geometry
+ 0.20 * Material
+ 0.20 * Elevation
+ 0.15 * Iconography
+ 0.10 * Rhythm
+ 0.05 * Alignment
+ 0.05 * Interaction
+ 0.05 * ReferenceCohesion
```

Required:

```text
Score >= 0.90
```

This score is an internal decision aid.

Do not create a report merely claiming the score.

The screenshot is the evidence.

---

# 57. FINAL SIDE-BY-SIDE GATE

Before completion, visually compare:

```text
NEW componentes-390.png

VS

Neumorphism_Dashboard_Professional.jpeg

VS

Neumorphism_Dashboard_mobile_.jpeg
```

Ask internally:

```text
Does the implementation share the same material language?
Does it have comparable visual discipline?
Is the geometry deliberate?
Is the depth obvious?
Are icons structurally integrated?
Is the composition calm and symmetric?
Does it look like one designed system?
```

If the answer to any is materially negative:

continue editing.

---

# 58. DO NOT OPTIMIZE FOR THE OLD SCREENSHOT

The current screenshot is not the aesthetic target.

Do not optimize for minimum code delta.

Do not preserve weak visual structure merely to reduce changes.

Preserve functionality.

Reconstruct presentation where necessary.

---

# 59. IMPLEMENTATION PRIORITY

Execute in this order:

```text
01. Global material + light model
02. Panel/container geometry
03. Action-family geometry
04. Action-family elevation
05. Iconographic system
06. C-01 / C-02
07. Processing / Success / Error / Disabled
08. C-03
09. C-04 / C-05 / C-06 coherence
10. C-09
11. C-08
12. Responsive validation
13. 390px screenshot
14. Acceptance gates
```

Do not polish secondary text before the material system is correct.

---

# 60. FINAL DIRECTIVE

The deliverable is not:

```text
"technically neumorphic"
```

The deliverable is:

```text
visibly professional neumorphism
```

The IDEAL references are not suggestions.

They define the visual quality threshold.

Do not make the implementation merely contain the same ingredients.

Make it exhibit the same design grammar:

```text
GEOMETRY
+
SYMMETRY
+
MATERIAL
+
LIGHT
+
DEPTH
+
ICONOGRAPHY
+
RHYTHM
+
INTERACTION
```

Preserve functionality.

Replace visual mediocrity.

Do not debate the direction.

Do not create another report.

Inspect.
Measure.
Implement.
Render.
Compare.
Correct.

Then deliver the evidence.
