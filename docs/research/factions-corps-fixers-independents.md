# Megacorps, Fixers & Civic/Independent Powers Catalog

**Research step:** 0.2b (parallel with the gang catalog, step 0.2a)
**Target:** Cyberpunk 2077 `2.5` (Phantom Liberty included), redscript 1.x stack
**Scope:** megacorporations, fixers, civic/independent powers, strategic assets
**Status:** research input for Step 0.4 (`data/` seeds → `world.db`) and the
Pillar 3 (Org Management) / Pillar 4 (Stock Market) designs. Not a design spec.

---

## 0. Method, confidence and the coordinate rule

### 0.1 Sources actually read

| Source | What it was used for |
| --- | --- |
| `docs/roadmap.md` | step scope, "~5 control centers per major district", pillar sequencing |
| `docs/glossary.md` | canonical vocabulary (Faction, Control Center, Sub-Territory, Heat) |
| `docs/architecture.md` | `factions` / `districts` / `sub_territories` / `landmarks` / `spawn_points` tables |
| `refs/cyberpunk/orphans.swift` | `gamedataAffiliation`, `gamedataDistrict`, `gamedataMappinVariant`, `gamedataVehicleManufacturer`, `ENcartStations`, record accessors (`District_Record`, `Affiliation_Record`, `Vendor_Record`, `FastTravelPoint_Record`, `DistrictPreventionData_Record`, `PreventionHeatData_Record`) |
| `refs/cyberpunk/core/systems/prevention/*.swift` | NCPD prevention/heat model, district stack, police agent registry, MaxTac |
| `refs/cyberpunk/core/systems/preventionSystem.swift` | heat stages 0–5, district data matrix selection, MaxTac/AV spawn rules |
| `refs/cyberpunk/cyberpunk/NPC/NPCPuppet.swift` | `Affiliation()` on character records (scan/"faction" display) |
| `refs/cyberpunk/core/systems/delamainTaxiSystem.swift`, `core/components/scriptComponents/delamainTaxiComponent.swift` | Delamain as a live service, not just flavour |
| `refs/cyberpunk/cyberpunk/UI/fullscreen/map/worldMap.swift`, `UI/mappins/mappinUtils.swift` | mappin variants usable as control-center/asset anchors |
| Community/canon lookups (Cyberpunk Wiki, modding docs) | fixer HQs, corp buildings, faction identities **not present in `refs/`** — always flagged `[canon]` |

### 0.2 Confidence tags used in every table

| Tag | Meaning |
| --- | --- |
| `[enum]` | Exact string verified in `refs/cyberpunk/orphans.swift` (`gamedataAffiliation` / `gamedataDistrict`) |
| `[record]` | Exact TweakDB record/accessor verified in `refs/` (name and return type) |
| `[script]` | Behaviour verified in decompiled script logic in `refs/` |
| `[canon]` | Game canon / community wiki; **not** present in `refs/`, safe for design, must be re-verified against game data before it becomes a coordinate or a DB row |
| `[design]` | My proposal for Neon Ascendancy, not game data |
| `[infer]` | Reasonable reading of an enum name (e.g. `Arroyo_Kendachi` ⇒ a Kendachi site in Arroyo); the location exists, the *role* is inferred |

### 0.3 Coordinate rule (non-negotiable)

> **No `(x, y, z)` value appears anywhere in this document.**
> Every physical anchor is named by its exact `gamedataDistrict` /
> `TweakDB` / `FastTravelPoint` identity only. All coordinates are
> `TBD (extract from game data)`.

Rationale: `refs/cyberpunk` contains decompiled **scripts**, not TweakDB records
or world sectors. The scripts prove that a district/affiliation *exists* and how
the engine classifies it; they cannot prove where it is. Inventing coordinates
would poison `world.db` and the map overlay in Step 0.5. Section 7 lists the
exact APIs to extract real coordinates later.

### 0.4 Two facts that shape the whole catalog

1. **`gamedataDistrict` is flat, not a tree.** Sub-districts (`Kabuki`,
   `CorpoPlaza`, `VistaDelRey`, …) are *siblings* of top-level districts
   (`Watson`, `CityCenter`, `Heywood`, …) in one 134-value enum (132 district
   records `0…131`, plus `Count`/`Invalid`). The hierarchy
   only exists at runtime via `District_Record.ParentDistrict()` `[record]`.
   Any seed file must store `parent_district_id` explicitly and must not assume
   enum ordering.
2. **`gamedataAffiliation` mixes gangs, corps, and civic bodies in one enum**
   `[enum]`. There is no `gamedataGang`. The Faction category in the glossary
   (Gang / Megacorp / Fixer Network / Civic-Independent) is therefore a
   **Neon Ascendancy concept layered on top** of `gamedataAffiliation`, and
   needs its own mapping table.

---

## 1. Ground truth enums

### 1.1 `gamedataAffiliation` — 46 values (44 real affiliations `0…43`, plus `Count`, `Invalid`)

This is the authoritative list of scannable affiliations in 2.5. Anything not in
this list is **not** a scannable faction and needs a synthetic faction id.

| Index | Affiliation | Notes |
| --- | --- | --- |
| 0 | `AfterlifeMercs` | mercenary guild centred on the Afterlife |
| 1 | `Aldecaldos` | nomad clan (gang catalog) |
| 2 | `Animals` | gang (gang catalog) |
| 3 | `Arasaka` | megacorp |
| 4 | `Barghest` | Dogtown militia (gang catalog) |
| 5 | `Biotechnica` | megacorp |
| 6 | `CityCouncil` | municipal government |
| 7 | `Civilian` | non-combatant |
| 8 | `Classified` | hidden affiliation (spoiler-safe label) |
| 9 | `KangTao` | megacorp |
| 10 | `Maelstrom` | gang |
| 11 | `MaelstromAndroid` | android variant |
| 12 | `Militech` | megacorp |
| 13 | `NCPD` | police |
| 14 | `NCPrison` | prison service / inmates |
| 15 | `NUSA` | federal government (FIA) |
| 16 | `NetWatch` | net-security agency |
| 17 | `News54` | media (Network 54) |
| 18 | `OA` | Orbital Air |
| 19 | `REDACTED` | hidden affiliation variant |
| 20 | `RecordingAgency` | braindance/recording industry |
| 21 | `SSI` | Secure Services Inc. (private security) |
| 22 | `Scavengers` | gang |
| 23 | `ScavengersAndroid` | android variant |
| 24 | `SixthStreet` | gang (note: no space, unlike the wiki name "6th Street") |
| 25 | `SixthStreetAndroid` | android variant |
| 26 | `SouthCalifornia` | state-level government |
| 27 | `TheMox` | gang (glossary files it as civic-independent) |
| 28 | `TraumaTeam` | private emergency medicine |
| 29 | `TygerClaws` | gang |
| 30 | `Unaffiliated` | no faction |
| 31 | `UnaffiliatedCorpo` | generic corporate employee (not a named corp) |
| 32 | `Unknown` | unknown |
| 33 | `Valentinos` | gang |
| 34 | `VoodooBoys` | gang |
| 35 | `Wraiths` | gang |
| 36 | `WraithsAndroid` | android variant |
| 37 | `Wraiths_Former` | ex-Wraith (quest state) |
| 38 | `Zetatech` | megacorp |
| 39 | `corpbud` | **unresolved** — see §4.9 |
| 40 | `crimson_harvest` | anti-corp terrorist org (PL) |
| 41 | `growl` | Growl FM (radio) affiliation tag |
| 42 | `highriders` | orbital habitat population |
| 43 | `private_press` | independent press |
| — | `Count` = 44, `Invalid` = 45 | sentinels |

**Design consequence:** only **13** affiliations are named corporations
(`Arasaka`, `Biotechnica`, `KangTao`, `Militech`, `NetWatch`, `News54`, `OA`,
`SSI`, `TraumaTeam`, `Zetatech`, `RecordingAgency`, `corpbud`, plus
`UnaffiliatedCorpo` as a generic). Kiroshi, Kendachi, Night Corp, Petrochem,
Budget Arms, WNS, EBM, Raven, Dynalar have **no affiliation record** and must be
modeled as synthetic factions with `affiliation_type = NULL`.

### 1.2 `gamedataDistrict` — 134 values (132 district records `0…131`, plus `Count`, `Invalid`)

Verbatim, in enum order. `ParentDistrict()` is the only source of hierarchy
`[record]`; do not infer parents from name prefixes alone (`Wellsprings` and
`Glen` are Heywood children, `CharterHill` is a Westbrook child, `Downtown` and
`CorpoPlaza` are City Center children).

<details>
<summary>Full enum (132 records + sentinels)</summary>

