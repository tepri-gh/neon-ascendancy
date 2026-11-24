# Pre-Partitioned Sub-Territory Overlays & Control-Center Dots on the In-Game World Map

Research report for **Roadmap Step 0.5 — In-Game Map Territory Visualization**
(Phase 0, pre-`v0.1.0`).

- Target: Cyberpunk 2077 2.5, redscript 1.x, ArchiveXL 1.28.11, TweakXL 1.12.2,
  no Codeware (per `docs/modding.md`), no CET in the shipping stack.
- Question: how should Neon Ascendancy draw pre-partitioned sub-territories
  (~5 per major district) and control-center dots on the vanilla World Map,
  with ownership-coloured fills, crisp shared borders, and near-zero frame cost?
- Method: read `docs/roadmap.md`, `docs/architecture.md`, the decompiled 2.5
  scripts under `refs/cyberpunk`, the game's own TweakDB `.tweak` sources under
  `<game>/tools/redmod/tweaks`, the 2.5 ink resource database, and the public
  modding record for the map renderer. No code was changed; no game was launched.
- Status: design research + prototype plan. Every mechanism marked
  **UNVERIFIED** needs an in-game spike before it becomes a design commitment.

---

## 0. TL;DR

| Path | What it gives | Alignment | Effort | Perf | Codeware-free | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| **D. Vanilla mappins** | Control-center dots, per-owner tint, custom tooltip | Native (exact) | Low | Native, negligible | Yes (needs TweakXL for a map-only mappin definition) | **Ship in `v0.1.0`** |
| **A. Ink vector overlay** | Pre-partitioned transparent fills + crisp borders + labels | Exact if projected from native anchor mappins (homography); otherwise affine approximation | Medium | Zero while idle; bounded while the camera moves | Yes (pure redscript possible) | **Target for `v0.2.0`**, gated on three spikes |
| **B. 3D overlay in the map scene** | Fills/borders inside the 3D hologram, perfect perspective | Perfect by construction | High (WolvenKit/Blender + scene injection) | Native | Asset-side yes; runtime recolour unresolved | Defer; one bounded spike only |
| **C. DX12/ImGui/CET overlay** | Anything | Requires reverse-engineered projection | High | Fine | No (CET) | Reject |
| **0. Do nothing** | Vanilla district/subdistrict borders already exist | — | Zero | Zero | Yes | Baseline to beat, not a plan |

**Recommendation.** Ship **D** for `v0.1.0` (dots + ownership tint + tooltip, plus
an optional mappin-anchored influence ring). Build **A** for `v0.2.0` as a
screen-space `inkShape` layer drawn from pre-authored polygons, projected with a
homography derived from four native-projected anchor mappins. Keep **B** as a
contained spike only if A fails its alignment or frame-cost gate. Do not build C.

The vanilla map already renders district **and** subdistrict borders from the 3D
hologram, so Neon Ascendancy does not need to draw geography to be legible on day
one; it needs to draw **ownership** and **control centers**. That is what D does.

---

## 1. How the vanilla World Map actually renders

### 1.1 The map is a 3D hologram rendered into a dynamic texture, with ink on top

The menu is `WorldMapMenuGameController extends MappinsContainerController
extends inkProjectedHUDGameController extends inkHUDGameController`
(`refs/cyberpunk/cyberpunk/UI/fullscreen/map/worldMap.swift:2`,
`refs/cyberpunk/cyberpunk/UI/mappins/mappinsContainers.swift:2`). The map visual
is not a large ink drawing. The 2.5 ink resource database shows the structure of
`base\gameplay\gui\fullscreen\world_map\world_map.inkwidget`:

```text
WorldMapRoot (3840x2160) -> Content
  order 0  EntityPreviewContainer  (1920x1080)   <- the map render
  order 1  GPSPathContainer        (1920x1080)   <- native GPS polylines
  order 2  DistrictsRoot           (550x400)     <- district/subdistrict labels
  order 3  SpawnContainer          (1920x1080)   <- every mappin widget
  order 4  vignette, 5 upperBg, 6-7 debug outline canvases, 8+ HUD panels
```

The `EntityPreview` library item is controlled by
`gameuiWorldMapPreviewGameController` and contains exactly one child,
`MapImage` — an `inkImageWidget` bound to atlas part `map` of
`base\gameplay\gui\fullscreen\world_map\world_map_atlas.inkatlas`, whose texture
is the **dynamic texture**
`base\gameplay\gui\fullscreen\world_map\world_map_texture.dtex`
(3840x2160). The preview controller's serialized fields are:

```text
gameuiWorldMapPreviewGameController
  canvas                   inkImageRef      -> MapImage
  viewTemplate             ../../entities/cameras/3dmap/3dmap_view.ent
  cursorTemplate           ../../entities/cameras/3dmap/3dmap_cursor.ent
  viewEnvironmentDefinition base\weather\24h_basic\3dmap.envparam
```

So the pipeline is:

```text
3D "hologram" scene (terrain + building volumes + district borders)
        |  camera (3dmap_view.ent, driven by WorldMapZoomLevel_Record)
        v
world_map_texture.dtex  (render target, 3840x2160)
        |  inkImageWidget "MapImage"
        v
world map UI  <- ink mappins are projected natively into the same 1920x1080 space
```

That the map is a **stylised model**, not the live game world, is confirmed by
the 2.5-era map overhaul ecosystem: *Realistic Map 3D* exists precisely because
"it makes the game draw the real city through the map camera" instead of the
blue hologram; *3D World Map Fixed* edits map-only building meshes; and public
extraction research describes map buildings as instance transforms stored in
`districts_data.xbm` data textures plus district/monument layout in
`3dmap_view.ent`. The model is nonetheless authored in **world coordinates**:
fast-travel mappins registered at real world positions land on the drawn
terminal, and the map cursor bounds are world-space (see 1.2). That is the
property this design relies on.

Consequences:

1. A 2D ink layer above `MapImage` is in **screen space of the map render**, not
   in map-model space. It can be projected correctly only by reproducing the map
   camera (or by deriving the projection from things the game already projects).
