# Research 0.2a — Gang Factions, Districts, Sub-Territories & Control Centers

Status: research complete for structure and naming; **coordinates deliberately
left `TBD`** (see §8). Feeds `data/` seeds in Step 0.4 and the map overlay in
Step 0.5.

Every claim is tagged with its evidence level:

| Tag | Meaning | Trust |
| --- | --- | --- |
| `[enum]` | Identifier verified in `refs/cyberpunk` (enum member, script symbol, TweakDB record accessor) | Primary, exact |
| `[wiki]` | Curated community documentation, consistent with vanilla in-game map/UI labels | Secondary, high but not authoritative |
| `[lore]` | Story/in-game knowledge with no primary artifact in this repo | Tertiary, needs confirmation |
| `[proposal]` | Neon Ascendancy design choice — **not** a game fact | Design |

No coordinate in this document is guessed. Every `(x, y, z)` is `TBD` until
extracted per §8.

---

## 1. Verified source anchors

| Anchor | Location | What it proves |
| --- | --- | --- |
| `enum gamedataDistrict` | `refs/cyberpunk/orphans.swift:4826-4961` | 132 real district records (`Count = 132`, `Invalid = 133`). Exact enum member names for every district, sub-district and named location. |
| `enum gamedataAffiliation` | `refs/cyberpunk/orphans.swift:4474-4521` | 44 real affiliation records (`Count = 44`, `Invalid = 45`). Exact gang/corp enum names. |
| `class District_Record` | `refs/cyberpunk/orphans.swift:18392-18433` | Districts carry `Gangs()` / `GetGangsCount()` (`[wref<Affiliation_Record>]`), `ParentDistrict()`, `Type() -> gamedataDistrict`, `EnumName()`, `LocalizedName()`, `UiIcon()`, `UiState()`, `CrimeMultiplier()`, `GunShotStimRange()`, `IsQuestDistrict()`, `PreventionPreset()`. **District→gang ownership is TweakDB data, not script logic.** |
| `class Affiliation_Record` | `refs/cyberpunk/orphans.swift:29856-29875` | `Type() -> gamedataAffiliation`, `EnumName()`, `LocalizedName()`, `IconPath()`, `AnimWrappers()` — gang display name/icon source. |
| `class DistrictPreventionData_Record` | `refs/cyberpunk/orphans.swift:32827-32858` | Per-district NCPD heat tables (`Heat1..Heat5`, `Recon`), `InputLockTime`, `SpawnOriginMaxDistance`. |
| `District` / `DistrictManager` | `refs/cyberpunk/core/systems/prevention/districtManager.swift:2-195` | Runtime sub-district stack; `IsDogTown()` (56), `IsBadlands()` (68) test `Type()` **and** `ParentDistrictHandle().Type()`; `GetCrimeMultiplier()` (26). Confirms sub-district records are parented to top-level districts. |
| `PreventionSystem.GetCurrentDistrict()` | `refs/cyberpunk/core/systems/preventionSystem.swift:403` | One-call runtime query for the player's current sub-district. |
| `PreventionSystem.OnDistrictAreaEntered` | `refs/cyberpunk/core/systems/preventionSystem.swift:3053-3065` | Existing district-entry event; `m_districtMultiplier = GetCrimeMultiplier()` — free per-district heat hook. |
| `WorldMapGameController.ShowGangsInfo` | `refs/cyberpunk/cyberpunk/UI/fullscreen/map/worldMap.swift:1298-1332` | The vanilla map's gang panel reads exactly `District_Record.Gangs()`, preferring the **sub**-district record when `GetGangsCount() > 0`, else the parent. This is the authoritative "who owns this sub-district" list the player sees. |
| `WorldMapDistrictLogicController` | `refs/cyberpunk/cyberpunk/UI/fullscreen/map/worldMap.swift:1830-1871` | Sub-district rendering: `IsSubDistrict() == ParentDistrict() != null`; sub-districts inherit the parent's `UiState()`. |
| `MappinUtils.GetDistrictRecord(gamedataDistrict)` | `refs/cyberpunk/cyberpunk/UI/mappins/mappinUtils.swift:6` | Enum → `District_Record` lookup; the correct resolver for parent/district metadata. |
| `PointOfInterestMappin` | `refs/cyberpunk/orphans.swift:46770-46781` | POI mappins expose `GetCharacterRecordID()`, `IsInsideSecurityAreaTrigger()` — an anchor source for named landmarks. |
| Gang site mappin variants | `refs/cyberpunk/orphans.swift:1235` (`GangWatchVariant = 56`), `1264` (`OutpostVariant = 85`), `1288` (`SmugglersDenVariant = 109`) | Vanilla gang-occupied sites already exist as map entities — the natural control-center candidates. |

### 1.1 Two hard findings that shape the data model

1. **Do not infer hierarchy from name prefixes.** Only `Badlands_*` and
   `Dogtown_*` use prefixes. Watson's sub-districts are bare names
   (`Northside`, `Kabuki`, `LittleChina`, `ArasakaWaterfront`), as are
   Westbrook/Heywood/Santo Domingo/Pacifica/City Center's. The only reliable
   parent link is TweakDB `ParentDistrict()` — resolve it at build time via
   `MappinUtils.GetDistrictRecord()`.
2. **Gang ownership is per-record TweakDB data** (`District_Record.Gangs`), and
   the vanilla map shows the *sub*-district list when non-empty, else the
   parent's. So a sub-district can legitimately have **zero** listed gangs
   (Arasaka Waterfront, North Oak, Corpo Plaza, Downtown, Biotechnica Flats,
   Laguna Bend, Red Peaks) while still being in a district. Our seed schema must
   allow `owner_faction_id = NULL` / `owner_kind = 'corp' | 'unclaimed'`.

The exact per-district `Gangs()` arrays cannot be read from this repo: TweakDB
record IDs are hashed and the arrays are binary. They **can** be dumped at
runtime (`District_Record.Gangs()`) or offline from a TweakDB dump — see §8.3.

---

## 2. Canonical district hierarchy

### 2.1 Top-level districts — 8