| Index | District record |
| --- | --- |
| 0 | `ArasakaWaterfront` |
| 1 | `ArasakaWaterfront_AbandonedWarehouse` |
| 2 | `ArasakaWaterfront_KonpekiPlaza` |
| 3 | `Arroyo` |
| 4 | `Arroyo_Arasaka_Warehouse` |
| 5 | `Arroyo_ClairesGarage` |
| 6 | `Arroyo_CytechFactory` |
| 7 | `Arroyo_Kendachi` |
| 8 | `Arroyo_KenmoreCafe` |
| 9 | `Arroyo_LasPalapas` |
| 10 | `Arroyo_Red_Dirt` |
| 11 | `Arroyo_TireEmpire` |
| 12 | `Badlands` |
| 13 | `Badlands_BiotechnicaFlats` |
| 14 | `Badlands_DryCreek` |
| 15 | `Badlands_JacksonPlains` |
| 16 | `Badlands_LagunaBend` |
| 17 | `Badlands_LasPalapas` |
| 18 | `Badlands_NorthSunriseOilField` |
| 19 | `Badlands_RattlesnakeCreek` |
| 20 | `Badlands_RedPeaks` |
| 21 | `Badlands_RockyRidge` |
| 22 | `Badlands_SantaClara` |
| 23 | `Badlands_SierraSonora` |
| 24 | `Badlands_SoCalBorderCrossing` |
| 25 | `Badlands_Spaceport` |
| 26 | `Badlands_VasquezPass` |
| 27 | `Badlands_Yucca` |
| 28 | `Badlands_YuccaGarage` |
| 29 | `Badlands_YuccaRadioTower` |
| 30 | `CharterHill` |
| 31 | `CharterHill_AuCabanon` |
| 32 | `CharterHill_PowerPlant` |
| 33 | `CityCenter` |
| 34 | `Coastview` |
| 35 | `Coastview_BattysHotel` |
| 36 | `Coastview_ButcherShop` |
| 37 | `Coastview_GrandImperialMall` |
| 38 | `Coastview_RundownApartment` |
| 39 | `Coastview_VDBChapel` |
| 40 | `Coastview_VDBMaglev` |
| 41 | `Coastview_q110Cyberspace` |
| 42 | `CorpoPlaza` |
| 43 | `CorpoPlaza_Apartment` |
| 44 | `CorpoPlaza_ArasakaTowerAtrium` |
| 45 | `CorpoPlaza_ArasakaTowerCEOFloor` |
| 46 | `CorpoPlaza_ArasakaTowerJenkins` |
| 47 | `CorpoPlaza_ArasakaTowerJungle` |
| 48 | `CorpoPlaza_ArasakaTowerLobby` |
| 49 | `CorpoPlaza_ArasakaTowerNest` |
| 50 | `CorpoPlaza_ArasakaTowerSaburoOffice` |
| 51 | `CorpoPlaza_ArasakaTowerUnlistedFloors` |
| 52 | `CorpoPlaza_ArasakaTowerUpperAtrium` |
| 53 | `CorpoPlaza_q201Cyberspace` |
| 54 | `Dogtown` |
| 55 | `Dogtown_Akebono` |
| 56 | `Dogtown_Brooklyn` |
| 57 | `Dogtown_CapitanCaliente` |
| 58 | `Dogtown_Cynosure` |
| 59 | `Dogtown_Expo` |
| 60 | `Dogtown_Hideout` |
| 61 | `Dogtown_Worldmap_Sub` |
| 62 | `Downtown` |
| 63 | `Downtown_Jinguji` |
| 64 | `Downtown_TheHammer` |
| 65 | `Glen` |
| 66 | `Glen_Apartment` |
| 67 | `Glen_Embers` |
| 68 | `Glen_MusicStore` |
| 69 | `Glen_NCPDLab` |
| 70 | `Glen_WichedTires` |
| 71 | `Heywood` |
| 72 | `JapanTown` |
| 73 | `JapanTown_Apartment` |
| 74 | `JapanTown_Clouds` |
| 75 | `JapanTown_DarkMatter` |
| 76 | `JapanTown_Fingers` |
| 77 | `JapanTown_FourthWallBdStudio` |
| 78 | `JapanTown_HiromisApartment` |
| 79 | `JapanTown_MegabuildingH8` |
| 80 | `JapanTown_VR_Tutorial` |
| 81 | `JapanTown_Wakakos_Pachinko_Parlor` |
| 82 | `Kabuki` |
| 83 | `Kabuki_JudysApartment` |
| 84 | `Kabuki_LizziesBar` |
| 85 | `Kabuki_NoTellMotel` |
| 86 | `LagunaBend_LakeHut` |
| 87 | `Langley_Clinic` |
| 88 | `LittleChina` |
| 89 | `LittleChina_Afterlife` |
| 90 | `LittleChina_MistysShop` |
| 91 | `LittleChina_Q101Cyberspace` |
| 92 | `LittleChina_RiotClub` |
| 93 | `LittleChina_TomsDiner` |
| 94 | `LittleChina_VApartment` |
| 95 | `LittleChina_VictorsClinic` |
| 96 | `MorroRock` |
| 97 | `MorroRock_NCX` |
| 98 | `NorthBadlands` |
| 99 | `NorthOaks` |
| 100 | `NorthOaks_Arasaka_Estate` |
| 101 | `NorthOaks_Columbarium` |
| 102 | `NorthOaks_Denny_Estate` |
| 103 | `NorthOaks_Kerry_Estate` |
| 104 | `Northside` |
| 105 | `Northside_All_Foods` |
| 106 | `Northside_Apartment` |
| 107 | `Northside_CleanCut` |
| 108 | `Northside_Totentaz` |
| 109 | `Northside_WNS` |
| 110 | `Pacifica` |
| 111 | `RanchoCoronado` |
| 112 | `RanchoCoronado_Caliente` |
| 113 | `RanchoCoronado_GunORama` |
| 114 | `RanchoCoronado_Piez` |
| 115 | `RanchoCoronado_Softsys` |
| 116 | `RanchoCoronado_Stylishly` |
| 117 | `SantoDomingo` |
| 118 | `SouthBadlands` |
| 119 | `SouthBadlands_EdgewoodFarm` |
| 120 | `SouthBadlands_PoppyFarm` |
| 121 | `SouthBadlands_TrailerPark` |
| 122 | `SouthBadlands_q201SpaceStation` |
| 123 | `VistaDelRey` |
| 124 | `Vista_del_Rey_Delamain` |
| 125 | `Vista_del_Rey_LaCatrina` |
| 126 | `Vista_del_rey_Abandoned_Apartment_Building` |
| 127 | `Vista_del_rey_ElCoyoteCojo` |
| 128 | `Watson` |
| 129 | `Wellsprings` |
| 130 | `WestWindEstate` |
| 131 | `Westbrook` |
| — | `Count` = 132, `Invalid` = 133 |

</details>

Observed naming inconsistencies to normalise in seeds (do **not** rename the
enum, but store a `canonical_id` alias): `Vista_del_Rey_Delamain` vs
`VistaDelRey`; `Vista_del_rey_Abandoned_Apartment_Building` (lowercase `rey`);
`NorthOaks` (enum) vs "North Oak" (UI); `JapanTown` (enum) vs "Japantown" (UI);
`Glen_WichedTires` (enum) vs "Wicked Tires" (UI).

### 1.3 Records and accessors that drive this catalog

| Record | Accessors | Why it matters |
| --- | --- | --- |
| `District_Record` `[record]` | `EnumName()`, `LocalizedName()`, `Type() : gamedataDistrict`, `ParentDistrict()`, `PreventionPreset() : DistrictPreventionData_Record`, `Gangs() : [Affiliation_Record]`, `UiIcon()`, `UiState()`, `PoliceRadioSceneEntryPoint()`, `GunShotStimRange()`, `CrimeMultiplier()`, `ExplosiveDeviceStimRangeMultiplier()`, `IsQuestDistrict()` | single source for the district tree, **per-district gang/affiliation set**, and the NCPD heat parameters |
| `Affiliation_Record` `[record]` | `Type() : gamedataAffiliation`, `EnumName()`, `LocalizedName()`, `IconPath()`, `AnimWrappers()` | faction row: id, label, map/scanner icon, animation set |
| `Vendor_Record` `[record]` | `LocalizedName()`, `Faction() : Affiliation_Record`, `VendorType()`, `VendorFilterTags()`, `ItemStock()` | corp storefronts and ripperdoc/Kiroshi channel. `Faction()` is how a shop becomes an economic asset of a corp |
| `FastTravelPoint_Record` `[record]` | `DisplayName()`, `Description()`, `District()`, `ShowOnWorldMap()`, `ShowInWorld()`, `SubwayStation()` | open-world, always-reachable anchors — the safest coordinate seeds |
| `DistrictPreventionData_Record` `[record]` | `Heat1()`…`Heat5()`, `Recon()`, `InputLockTime()`, `InputLockOverrideThreshold()`, `SpawnOriginMaxDistance()` | per-district police escalation package |
| `PreventionHeatData_Record` `[record]` | `UnitRecordsPool()`, `VehicleRecordPool()`, `SpawnRange()`, `VehicleSpawnDistanceRange()`, `AvRecord()`, `AvSpawnDistanceRange()`, `FallbackUnitData()` | exact NPC/vehicle pools per heat level — the template for "NCPD pressure" in the sim |
| `PreventionHeatTable_Record` `[record]` | `DisplayName()`, `Strategy0()`…`Strategy7()` (16 strategy accessors total) | per-heat response strategies |
| `ENcartStations` `[enum]` | 19 metro stations incl. `ARASAKA_TOWER`, `CITY_CENTER`, `CHARTER_HILL`, `VISTA_DEL_REY`, `WELLSPRINGS`, `RANCHO_CORONADO`, `PACIFICA_STADIUM` | cheap, dense, district-labelled anchor list |

---

## 2. Megacorporations

### 2.1 Summary

`Tier` is my economic weight for the Stock Market (1 = planetary mega, 4 =
niche/private). `NC anchors` are `gamedataDistrict` names only.