2. Because ink layers are ordered as above, a territory layer added inside
   `EntityPreview` renders **above the map, below the GPS route, district
   labels, and mappins** — exactly the readability stack we want.
3. District borders are inside the 3D render. No ink or script API can recolour,
   subdivide, or query them (1.3).

### 1.2 Camera, zoom, tilt, and the world-space extents

`WorldMapSettings.DefaultSettings` (`<game>/tools/redmod/tweaks/base/gameplay/static_data/database/ui/world_map/world_map.tweak:454-577`)
defines six zoom levels and the camera envelope:

| Level record | `zoom` (camera distance) | Reveals | Filter groups enabled |
| --- | --- | --- | --- |
| `ZoomLevelDistricts` | 11000 | district borders | Common, MainQuest, DogtownGate |
| `ZoomLevelSubDistricts` | 7000 | subdistrict borders | + Quest, CyberPsycho, Courier, WorldEncounter |
| `ZoomLevelImportant` | 4500 | important pins | + ApartmentToPurchase, Tarot |
| `ZoomLevelVendors` | 3500 | vendors | + Ripperdoc, Glamdoc, RelicDevice |
| `ZoomLevelAllMappins` | 2500 | all pins | + FastTravel, DropPoint |
| `ZoomLevelExtraMappins` | 1000 | street level | + Autofixer, Vendor, Exploration |

Every level inherits `BaseZoomLevel { rotation = (0, -85, 0); fov = 25 }`, i.e.
**5 degrees of tilt from straight down, 25 degree FOV, north-up**. The TopDown
camera mode allows pitch from -75 to -89 and sets `rotationSpeed = (0,0,0)`, so
vanilla 2.5 does **not** let the player rotate the map; mods such as *Map Street
View* and *3D World Map Explorer* re-enable `RotateYaw`/`RotatePitch`, so a
robust design must tolerate yaw and up to ~15 degrees of tilt.

The map's playable extents are given in **world units**:

```text
cursorBoundaryMin = (-5500, -7300)
cursorBoundaryMax = ( 6050,  5000)
```

These bounds are the natural coordinate frame for sub-territory polygons and the
validation envelope for `data/` seeds.

`WorldMapMenuGameController.GetCurrentZoom() -> Float` is a `protected final
native` getter (`worldMap.swift:216`). A mod can expose it without Codeware:

```redscript
@addMethod(WorldMapMenuGameController)
public final func NA_CurrentZoom() -> Float {
  return this.GetCurrentZoom();
}
```

This exact pattern is used by the shipping redscript-only *Map Street View* mod.
There is **no** script getter for camera yaw, pitch, or world position; that mod
tracks yaw/pitch itself by intercepting its own rotate commands.

### 1.3 District borders and `WorldMapDistrictLogicController`

`WorldMapDistrictLogicController` (`worldMap.swift:1830-1874`) is a small label
controller:

- `record: wref<District_Record>`, `type: gamedataDistrict`, `iconWidget:
  inkImageRef`, `selected: Bool`.
- `OnInitDistrict()` sets the root widget state from
  `District_Record.UiState()` and the icon from `UiIcon()`. Subdistricts copy
  the parent district's state and hide the icon.
- `OnSetSelected()` plays `OnSelectDistrict` / `OnDeselectDistrict`.

The `DistrictOutline` library item in `world_map.inkwidget` contains a canvas
named `District`, an `inkLinePatternWidget` named `path` and an `inkImageWidget`
named `icon` (district icon). It is a **map label**, not a border polygon.

The border toggles are the zoom-level flags `showDistricts` / `showSubDistricts`
(`world_map.tweak:460-484`), and `WorldMapMenuGameController` only plays ink
animations for the label containers when the view changes
(`OnDistrictViewChanged` -> `OnShowDistricts` / `OnShowSubDistricts`,
`worldMap.swift:613-631`). Hovering a district updates the name panel and the
"leading gangs" list (`OnUpdateHoveredDistricts`, `worldMap.swift:633-652`).

**Therefore:** there is no supported way to colour, subdivide, or convert the
vanilla district borders into faction territory. Any sub-territory visual must be
drawn by us (A/B/C) or represented by pins (D).

The vanilla district tree is useful for planning only. From
`<game>/tools/redmod/tweaks/base/gameplay/static_data/database/fasttravel/districts.tweak`,
the six city districts have 16 direct subdistricts:

| District | Vanilla subdistricts |
| --- | --- |
| Watson | Arasaka Waterfront, Kabuki, Little China, Northside |
| Westbrook | Charter Hill, Japantown, North Oaks |
| City Center | Corpo Plaza, Downtown |
| Heywood | The Glen, Vista del Rey, Wellsprings |
| Santo Domingo | Arroyo, Rancho Coronado |
| Pacifica | Coastview, West Wind Estate |
| Dogtown (PL) | Worldmap Sub |

`~5 control centers per major district` is finer than the vanilla subdistrict
grid in most districts (and can cross vanilla subdistrict lines). Do not try to
derive our partition from vanilla subdistricts; author or generate it (section 5).

### 1.4 Mappins: the only first-class, scriptable map primitive

`MappinSystem` (`refs/cyberpunk/orphans.swift:18464-18490`) is the sanctioned
extension point:

```redscript
RegisterMappin(data: MappinData, position: Vector4) -> NewMappinID
RegisterMappinWithObject(data, object, opt slotName, opt offset) -> NewMappinID
SetMappinActive(id, active) / SetMappinPosition(id, position)
SetMappinScriptData(id, scriptData) / SetMappinDebugCaption(id, caption)
ChangeMappinVariant(id, variant) / UnregisterMappin(id)
```

`MappinData` has exactly six fields (`orphans.swift:18447`):

```redscript
mappinType: TweakDBID, variant: gamedataMappinVariant, active: Bool,
debugCaption: String, visibleThroughWalls: Bool, scriptData: ref<MappinScriptData>
```