| # | `gamedataDistrict` | Label | Sub-districts | Notes |
| --- | --- | --- | --- | --- |
| 1 | `Watson` (128) | Watson | 4 | Highest content density; starting district for Act 1. |
| 2 | `Westbrook` (131) | Westbrook | 3 | Tyger Claws entertainment economy. |
| 3 | `Heywood` (71) | Heywood | 3 | Valentinos heartland. |
| 4 | `SantoDomingo` (117) | Santo Domingo | 2 | Industrial; 6th Street security economy. |
| 5 | `Pacifica` (110) | Pacifica | 2 | Combat zone; no NCPD services. |
| 6 | `CityCenter` (33) | City Center | 2 | Corporate; no gangs on the vanilla gang panel. |
| 7 | `Badlands` (12) | Badlands | 18 records (15 `Badlands_*` + `NorthBadlands` + `SouthBadlands` + `MorroRock`) | Nomad/raider; `IsBadlands()` gate at `preventionSystem.swift:2429`. |
| 8 | `Dogtown` (54) | Dogtown | 6 | Phantom Liberty sovereign zone; `IsDogTown()` gate plus special map label `LocKey#10946` (`worldMap.swift:638`). |

### 2.2 Sub-districts — 40 records

`gamedataDistrict` value in parentheses. Parent is the top-level district above
(verified structurally by `ParentDistrict()`, `districtManager.swift:56-78`).
Gang column is the vanilla map panel list `[wiki]`.

**Watson (4)**

| Enum | Value | Gangs on map | Economic character |
| --- | --- | --- | --- |
| `ArasakaWaterfront` | 0 | — (corp/Arasaka security) | Corporate waterfront, docks, Konpeki Plaza |
| `Kabuki` | 82 | Tyger Claws, Maelstrom, The Mox | Black-market bazaar, unlicensed clinics |
| `LittleChina` | 88 | Tyger Claws | Dense mixed residential/commercial, merc bars |
| `Northside` | 104 | Maelstrom, The Mox, Scavengers | Derelict industry, docks, warehouses, scrapyards |

**Westbrook (3)**

| Enum | Value | Gangs on map | Economic character |
| --- | --- | --- | --- |
| `CharterHill` | 30 | Tyger Claws, 6th Street | Utilities + upscale residential/retail |
| `JapanTown` | 72 | Tyger Claws | Nightlife, casinos, dollhouses, BD studios |
| `NorthOaks` | 99 | — (corp/private security) | Wealthy hills, estates, Columbarium |

**Heywood (3)**

| Enum | Value | Gangs on map | Economic character |
| --- | --- | --- | --- |
| `Glen` | 65 | Valentinos | Mixed commercial, NCPD lab, upscale dining |
| `VistaDelRey` | 123 | Valentinos, 6th Street | Residential + street market |
| `Wellsprings` | 129 | Valentinos | Working waterfront, mall retail, tourism |

**Santo Domingo (2)**

| Enum | Value | Gangs on map | Economic character |
| --- | --- | --- | --- |
| `Arroyo` | 3 | 6th Street | Heavy industry, power, factories, junkyards |
| `RanchoCoronado` | 111 | 6th Street | Suburban worker housing, local retail |

**Pacifica (2)**

| Enum | Value | Gangs on map | Economic character |
| --- | --- | --- | --- |
| `Coastview` | 34 | Voodoo Boys, Animals | Abandoned resort: mall, pier, hotels |
| `WestWindEstate` | 130 | Voodoo Boys, Animals | Neglected housing blocks, unfinished metro |

**City Center (2)**

| Enum | Value | Gangs on map | Economic character |
| --- | --- | --- | --- |
| `CorpoPlaza` | 42 | — (Arasaka/Militech/NCPD) | Corporate HQ campus, monument plaza |
| `Downtown` | 62 | — (corp/private security) | Offices, luxury hotels, nightclubs, marina |

**Dogtown (6 — 5 areas + 1 map marker)**

| Enum | Value | Gangs on map | Economic character |
| --- | --- | --- | --- |
| `Dogtown_Akebono` | 55 | Barghest | Residential/commercial area (parent label TBD) |
| `Dogtown_Brooklyn` | 56 | Barghest | Named area (parent label TBD) |
| `Dogtown_CapitanCaliente` | 57 | Barghest | Bar/venue area |
| `Dogtown_Cynosure` | 58 | Barghest | Sealed military/tech bunker complex |
| `Dogtown_Expo` | 59 | Barghest | Expo/event grounds |
| `Dogtown_Hideout` | 60 | Barghest | Hideout interior/POI cluster |
| `Dogtown_Worldmap_Sub` | 61 | — | **Map subdivision marker, not a place** — exclude from `sub_territories` |

**Badlands (18 records)**

| Enum | Value | Gangs on map | Economic character |
| --- | --- | --- | --- |
| `Badlands_BiotechnicaFlats` | 13 | — (Biotechnica) | Protein farms, agri-corp |
| `Badlands_DryCreek` | 14 | TBD | Desert settlement |
| `Badlands_JacksonPlains` | 15 | Wraiths | Power plant / energy |
| `Badlands_LagunaBend` | 16 | — | Drowned town, lake |
| `Badlands_LasPalapas` | 17 | TBD | Motel crossroads |
| `Badlands_NorthSunriseOilField` | 18 | TBD | Oil field |
| `Badlands_RattlesnakeCreek` | 19 | TBD | Creek settlement |
| `Badlands_RedPeaks` | 20 | — | Trailer park, desert |
| `Badlands_RockyRidge` | 21 | Raffen Shiv (≈ `Wraiths`) | Trailer park / raider camp |
| `Badlands_SantaClara` | 22 | TBD | Desert | 
| `Badlands_SierraSonora` | 23 | TBD (Aldecaldo patrol `[lore]`) | Landfill, wind farms |
| `Badlands_SoCalBorderCrossing` | 24 | TBD | Border checkpoint |
| `Badlands_Spaceport` | 25 | TBD (corp) | Spaceport logistics |
| `Badlands_VasquezPass` | 26 | TBD | Mountain pass |
| `Badlands_Yucca` | 27 | TBD | Small border town |
| `NorthBadlands` | 98 | TBD | Grouping record (verify) |
| `SouthBadlands` | 118 | TBD | Grouping record (verify) |
| `MorroRock` | 96 | TBD | Coastal rock / NCX |

