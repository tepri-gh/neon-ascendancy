# Phase 0 Research Index

Six parallel research reports produced on 2026-11-23 using OpenCode Go
(DeepSeek V4.1 Flash 1017, `variant: high`), grounded in the local Cyberpunk
2077 2.5 install, `refs/cyberpunk`, `refs/RED4ext.SDK`, and `refs/cp2077-red-lib`.

| Report | Step | Key Takeaway |
| --- | --- | --- |
| [`campaign-sanitizer.md`](campaign-sanitizer.md) | 0.1 | Era-detection fact spine (`> 0` checks; never force `q005_done`/`q101_done`), Tier 1 redscript gates (`PhoneSystem.OnTriggerCall` preserving `EndCall`, `InteractionUIBase.OnDialogsData`, `CreateMappinUIProfile`, `JohnnySickness` removal), and a 10-minute CET verification playbook for 7 in-game unknowns (including 2.2/2.3 passenger Johnny). |
| [`factions-gangs-territories.md`](factions-gangs-territories.md) | 0.2a | All 132 `gamedataDistrict` entries (8 top-level, 40 sub-districts, 84 named locations) and all 11 gangs mapped into 44 proposed sub-territories (~5/district). Flags `ParentDistrict()` vs bare names, `owner_kind` (`gang`/`corp`/`enclave`/`unclaimed`), and excluding `Dogtown_Worldmap_Sub`. |
| [`factions-corps-fixers-independents.md`](factions-corps-fixers-independents.md) | 0.2b | Only 13 named corps exist in `gamedataAffiliation`; Night Corp, Kiroshi, Kendachi, Petrochem, and Budget Arms require synthetic faction IDs. Maps all 8 active fixers, NCPD heat model, Delamain, City Council permit loop, 11 purchasable corp assets, and 13 stock tickers + `NCRE`/`NCB`. |
| [`game-data-extraction.md`](game-data-extraction.md) | 0.2c | Native Linux `WolvenKit.CLI 10.0.0-beta.1` (`DOTNET_ROLL_FORWARD=Major`) + plain-text `<game>/tools/redmod/tweaks/**/*.tweak` (98.5% character coverage; skip hashed `tweakdb.bin`). Extract `content -> ep1` (EP1 updates all three `always_loaded_0/1/2` files: 10,324 communities, 27,411 entries, 3,378 prefab areas + 33,953 traffic lanes in `all.traffic_persistent`). |
| [`native-db-architecture.md`](native-db-architecture.md) | 0.3 | `clang-cl` 23.1.5 + `lld-link` + CMake + Ninja already work locally (only `xwin` provisioning needed); **must link `/MT`** because Proton 11's builtin `msvcp140.dll` lacks `__std_*`. No universal script save hook exists—use a 20-byte durable revision watermark in `ScriptableSystem` advanced *after* SQLite `COMMIT` + fork on `OnRestored`. |
| [`world-map-visualization.md`](world-map-visualization.md) | 0.5 | World Map renders a 3D hologram to `world_map_texture.dtex`; `WorldMapDistrictLogicController` only drives labels/icons. Ship vanilla `MappinSystem` control-center dots in `v0.1.0`, then pre-partitioned `inkShape` polygons inside `EntityPreview` projected via a 4-anchor-mappin homography in `v0.2.0` (gated on 3 quick spikes). |