`mappinType` points at a TweakDB `MappinDefinition`, which controls **where** the
pin may appear (`ShowOnMinimap`, `ShowOnMap`, `ShowInWorld`,
`VisibilityRange`, `PossibleVariants`; `orphans.swift:16381-16390`,
`base/gameplay/static_data/database/mappins/mappins.tweak`).

The runtime UI path is:

```text
MappinSystem
  -> MappinsGroup_Record (groupName/widgetState; world_map.tweak:348-436)
  -> MappinUIFilterGroup_Record (which variants a filter toggles)
  -> WorldMapZoomLevel_Record.mappinFilterGroups (which filters exist per zoom)
  -> MappinsContainerController.CreateMappinUIProfile(...)   <- scripted hook point
  -> BaseWorldMapMappinController + an inkwidget from MappinUIProfile
```

Two facts make this path unusually friendly:

1. `WorldMapMenuGameController.CreateMappinUIProfile` is a **scripted** method
   (`public func`, not `native`) at `worldMap.swift:1433-1441`. It currently
   returns the same widget for every map mappin. It can be wrapped.
2. `MapMappinUIProfile.Default`
   (`base/gameplay/static_data/database/ui/mappin_ui/mappin_ui_runtime_profiles_map.tweak:4-15`)
   disables screen clamping (`clampX = clampY = false`), marks all five tiers
   visible, disables distance scaling, and uses
   `MappinUISpawnProfile.Always`. Together with a variant that belongs to an
   always-enabled filter group, map pins exist at every zoom level; because
   clamping is off, their widget positions should remain valid when off-screen
   (verify in P9).

Filter visibility is the real gate. Our dots must remain visible at
`ZoomLevelDistricts` (the default "zoomed all the way out" view), where only
`CommonFilterGroup`, `MainQuestFilterGroup` and `DogtownGateFilterGroup` are
active (`world_map.tweak:460-471`). `Mappins.DefaultQuestVariant` and
`Mappins.PointOfInterest_ExclamationMarkVariant` are members of
`WorldMap.MainQuestFilterGroup`, so a dot using `DefaultQuestVariant` is visible
at **all six** zoom levels. `OutpostVariant`, `MinorActivityVariant`, etc. live
in `StoryFilterGroup` and would vanish when zoomed out.

Two hard limits:

- **`gamedataMappinVariant` is a compiled enum.** A TweakDB `MappinVariant`
  record only names an existing enum value; TweakXL cannot add a new variant.
  Reuse a vanilla variant.
- **`MappinScriptData` is `importOnly`** (REDnode's 2.5 type dump; orphans
  `20593`). The safe payload strategy is a registry keyed by
  `NewMappinID.value: Uint64`; `data.debugCaption` can carry a human-readable
  name. Do not build the view on a custom `MappinScriptData` subclass unless a
  spike proves redscript 1.x permits it.

Hook points that are scripted and can be wrapped without Codeware:

| Class.method | File | Use |
| --- | --- | --- |
| `WorldMapMenuGameController.CreateMappinUIProfile` | `worldMap.swift:1433` | choose a custom mappin widget/profile |
| `BaseWorldMapMappinController.UpdateIcon` | `worldMap.swift:1670` | per-faction tint, cached; runs on every mappin update |
| `BaseWorldMapMappinController.UpdateVisibility` | `worldMap.swift:1648` | force visibility if a filter fights us |
| `WorldMapTooltipController.SetData` | `worldMapTooltips.swift:223` | replace title/description for our pins |
| `WorldMapMenuGameController.OnEntityAttached/OnEntityDetached` | `worldMap.swift:490/529` | create/destroy a map overlay |
| `WorldMapMenuGameController.OnZoomLevelChanged/OnZoomTransitionFinished` | `worldMap.swift:542/548` | invalidate a projection |
| `WorldMapMenuGameController.OnAxisInput/OnRelativeInput` | `worldMap.swift:990+` | mark a pan dirty |
| `BaseMappinBaseController.GetMappin/GetRootWidget` | `mappinsControllers.swift:14,95` | identify a pin, read its screen position |

---

## 2. Options, in detail

### Option D — Control-center dots via vanilla `MappinSystem` (ship this first)

**Mechanism.** One mappin per control center, registered from redscript at a real
world position (the sub-territory anchor from `data/`). The pin is map-only
because we add a dedicated `MappinDefinition`; ownership is expressed as a tint
on the vanilla pin icon; hovering shows our own tooltip.

**TweakDB (TweakXL `.tweak` text, `src/r6/tweaks/`):**

```text
package NeonAscendancy
using RTDB

ControlCenterMappin : MappinDefinition
{
    showOnMinimap = false;   // no clutter on the minimap or HUD
    showOnMap = true;
    showInWorld = false;
    visibilityRange = 0;
    possibleVariants = [ "Mappins.DefaultQuestVariant" ];
}
```

`DefaultQuestVariant` is chosen because it belongs to `MainQuestFilterGroup`
(visible at every zoom) and has no side effects that require a journal entry.
The vanilla map will treat it as a selectable pin; left-click may track it, which
is arguably a useful free behaviour (set a route to a control center) rather than
a bug — decide in P7.

**Registration (redscript sketch):**

```redscript
let data: MappinData;
data.mappinType = t"NeonAscendancy.ControlCenterMappin";
data.variant = gamedataMappinVariant.DefaultQuestVariant;
data.active = true;
data.visibleThroughWalls = true;
data.debugCaption = subTerritoryName;      // caption carried by the pin (see note)
let id: NewMappinID = GameInstance.GetMappinSystem(game)
    .RegisterMappin(data, new Vector4(x, y, z, 1.0));
```

Store `id.value` in the territory view state; re-register on load (runtime
mappins are not save-persistent). Suppress minimap/HUD copies with
`ShowOnMinimap/ShowInWorld = false`.

`debugCaption` is the only string field on `MappinData` in this build
(`orphans.swift:18447`; the 2.5 REDnode dump additionally lists
`localizedCaption`, which the decompiled 2.5 scripts do not show). Treat it as a
dev caption and render the player-facing name from our own registry in the
tooltip and overlay labels; do not assume vanilla will display it.