> **Discrepancy to resolve (do not paper over):** the community wiki lists only
> **5** Badlands sub-districts (Rocky Ridge, Biotechnica Flats, Jackson Plains,
> Laguna Bend, Red Peaks) while the enum carries 15 `Badlands_*` records plus
> three further records (`NorthBadlands` 98, `SouthBadlands` 118, `MorroRock` 96)
> whose sub-district status is unconfirmed. Only the 5 are corroborated by a
> second source. Treat the rest as `[enum]`-verified identifiers with
> `[wiki]`-unconfirmed in-world extents; confirm with a TweakDB
> `ParentDistrict()` dump before seeding.

### 2.3 Named sub-locations (POI / interior / quest-only) — 84 records

`gamedataDistrict` mixes geography with named destinations. Of the 132 records,
**8 top-level + 40 sub-districts + 84 named locations = 132**, which is a clean
accounting of `Count = 132`.

These 84 are the highest-value **control-center anchors**: the enum name itself
proves the landmark exists and belongs to that sub-district. Highlights (the full
per-territory mapping is in the "anchor enum" column of §4):

| Sub-district | Named locations in enum |
| --- | --- |
| ArasakaWaterfront | `KonpekiPlaza`, `AbandonedWarehouse` |
| Northside | `All_Foods`, `Totentaz`, `CleanCut`, `WNS`, `Apartment` |
| Kabuki | `LizziesBar`, `JudysApartment`, `NoTellMotel` |
| LittleChina | `Afterlife`, `TomsDiner`, `VictorsClinic`, `MistysShop`, `RiotClub`, `VApartment`, `Q101Cyberspace` |
| JapanTown | `Clouds`, `DarkMatter`, `Fingers`, `FourthWallBdStudio`, `HiromisApartment`, `MegabuildingH8`, `Wakakos_Pachinko_Parlor`, `Apartment`, `VR_Tutorial` |
| CharterHill | `AuCabanon`, `PowerPlant` |
| NorthOaks | `Arasaka_Estate`, `Columbarium`, `Denny_Estate`, `Kerry_Estate` |
| Wellsprings | *(none)* |
| VistaDelRey | `ElCoyoteCojo`, `LaCatrina`, `Delamain`, `Abandoned_Apartment_Building` |
| Glen | `Embers`, `NCPDLab`, `MusicStore`, `WichedTires`, `Apartment` |
| Arroyo | `Red_Dirt`, `Arasaka_Warehouse`, `CytechFactory`, `Kendachi`, `KenmoreCafe`, `LasPalapas`, `TireEmpire`, `ClairesGarage` |
| RanchoCoronado | `GunORama`, `Caliente`, `Piez`, `Softsys`, `Stylishly` |
| Coastview | `GrandImperialMall`, `VDBChapel`, `VDBMaglev`, `BattysHotel`, `ButcherShop`, `RundownApartment`, `q110Cyberspace` |
| WestWindEstate | *(none)* |
| CorpoPlaza | `Apartment`, 9× `ArasakaTower*` floors, `q201Cyberspace` |
| Downtown | `Jinguji`, `TheHammer` |
| Dogtown | `Akebono`, `Brooklyn`, `CapitanCaliente`, `Cynosure`, `Expo`, `Hideout` (plus `Worldmap_Sub` marker) |
| Badlands | `YuccaGarage`, `YuccaRadioTower`, `LagunaBend_LakeHut`, `MorroRock_NCX`, `SouthBadlands_EdgewoodFarm`, `SouthBadlands_PoppyFarm`, `SouthBadlands_TrailerPark`, `SouthBadlands_q201SpaceStation` |
| Unparented POI | `Langley_Clinic` (87) — no matching sub-district record; treat as standalone |

Two classes of these must **not** become control centers:
- **Interiors/quest rooms**: `CorpoPlaza_ArasakaTower*` floors, `Glen_Apartment`,
  `JapanTown_Apartment`, `Northside_Apartment`, `Vista_del_rey_Abandoned_Apartment_Building`,
  `Dogtown_Hideout`.
- **Cyberspace**: `Coastview_q110Cyberspace`, `CorpoPlaza_q201Cyberspace`,
  `LittleChina_Q101Cyberspace`, `SouthBadlands_q201SpaceStation`,
  `JapanTown_VR_Tutorial`. Filter by `District_Record.IsQuestDistrict()`
  (`orphans.swift:18430`) before seeding.

---

## 3. Gang faction catalog

### 3.1 The eleven catalog gangs — exact enum names

| # | `gamedataAffiliation` | Value | Display | Vanilla turf (sub-districts) | Rivals / allies `[lore]` | Typical enemy archetypes `[lore]` |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `Maelstrom` | 10 | Maelstrom | Northside (primary), Kabuki (pressure) | Rival: Tyger Claws, Scavengers, Mox, NCPD; ally: none | Chrome-heavy heavies, shotgunners, tech-weapon snipers, netrunners; faceplate/optics motif |
| 2 | `TygerClaws` | 29 | Tyger Claws | Kabuki, Little China (primary); JapanTown, Charter Hill | Rival: Maelstrom, Mox, Valentinos, 6th Street; corp ties: Arasaka | Katana/mantis melee, smart SMGs, netrunners, "assassin" elites |
| 3 | `Valentinos` | 33 | Valentinos | Wellsprings, Vista del Rey, The Glen (primary) | Rival: 6th Street (long war), Tyger Claws; fixer: Padre | Pistol/SMG street soldiers, machete melee, low-tier veterans |
| 4 | `SixthStreet` | 24 | 6th Street | Arroyo, Rancho Coronado (primary); Vista del Rey, Charter Hill | Rival: Valentinos, Tyger Claws, Maelstrom; hostile to corps | Assault rifles, snipers, grenades, military-veteran soldiers |
| 5 | `VoodooBoys` | 34 | Voodoo Boys | Coastview, West Wind Estate (primary); Dogtown business | Rival: Animals, NetWatch, Scavengers; deals with Barghest | Netrunners, quickhack/ICE specialists, mantis-blade escorts |
| 6 | `Animals` | 2 | Animals | Coastview, West Wind Estate (primary); Arroyo presence | Rival: Voodoo Boys; mercenary for corps | Melee brawlers, gorilla arms, berserk, high body/armor |
| 7 | `Scavengers` | 22 | Scavengers | Northside, Coastview, West Wind Estate, Dogtown; everywhere opportunistically | Rival: all (no allies) | Junk guns, improvised melee, ambush squads, organ-harvest sites |
| 8 | `Wraiths` | 35 | Wraiths (Raffen Shiv) | Badlands: Rocky Ridge, Jackson Plains | Rival: Aldecaldos, nomads, corps | Rifle raiders, vehicle ambush, convoy hits |
| 9 | `Aldecaldos` | 1 | Aldecaldos | Badlands camps; allied to player post-story | Rival: Wraiths/Raffen Shiv; ally: V | Rifles, nomad convoy, defensive camp |
| 10 | `Barghest` | 4 | Barghest | All of Dogtown (sovereign) | Tolerates VDB business; hostile to NUSA/Militech/intruders; uses Scavengers | Military kit, armor, drones/turrets, squad tactics |
| 11 | `TheMox` | 27 | The Mox | Lizzie's Bar (Kabuki) — **building, not a district** | Rival: Tyger Claws (split off), Maelstrom; protects sex workers | Light melee/street fighters; small numbers |