| Corp | Affiliation | Tier | Sector | NC anchors (district records) | Ticker `[design]` |
| --- | --- | --- | --- | --- | --- |
| Arasaka | `Arasaka` `[enum]` | 1 | security, banking, arms, cyberware | `CorpoPlaza_ArasakaTower*` (10 floors), `ArasakaWaterfront*` + `ArasakaWaterfront_KonpekiPlaza`, `Arroyo_Arasaka_Warehouse`, `NorthOaks_Arasaka_Estate` | `ARSK` |
| Militech | `Militech` `[enum]` | 1 | arms, PMC, vehicles, AV | Corpo Plaza offices `[canon]`; `Dogtown_Cynosure` (Militech black site) `[canon]`; vehicle manufacturer `Militech` `[enum]` | `MLTC` |
| Kang Tao | `KangTao` `[enum]` | 2 | smart weapons, drones, AV, electronics | Corpo Plaza tower `[canon]` | `KTAO` |
| Biotechnica | `Biotechnica` `[enum]` | 2 | agri-protein, pharma, biotech, biofuel | `Badlands_BiotechnicaFlats`, Corpo Plaza office `[canon]` | `BIOT` |
| Zetatech | `Zetatech` `[enum]` | 2 | electronics, cyberware, AV, vehicles, netgear | "Zetatech Building", Berkeley Avenue, central NC `[canon]`; `gamedataVehicleManufacturer.Zetatech` `[enum]` | `ZETA` |
| Night Corp | **none** (no affiliation record) | 2 | municipal infrastructure, utilities, construction, water/power | Night Corp HQ, `Downtown` (City Center) `[canon]`; `CharterHill_PowerPlant` `[infer]` | `NGTCP` |
| NetWatch | `NetWatch` `[enum]` | 2 | net security, Blackwall containment | no NC HQ (HQ London `[canon]`); agents/outposts only | `NTWT` |
| Trauma Team | `TraumaTeam` `[enum]` | 2 | private emergency medicine, insurance, AV | AV response citywide `[script]`; no verified 2077 interior | `TRMA` |
| N54 (Network 54) | `News54` `[enum]` | 3 | broadcast media, advertising | N54 offices, `Downtown` (City Center) `[canon]`; distinct from `Northside_WNS` | `NWS54` |
| Orbital Air | `OA` `[enum]` | 2 | orbital launch, cargo, tourism | `Badlands_Spaceport` `[enum+canon]` | `ORBA` |
| Kiroshi | **none** | 3 | optics/cyberware (Kiroshi Optics) | no verified building; retail via ripperdocs `[script]` | `KIRO` |
| Kendachi | **none** | 4 | melee weapons, monofilament | `Arroyo_Kendachi` `[enum+infer]` | `KEND` |
| SSI (Secure Services Inc.) | `SSI` `[enum]` | 4 | private security, intelligence front | Peralez protective detail / surveillance `[canon]` | private |
| Budget Arms | **none** | 4 | cheap firearms | none verified (`corpbud` ≠ Budget Arms, see §4.9) | `BDA` |
| Petrochem | **none** (NPCs are `UnaffiliatedCorpo`) | 2 | CHOOH2 fuel, petrochemicals | Corpo Plaza tower `[canon]`; `Badlands_NorthSunriseOilField` `[infer]` | `PTRC` |

### 2.2 Profiles

#### Arasaka — `ARSK`
- **Affiliation:** `Arasaka` `[enum]`. Scannable on guards, drones, vehicles,
  and the `Character.arasaka_exo` record `[script]`.
- **Physical presence (all enum-verified):** `CorpoPlaza_ArasakaTowerLobby`,
  `…Atrium`, `…UpperAtrium`, `…CEOFloor`, `…SaburoOffice`, `…Jenkins`,
  `…Jungle`, `…Nest`, `…UnlistedFloors`; `ArasakaWaterfront`,
  `ArasakaWaterfront_KonpekiPlaza`, `ArasakaWaterfront_AbandonedWarehouse`
  (Watson); `Arroyo_Arasaka_Warehouse` (Santo Domingo);
  `NorthOaks_Arasaka_Estate` (Westbrook/North Oak).
- **Sector:** corporate security, banking, weapons, cyberware, heavy industry.
- **Market role:** the "flight to safety" ticker. Rises on NCPD crackdowns,
  corporate-security contracts, and Arasaka facility defence; falls on
  successful raids on Arasaka property, Waterfront sabotage, and public
  scandals. Highest beta to `CityCenter`/`Watson` heat.
- **Asset candidacy:** `ArasakaWaterfront_AbandonedWarehouse` is the best
  *entry-tier* corporate purchase (derelict, corp-branded, waterfront
  logistics). Tower floors are end-game prestige assets only.
- **Confidence:** buildings `[enum]`; ownership/sector `[canon]`.

#### Militech — `MLTC`
- **Affiliation:** `Militech` `[enum]`; also `gamedataVehicleManufacturer.Militech`
  `[enum]` (so vehicles carry the brand independently of NPC affiliation).
- **Physical presence:** Militech Offices in Corporate Plaza, directly opposite
  Arasaka Tower `[canon]`; `Dogtown_Cynosure` is the Militech Project Cynosure
  black site `[canon]`. No Militech entry exists in `gamedataDistrict`, so the
  Corpo Plaza building must be seeded as a `landmark` row keyed to the
  `CorpoPlaza` district record, **not** to a district enum value.
- **Sector:** arms manufacturing, private military, armored vehicles, AVs.
- **Market role:** the counter-weight to Arasaka. Rises on NCPD/municipal
  contracts, Barghest suppression, and NUSA federal spending; falls on arms
  embargoes, Cynosure exposure, and Dogtown losses. Natural hedge: long `MLTC`
  / short `ARSK` when city heat rises.
- **Asset candidacy:** Dogtown depot / Cynosure-adjacent logistics (PL-gated,
  high risk, high return). Corpo Plaza office floor = prestige.
- **Confidence:** affiliation/vehicle brand `[enum]`; buildings `[canon]`.

#### Kang Tao — `KTAO`
- **Affiliation:** `KangTao` `[enum]`.
- **Physical presence:** Kang Tao Building in Corporate Plaza, beside Petrochem
  Tower `[canon]`. Not a `gamedataDistrict` entry → `landmark` row under
  `CorpoPlaza`.
- **Sector:** smart weapons, drones, AVs, consumer electronics.
- **Market role:** high-beta arms/electronics. Rises on smart-weapon demand and
  drone contracts; falls on tech espionage, IP theft, and cargo interception.
- **Asset candidacy:** R&D floor (espionage missions), AV hangar (logistics).
- **Confidence:** affiliation `[enum]`; building `[canon]`.

#### Biotechnica — `BIOT`
- **Affiliation:** `Biotechnica` `[enum]`.
- **Physical presence:** `Badlands_BiotechnicaFlats` — a vast greenhouse/protein
  farm complex in the southern Badlands that supplies a large share of Night
  City's food `[enum+canon]`; Corpo Plaza office `[canon]`.
- **Sector:** protein/agriculture, pharmaceuticals, biotech, biofuel.
- **Market role:** the only *physical supply-chain* ticker. Rises on food
  scarcity, drought/storm events, and NCPD protection contracts; falls on
  greenhouse raids, contamination, and Crimson Harvest-style attacks. This is
  the best ticker for tying **Badlands territory ownership** to price.
- **Asset candidacy:** greenhouse block inside Biotechnica Flats (the single
  best "farm" asset for a Corp-path player), water/irrigation node.
- **Confidence:** district `[enum]`; role `[canon]`; the Corpo Plaza office is
  `[canon]` only.

#### Zetatech — `ZETA`
- **Affiliation:** `Zetatech` `[enum]`; `gamedataVehicleManufacturer.Zetatech`
  `[enum]`; `DevicesUIStyles.Zetatech` exists as a device UI style `[script]`.
- **Physical presence:** Zetatech Building on Berkeley Avenue, central Night
  City, its main city office `[canon]`. Not a district enum → `landmark` under
  the correct parent (City Center/Downtown; exact `District_Record` TBD).
- **Sector:** electronics, cyberware, AVs, netrunning hardware, vehicles.
- **Market role:** "picks and shovels" of the netrunner economy. Rises with
  cyberware demand and netrunner activity; falls on Blackwall incidents and
  data breaches. Low political exposure (declared neutral) ⇒ low volatility
  from turf wars, high volatility from tech events.
- **Asset candidacy:** AV pad, electronics plant, netrunner lab.
- **Confidence:** affiliation/brand `[enum]`; building `[canon]`.

#### Night Corp — `NGTCP`
- **Affiliation:** **none.** There is no `gamedataAffiliation.NightCorp`.
  Night Corp personnel presumably scan as `UnaffiliatedCorpo` or `Classified`.
  This is the single biggest gap in the corp catalog and must be handled with a
  synthetic faction id + `affiliation_enum = NULL`.
- **Physical presence:** Night Corp Headquarters, City Center / `Downtown`
  `[canon]` (the art book places it in Corporate Plaza; in-game the HQ is in the
  Downtown area — seed as `landmark` with `district = Downtown`, note the
  discrepancy).
- **Sector:** city infrastructure, utilities, construction, water, power,
  municipal contracts; covert behavioural research ("Project Oracle") `[canon]`.
- **Market role:** the municipal monopoly. Lowest beta, steadiest drift, but
  jumps on City Council policy, `CharterHill_PowerPlant` events, and
  infrastructure sabotage. Perfect "bond proxy" instrument.
- **Asset candidacy:** `CharterHill_PowerPlant` (utility asset — district-wide
  income modifier, not just a property), water treatment, construction yard.