**Ownership tint.** Wrap `UpdateIcon` and set the icon tint only when the owner
changed (a per-controller cached faction id):

```redscript
@addField(BaseWorldMapMappinController)
private let m_naCachedFaction: Int32 = -1;

@wrapMethod(BaseWorldMapMappinController)
protected func UpdateIcon() -> Void {
  wrappedMethod();
  let faction: Int32 = NAMapView.GetFactionForMappin(this.GetMappin().GetNewMappinID());
  if faction >= 0 && faction != this.m_naCachedFaction {
    this.m_naCachedFaction = faction;
    inkWidgetRef.Get(this.iconWidget).SetTintColor(NAFactions.DotColor(faction));
  }
}
```

`iconWidget` is a `protected` field on `BaseMappinBaseController`
(`mappinsControllers.swift:4`), so a wrapper in the derived class can reach it.
`inkWidget.SetTintColor(HDRColor)` is public
(`core/ui/baseWidgets/abstractWidgets.swift:145`).

**Tooltip.** Wrap `WorldMapTooltipController.SetData`; after `wrappedMethod`,
if the mappin id belongs to us, overwrite `m_titleText` (sub-territory name) and
`m_descText` (owner, income, contest state) and hide the gig/threat/travel panels
that vanilla set. `m_titleText`/`m_descText` are `protected edit` refs
(`worldMapTooltips.swift:171-177`). This is the only way to get real content:
vanilla falls back to generic strings from `MappinUIUtils.MappinToString`
(`worldMapTooltips.swift:444-449`).

**Cost.** ~40-60 extra native pins on top of a vanilla map that public
extraction reports at ~700 POIs and ~4,300 quest markers. Their widgets are
native-projected; the only script work is one cached
tint compare per pin per update, and tooltip text on hover. This is firmly inside
the "near-zero overhead" budget in `docs/architecture.md`.

**Limits.**
- The icon is a vanilla atlas part; faction identity is colour, not a bespoke
  glyph. A custom glyph needs a custom mappin `inkwidget` + atlas (small
  ArchiveXL asset) and a wrapped `CreateMappinUIProfile`; add it in `v0.1.x` only
  if colour proves insufficient.
- Pins are filtered by the "Jobs" checkbox (`MainQuestFilterGroup`). Turning that
  filter off hides territory pins. A dedicated filter group is possible with
  TweakXL, but `gamedataWorldMapFilter` has a fixed, contended set of custom
  slots (the *Custom Map Filters Panel* mod documents the collisions), so this is
  not worth it before `v0.2.0`.
- Pins do not show territory *extent*. Fill that gap with D+ or A.

### Option D+ — Mappin-anchored influence ring (cheap stopgap)

Reparent one `inkShape` (a circle/stroke, `shapeVariant = Border`) as a **child
of the control-center mappin's root widget**, centred on the pin. The pin's
native projection positions the ring for free; the only per-zoom work is setting
its size from a scalar `pixels-per-world-unit`, derived from
`GetCurrentZoom()` and the TweakDB FOV, or from two anchor pins.

- Pros: perfect pin alignment, no homography, one scalar update per zoom step,
  no per-frame work while the camera is still.
- Cons: circles are not a partition; overlapping influence radii can look messy.
- Verdict: good `v0.1.0` visual if the polygon spike slips; prototype with D.

### Option A — Screen-space vector overlay (`inkShape` layer) — the Stellaris look

**Mechanism.** Create one `inkShape` per sub-territory, inside the map preview
canvas, and set its polygon vertices to the **screen projection** of the
sub-territory polygon each time the camera changes. Fills use the widget tint
plus `fillOpacity`; borders use `borderColor` / `borderOpacity` /
`lineThickness` / `jointStyle`. `inkShape` is a real imported class with public
fields (`orphans.swift:52430-52448`):

```redscript
shape.shapeVariant = inkEShapeVariant.FillAndBorder;
shape.fillOpacity  = 0.18;      // faction tint, low alpha
shape.borderOpacity = 0.90;
shape.lineThickness = 2.0;      // pixels, crisp
shape.jointStyle    = inkEJointStyle.MITER;
shape.borderColor   = NA.White;
shape.vertexList    = projectedPoints;   // local pixel coords
```

`inkShape` is constructed and reparented like any other ink widget; the
redscript-only *Map Street View* mod proves that `new inkRectangle()` /
`new inkText()` + `Reparent(root)` works without Codeware, and the same pattern
applies to `new inkShape()`.

**Where it goes.** `GetEntityPreview().GetRootWidget()` is the `EntityPreview`
canvas that contains `MapImage`. Reparent the shapes there (after `MapImage`).
Z-order is then: map render < territory fills/borders < GPS route < district
labels < mappins < HUD. Coordinates are the same layer space the native mappin
projection uses.

**Projection.** There is no script API for the map camera matrix. Derive the
world-plane -> screen mapping from **four anchor mappins** registered at known
world coordinates (the map bounds corners are a natural choice). Because
`MapMappinUIProfile.Default` disables clamping, an anchor *should* keep a valid
projected position even when it is off-screen (P9 verifies this); read them from
a wrapped `UpdateIcon`:

```redscript
let p: Vector2 = WidgetUtils.LocalToGlobal(this.GetRootWidget());
// store p in the anchor table keyed by mappin id
```

`WidgetUtils.LocalToGlobal(widget, opt localOffset) -> Vector2`
(`orphans.swift:40647`) is public. A projection of a world plane under a
perspective camera is a **homography**. From four anchors (world `(u,v)` in the
map rectangle -> screen quad `p00,p10,p11,p01`) compute the 3x3 matrix once per
camera change (closed form, Appendix B), then transform each polygon vertex.
This is exact for the ground plane even under modded yaw/tilt, and it makes the
overlay agree with the game's own pins by construction.