### 3.2 Variant and non-catalog affiliations in the same enum

| Enum | Value | Why it matters |
| --- | --- | --- |
| `MaelstromAndroid` | 11 | Android/cyborg spawn variant — reuse for elite spawns |
| `ScavengersAndroid` | 23 | Android variant |
| `SixthStreetAndroid` | 25 | Android variant |
| `WraithsAndroid` | 36 | Android variant |
| `Wraiths_Former` | 37 | Ex-Wraith — useful for defector/recruit missions |
| `AfterlifeMercs` | 0 | Neutral merc faction (Afterlife) — candidate "independent" owner |
| `Arasaka` | 3 | City Center / Arasaka Waterfront / Arroyo warehouse |
| `Militech` | 12 | City Center, Dogtown/NUSA pressure |
| `Biotechnica` | 5 | Biotechnica Flats |
| `KangTao` | 9 | Corp presence (weapons) |
| `Zetatech` | 38 | Corp presence |
| `NetWatch` | 16 | VDB antagonist; espionage pillar |
| `TraumaTeam` | 28 | Civic service, not territory |
| `NCPD` | 13 | Civic; absent in Pacifica/Dogtown |
| `NUSA` | 15 | Dogtown/Phantom Liberty pressure |
| `CityCouncil` | 6 | Civic authority — Corp Plaza / Downtown legitimacy |
| `NCPrison` | 14 | Prison facility |
| `News54` | 17, `OA` 18, `SSI` 21, `RecordingAgency` 20 | Media/logistics color, not territory |
| `Civilian` | 7 | Populace/neutral spawns |
| `Unaffiliated` | 30 | Neutral/unaligned spawns |
| `UnaffiliatedCorpo` | 31 | Corpo civilian spawns |
| `Unknown` | 32 | Fallback |
| `Classified` | 8 | Placeholder — never seed |
| `REDACTED` | 19 | Placeholder — never seed |
| `corpbud` | 39 | Present in enum, no verified world presence — do not seed |
| `crimson_harvest` | 40 | Present in enum, no verified world presence — do not seed |
| `growl` | 41 | Present in enum, no verified world presence — do not seed |
| `highriders` | 42 | Present in enum, no verified world presence — do not seed |
| `private_press` | 43 | Present in enum, no verified world presence — do not seed |
| `SouthCalifornia` | 26 | Regional authority (border crossing) |

### 3.3 Ownership ambiguities the schema must absorb

1. **`The Mox` owns no sub-district.** They hold one building inside Tyger Claws
   territory. Model as `owner_kind = 'enclave'` with a parent `contested`
   territory, or the overlay will paint one gang's colour across all of Kabuki.
2. **`Raffen Shiv` has no enum.** The wiki lists Rocky Ridge as Raffen Shiv; the
   game models them as `Wraiths` (plus `Wraiths_Former`). Use `Wraiths` and keep
   "Raffen Shiv" as a display/lore alias — do not invent a new faction id.
3. **Corp "ownership" is a different kind of claim.** City Center, Arasaka
   Waterfront and North Oak have no gang panel entry, but they are not unowned:
   they are corp/private-security space. Needs `owner_kind = 'corp'` (with
   `Arasaka` / `Militech` / `CityCouncil` / `Biotechnica` as owner) and a
   separate `claim_strength` so an early-game gang can contest them at a high
   cost instead of instantly flipping.
4. **Multi-gang sub-districts are the norm, not the exception.** Six of the 14
   inhabited sub-districts list 2–3 gangs. A single `owner_faction_id` cannot
   represent that; the seed needs `contested_by[]` + `control_share` weights.

---

## 4. Proposed sub-territory partition

44 sub-territories (target 35–45): Watson 6, Westbrook 5, Heywood 5,
Santo Domingo 5, Pacifica 5, City Center 5, Badlands 7, Dogtown 6.

Rules applied:
- Every sub-territory anchors on a **named, real landmark** (prefer one with a
  `gamedataDistrict` enum member, so the anchor is provably real).
- `parent_district` always names an actual `gamedataDistrict` member, so the
  runtime can resolve `District_Record` metadata for it.
- `initial_owner` follows the vanilla map panel `[wiki]`; where the panel lists
  multiple gangs, `primary` is the dominant one and the rest go to
  `contested_by`.
- Coordinates: **all `TBD`**.
- IDs: lowercase snake, `subdistrict_landmark`, stable and greppable. Renaming a
  landmark in-game must not force an ID change, so IDs use the short landmark
  key, not the display name.

### 4.1 Watson — 6