- **Confidence:** HQ `[canon]`; power plant link is `[infer]` from the enum name.

#### NetWatch — `NTWT`
- **Affiliation:** `NetWatch` `[enum]`.
- **Physical presence:** headquartered in London `[canon]`; in Night City it
  operates through agents, checkpoints, and field outposts rather than a tower.
  Community sources place a NetWatch camp outside Night City `[canon]` — not
  enum-verified, so no district row yet.
- **Sector:** net security, Blackwall monitoring, netrunner interdiction.
- **Market role:** event-driven, low-float, quasi-sovereign. Spikes on
  Blackwall breaches, rogue-AI incidents, and mass netrunner activity; falls
  when netcrime goes unpoliced. Do **not** give it territory exposure.
- **Asset candidacy:** none (not purchasable). Use as a **mission client** and
  as a heat modifier for netrunner/espionage missions.
- **Confidence:** affiliation `[enum]`; posture `[canon]`.

#### Trauma Team — `TRMA`
- **Affiliation:** `TraumaTeam` `[enum]` (AVs and medics spawn citywide).
- **Physical presence:** AV response across all districts `[script]`; a
  Trauma Team tower exists in 2020/RED lore `[canon]` but no 2077 interior or
  district entry is verified. Treat as a **service overlay**, not a building.
- **Sector:** private emergency medicine, subscription insurance, AV logistics.
- **Market role:** inverse-violence ticker. Rises with citywide heat, cyberpsycho
  incidents, gang violence, and platinum-subscription penetration; falls when
  NCPD response improves or violence drops. Great causally-legible instrument
  for players ("my raids made TRMA go up").
- **Asset candidacy:** district med-bay / AV pad (upgradeable facility that
  reduces player org casualty losses).
- **Confidence:** affiliation `[enum]`; business model `[canon]`.

#### N54 / News54 — `NWS54`
- **Affiliation:** `News54` `[enum]`.
- **Physical presence:** Network 54 offices in `Downtown`, City Center `[canon]`.
  **Do not confuse** with `Northside_WNS` (World News Service, a different
  outlet with its own district record in Watson).
- **Sector:** broadcast news, advertising, propaganda.
- **Market role:** attention economy. Rises on scandal, crisis, and war
  coverage; falls on media repression and network sabotage. Natural vehicle for
  **Espionage** missions (plant a story, bury a story, blackmail a councillor).
- **Asset candidacy:** broadcast floor (media asset → org notoriety multiplier).
- **Confidence:** affiliation `[enum]`; building `[canon]`.

#### Orbital Air — `ORBA`
- **Affiliation:** `OA` `[enum]` (note: the enum value is `OA`, not
  `OrbitalAir` — a seed file must not guess the spelling).
- **Physical presence:** `Badlands_Spaceport` — the Orbital Air Space Center and
  launch/terminal complex `[enum+canon]`.
- **Sector:** orbital launch, heavy cargo, tourism, high-value smuggling.
- **Market role:** the "exports" ticker. Rises on launch cadence and cargo
  throughput; falls on smuggling crackdowns, launch failures, and border
  closures at `Badlands_SoCalBorderCrossing`.
- **Asset candidacy:** spaceport hangar/warehouse (best high-tier logistics
  asset; excellent target for the deferred Road-Chunk Transit Ledger).
- **Confidence:** district `[enum]`; operator `[canon]`.

#### Kiroshi — `KIRO`
- **Affiliation:** **none.** No `gamedataAffiliation.Kiroshi`; optics appear only
  as items (`Items.AdvancedKiroshiOptics_*`, `AttachmentSlots.KiroshiOpticsSlot1..3`)
  `[enum/script]`.
- **Physical presence:** no verified building; Kiroshi is a *channel* brand sold
  through ripperdocs `[script]`. Seed as `landmark`-less faction with
  `vendor_channel = ripperdoc`.
- **Sector:** optics, cyberware.
- **Market role:** consumer-cyberware proxy. Rises with player/merc cyberware
  spend and ripperdoc footfall; falls on cyberware regulation and black-market
  undercutting.
- **Asset candidacy:** none (license/clinic partnership instead).
- **Confidence:** items `[enum/script]`; corporate status `[canon]`.

#### Kendachi — `KEND`
- **Affiliation:** **none.** No affiliation record and no item-brand enum entry
  beyond the district name.