If anchor positions turn out to be unreliable when far off-screen, fall back to:
1. on-screen anchors only (pick the four nearest visible pins), or
2. known camera math: `pixelsPerUnit = viewportHalfHeight / (zoom *
   tan(fov/2))`, yaw/pitch from the active `WorldMapZoomLevel_Record` (and from
   tracked deltas when a rotation mod is installed), translation from one anchor.

**Update policy (this is what keeps it cheap):**

- On map open (`OnEntityAttached`): build the shape widgets once, build the
  homography from the anchors, project all polygons once.
- On pan (`OnAxisInput`/`OnRelativeInput`): do **not** re-tessellate. Move a
  single parent canvas or add a per-shape margin delta computed from one anchor.
  Perspective change from translation at 5 degrees of tilt is sub-pixel over a
  pan step.
- On zoom level change / transition finished, and whenever an anchor moves more
  than an epsilon from its predicted position (rotation mods): recompute the
  homography and re-project vertices.
- On `TerritoryOwnerChanged`: update fill tint/border colour/opacity only
  (no geometry).
- Steady state: zero script work.

A per-frame tick is available without Codeware if needed, via a 1 ms ink
animation re-armed on `OnFinish` (the exact pattern in *Map Street View*; game
time is frozen in the menu, so the delay system is not usable). Prefer the
event-driven policy; use the ticker only while a transition/rotation is active.

**Geometry budget.** ~30-40 city sub-territories, simplified to <= 12-16
vertices each = ~500 points. Re-projecting 500 points with a homography is a few
thousand float operations; the real cost is assigning `vertexList` arrays (one
array copy per shape) while the camera moves. Keep polygons lean, coalesce all
shapes into one parent canvas so panning is a single transform, and re-project
only during transitions. A 30 Hz re-projection (every other frame) is acceptable
for an abstract overlay and halves the cost if needed.

**Authoring.** Polygons are authored/generated offline in world XY inside the
`cursorBoundary` rectangle; no ink assets are required for the shapes. Optional
per-territory label text (`inkText`) can be added later and positioned with the
same homography, shown only at `ZoomLevelSubDistricts` and closer.

**Risks (all spike-able).**
1. **Runtime `vertexList` updates**: every shipped `inkShapeWidget` has a
   `shapeResource` + a cached `vertexList`; no vanilla asset exercises a
   runtime-only polygon. If assigning `vertexList` does not invalidate the shape,
   fall back to (a) one authored `.inkshapecollection` preset per sub-territory
   and affine placement, or (b) pre-distorted shape sets per zoom level. This is
   the single highest-risk item in A.
2. **Anchor reliability off-screen** (see above).
3. **Layer scale**: the authored sizes are 1920x1080 but the ink layer may
   stretch to 3840x2160; derive the preview->global scale from two
   `LocalToGlobal` probes instead of hard-coding 1920x1080.
4. **Compatibility**: recolour/map-control mods are fine; a mod that replaces
   the whole world map menu or hooks the same controllers can compose or need a
   load-order note. Our shapes are additive.

**Verdict.** This is the right "polished" path: pure redscript, no Codeware, no
overwriting game assets, event-driven cost. Gate it behind the `vertexList` and
anchor spikes.

### Option B — 3D overlay in the map's own scene (mesh / injected entity)

**Idea.** Put transparent faction polygons and border strips into the 3D
hologram scene so tilt/pan/zoom apply natively and buildings occlude correctly.

**What is actually possible.** ArchiveXL can patch `.ent` / `.app` `components`
(and `appearances`, `entity`, `visualTags`) non-destructively, and ArchiveXL is
already pinned. The map's scene/camera template is
`base\entities\cameras\3dmap\3dmap_view.ent`; the map's geometry is the
hologram model (terrain meshes + building instances encoded in
`districts_data.xbm`), not a normal streamed world. So the plausible route is to
patch the map's view/scene template with an extra mesh component, or to spawn a
map-only entity.

**Why it is not the recommendation.**
- **Authoring cost**: polygons must be modelled in the map model's space and
  kept aligned with map edits. This is Blender + WolvenKit work for every border
  change, versus a text polygon in `data/`.
- **Runtime recolouring is unresolved**: ownership changes must swap appearance /
  material / chunk mask on an entity that is instantiated natively by the preview
  controller. Redscript can set mesh appearance on an entity it holds
  (`GameObject.SetMeshAppearanceEvent`, `deviceBase.SetMeshAppearance`), but
  nothing in the exposed API hands us the map scene entity. Pre-authoring one
  appearance per faction and swapping it requires that handle; otherwise the map
  would be static until reopened.
- **Compatibility**: injecting components into `3dmap_view.ent` conflicts with
  map overhaul mods (3D World Map Fixed, Realistic Map 3D, camera mods), which
  are exactly the mods our players will run.
- **Alignment does not come for free anyway**: the hologram has metre-scale
  placement errors relative to the real world (3D World Map Fixed moves whole
  districts by ~5 m), so "perfect by construction" is only true relative to the
  hologram, not to the gameplay coordinates used by spawns and missions.

**Verdict.** Do not schedule. If A's `vertexList` spike fails *and* alignment
proves unacceptable, spend one bounded spike asking whether
`3dmap_view.ent` components can be patched and driven at runtime. Record the
answer either way.

### Option B2 — Native render-target compositing (RED4ext, future)

A native plugin could hook the map's render pass and draw world-space polygons
into `world_map_texture.dtex`/the same target with the map camera's matrices.
This is the technically ideal outcome (native performance, perfect perspective,
building occlusion), but it is engine-internals work with high patch fragility,
and it assumes the native core from Step 0.3 exists. Not before `v0.2.0`; not
needed for the design gate.

### Option C — DX12 / ImGui / CET overlay

Reject for the shipping product:

- CET is a developer tool, absent from the pinned stack, and a heavy user-facing
  dependency for a gameplay mod.
- There is no published map camera matrix; the projection would be
  reverse-engineered on top of a reverse-engineered render hook.
- Drawing over the game's swapchain bypasses ink composition (vignette, letterbox,
  HDR/tonemap, screenshots) and duplicates input handling and localization.