| `sub_territory_id` | `parent_district` | Initial owner | Contested by | Control center (anchor) | Anchor enum | Economy |
| --- | --- | --- | --- | --- | --- | --- |
| `northside_totentanz` | `Northside` | `Maelstrom` | `TheMox` | Totentanz club (upper floors of unfinished hotel) | `Northside_Totentaz` | Nightlife, drug retail, gang social hub |
| `northside_all_foods` | `Northside` | `Maelstrom` | `Scavengers`, `TheMox` | All Foods processing plant | `Northside_All_Foods` | Food processing, smuggling, chop-shop |
| `kabuki_market` | `Kabuki` | `TygerClaws` | `Maelstrom`, `Scavengers` | Kabuki Market / roundabout bazaar | — (`[wiki]`) | Black market, unlicensed clinics, grey retail |
| `kabuki_lizzies` | `Kabuki` | `TheMox` (enclave) | `TygerClaws` | Lizzie's Bar — Mox HQ | `Kabuki_LizziesBar` | Braindance club, protection economy |
| `little_china_afterlife` | `LittleChina` | `TygerClaws` | `AfterlifeMercs` (neutral) | Afterlife merc bar | `LittleChina_Afterlife` | Mercenary contracting, fixer hub |
| `arasaka_waterfront_konpeki` | `ArasakaWaterfront` | `Arasaka` (corp) | `Maelstrom`, `Scavengers` | Konpeki Plaza / waterfront docks | `ArasakaWaterfront_KonpekiPlaza` | Corporate port, high-value logistics |

### 4.2 Westbrook — 5

| `sub_territory_id` | `parent_district` | Initial owner | Contested by | Control center (anchor) | Anchor enum | Economy |
| --- | --- | --- | --- | --- | --- | --- |
| `japantown_clouds` | `JapanTown` | `TygerClaws` | — | Clouds dollhouse, Megabuilding H8 | `JapanTown_Clouds` | Dollhouse, hospitality, extortion |
| `japantown_jigjig` | `JapanTown` | `TygerClaws` | `Scavengers` | Jig-Jig Street red-light strip | — (`[wiki]`) | Red-light, casinos, BD parlors |
| `charter_hill_power_plant` | `CharterHill` | `TygerClaws` | `SixthStreet` | Charter Hill Power Plant | `CharterHill_PowerPlant` | Utilities, industrial extortion |
| `charter_hill_au_cabanon` | `CharterHill` | `TygerClaws` | `SixthStreet` | Au Cabanon restaurant / upscale retail | `CharterHill_AuCabanon` | Fine dining, luxury retail, protection |
| `north_oak_columbarium` | `NorthOaks` | `CityCouncil` (corp/private) | `TygerClaws` | Columbarium / hillside estates | `NorthOaks_Columbarium` | Memorial services, wealthy estates |

### 4.3 Heywood — 5

| `sub_territory_id` | `parent_district` | Initial owner | Contested by | Control center (anchor) | Anchor enum | Economy |
| --- | --- | --- | --- | --- | --- | --- |
| `wellsprings_auto_shop` | `Wellsprings` | `Valentinos` | — | Valentino Auto Shop (Russell St) | — (`[wiki]`) | Vehicle repair, chop-shop, smuggling |
| `wellsprings_bulwark` | `Wellsprings` | `Valentinos` | `Scavengers` | Bulwark waterfront mall | — (`[wiki]`) | Retail, tourism, waterfront cargo |
| `vista_del_rey_el_coyote` | `VistaDelRey` | `Valentinos` | `SixthStreet` | El Coyote Cojo bar | `Vista_del_rey_ElCoyoteCojo` | Bar, community hub, protection |
| `vista_del_rey_la_catrina` | `VistaDelRey` | `Valentinos` | `SixthStreet` | La Catrina | `Vista_del_Rey_LaCatrina` | Street market, food retail |
| `glen_embers` | `Glen` | `Valentinos` | — | Embers restaurant | `Glen_Embers` | Upscale dining, money laundering |

### 4.4 Santo Domingo — 5

| `sub_territory_id` | `parent_district` | Initial owner | Contested by | Control center (anchor) | Anchor enum | Economy |
| --- | --- | --- | --- | --- | --- | --- |
| `arroyo_red_dirt` | `Arroyo` | `SixthStreet` | `Valentinos`, `Animals` | Red Dirt bar | `Arroyo_Red_Dirt` | Bar, worker recruitment, protection |
| `arroyo_arasaka_warehouse` | `Arroyo` | `SixthStreet` | `Arasaka` (corp) | Arasaka Industrial Park / warehouse | `Arroyo_Arasaka_Warehouse` | Corporate logistics, cargo theft |
| `arroyo_cytech` | `Arroyo` | `SixthStreet` | — | Cytech Factory | `Arroyo_CytechFactory` | Heavy manufacturing, automation |
| `rancho_coronado_megabuilding_h7` | `RanchoCoronado` | `SixthStreet` | — | Megabuilding H7 (largest in NC) | — (`[wiki]`) | Dense worker housing, local retail |
| `rancho_coronado_gun_o_rama` | `RanchoCoronado` | `SixthStreet` | — | Gun-O-Rama | `RanchoCoronado_GunORama` | Firearms retail, suburban security |

### 4.5 Pacifica — 5

| `sub_territory_id` | `parent_district` | Initial owner | Contested by | Control center (anchor) | Anchor enum | Economy |
| --- | --- | --- | --- | --- | --- | --- |
| `coastview_grand_imperial_mall` | `Coastview` | `Animals` | `VoodooBoys`, `Scavengers` | Grand Imperial Mall (unfinished) | `Coastview_GrandImperialMall` | Abandoned retail, drug lab, ambush ground |
| `coastview_vdb_chapel` | `Coastview` | `VoodooBoys` | `Animals` | Pacifica Serenity Bible Church | `Coastview_VDBChapel` | Netrunning, chapel-front contraband |
| `coastview_battys_hotel` | `Coastview` | `VoodooBoys` | `Scavengers` | Batty's Hotel (derelict) | `Coastview_BattysHotel` | Squat/hotel, human trafficking |
| `west_wind_apartments` | `WestWindEstate` | `VoodooBoys` | `Scavengers`, `Animals` | West Wind Apartments | — (`[wiki]`) | Housing blocks, unlicensed trade |
| `west_wind_ncart` | `WestWindEstate` | `Scavengers` | `VoodooBoys` | Unfinished NCART station | — (`[wiki]`) | Transit tunnels, smuggling routes |

### 4.6 City Center — 5 (corp-shared, no gang panel entries)