- **Physical presence:** `Arroyo_Kendachi` — a Kendachi site in Arroyo, Santo
  Domingo `[enum+infer]` (the record exists; that it is a Kendachi plant is
  inferred from the name and Kendachi's melee-weapons business).
- **Sector:** melee weapons, monofilament/monowire, industrial cutting.
- **Market role:** niche industrial ticker; low volume, spiky on melee/industrial
  contracts. Good "penny stock" for early player capital.
- **Asset candidacy:** the Arroyo plant itself — a plausible first *industrial*
  Corp asset with a small, legible income stream.
- **Confidence:** district `[enum]`; role `[infer]`.

#### SSI — Secure Services Inc. — `SSI`
- **Affiliation:** `SSI` `[enum]`.
- **Physical presence:** no HQ; deployed as the Peralezes' private security and
  surveillance detail `[canon]`, tied to the `Dream On` thread.
- **Sector:** private security, protective intelligence, covert behavioural
  operations (front for a higher actor).
- **Market role:** private/untraded `[design]`. If the player wants an SSI
  instrument, use it as an **event contract** rather than equity.
- **Sandbox role:** the canonical "security contractor that is actually a front"
  — ideal antagonist/client for Espionage missions and for the Corp path's
  first hostile takeover.
- **Confidence:** affiliation `[enum]`; role `[canon]`.

#### Budget Arms — `BDA`
- **Affiliation:** **none.** No affiliation record. `corpbud` is **not** Budget
  Arms (see §4.9).
- **Physical presence:** products only; no building, no district entry.
- **Sector:** ultra-cheap disposable firearms.
- **Market role:** volume/commodity arms proxy; inverse of premium arms
  (Arasaka/Militech) during economic downturns. Optional flavour ticker.
- **Confidence:** brand `[canon]`; nothing else verified.

#### Petrochem — `PTRC` (mentioned for completeness)
- **Affiliation:** **none.** Notable gap: Petrochem is a top-tier corp with a
  Corpo Plaza tower `[canon]` but its NPCs have no affiliation enum, so it will
  scan as `UnaffiliatedCorpo`.
- **Physical presence:** Corpo Plaza tower `[canon]`;
  `Badlands_NorthSunriseOilField` `[infer]` as its extraction site.
- **Sector:** CHOOH2, oil, refining, fuel distribution.
- **Market role:** energy input cost for every other ticker. Rises on fuel
  scarcity and convoy disruption; falls on fuel substitution and Biotechnica
  biofuel gains. Strong hook for the transit ledger (fuel convoys).
- **Asset candidacy:** oil field pump station, fuel depot.

### 2.3 Secondary corporations (mention-only, do not model in v0.1–0.4)

`Arroyo_CytechFactory` (Cytech manufacturing), `RanchoCoronado_Softsys`
(software), `Downtown_Jinguji` (Jinguji retail), `Northside_WNS` (World News
Service broadcast), `MorroRock_NCX` (broadcast/relay site), `EMB Petrochem
Stadium` in Dogtown `[canon]`, Raven Microcybernetics, Dynalar, Moore
Technologies, Tsunami Defense Systems, Merrill Asuka & Finch. Each has either a
district record, a lore role, or both — but no affiliation enum and no
market-relevant behaviour that the four pillars need. Add them as `landmarks`
only when a mission needs the location.

---

## 3. Fixers

Fixers are **not** territory holders. In `gamedataAffiliation` none of them
appear (only the `AfterlifeMercs` guild tag exists), so the **Fixer Network**
faction category from the glossary must be synthetic, with `influence` instead
of `territory`.

### 3.1 Summary

| Fixer | Jurisdiction (district records) | Physical hub | Gangs / corps in orbit | Post-campaign sandbox role `[design]` |
| --- | --- | --- | --- | --- |
| Regina Jones | `Watson` — `Kabuki`, `LittleChina`, `Northside`, `ArasakaWaterfront` `[canon]` | Corpo-owned apartment block in Kabuki `[canon]`; no district enum | Tyger Claws, Maelstrom, Scavengers; ex-media (N54-adjacent) | Watson contract broker; anti-trafficking bias; pays premium for Scavenger disruption |
| Wakako Okada | `Westbrook` — `JapanTown`, `CharterHill` `[canon]` | `JapanTown_Wakakos_Pachinko_Parlor` `[enum]` | Tyger Claws (family ties), Arasaka (cautious), Zetatech | Westbrook broker; the "respectable" fixer; gates Japantown/Charter Hill assets |
| Sebastian "Padre" Ibarra | `Heywood` — `Wellsprings`, `Glen`, `VistaDelRey` `[canon]` | Wellsprings, Heywood `[canon]` (church/community anchor; no enum) | Valentinos, 6th Street; City Council contacts | Heywood broker + civic broker; can launder org reputation, mediate with NCPD |
| Muamar "El Capitán" Reyes | `SantoDomingo` — `RanchoCoronado`, `Arroyo` `[canon]` | Garage in southern `RanchoCoronado` `[canon]`; no enum | 6th Street, Valentinos; vehicle trade | Santo Domingo broker; **vehicle/transport** specialist → transit ledger client |
| Dakota Smith | `Badlands` — `Badlands_RockyRidge`, southern camps `[canon]` | Auto repair shop in `Badlands_RockyRidge` `[canon]` | Aldecaldos, Wraiths (enemy) | Badlands broker; nomad logistics; convoy escort/raid missions |
| Dino Dinovic | `CityCenter` — `Downtown`, `CorpoPlaza` `[canon]` | Electric Orgasm bar, `Downtown` `[canon]` | Corpos, high-tier mercs, media | City Center broker; corporate espionage and nightlife contracts |
| Rogue Amendiares | citywide (Afterlife) `[canon]` | `LittleChina_Afterlife` `[enum]` | AfterlifeMercs; all major players | endgame broker / mercenary guild master; unlocks high-tier missions |
| Mr. Hands | `Pacifica` + `Dogtown` `[canon]` | Heavy Hearts Club, Dogtown `[canon]`; Pacifica gigs pre-PL | Barghest (transactional), NUSA/FIA, Voodoo Boys | Dogtown/Pacifica broker; the political/espionage channel |
| Faraday | `Pacifica` (Voodoo Boys-adjacent) `[canon]` | none persistent | Voodoo Boys, NetWatch (double game) | **removed** — see §3.3 |
| Dexter DeShawn | `Watson` (Heist) `[canon]` | none persistent | none | **removed** — see §3.3 |

### 3.2 Profiles and notes

- **Regina Jones** — Watson fixer, ex-media. Covers `Kabuki`, `LittleChina`,
  `Northside`, and the `ArasakaWaterfront` fringe `[canon]`. Her gigs are the
  densest early-game contract source, which makes her the natural **tutorial
  broker** for the Dynamic Mission Generator. Post-campaign: keep her hostile to
  human trafficking (Scavengers) and neutral to The Mox.
- **Wakako Okada** — Westbrook fixer, operates from
  `JapanTown_Wakakos_Pachinko_Parlor` `[enum]`. The pachinko parlor is a
  **verified district record**, so it is the only fixer hub that can be seeded
  from enum data alone. Her family ties to Tyger Claws make her the natural
  intermediary for Japantown/Charter Hill purchases.
- **Sebastian "Padre" Ibarra** — Heywood fixer, ex-priest, based in Wellsprings
  `[canon]`. Wellsprings has a district record but no sub-location enum, so his
  hub needs a `landmark` row with `source = TBD`. **Design value:** he is the
  cleanest bridge between the gang path and the civic path (City Council,
  NCPD, community legitimacy).
- **Muamar "El Capitán" Reyes** — Santo Domingo fixer, garage in southern
  `RanchoCoronado` `[canon]`. Vehicle-theft/transport gigs → the natural client
  for the deferred **Road-Chunk Vehicle Transit Ledger**. Do **not** confuse him
  with `Dogtown_CapitanCaliente`: that record is an **abandoned restaurant in
  Eden Plaza, Dogtown** used by a PL main job, *not* El Capitán's base `[canon]`.
  This is exactly the kind of name collision that would create a fake control
  center if the seed were generated from string matching.
- **Dakota Smith** — Badlands fixer at an auto repair shop in
  `Badlands_RockyRidge` `[canon]`. Aldecaldo-adjacent, hostile to Wraiths. Her
  hub is the natural Badlands logistics anchor and pairs with
  `Badlands_YuccaGarage` and `Badlands_Spaceport`.
- **Dino Dinovic** — City Center fixer, owns the Electric Orgasm bar in
  `Downtown` `[canon]`. Covers `Downtown` and `CorpoPlaza`. Because City Center
  has no gang turf, Dino is the main **non-corp** contract source there — useful
  for keeping City Center playable without inventing gang control.
- **Rogue Amendiares** — runs the Afterlife in `LittleChina_Afterlife` `[enum]`,
  the `AfterlifeMercs` hub. Post-campaign she is the **guild master**: unlock
  condition for tier-3+ missions, merc hiring, and cross-faction introductions.
  Her survival is ending-dependent `[canon]` — the sandbox must not hard-require
  her; fall back to a generic Afterlife "concierge" if the save says otherwise.
- **Mr. Hands** — Pacifica pre-PL, Dogtown in PL; in-person at the Heavy Hearts
  Club `[canon]`. He is the **political/espionage** broker and the natural
  mission source for NUSA/FIA, Barghest, and Dogtown assets. Dogtown is
  PL-gated, so his availability must be era-checked by the Sandbox Sanitizer.

### 3.3 Removed fixers (status honesty)

- **Faraday** — Pacifica/Voodoo Boys-adjacent fixer; his arc ends with his death
  at the close of `Transmission` `[canon]`. He must **not** be in the fixer pool
  for post-campaign saves. If a pre-`Transmission` save loads, he may exist as a
  temporary broker with a `scripted_death` flag.
- **Dexter DeShawn** — Heist-era fixer; killed during the prologue `[canon]`.
  Never a sandbox broker. Keep only as a historical/quest reference.
- Note for the record: the *Edgerunners* character Faraday is a different person
  from the 2077 game fixer; do not merge their lore.

### 3.4 Fixer network model (design hooks)

- Fixers hold **influence**, not territory: `fixer_influence(fixer_id,
  district_id, influence)` with 0–100 per district. Territory flips and mission
  outcomes move influence; influence gates contract tier and price.
- Each fixer has `bias` tags (e.g. Regina: `anti_trafficking`; Padre:
  `civic_legitimacy`; Dakota: `nomad_logistics`; Dino: `corp_espionage`) that
  weight mission templates.
- Fixers should be **suppressible but not deletable** by the Sandbox Sanitizer:
  vanilla gig calls are blocked (`PhoneSystem.OnTriggerCall`), but the NPC and
  their hub remain in the world so Neon Ascendancy can reuse them.
- Fixers are the cheapest way to give City Center and Badlands content without
  inventing corp or gang control there.

---

## 4. Civic & independent powers

### 4.1 NCPD — `NCPD`

**Evidence.** `gamedataAffiliation.NCPD` `[enum]`; vehicles check
`vehicleRecord.Affiliation().Type() == NCPD` `[script]`; the prevention system
owns a five-to-six stage heat model `[script]`.

**Structure to model**

| Concept | Game data | Design use `[design]` |
| --- | --- | --- |
| Heat stages | `EPreventionHeatStage.Heat_0 … Heat_5` `[enum]` | map to a 0–100 `district_heat` scalar with 6 bands |
| Per-district preset | `District_Record.PreventionPreset()` → `DistrictPreventionData_Record` `[record]` | **never hardcode "NCPD"**: read the preset per district; fall back to `PreventionData.NCPD` only when invalid `[script]` |
| Stage payload | `Heat1()`…`Heat5()`, `Recon()` `[record]` | unit count, spawn range, spawn interval, vehicle pool per band |
| District crime scale | `District_Record.CrimeMultiplier()` `[script]` | `heat_gain = base_crime * multiplier`; gives poor districts faster escalation |
| Gunshot/explosion radius | `GunShotStimRange()`, `ExplosiveDeviceStimRangeMultiplier()` `[record]` | how far a firefight pulls patrols — directly reusable for mission "noise" |
| MaxTac | heat 5; `MaxTac` NPC rarity; AV spawn capped at 1 concurrent `[script]` | tier-3+ retaliation unit; a raid that drags on should summon MaxTac |
| Dogtown override | `PreventionData.DogTownDataMatrix`, `DogTown_Kurt_DataMatrix`, `DogTown_Bennet_DataMatrix` `[script]` | Dogtown police are Barghest-flavoured; separate heat table |
| Districts with no record | fallback `t"PreventionData.NCPD"` `[script]` | safe default for synthetic sub-territories |

**Physical anchors**

| Anchor | District record | Confidence |
| --- | --- | --- |
| NCPD laboratory | `Glen_NCPDLab` | `[enum]` (Heywood / The Glen) |
| Night City Hall (municipal, adjacent to NCPD politics) | `Glen` | `[canon]` |
| NCPD HQ building (in-game, barricaded) | district TBD — verify in world data | `[canon]`, **not** enum-verified |
| District precincts | no enum records; per-district TBD | `[canon]` |

**Sandbox role.** NCPD is a **pressure faction**, not a turf faction. It should
own `heat`, not polygons. Player options: pay fines, bribe, do NCPD contracts
(the `HasLinkToBountySystem` stat exists on characters `[script]`), or fight.
Post-campaign, an NCPD "contract" income stream is a clean way to reward
low-heat play.

### 4.2 City Council — `CityCouncil`

- **Affiliation:** `CityCouncil` `[enum]` — confirmed as a scannable faction.
- **Seat of government:** Night City Hall, in `Glen`, Heywood `[canon]`.
- **Known figures:** Councilwoman Cole (target of a Dino gig) `[canon]`;
  Jefferson Peralez (mayoral candidate) `[canon]`.
- **Sandbox role:** the **licensing and zoning gate** for the Corp path.
  Purchasing a corporate asset above a value threshold should require a council
  permit; permits can be bought, blackmailed, or earned. Policy events
  (tax change, NCPD funding, corp incentive) are excellent `SimEvent` sources
  that move `NGTCP`, `TRMA`, and `MLTC`.
- **Physical control center:** City Hall plaza (`Glen`) — a civic, non-gang
  control center candidate, which makes Heywood's five anchors achievable.

### 4.3 NCP Prison — `NCPrison`

- **Affiliation:** `NCPrison` `[enum]`.
- **Physical presence:** no district record; prison facility location TBD.
- **Sandbox role:** mission target (breakout, inmate extraction, contraband) and
  a "corrections contract" income for a corp/gang with political cover. Low
  priority for v0.1; keep as a mission template only.

### 4.4 NUSA — `NUSA`

- **Affiliation:** `NUSA` `[enum]` (federal; FIA agents, Reed/Myers arc).
- **Physical presence:** no Night City building; presence via Dogtown operations
  and federal installations `[canon]`.
- **Sandbox role:** top-tier **espionage client** and the only actor that can
  override City Council. Federal contracts should pay the most and generate the
  most heat. Do not give NUSA territory.

### 4.5 Afterlife Mercs — `AfterlifeMercs`

- **Affiliation:** `AfterlifeMercs` `[enum]`.
- **Hub:** `LittleChina_Afterlife` `[enum]` — a verified district record.
- **Sandbox role:** the **mercenary labour market**. Hiring, contract tiers,
  reputation. This is the cleanest non-gang faction to own a Control Center in
  Little China without duplicating gang turf.

### 4.6 Delamain — no affiliation enum

Delamain has **no `gamedataAffiliation` entry**, yet it is one of the most
mechanically real independents in the game:

- **HQ verified by district record:** `Vista_del_Rey_Delamain` `[enum]` — the
  Delamain depot/HQ in Vista del Rey, Heywood.
- **Fleet is a live system:** `DelamainTaxiSystem`, `DelamainTaxiComponent`,
  `DelamainTaxiState` (`Spawned`, `Parked`, `Started`, `Freeroam`, `Arrived`,
  `Cancelled`, `Ready`), `PayTravelRequest`, `CancelDelamainRideRequest`
  `[script]`.
- **Brand:** `gamedataVehicleManufacturer.Delamain` `[enum]`.
- **Map presence:** `gamedataMappinVariant.Zzz19_DelamainTaxiVariant` and
  `Zzz20_DelamainTaxiDestinationVariant` `[enum]`.
- **Post-campaign dependency:** `Don't Lose Your Mind` has mutually exclusive
  outcomes (merge / destroy / reset) `[canon]`. The sandbox must read the quest
  fact and degrade the fleet if Delamain was destroyed. **Do not** assume the
  fleet exists.
- **Sandbox role:** mobility utility + logistics contractor. A Delamain depot
  is an excellent **purchasable asset** for a Corp path (transport income,
  transit-ledger integration), and `Vista_del_Rey_Delamain` gives Heywood a
  corporate-flavoured anchor that is not a gang.

### 4.7 The Mox — `TheMox`

- **Affiliation:** `TheMox` `[enum]`. The glossary example lists The Mox under
  Civic/Independent; the game treats it as a gang affiliation. Pick one
  classification and keep it consistent: recommended **Gang** in
  `factions.category`, with `civic_aligned = true`.
- **Hub:** `Kabuki_LizziesBar` `[enum]` — Lizzie's Bar, Kabuki, Watson.
- **Sandbox role:** neutral-ish protector faction; hostile to trafficking and
  to Maelstrom. Ideal "ally" for a player who wants low-heat income in Kabuki.

### 4.8 Recording Agency — `RecordingAgency`

- **Affiliation:** `RecordingAgency` `[enum]`.
- **Likely anchor:** `JapanTown_FourthWallBdStudio` `[enum]` (Fourth Wall BD
  studio, Japantown) `[infer]`.
- **Sandbox role:** braindance production = **blackmail material** and
  **Espionage mission** source. Low priority, but it is the only "industry"
  affiliation that is neither corp nor gang, so it is worth keeping as a
  mission-template flavour rather than a faction with territory.

### 4.9 Unresolved / low-value affiliation tags

| Tag | Status | Recommendation |
| --- | --- | --- |
| `corpbud` | **Unresolved.** Documented as a selectable vendor affiliation in CDPR's VendorsXL guide, alongside `Zetatech`, `OA`, `NUSA`, `Crimson_Harvest`, `Private_Press`, `Growl`, `Highriders` `[canon]`. No lore corp of that name. It is **not** Budget Arms. | Do **not** create a faction row. Treat as a generic "corporate budget/brand" NPC tag; map to `UnaffiliatedCorpo` for simulation. Flag for verification in TweakDB (`Affiliation.corpbud` record). |
| `crimson_harvest` | Anti-corporate terrorist organisation, PL-era `[canon]` | Mission antagonist only; no territory. Good source of `MarketShock` events against `BIOT`. |
| `growl` | Growl FM radio affiliation `[canon]` | Media flavour; no faction row. |
| `highriders` | Orbital-habitat population `[canon]` | Not present in Night City; skip. |
| `private_press` | Independent press `[canon]` | Media flavour; useful for N54 rivalry stories. |
| `SouthCalifornia` | State-level government `[canon]` | Mention-only; NUSA covers federal. |
| `Classified` / `REDACTED` / `Unknown` | Spoiler-safe labels `[enum]` | Map to `Unknown` internally; never display raw. |
| `Civilian` / `Unaffiliated` / `UnaffiliatedCorpo` | Non-factions `[enum]` | `civilian` bucket; excluded from ownership. |
| `*Android` / `Wraiths_Former` | Variants `[enum]` | Collapse to parent faction on import. |

### 4.10 Civics with no affiliation enum (seed as `landmark` only)

Night City Hall (`Glen`), NCPD HQ (district TBD), `MorroRock_NCX`,
`Langley_Clinic`, `Northside_WNS`, `Downtown_Jinguji`, `RanchoCoronado_GunORama`,
`RanchoCoronado_Stylishly`, `RanchoCoronado_Piez`, `Arroyo_TireEmpire`,
`Arroyo_KenmoreCafe`, `Arroyo_LasPalapas`, `Arroyo_Red_Dirt`,
`Arroyo_ClairesGarage`, `Kabuki_NoTellMotel`, `LittleChina_RiotClub`,
`LittleChina_TomsDiner`, `JapanTown_DarkMatter`, `JapanTown_Clouds`,
`JapanTown_MegabuildingH8`, `NorthOaks_Columbarium`, `Glen_Embers`,
`Downtown_TheHammer`, `Coastview_ButcherShop`, `Dogtown_Akebono`,
`Dogtown_Brooklyn`, `Dogtown_Expo`, `Badlands_YuccaRadioTower`,
`Badlands_YuccaGarage`, `SouthBadlands_TrailerPark`,
`SouthBadlands_EdgewoodFarm`, `SouthBadlands_PoppyFarm`.
Each is enum-verified as a location; most roles are `[infer]` from the name.

---

## 5. Strategic assets: control centers and purchasable targets

### 5.1 Selection rules (apply before any coordinate work)

`[design]` — derived from verified constraints, not invented lore:

1. **Anchor must be a district record or a named landmark inside one.** No
   synthetic place names.
2. **Exclude interiors that only exist for a quest.** Heuristic: records ending
   in `_q1xxCyberspace`, `_q201Cyberspace`, `_q110Cyberspace`, `_Hideout`,
   `_Apartment`, `_VR_Tutorial`, `_Worldmap_Sub` are **not** control centers.
   Check `District_Record.IsQuestDistrict()` `[record]`. Tower lobbies/atriums
   are only public in specific quest states — treat them as landmark-only until
   accessibility is verified in-game.
3. **Prefer open-air or street-level anchors** with room for 8–20 NPCs and a
   vehicle spawn: plazas, markets, garages, depots, bars, terminals.
4. **Prefer anchors that already have a fast-travel point or metro station** —
   `FastTravelPoint_Record` / `ENcartStations` prove the player can reach them
   in every era (Step 0.1).
5. **One Control Center per sub-territory, ~5 per top-level district.** Badlands
   is geographically enormous; allow 6–8 and treat "5" as a floor, not a cap.
6. **No corp-owned anchor becomes gang turf.** Corpo Plaza and Charter Hill
   should be **asset/contest** zones (buy, raid, sabotage), not gang capture
   zones — otherwise the map contradicts the fiction and Arasaka Tower becomes
   a gang hideout.
7. **Dogtown is era-gated.** Only seed Dogtown anchors when the save has PL
   content; otherwise the map overlay must not paint an inaccessible district.

### 5.2 District coverage matrix

`Anchor count` = enum records available in that top-level district (a proxy for
granularity, **not** a spawn count).

> **Coordination with step 0.2a.** The gang-owned sub-territory partition is
> owned by `docs/research/factions-gangs-territories.md` (6/5/5/5/5/5/7/6
> sub-territories). This matrix is **not** a competing partition: it only names
> the corp/civic/fixer anchors that the gang partition cannot represent
> (Corpo Plaza, Charter Hill, City Hall, Delamain, Biotechnica Flats, Spaceport,
> Cynosure). Where the two overlap, the gang document wins and this table's
> anchor becomes a landmark inside that sub-territory.

| Top-level district | Sub-districts (records) | Anchor count | Proposed control centers (5) | Notes |
| --- | --- | --- | --- | --- |
| Watson | `Kabuki`, `LittleChina`, `Northside`, `ArasakaWaterfront`, parent `Watson` | 22 | `Kabuki_LizziesBar` (Mox), `LittleChina_Afterlife` (AfterlifeMercs), `Northside_All_Foods` (Maelstrom turf), `Northside_Totentaz` (club), `ArasakaWaterfront_AbandonedWarehouse` (corp/contest) | densest district; 3 gang + 1 fixer-guild + 1 corp anchor |
| Westbrook | `JapanTown`, `CharterHill`, `NorthOaks`, parent `Westbrook` | 19 | `JapanTown_Wakakos_Pachinko_Parlor` (fixer), `JapanTown_Clouds` (Tyger Claws), `CharterHill_PowerPlant` (utility/contest), `NorthOaks_Arasaka_Estate` (corp), `JapanTown_DarkMatter` (nightlife) | mix of fixer, gang, corp, utility |
| Heywood | `Wellsprings`, `Glen`, `VistaDelRey`, parent `Heywood` | 13 | `Glen` (City Hall civic anchor), `Glen_NCPDLab` (NCPD), `Vista_del_Rey_Delamain` (Delamain), `Vista_del_rey_ElCoyoteCojo` (Valentinos), `Wellsprings` (Padre) | only district where civic assets outnumber gang assets |
| Santo Domingo | `Arroyo`, `RanchoCoronado`, parent `SantoDomingo` | 16 | `Arroyo_Kendachi` (industrial), `Arroyo_Arasaka_Warehouse` (corp), `Arroyo_TireEmpire` (street), `RanchoCoronado_GunORama` (retail), El Capitán garage (fixer, TBD id) | the "working city" district; best Corp-path industrial assets |
| Pacifica | `Coastview`, `WestWindEstate`, parent `Pacifica` | 10 | `Coastview_GrandImperialMall` (Animals), `Coastview_VDBChapel` (Voodoo Boys), `Coastview_VDBMaglev` (VDB), `Coastview_BattysHotel`, `WestWindEstate` (residential) | no corp presence; pure gang/combat zone |
| City Center | `CorpoPlaza`, `Downtown`, parent `CityCenter` | 16 | Arasaka Tower atrium (corp, **contest only**), Militech Offices (corp, landmark TBD), `Downtown` (Night Corp HQ + N54), `Downtown_TheHammer`, `CorpoPlaza` plaza | **no gang ownership**; ownership model = corp asset control + NCPD heat |
| Badlands | `NorthBadlands`, `SouthBadlands`, 21 named areas | 24 | `Badlands_BiotechnicaFlats` (corp/agri), `Badlands_Spaceport` (Orbital Air), `Badlands_RockyRidge` (Dakota/Aldecaldos), `Badlands_NorthSunriseOilField` (Petrochem `[infer]`), `Badlands_SoCalBorderCrossing` (smuggling); optional `Badlands_Yucca`, `Badlands_RedPeaks` | allow 7; convoy/transit content lives here |
| Dogtown | `Dogtown` + 7 sub-areas | 8 | Black Sapphire (Barghest HQ, TBD id), `Dogtown_Expo`, `Dogtown_Cynosure` (Militech black site), `Dogtown_CapitanCaliente` (Eden Plaza), Heavy Hearts Club (Mr. Hands, TBD id) | PL-gated; Barghest = police + owner simultaneously |

**Total:** 40 anchors (≈5 × 8 districts), with Badlands tunable to 7.

### 5.3 Purchasable Corporation HQ / asset targets (Pillar 3)

Price bands are `[design]` and deliberately wide; they exist to rank assets, not
to fix economy numbers.

| Tier | Asset | Anchor | Why it works | Price band (eddies) |
| --- | --- | --- | --- | --- |
| 1 — starter | Derelict warehouse | `ArasakaWaterfront_AbandonedWarehouse` | corp-branded, waterfront logistics, low NPC density, no gang owner | 150k–300k |
| 1 — starter | Street retail | `RanchoCoronado_GunORama` | legal front, steady small income, 6th Street pressure | 200k–400k |
| 2 — industrial | Kendachi plant | `Arroyo_Kendachi` | manufacturing income, NCPD heat from industrial accidents | 800k–1.5M |
| 2 — industrial | Cytech factory | `Arroyo_CytechFactory` | electronics output, ties to `ZETA`/`KTAO` supply | 700k–1.3M |
| 2 — agri | Greenhouse block | `Badlands_BiotechnicaFlats` | food supply → `BIOT` exposure, weather/raid risk | 900k–1.8M |
| 2 — mobility | Delamain depot | `Vista_del_Rey_Delamain` | transport income + transit-ledger integration (quest-state gated) | 600k–1.2M |
| 3 — infrastructure | Power plant | `CharterHill_PowerPlant` | district-wide income modifier; Night Corp entanglement | 3M–6M |
| 3 — media | Broadcast floor | `Northside_WNS` or N54 offices (`Downtown`) | notoriety multiplier, propaganda missions | 2M–4M |
| 3 — logistics | Spaceport hangar | `Badlands_Spaceport` | highest throughput, smuggling and federal attention | 5M–10M |
| 4 — prestige | Corpo Plaza office floor | `CorpoPlaza_ArasakaTowerUnlistedFloors` (or Militech/Kang Tao towers) | legitimacy, market signal, extreme price and heat | 10M–25M |
| 4 — black | Cynosure bunker | `Dogtown_Cynosure` | unique tech, Militech retaliation, PL-gated | 8M–15M |

**Purchase gate chain** `[design]`: capital → City Council permit (`CityCouncil`)
→ physical handover mission (owner defends, NCPD or gang interference) →
registered asset row → income + market exposure. This gives Pillar 3 a
three-beat loop per asset instead of a shop menu.

### 5.4 Coordinates

Every control center, landmark, HQ, purchase target, and spawn point in this
document: **`TBD (extract from game data)`**. Section 7 is the extraction plan.

---

## 6. Stock Market design hooks

### 6.1 Instruments

`[design]`

1. **Equity** — one ticker per modeled corp (table below). Price = f(sector
   drift, district exposure, event shocks, player manipulation).
2. **Short positions** — allowed on all equities; borrow cost scales with
   volatility and with the player's `OrgNotoriety`.
3. **District index (`NCRE`)** — a cap-weighted basket of district asset values;
   rises when territory is stable and productive, falls on contest/heat.
   This is how gang play plugs into the market without a gang ticker.
4. **Municipal bond (`NCB`)** — Night Corp / City Council credit; yields rise
   with citywide heat and NCPD funding gaps.
5. **Private/event contracts** — NetWatch, SSI, NUSA: not equities; binary
   payouts on espionage outcomes.

Deliberately **not** included: per-gang tickers (gangs do not have public
capital), crypto, or per-mission "stock tips". Keep the market legible.

### 6.2 Ticker table

| Ticker | Corp | Sector | Float `[design]` | Beta | Positive drivers | Negative drivers |
| --- | --- | --- | --- | --- | --- | --- |
| `ARSK` | Arasaka | security/banking/arms | high | 0.9 | raids on rivals, NCPD crackdowns, tower defence, Waterfront throughput | Arasaka property raids, scandals, Waterfront sabotage |
| `MLTC` | Militech | arms/PMC | high | 1.1 | NCPD contracts, Barghest suppression, NUSA spending, Cynosure secrecy | arms embargo, Cynosure exposure, Dogtown losses |
| `KTAO` | Kang Tao | smart weapons/drones | mid | 1.4 | drone/smart-weapon demand, AV contracts | IP theft, cargo interception, espionage |
| `BIOT` | Biotechnica | agri/pharma | mid | 0.8 | food scarcity, greenhouse security, pharma demand | Flats raids, contamination, Crimson Harvest attacks |
| `ZETA` | Zetatech | electronics/cyberware | mid | 1.3 | cyberware demand, netrunner activity, AV sales | Blackwall incidents, data breaches, neutrality breaking |
| `NGTCP` | Night Corp | infrastructure/utilities | low | 0.4 | Council policy, plant uptime, construction contracts | sabotage, power outages, Oracle exposure |
| `NTWT` | NetWatch | net security | very low | 1.6 | Blackwall breaches, netrunner manhunts | unpoliced netcrime, jurisdiction losses |
| `TRMA` | Trauma Team | private medical | mid | 0.7 | citywide heat, cyberpsycho events, violence | calm periods, NCPD improvement, subscription churn |
| `NWS54` | N54 | media | mid | 1.2 | scandal, crisis, war coverage | media repression, network sabotage |
| `ORBA` | Orbital Air | orbital logistics | mid | 1.5 | launch cadence, cargo throughput, tourism | smuggling crackdowns, launch failures, border closures |
| `KIRO` | Kiroshi | optics | low | 1.0 | cyberware spend, ripperdoc footfall | regulation, black-market undercutting |
| `KEND` | Kendachi | melee/industrial | very low | 1.7 | industrial contracts, melee demand | cheap imports, plant raid |
| `PTRC` | Petrochem | fuel/energy | high | 0.9 | fuel scarcity, convoy disruption | biofuel substitution (`BIOT` up), depot raids |

### 6.3 `SimEvent` → market mapping

| SimEvent | Market effect `[design]` |
| --- | --- |
| `TerritoryOwnerChanged` | district index moves; each ticker has a signed exposure weight per district (`corp_district_exposure`) |
| `MissionCompleted` (Economic) | + corp exposure if the mission served that corp's asset; − rival |
| `MissionCompleted` (Espionage) | discrete shock to target ticker (−3%…−12% scaled by mission tier) |
| `MissionFailed` | inverse, plus volatility spike |
| `HeatChanged` | `TRMA` up, `NGTCP`/`NCB` down, `NTWT` up if netcrime-driven, `MLTC` up if NCPD-funded |
| `OrgNotorietyChanged` | player-org-linked assets move `NCRE`; high notoriety raises borrow cost and volatility |
| `IncomeSettled` | slow drift toward asset fair value (mean reversion) |
| `CycleElapsed` | sector drift + bounded noise, seeded deterministically per `(playthroughId, cycle)` |

Rules that keep this honest: one shock per event, bounded per-cycle move
(±8% default), no cross-ticker mutation outside the event queue, and the whole
market advances only on `CycleElapsed` or a discrete event — never per frame
(architecture §1.2).

### 6.4 Exposure weights (how to store them)

`corp_district_exposure(corp_id, district_id, weight)` with weights in
`[-1.0, +1.0]`. Suggested seed shape:

- `ARSK`: `+1.0` CityCenter, `+0.8` Watson (Waterfront), `+0.4` Westbrook (North Oak)
- `MLTC`: `+1.0` CityCenter, `+0.7` Dogtown, `+0.3` Santo Domingo
- `BIOT`: `+1.0` Badlands, `+0.3` CityCenter
- `ORBA`: `+1.0` Badlands (Spaceport)
- `NGTCP`: `+0.9` City Center (Downtown), `+0.6` Westbrook (Charter Hill), `+0.5` all others
- `TRMA`: uniform `+0.5` citywide, `0.0` Badlands
- `KEND`: `+0.8` Santo Domingo (Arroyo)
- `KIRO`: uniform `+0.3` (channel brand, no single district)

This table is the bridge between Pillar 1 (territory) and Pillar 4 (market):
a territory flip in Arroyo should visibly move `KEND` and `MLTC`, and barely
move `ORBA`.

---

## 7. Data extraction backlog (turning names into coordinates)

Everything below uses verified APIs. Nothing here requires guessing.

1. **District tree + per-district affiliation sets**
   `MappinUtils.GetDistrictRecord(districtType)` for every
   `gamedataDistrict` value `0…131`; read `EnumName()`, `LocalizedName()`,
   `Type()`, `ParentDistrict()`, `PreventionPreset()`, `Gangs()`,
   `CrimeMultiplier()`, `GunShotStimRange()`, `UiIcon()`, `IsQuestDistrict()`.
   Output: `districts` + `district_affiliations` seed files.
   This also gives the **authoritative gang set per district** — cross-check it
   against the gang catalog instead of trusting map folklore.
2. **Open-world anchors with positions**
   Scan all `FastTravelPoint_Record`s, then resolve
   `FastTravelPointData.markerRef` (a `NodeRef`) to a world position.
   These are guaranteed reachable, era-stable anchors — ideal first
   `control_centers` coordinates. `ENcartStations` (19 stations) gives a second,
   coarser set for sanity checks.
3. **Gang/outpost mappins**
   `gamedataMappinVariant.OutpostVariant`, `GangWatchVariant`,
   `SmugglersDenVariant`, `Zzz22_CityTourLandmark` `[enum]` — registered mappins
   carry positions and are the best source for gang compound anchors and
   landmark seeds.
4. **Vendor/corp storefronts**
   `Vendor_Record.Faction()` → `Affiliation_Record.Type()`; join to the vendor's
   world position. Gives corp retail footprints (Kiroshi via ripperdocs,
   Zetatech/Kang Tao electronics, gun shops) per district.
5. **Prevention presets**
   Read `District_Record.PreventionPreset()` per district and store the exact
   TweakDB ID. Do not hardcode `PreventionData.NCPD`; it is only the fallback
   `[script]`.
6. **World spawn points**
   WolvenKit extraction of `.streamingsector` `worldSpawnPoint` /
   community nodes for `spawn_points` rows, tagged with the sector path. This is
   the only honest source for exact NPC spawn coordinates.
7. **Landmark interiors**
   Corpo Plaza towers (Arasaka, Militech, Kang Tao, Biotechnica, Petrochem),
   City Hall, NCPD HQ, Black Sapphire, Heavy Hearts, Padre's church, El Capitán's
   garage: no district record → store as `landmarks` with `source = manual` and
   coordinates `TBD` until extracted from world data.

**Acceptance gate for Step 0.4:** a `control_centers` row is valid only if it
has (a) a `district_id` from the enum, (b) a `source` field naming where the
position came from, and (c) a non-null position *or* an explicit
`TBD` marker that the generator rejects for shipping builds.

---

## 8. Gaps, risks and open questions

1. **`corpbud` is unexplained.** Do not model it as a corporation. Verify the
   `Affiliation.corpbud` TweakDB record before any UI text uses it.
2. **Night Corp, Kiroshi, Kendachi, Petrochem, Budget Arms have no affiliation
   enum.** They need synthetic faction ids. This also means a scan-based
   "which corp owns this NPC" check will silently fail for them.
3. **Corpo Plaza corp buildings are not district records.** Arasaka is the only
   tower with enum coverage (`CorpoPlaza_ArasakaTower*`). Militech, Kang Tao,
   Biotechnica, Petrochem towers must be landmarks, which makes them weaker map
   anchors (no `District_Record.IsQuestDistrict()` protection, no
   `PreventionPreset` inheritance).
4. **`Dogtown_CapitanCaliente` is a trap.** It is an abandoned restaurant in Eden
   Plaza used by a PL main job, not El Capitán's base. Name-matching would
   create a fake Muamar control center.
5. **Fixer hubs are mostly not district records.** Only
   `JapanTown_Wakakos_Pachinko_Parlor` and `LittleChina_Afterlife` are verified.
   Regina/Kabuki, Padre/Wellsprings, Muamar/Rancho Coronado, Dakota/Rocky Ridge,
   Dino/Downtown (Electric Orgasm), Mr. Hands/Dogtown (Heavy Hearts) need
   landmark rows.
6. **Dogtown is Phantom-Liberty gated.** Era detection must gate control
   centers, the map overlay, and Mr. Hands' contract pool.
7. **Ending-dependent actors.** Rogue and Delamain can be dead or permanently
   altered by an ending `[canon]`, and Barghest's leadership and Mr. Hands' role
   shift with Phantom Liberty outcomes. Every faction row that depends on a
   living NPC needs a `fallback_faction_id` and a save-fact guard.
8. **City Center has no gang turf.** Do not force five gang-owned control
   centers there. Use corp asset control + NCPD heat + Dino's contracts.
9. **Badlands granularity.** 21 named areas across a huge map will not fit
   "5 per district" cleanly; allow 7–8 and let the generator cluster them.
10. **Trauma Team and NetWatch have no purchasable real estate.** Their market
    exposure is event-driven only; do not invent buildings for them.
11. **`TheMox` classification conflict.** `gamedataAffiliation` treats it as a
    gang; the glossary example lists it as civic/independent. Choose one and
    document it before seeds are written.
12. **Affiliation indices are not stable API.** Store `EnumName()` strings, never
    ints; mods and patches can reorder enums.

---

## 9. Source index

**In-repo (primary, authoritative for names):**

- `refs/cyberpunk/orphans.swift:4474` — `gamedataAffiliation`
- `refs/cyberpunk/orphans.swift:4826` — `gamedataDistrict`
- `refs/cyberpunk/orphans.swift:1178` — `gamedataMappinVariant`
- `refs/cyberpunk/orphans.swift:5409` / `5439` — `gamedataVehicleModel` / `gamedataVehicleManufacturer`
- `refs/cyberpunk/orphans.swift:11119` — `ENcartStations`
- `refs/cyberpunk/orphans.swift:18375` — `FastTravelPoint_Record`
- `refs/cyberpunk/orphans.swift:18392` — `District_Record`
- `refs/cyberpunk/orphans.swift:29856` — `Affiliation_Record`
- `refs/cyberpunk/orphans.swift:16015` — `Vendor_Record`
- `refs/cyberpunk/orphans.swift:32827` — `DistrictPreventionData_Record`
- `refs/cyberpunk/orphans.swift:33503` — `PreventionHeatData_Record`
- `refs/cyberpunk/orphans.swift:9235` — `EPreventionHeatStage`
- `refs/cyberpunk/core/systems/prevention/districtManager.swift` — district stack, preset fallback, crime multiplier
- `refs/cyberpunk/core/systems/preventionSystem.swift` — heat stages, Dogtown matrices, MaxTac/AV rules
- `refs/cyberpunk/core/systems/prevention/policeAgentsRegistry.swift` — MaxTac registry, spawn distances
- `refs/cyberpunk/cyberpunk/NPC/NPCPuppet.swift` — `Affiliation()` on character records
- `refs/cyberpunk/core/systems/delamainTaxiSystem.swift`, `refs/cyberpunk/core/components/scriptComponents/delamainTaxiComponent.swift` — Delamain service state machine

**Out-of-repo (canon/community; flagged `[canon]`, must be re-verified):**

- Cyberpunk Wiki — Dino Dinovic (Electric Orgasm, Downtown), Muamar Reyes (Rancho
  Coronado garage), Dakota Smith (Rocky Ridge), Padre (Wellsprings), Mr. Hands
  (Heavy Hearts Club, Dogtown), Faraday (Transmission), Delamain outcomes.
- Cyberpunk Wiki — Night Corp HQ (City Center/Downtown), N54 offices (Downtown),
  Militech Offices / Kang Tao Building (Corporate Plaza), Zetatech Building
  (Berkeley Avenue), Biotechnica Flats, Orbital Air Spaceport, Night City Hall
  (The Glen).
- CDPR Modding Docs / VendorsXL — the affiliation picker list that documents
  `Corpbud`, `Crimson_Harvest`, `Private_Press`, `Growl`, `Highriders` as
  affiliation labels.
- Cyberpunk Wiki — SSI = Secure Services Inc., Peralez private security front.

**Explicit non-sources:** no coordinate was taken from a wiki, a map site, or a
mod. No game launch, no `git commit`, no subagents.