- The overlay would have to be re-verified every game patch, for no visual gain
  over A.

CET remains fine for dev-time inspection and console experiments.

---

## 3. Comparison

Scored for Neon Ascendancy's actual constraints (Codeware-free, near-zero
per-frame cost, pre-partitioned readability, low compatibility risk).

| Criterion | A ink overlay | B 3D scene | C native/ImGui | D mappins |
| --- | --- | --- | --- | --- |
| Alignment with pan/zoom | Exact with anchors; affine fallback ~1-2 % | Exact | Exact | Native exact |
| Alignment with modded tilt/rotation | Homography handles it | Exact | Exact | Exact |
| Faction fill + crisp border | Yes (fill + stroke) | Yes | Yes | No (dots only) |
| Ownership recolour at runtime | O(1) field writes | Unresolved | Yes | O(1) tint |
| Authoring | Text polygons (`data/`) | Blender/WolvenKit + scene patch | Native code | Coordinates only |
| Per-frame cost | Zero idle; bounded during camera motion | Zero | Native | Native |
| Codeware-free | Yes | Yes (asset side) | No (CET) | Yes |
| Conflict surface | Low (additive UI) | High (map assets) | High | Low |
| Failure mode | Misalignment / no re-tessellation | Invisible/static overlay, patch breakage | Crash/black overlay | None |
| Time to first value | Days | Weeks | Weeks-months | Hours |

A note on why A wins over B for our use case: the overlay is an **abstraction
layer** (ownership), not geography. Drawing it above buildings and below labels
is a feature, not a limitation; Stellaris-style borders are meant to be read as
UI. B's only real advantage is occlusion, which we do not want for territory
fills.

---

## 4. Recommendation and phased plan

### `v0.1.0` — ownership legibility (Option D, plus D+ if it spikes clean)