| `sub_territory_id` | `parent_district` | Initial owner | Contested by | Control center (anchor) | Anchor enum | Economy |
| --- | --- | --- | --- | --- | --- | --- |
| `corpo_plaza_arasaka_tower` | `CorpoPlaza` | `Arasaka` (corp) | `Militech`, player gang (late) | Arasaka Tower lobby/atrium | `CorpoPlaza_ArasakaTowerLobby` | Corporate HQ, data, executive security |
| `corpo_plaza_memorial` | `CorpoPlaza` | `CityCouncil` (corp) | `Militech`, `NCPD` | Corpo Plaza roundabout / memorial esplanade | — (`[lore]`) | Civic space, prestige, surveillance |
| `downtown_jinguji` | `Downtown` | `CityCouncil` (corp) | — | Jinguji luxury store | `Downtown_Jinguji` | Luxury retail, money laundering |
| `downtown_the_hammer` | `Downtown` | `CityCouncil` (corp) | `TygerClaws` (unverified) | The Hammer club | `Downtown_TheHammer` | Nightclub, blackmail, vice |
| `downtown_gold_beach_marina` | `Downtown` | `CityCouncil` (corp) | `Scavengers` | Gold Beach Marina | — (`[wiki]`) | Private marina, contraband landing |

### 4.7 Badlands — 7

| `sub_territory_id` | `parent_district` | Initial owner | Contested by | Control center (anchor) | Anchor enum | Economy |
| --- | --- | --- | --- | --- | --- | --- |
| `badlands_rocky_ridge` | `Badlands_RockyRidge` | `Wraiths` | `Aldecaldos` | Rocky Ridge trailer park / raider camp | `Badlands_RockyRidge` | Raiding base, scavenging, stolen goods |
| `badlands_jackson_plains` | `Badlands_JacksonPlains` | `Wraiths` | `Aldecaldos` | Jackson Plains power plant | `Badlands_JacksonPlains` | Energy infrastructure, extortion |
| `badlands_biotechnica_flats` | `Badlands_BiotechnicaFlats` | `Biotechnica` (corp) | `Wraiths` | Biotechnica protein farms | `Badlands_BiotechnicaFlats` | Agri-corp production, chemical logistics |
| `badlands_laguna_bend` | `Badlands_LagunaBend` | `NULL` (unclaimed) | `Scavengers`, `Wraiths` | Laguna Bend lake hut / drowned town | `LagunaBend_LakeHut` | Ruins, salvage, toxic-water hazard |
| `badlands_red_peaks` | `Badlands_RedPeaks` | `NULL` (unclaimed) | `Wraiths` | Red Peaks trailer park | `Badlands_RedPeaks` | Trailer park, transient settlement |
| `badlands_sierra_sonora` | `Badlands_SierraSonora` | `Aldecaldos` (`[lore]`) | `Wraiths` | Sierra Sonora landfill / wind farms | `Badlands_SierraSonora` | Nomad camp, salvage, wind power |
| `badlands_ncx_spaceport` | `Badlands_Spaceport` | `OA` / corp (`[lore]`) | `Wraiths`, `Scavengers` | NCX spaceport (Morro Rock) | `MorroRock_NCX` | Orbital logistics, high-value cargo |

### 4.8 Dogtown — 6

| `sub_territory_id` | `parent_district` | Initial owner | Contested by | Control center (anchor) | Anchor enum | Economy |
| --- | --- | --- | --- | --- | --- | --- |
| `dogtown_black_sapphire` | `Dogtown` | `Barghest` | — | Black Sapphire (unfinished hotel) | — (`[wiki]`) | Hospitality, arms deals, Hansen's venue |
| `dogtown_stadium` | `Dogtown` | `Barghest` | `VoodooBoys` (business) | EBM Petrochem Stadium market | — (`[wiki]`) | Black market, arms, contract work |
| `dogtown_longshore_stacks` | `Dogtown` | `Barghest` | `Scavengers` | Longshore Stacks container district | — (`[wiki]`) | Container port, smuggling, cheap housing |
| `dogtown_luxor_heights` | `Dogtown` | `Barghest` | `VoodooBoys` | Luxor High Wellness Spa / hillside | — (`[wiki]`) | Luxury services, VDB data business |
| `dogtown_terra_cognita` | `Dogtown` | `Barghest` | `Scavengers` | Terra Cognita abandoned tech park | — (`[wiki]`) | Ruins, tech salvage, ambush ground |
| `dogtown_cynosure` | `Dogtown_Cynosure` | `Barghest` | — | Cynosure Site D bunker complex | `Dogtown_Cynosure` | Sealed military tech, high-risk loot |

### 4.9 Coverage summary

| District | Sub-territories | Vanilla sub-districts covered | Corp/unclaimed entries |
| --- | --- | --- | --- |
| Watson | 6 | 4 / 4 | 1 (`Arasaka`) |
| Westbrook | 5 | 3 / 3 | 1 (`CityCouncil`) |
| Heywood | 5 | 3 / 3 | 0 |
| Santo Domingo | 5 | 2 / 2 | 0 (1 corp-contested) |
| Pacifica | 5 | 2 / 2 | 0 |
| City Center | 5 | 2 / 2 | 5 (`Arasaka`, `CityCouncil`) |
| Badlands | 7 | 5 / 5 `[wiki]` + 2 extras | 4 (`Biotechnica`, `OA`, `NULL`×2) |
| Dogtown | 6 | 5 wiki areas + `Cynosure` | 0 |
| **Total** | **44** | **25 sub-district records touched** | **11** |

Gang representation as initial owner: Maelstrom 2, Tyger Claws 6, Valentinos 5,
6th Street 5, Voodoo Boys 3, Animals 1, Scavengers 1, Wraiths 2, Aldecaldos 1,
Barghest 6, The Mox 1 (33), plus 9 corp-owned and 2 unclaimed = 44. All eleven
catalog gangs appear.

---

## 5. Contested and ambiguous zones (decisions needed before Step 0.4)