1. **Map-only control-center pins** for the initial sub-territories (start with
   the player's district and one rival district, not all of Night City):
   - TweakXL `MappinDefinition` (`showOnMinimap=false`, `showInWorld=false`,
     `showOnMap=true`, variant `DefaultQuestVariant`).
   - Register on map open / session ready; registry keyed by `NewMappinID.value`.
   - `debugCaption` = sub-territory id, for debugging only; the player-facing
     name lives in our registry and is rendered by the tooltip.
2. **Ownership tint** in a wrapped `BaseWorldMapMappinController.UpdateIcon`,
   cached per pin; faction colours from `data/`.
3. **Custom tooltip** via a wrapped `WorldMapTooltipController.SetData`:
   sub-territory name, owner, income/upkeep, contest state.
4. **Immediate ownership flip**: the `TerritoryOwnerChanged` view diff updates the
   registry; the tint follows on the next mappin update (same frame or next).
   No mappin re-registration needed.
5. **Optional D+ influence ring** if the spike passes: a stroked circle child of
   each pin, radius = influence radius, scaled by `GetCurrentZoom()`/FOV.
6. **Debug-only on-screen text** (an `inkText` created and reparented like
   *Map Street View*'s debug panel) to show pin count, current zoom, and
   projection error during the spike. No CET required.

Acceptance: opening the map shows exactly one dot per control center at every
zoom level; dots are invisible on the minimap/HUD; tint flips within one frame of
an ownership change; tooltip is correct after reload; frame time delta while the
map is open is within noise.

### `v0.2.0` — polished pre-partitioned borders (Option A)

1. Author/generate the full partition (section 5) and simplify polygons.
2. Create the overlay layer in `EntityPreview`; build 4 anchor pins; implement
   the homography and reprojection policy.
3. Add fills + borders, ownership recolour, optional labels at
   `ZoomLevelSubDistricts` and closer.
4. Add a display toggle (keybind or a small toggle in our own UI); do not fight
   the vanilla filter system.
5. Re-run the prototype checks, especially frame cost during a full pan/zoom
   sweep and the modded-rotation case.

### Later, only if A fails its gate

- Spike B (map-scene injection + runtime appearance) or B2 (native compositing).
- Do not ship C.

---

## 5. Data and integration design

### 5.1 Sub-territory geometry

Store in `data/` as human-readable seeds, compiled into `world.db` by the
Step 0.4 generator:

```text
sub_territories(
  id, district_id, name_key,
  center_x, center_y, center_z,          -- control-center NPC hub (spawn anchor)
  polygon: [[x,y], ...],                 -- world XY, closed, CCW, <= 16 pts
  faction_id, base_income, base_heat,
  influence_radius                        -- optional D+ ring
)
```

Rules:
- Coordinates are **world XY**, validated inside `[-5500, 6050] x [-7300, 5000]`
  and inside the parent district polygon.
- Polygons form a **planar partition**: shared edges use identical vertices, no
  overlaps, no gaps. Generate cells (Voronoi/cost-distance around control
  centres), clip to district boundaries, then simplify with a
  Ramer-Douglas-Peucker pass that preserves shared edges.
- Z is a single ground-plane value per sub-territory (or per district) for the
  overlay. Borders are an abstraction; they do not need to follow terrain.
- District polygons must be acquired once (extract the map's district border
  geometry with WolvenKit/Blender, or trace from the map at a known zoom with
  the anchor calibration) and checked into `data/` as reference geometry.

### 5.2 View pipeline (no per-frame database access)

```text
native sim  --SimEvent(TerritoryOwnerChanged)-->  redscript view adapter
                                                   |
                                    update in-memory ViewState (owner/color)
                                                   |
                    +------------------------------+-----------------------------+
                    |                                                            |
        mappin registry (tint next frame)                       overlay shapes (recolour O(1))
```

- The view adapter keeps a dense array of sub-territories with owner and colour;
  no SQL, no scans, no allocations on the render path.
- `TerritoryOwnerChanged` is the only event that touches colours; `OnEntityAttached`
  is the only event that builds geometry.
- On save/load, the view rebuilds from the native snapshot and re-registers pins;
  registration is idempotent (unregister old ids, register once).
- Mappin ids are runtime-only: never persist them; persist sub-territory ids and
  derive pin ids.

### 5.3 Map lifecycle

- `OnEntityAttached`: build overlay + register pins/anchors (or reuse persistent
  pins if they survive map close; verify).
- `OnEntityDetached` / `OnUninitialize`: drop widget refs, stop the ticker, keep
  or unregister pins according to the spike result.
- If pins persist while the map is closed, that is fine: `showOnMap` only and
  `showOnMinimap=false` keep them out of the HUD.
- Do not register pins before the world/player exists; use the same
  session-ready hook as the rest of the mod.

---

## 6. Performance budget and guardrails

- **Pins**: 40-60 native pins; one cached tint compare per pin per UI update.
  Below measurement noise relative to vanilla's thousands of mappins.
- **Overlay**: zero script cost while the camera is still. During a pan, a single
  transform; during a zoom transition or rotation, <= ~500 point projections.
  No per-frame allocations in steady state; do not rebuild widgets on ownership
  change.
- **Hard rules**: no SQLite or world scans on the UI thread; no `ArrayPush` in a
  per-frame loop; no `vertexList` rebuild when only colours changed; no per-frame
  `GetMappins` enumeration (cache widget refs).
- **Measurement**: on-screen frame-time text (ink) or CET profiler during dev;
  record p50/p99 frame time with the map open, idle and during a full
  zoom-out -> zoom-in sweep, with and without the overlay. Gate A on "indistinguishable
  from vanilla within 0.2 ms p99 on the dev machine".

---

## 7. Prototype checks (in-game, ordered)

Run these as a throwaway dev mod, not as product code. Use on-screen ink debug
text (CET is not installed); log only through a dev logger.

| # | Check | Steps | Pass criteria |
| --- | --- | --- | --- |
| P0 | Baseline map health | Boot, open map, pan/zoom all six levels | No script errors; note vanilla frame time |
| P1 | TweakXL mappin definition | Add `NeonAscendancy.ControlCenterMappin`; `TDBID.Create` + `GetMappinDefinitionRecord` returns it | Record resolves; no TweakDB errors |
| P2 | Map-only pin | Register one pin at a known fast-travel terminal; open map; open minimap | Pin appears exactly on the terminal on the map; absent on minimap/HUD |
| P3 | Zoom-level visibility | Zoom through all six levels | Pin visible at every level (not filtered out at `ZoomLevelDistricts`) |
| P4 | Ownership tint | Wrap `UpdateIcon`; flip a test faction id at runtime | Icon colour changes within one frame; no per-frame tint churn (log change count) |
| P5 | Tooltip | Wrap `WorldMapTooltipController.SetData`; hover the pin | Our title/description; no vanilla gig/threat/fast-travel leftovers |
| P6 | Reload idempotency | Save, reload, reopen map twice | Exactly one pin per center (no duplicates); tooltip intact |
| P7 | Selection/tracking side effects | Click/hover our pin; track it | No crash; decide whether tracking is acceptable; if not, suppress it |
| P8 | Preview canvas access | From `OnEntityAttached`, `GetEntityPreview().GetRootWidget()`; reparent a red 200x200 `inkShape`/`inkRectangle` | Shape renders above the map, below GPS/labels/pins; correct position/scale at 1080p and 4K |
| P9 | Anchor pin projection | Register 4 pins at the map-bound corners; log their `LocalToGlobal` positions; compare with expected screen corners at each zoom level | Positions are finite and consistent; off-screen anchors still valid |
| P10 | Homography accuracy | Draw a crosshair at a known world point from the H (not a pin); compare with a pin at the same point | <= 2 px error at screen centre and corners, all six levels |
| P11 | `vertexList` mutation | One `inkShape`; change `vertexList` at runtime between two quads | Shape re-tessellates. If not, test `SetShapeResource` + `ChangeShape` per zoom, then the affine fallback |
| P12 | Full overlay cost | 40 shapes; full pan/zoom sweep; rotation mod (Map Street View) | No visible lag; p99 within budget; no per-frame array growth |
| P13 | Modded rotation/tilt | With Map Street View active, rotate/tilt and pan | Borders stay attached; H recomputes; no drift |
| P14 | Compatibility | Map Street View, 3D World Map Explorer, Preem Map, 3D World Map Fixed, Custom Map Filters Panel | No crashes; our pins/overlay still correct; note any filter collisions |
| P15 | D+ ring (optional) | Reparent a stroked circle into a pin root; zoom | Ring centred on pin; radius tracks zoom; does not inherit unwanted pin animations |

Gate for A: P9, P10, P11 and P12 must pass. If P11 fails, A is downgraded to
"pre-authored shape presets + affine", which is still shippable if P10's error at
screen corners is <= ~6 px.

---

## 8. Open questions and decision gates

1. **`vertexList` runtime mutation** — the make-or-break for cheap exact polygons.
   If it fails, either author per-zoom shape sets (more data, more memory) or
   accept an affine overlay.
2. **Off-screen anchor validity** — determines whether a fixed 4-corner
   homography works at every zoom, or whether anchors must be adaptive.
3. **Whether mappin widgets persist across map close** — affects lifecycle
   complexity, not the design.
4. **Vanilla subdistrict borders vs our partition** — decide whether to align
   geometry where possible for player familiarity, knowing the borders cannot be
   recoloured.
5. **Filter UX** — accept the "Jobs" checkbox coupling in `v0.1.0`, or spend a
   TweakXL custom-filter slot later (contentious; see Custom Map Filters Panel).
6. **Bounded B spike** — only if A fails; success criterion is a runtime
   appearance swap on the map scene entity, not "a mesh appears once".

Per the repo's engineering rules: if two attempts at the anchor projection fail,
stop and write down the assumption before patching again. The likely wrong
assumption would be "mappin widget positions are the camera projection"; the
fallback is to read the camera/view entity from native code (B2), not to keep
adding fudge factors.

---

## Appendix A — Evidence index

Local (gitignored) references:

- `refs/cyberpunk/cyberpunk/UI/fullscreen/map/worldMap.swift`
  - `:2` class hierarchy; `:220-258` `OnInitialize`; `:490-519`
    `OnEntityAttached`; `:542-584` zoom callbacks; `:613-652` district view and
    hover; `:1433-1441` `CreateMappinUIProfile`; `:1585-1808`
    `BaseWorldMapMappinController`; `:1648-1684` visibility/icon; `:1830-1874`
    `WorldMapDistrictLogicController`; `:216` `GetCurrentZoom`.
- `refs/cyberpunk/cyberpunk/UI/fullscreen/map/worldMapTooltips.swift`
  - `:2-114` tooltip container; `:116-167` base tooltip; `:169-523`
    `WorldMapTooltipController.SetData` (title fallbacks at `:444-449`).
- `refs/cyberpunk/cyberpunk/UI/mappins/*.swift`
  - `mappinsContainers.swift:2-15` `MappinsContainerController`;
    `:43-139` `WorldMappinsContainerController`.
  - `mappinsControllers.swift:2-110` `BaseMappinBaseController`.
  - `mappinUtils.swift:2-21` `MappinUtils`; `:23-239` `MappinUIUtils`
    (variant -> texture/colour/string).
  - `questMappins.swift:1-120` `QuestMappinController` (display name, icon).
- `refs/cyberpunk/orphans.swift`
  - `:18447-18490` `MappinData` / `MappinSystem`; `:29474` `NewMappinID`;
    `:45481-45516` `IMappin`; `:46730` `MappinControllerCustomData`;
    `:52294-52297` `inkLinePattern.AddVertex`; `:52430-52448` `inkShape`;
    `:54961-54975` `inkWorldMapPreviewGameController`; `:55053-55090`
    `WorldMapSettings_Record`; `:67577-67605` `WorldMapZoomLevel_Record`;
    `:16381-16424` `MappinDefinition` / `MappinUIRuntimeProfile`;
    `:40647` `WidgetUtils.LocalToGlobal`; `:68286` `GetScreenPosition`.
- `refs/cyberpunk/core/ui/baseWidgets/abstractWidgets.swift:1-260`
  - runtime widget creation/reparent, `SetTintColor`, `SetScale/SetShear/
    SetRotation/SetTranslation`, `SetSize`, `SetOpacity`.
- `refs/cyberpunk/core/ui/baseControllers/hudGameController.swift:114`
  - `inkProjectedHUDGameController`.

Game install (machine-local):

- `<game>/tools/redmod/tweaks/base/gameplay/static_data/database/ui/world_map/world_map.tweak`
  - `:4-112` filters; `:114-346` filter groups; `:348-436` mappin groups;
    `:438-451` quick/custom filter lists; `:454-528` zoom levels; `:530-577`
    camera settings and cursor bounds.
- `<game>/tools/redmod/tweaks/base/gameplay/static_data/database/ui/mappin_ui/mappin_ui_runtime_profiles_map.tweak`
  - `MapMappinUIProfile.Default` (no clamping, all tiers, no distance scaling).
- `<game>/tools/redmod/tweaks/base/gameplay/static_data/database/ui/mappin_ui/mappin_ui_spawn_profiles.tweak`
  - `Always`, `ShortRange`, etc.
- `<game>/tools/redmod/tweaks/base/gameplay/static_data/database/mappins/mappins.tweak`
  - `DefaultStaticMappin`, `showOnMinimap/Map/World` semantics.
- `<game>/tools/redmod/tweaks/base/gameplay/static_data/database/fasttravel/districts.tweak`
  - district/subdistrict tree (`parentDistrict`).

Ink resource database (2.5, external): `base\gameplay\gui\fullscreen\world_map\world_map.inkwidget`
items `Root` (`gameuiWorldMapMenuGameController`), `EntityPreview`
(`gameuiWorldMapPreviewGameController`), `DistrictOutline`, `GroupOutline`,
`MappinOutline`; `world_map_atlas.inkatlas` part `map` bound to
`world_map_texture.dtex`; `Content` child order as listed in 1.1.

Public sources consulted (not authoritative for our build, but consistent):
`Map Street View` (redscript-only map rotation + per-frame ink ticker +
`@addMethod` exposing `GetCurrentZoom`), `3D World Map Explorer`, `3D World Map
Fixed`, `Realistic Map 3D`, `Map Switcher`, `Preem Map`, `Custom Map Filters
Panel`, `psiberx` custom map pins gist, REDnode 2.5 type dump (`importOnly`
semantics), and the 2.5 map-extraction write-up describing `districts_data.xbm`
and `3dmap_view.ent`.

## Appendix B — Plane homography from four anchors

Map world rectangle `[x0,x1] x [y0,y1]` normalised to `u,v in [0,1]`. Four
anchor screen points: `p00` (0,0), `p10` (1,0), `p11` (1,1), `p01` (0,1).

```text
dx1 = p10.x - p11.x   dx2 = p01.x - p11.x
dx3 = p00.x - p10.x + p11.x - p01.x
dy1 = p10.y - p11.y   dy2 = p01.y - p11.y
dy3 = p00.y - p10.y + p11.y - p01.y

det = dx1*dy2 - dx2*dy1
a13 = (dx3*dy2 - dx2*dy3) / det
a23 = (dx1*dy3 - dx3*dy1) / det

a11 = p10.x - p00.x + a13*p10.x
a21 = p01.x - p00.x + a23*p01.x
a31 = p00.x
a12 = p10.y - p00.y + a13*p10.y
a22 = p01.y - p00.y + a23*p01.y
a32 = p00.y

screen.x = (a11*u + a21*v + a31) / (a13*u + a23*v + 1)
screen.y = (a12*u + a22*v + a32) / (a13*u + a23*v + 1)
```

Degenerate quads (collinear anchors, `det ~ 0`) must be rejected; keep the last
valid homography. Convert screen coordinates into the overlay container's local
space with the same transform used for the anchors (probe two points to derive
the scale, do not assume 1920x1080).