| Zone | Ambiguity | Evidence | Recommendation |
| --- | --- | --- | --- |
| Kabuki | 3 gangs listed (Tyger Claws, Maelstrom, Mox) | `[wiki]` | Split into `kabuki_market` (Tyger) + `kabuki_lizzies` (Mox enclave); Maelstrom as raider pressure, not owner |
| Northside | 3 gangs listed (Maelstrom, Mox, Scavengers) | `[wiki]` | Maelstrom owns both; Mox/Scavs as contest modifiers |
| Charter Hill | Tyger Claws **and** 6th Street | `[wiki]` | Tyger primary, 6th Street contest — 6th Street reaching into Westbrook is the interesting story beat |
| Vista del Rey | Valentinos **and** 6th Street | `[wiki]` | Valentinos primary; 6th Street contest (matches Heywood/Santo Domingo war) |
| Arasaka Waterfront | No gang panel entry, but not "unowned" | `[wiki]` | `owner_kind = 'corp'`, owner `Arasaka`, claim strength high |
| North Oak | No gang panel entry | `[wiki]` | `CityCouncil`/private security; low-value target, high heat |
| City Center (both) | No gang panel entry | `[wiki]` | Corp ownership only; player gang contest should be a late-game, high-heat action |
| Corpo Plaza roundabout | Anchor landmark is `[lore]`, no enum | — | Replace with `CorpoPlaza_Apartment` or a TweakDB-confirmed POI if the esplanade can't be verified |
| Downtown / The Hammer | Gang operator unverified | — | Keep as corp-owned until confirmed; do not label Tyger Claws without evidence |
| Rocky Ridge | Wiki says **Raffen Shiv**, enum only has `Wraiths` | `[enum]` + `[wiki]` | Map to `Wraiths`, store `"Raffen Shiv"` as lore alias |
| Badlands `NorthBadlands` / `SouthBadlands` | May be grouping records, not places | `[enum]` only | Exclude from territory list; verify with `ParentDistrict()` dump |
| 10 unverified `Badlands_*` regions | Wiki lists only 5 sub-districts | count mismatch | Do not seed until TweakDB dump confirms parent + gang list |
| Dogtown `Dogtown_*` records | `[enum]` names (Akebono, Brooklyn, Expo) don't map 1:1 to the wiki's area names (Golden Pacific, Longshore Stacks, Luxor Heights, Terra Cognita) | both | Need a TweakDB parent/label dump; my 6 territories use the wiki area names, which are what players recognise |
| `Dogtown_Worldmap_Sub` | Map subdivision marker | `[enum]` | Hard-exclude from seeds |
| Wellsprings / West Wind Estate | Have **zero** named locations in the enum | `[enum]` | Anchors come from `[wiki]` only; coordinates must be captured in-game |
| Langley Clinic | POI with no parent sub-district | `[enum]` | Standalone landmark; do not attach to a territory without a dump |
| The Mox | Holds a building, not a district | `[wiki]` + `[enum]` | Use `owner_kind = 'enclave'`; needs schema support in Step 0.4 |

---

## 6. Suggested faction/turf heat parameters (design, tunable)

Derived from `District_Record` fields that actually exist, so these can be
computed rather than invented where possible:

| Parameter | Source | Use |
| --- | --- | --- |
| `crime_multiplier` | `District_Record.CrimeMultiplier()` (`orphans.swift:18426`) | Scale heat gain per district (Pacifica/Dogtown high, Westbrook low). |
| `gunshot_stim_range` | `District_Record.GunShotStimRange()` (18424) | How far violence propagates NCPD attention. |
| `explosive_stim_multiplier` | `District_Record.ExplosiveDeviceStimRangeMultiplier()` (18428) | Explosive-based missions generate more heat. |
| `prevention_preset` | `District_Record.PreventionPreset()` (18400) | NCPD response tier per district (Pacifica none, City Center max). |
| `is_quest_district` | `District_Record.IsQuestDistrict()` (18430) | Distinguish quest-only interiors from geography. |
| `claim_strength` | `[proposal]` | 1.0 gang-owned, 0.6 contested, 1.2 corp, 0.2 unclaimed. |

Per-district `crime_multiplier` values are TBD (TweakDB), but they are one
one-line native read per district — cache them once at load, never per frame.

---

## 7. Seed shape ready for `data/`

Minimum columns per table, matching `docs/architecture.md` §3.3.

```yaml
# data/factions.yaml (excerpt)
- id: maelstrom
  enum_name: Maelstrom          # verified, orphans.swift:4485
  enum_value: 10
  display_name: Maelstrom
  category: gang                # gang | corp | fixer | civic | independent
  icon_ref: TBD                 # Affiliation_Record.IconPath()
  color_hex: "#8B1E3F"          # [proposal]
  rival_ids: [tyger_claws, the_mox, scavengers, ncpd]
  ally_ids: []
```

```yaml
# data/sub_territories.yaml (excerpt — the requested example id)
- id: northside_all_foods
  display_name: All Foods
  major_district_id: watson               # gamedataDistrict.Watson
  parent_district_id: northside           # gamedataDistrict.Northside
  owner_faction_id: maelstrom
  owner_kind: gang                        # gang | corp | city | unclaimed | enclave
  contested_by: [scavengers, the_mox]
  control_center_landmark_id: northside_all_foods_plant
  anchor_enum: Northside_All_Foods        # verified, orphans.swift:105
  economy_tags: [food_processing, smuggling, chop_shop]
  base_income: TBD                        # balance pass, not research
  heat_modifier: TBD                      # from District_Record.CrimeMultiplier()
  x: TBD                                  # §8 — never guess
  y: TBD
  z: TBD
  confidence: verified_enum
```

```yaml
# data/landmarks.yaml (excerpt)
- id: northside_all_foods_plant
  display_name: All Foods Plant
  anchor_enum: Northside_All_Foods
  sub_territory_id: northside_all_foods
  kind: factory
  mappin_variant: OutpostVariant          # orphans.swift:1264
  x: TBD
  y: TBD
  z: TBD
```

```yaml
# data/spawn_points.yaml (excerpt)
- id: TBD                                  # assigned by extractor
  sub_territory_id: northside_all_foods
  faction_id: maelstrom
  archetype_record: TBD                   # TweakDB Character/Archetype record
  encounter_type: control_center           # control_center | patrol | ambush | static
  x: TBD
  y: TBD
  z: TBD
  source: TBD                             # e.g. community-area dump path
```

Validation rules for the `data/` generator (Step 0.4):
1. `parent_district_id` must be a real `gamedataDistrict` member, and
   `major_district_id` must be that record's `ParentDistrict()` (or equal for
   top-level). Enforce, do not assume.
2. No duplicate anchor enums across territories.
3. Reject any row whose anchor enum has `IsQuestDistrict() == true` or whose
   enum name contains `Cyberspace`.
4. Reject `(0, 0, 0)` and any coordinate outside the parent district's bounds.
5. `owner_kind` must be consistent with the faction's `category`
   (corp owner ⇒ `owner_kind = corp`, etc.).
6. `TheMox` may only be owner when `owner_kind = enclave`.

---

## 8. Coordinates: what is missing and how to get it honestly

**Nothing in this document is a coordinate.** `gamedataDistrict` is a pure label
enum; `District_Record` exposes no position. There is no coordinate to copy out
of `refs/cyberpunk`, so every `(x, y, z)` is `TBD`.

### 8.1 Extraction options, cheapest first

1. **Fast-travel points (recommended first pass).** Each fast-travel point is a
   named world location with a stored transform. ~90% of the 44 anchors have a
   fast-travel point within a few metres. Extract from the fast-travel /
   `Mappin` records (WolvenKit archive export → `.json`), then snap each anchor
   manually to its landmark.
2. **In-game capture (highest confidence, ~10 min/territory).** Stand on the
   anchor, read `Game.GetPlayer().GetWorldPosition()` (CET console). This is a
   primary measurement and is the only method that guarantees "where NPCs
   actually spawn" for that control center.
3. **Mappin/POI data.** `MappinSystem` / `PointOfInterestMappin`
   (`orphans.swift:46770`) and the vanilla gang-site mappins
   (`GangWatchVariant` 56, `OutpostVariant` 85, `SmugglersDenVariant` 109) have
   world transforms; a one-time in-game dump of all mappins of those variants
   yields exactly the gang-occupied sites we want as control centers.
4. **Community-area resources.** Gang spawn clusters live in community/spawner
   resources (`NPCPuppet`/community references) — the ground truth for
   "typical enemy archetypes" and spawn counts per site.
5. **TweakDB dump for the non-coordinate facts still missing:**
   `District_Record.Gangs()`, `ParentDistrict()`, `EnumName()`,
   `CrimeMultiplier()`, `PreventionPreset()`, and `Affiliation_Record`
   display/icon data. A single in-game dump script solves §1.1, §2.2 and §5 at
   once.

### 8.2 Runtime cross-check that needs no new data

`PreventionSystem.GetCurrentDistrict().GetDistrictRecord().Type()` returns the
exact `gamedataDistrict` the player is standing in
(`preventionSystem.swift:403`, `districtManager.swift:188`). So the seed's
`parent_district_id` can be validated in-game for free: walk to a control
center, assert the reported enum equals the seeded one. Build this as a
dev-only diagnostic before trusting any hand-entered coordinate.

### 8.3 Coordinate honesty table

| Item | Status |
| --- | --- |
| District/sub-district enum names and values | **Verified** (`orphans.swift:4826-4961`) |
| Gang enum names and values | **Verified** (`orphans.swift:4474-4521`) |
| District→affiliation ownership field exists | **Verified** (`District_Record.Gangs`, `orphans.swift:18408`) |
| Exact per-district gang arrays | **Not extracted** — TweakDB binary, hashed IDs |
| Sub-district parentage | **Structurally verified**, per-record mapping not extracted |
| Landmark existence per sub-district | **Verified** via enum names (§2.3) |
| Landmark `(x, y, z)` | **TBD** — all 44 |
| Spawn point coordinates / archetype records | **TBD** |
| Per-district crime multiplier values | **TBD** (field verified) |

---

## 9. Open questions for the design gate

1. **Enclave support** — confirm the schema allows a building-level owner
   (`The Mox` / Lizzie's Bar) inside another gang's sub-territory, or accept
   painting all of Kabuki as Mox.
2. **Corp contest model** — should a starting gang be able to take City Center
   at all, or is corp space permanently non-flippable in v0.1.0?
3. **Badlands granularity** — 7 territories across a huge map vs 5 wiki
   sub-districts: pick one after the TweakDB dump resolves the 10 unconfirmed
   `Badlands_*` records.
4. **Dogtown naming** — ship wiki-recognisable area names (Golden Pacific,
   Longshore Stacks, Luxor Heights, Terra Cognita) or match the `Dogtown_*`
   enum records? Players navigate by the former; the enum is what the engine
   reports. Recommend: enum for `parent_district`, wiki names for
   `display_name`.
5. **`NorthBadlands` / `SouthBadlands`** — grouping records or real places?
   Determines whether the Badlands overlay needs 2 or 5+ polygons.
6. **Archetype sourcing** — are spawn archetypes pulled from TweakDB
   `Character.*` records per gang, or authored per sub-territory? This decides
   whether `spawn_points` needs a per-site override column.

---

## 10. Sources

Primary (in-repo, `refs/cyberpunk`):
- `orphans.swift:4826-4961` — `enum gamedataDistrict` (132 records).
- `orphans.swift:4474-4521` — `enum gamedataAffiliation` (44 records).
- `orphans.swift:18392-18433` — `District_Record`.
- `orphans.swift:29856-29875` — `Affiliation_Record`.
- `orphans.swift:32827-32858` — `DistrictPreventionData_Record`.
- `orphans.swift:46770-46781` — `PointOfInterestMappin`.
- `orphans.swift:1235`, `1264`, `1288` — gang-site mappin variants.
- `core/systems/prevention/districtManager.swift:2-195` — `District`, `DistrictManager`.
- `core/systems/preventionSystem.swift:403`, `2429`, `3053-3065` — current district,
  Badlands gate, district-entry heat multiplier.
- `cyberpunk/UI/fullscreen/map/worldMap.swift:1298-1332`, `1830-1871` — gang panel
  and sub-district rendering.
- `cyberpunk/UI/mappins/mappinUtils.swift:6` — enum → `District_Record`.

Secondary (community documentation, `[wiki]` tags; used only for gang panels,
landmark names and area labels, never for identifiers or coordinates):
- `wiki.eso-ui.com` Cyberpunk 2077 location pages: Watson/Kabuki, Northside,
  Westbrook/Japantown, Heywood/Wellsprings, Santo Domingo/Arroyo,
  Rancho Coronado, Pacifica/Coastview, West Wind Estate, City Center/Downtown,
  Badlands, Dogtown.
