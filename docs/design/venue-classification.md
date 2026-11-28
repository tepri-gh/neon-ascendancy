# Automated Venue & Node Classification

Status: **finalized** (owner calls & staffing pass applied 2026-11-28). Policy: [`venue-node-policy.md`](venue-node-policy.md), [`node-garrison-and-assault.md`](node-garrison-and-assault.md). Machine-readable source: [`data/venues/classification.json`](../../data/venues/classification.json).

## 1. Summary

- **Total classified:** 194 (169 approved + 6 hand-built + 19 hustle shortlist)
- **Buckets:** `123` nodes, `51` civilian-only venues, `7` neutral hubs, `13` excluded, **`0` undecided**
- **Node types:** {'economy': 56, 'military': 24, 'tech': 31, 'espionage': 12} *(garages, chop shops & drug labs → `tech`)*
- **Node sizes:** {'medium': 73, 'large': 31, 'small': 17, 'very_large': 2}
- **Special tags:** `23` mapped logistics nodes (`is_logistics`, plus pending megacorp HQs), `12` VIP meeting spots (`is_meeting_spot`)
- **Bosses:** 13 lore bosses (0 conflicts), 110 dynamically generated lieutenants
- **Pending `owner-decisions.md` items resolved:** 121 / 121

### Nodes by initial controller

| Faction | Nodes | Logistics | Mapped HQ | Lore Bosses Placed |
| --- | ---: | ---: | --- | --- |
| `tyger_claws` | 16 | 1 | loc_sts_wat_kab_07 | Oswald Forrest (Woodman) (`loc_q105_dollhouse`), Jotaro Shobo (`loc_sts_wat_kab_07`) |
| `valentinos` | 6 | 1 | loc_sts_hey_rey_06 | — |
| `maelstrom` | 10 | 3 | loc_sq011_totentanz | — |
| `sixth_street` | 9 | 2 | loc_sts_std_arr_11 | — |
| `animals` | 7 | 0 | loc_q110_pacifica_mall | Sasquatch (`loc_q110_pacifica_mall`), Logan Garcia (`loc_sts_pac_wwd_05_paint_factory`) |
| `voodoo_boys` | 6 | 0 | loc_q110_netrunners_den | Brigitte (`loc_q110_elders_lair`), Placide (`loc_q110_netrunners_den`), Slider (`loc_q303_hill_park_spa`) |
| `the_mox` | 2 | 0 | loc_q004_lizzys_nightclub | Susie Q (`loc_q004_lizzys_nightclub`) |
| `wraiths` | 10 | 2 | loc_sq004_raffen_shiv_camp | Nash (`loc_q103_mine_ambush`) |
| `aldecaldos` | 3 | 1 | loc_sq004_mobile_camp | Saul Bright (`loc_sq004_mobile_camp`) |
| `arasaka` | 6 | 2 | loc_arasaka_tower | — |
| `militech` | 11 | 4 (+1 HQ) | *(pending HQ: Militech Offices, logistics)* | — |
| `kang_tao` | 1 | 0 (+1 HQ) | *(pending HQ: Kang Tao Building, logistics)* | — |
| `biotechnica` | 1 | 0 (+1 HQ) | *(pending HQ: Protein Flats, logistics)* | — |
| `petrochem` | 0 | 0 (+1 HQ) | *(pending HQ: North Sunrise Oil Fields, logistics)* | — |
| `barghest` | 6 | 2 | loc_q303_paradise | Kurt Hansen (`loc_q303_paradise`), Carl “Dodger” Robinson (`loc_sts_ep1_10`) |
| `ncpd` | 9 | 1 | *(pending HQ: Little China Precinct)* | Sheriff Jones (`loc_q000_roadhouse_town`) |
| `scavs` | 20 | 4 | *(none — cells)* | — |

## 2. Confirmed Nodes (123)

| Controller | Size | Type | Tags | Venue ID | Display Name | Boss | Needs Garrison Work |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `aldecaldos` | large | military | logistics | `loc_sq004_mobile_camp` | Mobile Camp (Aldecaldo Camp, Rocky Ridge Plains) **(HQ)** | **Saul Bright** (lore) | no |
| `aldecaldos` | medium | economy | — | `loc_q103_roadhouse` | Sunset Motel (Rocky Ridge roadhouse, Interstate 9) | Aldecaldos Roadhouse Lieutenant (gen) | yes |
| `aldecaldos` | medium | tech | — | `loc_sq024_mariannes_garage` | Claire's Garage | Aldecaldos Lieutenant (gen) | yes |
| `animals` | large | military | — | `loc_q110_pacifica_mall` | Grand Imperial Mall (GIM), Coastview **(HQ)** | **Sasquatch** (lore) | no |
| `animals` | large | economy | — | `loc_sts_cct_dtn_03` | Empathy | Animals lieutenant (gen) | yes |
| `animals` | medium | economy | — | `loc_rosebud` | Red Queen's Race (Charter Hill basement club) | Animals lieutenant (gen) | no |
| `animals` | medium | economy | — | `loc_sq017_nightclub` | Riot | Animals club security lieutenant (gen) | yes |
| `animals` | medium | economy | — | `loc_sts_cct_dtn_02_metal_club` | 7th Hell | Animals Lieutenant (gen) | yes |
| `animals` | medium | economy | — | `loc_sts_pac_wwd_05_paint_factory` | Tripple Xtreme Epic Workout Center (Old Paint Factory) | **Logan Garcia** (lore) | no |
| `animals` | small | economy | — | `loc_sts_hey_spr_06` | Data Inc. electronics store — Wellsprings, Heywood (Hot Merchandise) | Animals Lieutenant (gen) | yes |
| `arasaka` | very_large | espionage | multi-type, logistics | `loc_arasaka_tower` | Arasaka Tower — Corpo Plaza (lobby and counter-intelligence floor) **(HQ)** | Arasaka counter-intelligence lieutenant (gen) | yes |
| `arasaka` | large | economy | meeting_spot | `loc_q004_q005_arasaka_hotel` | Konpeki Plaza | Arasaka Lieutenant (gen) | yes |
| `arasaka` | large | economy | logistics | `loc_q112_arasaka_industrial_park_warehouse` | Arasaka Industrial Park Warehouse (Arroyo) | Arasaka Lieutenant (gen) | yes |
| `arasaka` | large | military | meeting_spot | `loc_q113_arasaka_estate` | Arasaka Estate (North Oak) | Arasaka Lieutenant (gen) | yes |
| `arasaka` | medium | tech | — | `loc_mq059_freedom` | Rayfield Contractor Site — Bullard & Sequoia (Rancho Coronado) | Arasaka contractor security lieutenant (gen) | yes |
| `arasaka` | small | economy | meeting_spot | `loc_q115_fancy_restaurant` | Embers | Arasaka Venue Lieutenant (gen) | yes |
| `barghest` | large | economy | — | `loc_pr_stadium` | EBM Petrochem Stadium (Dogtown black market and Barghest base) | Barghest market lieutenant (gen) | yes |
| `barghest` | large | economy | meeting_spot | `loc_q303_paradise` | Black Sapphire (Dogtown) **(HQ)** | **Kurt Hansen** (lore) | yes |
| `barghest` | large | tech | — | `loc_sts_ep1_13` | Center for Neuromotor Development, Site 341 (Talent Academy) | Barghest academy security lieutenant (gen) | yes |
| `barghest` | medium | economy | logistics | `loc_q301_crashsite_way_up` | Stacks Container Yard (Dogtown, below Luxor Heights) | Barghest Lieutenant (gen) | yes |
| `barghest` | medium | military | logistics | `loc_q303_combat_zone_gate` | Dogtown Gate Checkpoint (Combat Zone Border) | Barghest Lieutenant (gen) | yes |
| `barghest` | medium | military | — | `loc_sts_ep1_10` | Abandoned Pacifica NCPD Precinct — Dodger's Barghest base (Coastview) | **Carl “Dodger” Robinson** (lore) | yes |
| `biotechnica` | medium | economy | meeting_spot | `loc_sts_cct_dtn_04` | Biotechnica Hotel (Republic Way, Downtown) | Biotechnica Lieutenant (gen) | yes |
| `kang_tao` | small | tech | — | `loc_q104_gas_station` | SovOil Fuel Station (Highway 101) | Kang Tao Station Lieutenant (gen) | yes |
| `maelstrom` | large | military | — | `loc_q003_meat_factory` | All Foods | Maelstrom lieutenant (gen) | yes |
| `maelstrom` | large | economy | — | `loc_sq011_totentanz` | Totentanz **(HQ)** | Maelstrom Lieutenant (gen) | yes |
| `maelstrom` | large | economy | logistics | `loc_sq031_ruinedship` | DV Ebunike (Ebunike Docks) | Maelstrom Lieutenant (gen) | yes |
| `maelstrom` | medium | economy | logistics | `loc_mq032_maelstrom_warehouse` | Abandoned Warehouse — Northside docks (Maelstrom stash) | Maelstrom Lieutenant (gen) | yes |
| `maelstrom` | medium | espionage | — | `loc_sts_wat_nid_04_netrunner_hideout` | Dirty Biz XBD studio (Maelstrom-guarded netrunner hideout, Northside) | Maelstrom Lieutenant (gen) | yes |
| `maelstrom` | medium | tech | — | `loc_sts_wat_nid_05` | HeavenMed clinic (Daniels St., Northside) | Maelstrom Lieutenant (gen) | yes |
| `maelstrom` | medium | tech | — | `loc_sts_wat_nid_06` | Maelstrom chop shop (Offshore St warehouse, Northside) | Maelstrom lieutenant (gen) | yes |
| `maelstrom` | medium | economy | logistics | `loc_sts_wat_nid_07` | Maelstrom warehouse — Industrial & Eisenhower (Northside) | Maelstrom Lieutenant (gen) | yes |
| `maelstrom` | small | military | — | `hustle_wat_nid_02` | wat_nid_02 (Northside) | Maelstrom Lieutenant (gen) | no |
| `maelstrom` | small | tech | — | `loc_sts_wat_kab_02_ripperdoc_lab` | North Kabuki Ripperdoc Lab | Maelstrom Lieutenant (gen) | yes |
| `militech` | medium | economy | logistics | `hustle_bls_ina_se1_23` | bls_ina_se1_23 (Badlands) | Militech lieutenant (gen) | yes |
| `militech` | medium | military | — | `hustle_wbr_hil_01` | wbr_hil_01 (Charter Hill) | Militech black-site lieutenant (gen) | yes |
| `militech` | medium | military | logistics | `loc_q000_border_crossing` | SoCal Border Crossing | Militech Lieutenant (gen) | yes |
| `militech` | medium | tech | — | `loc_q114_tunnel_site` | Maglev Tunnel Construction Site (Badlands) | Militech Tunnel Site Lieutenant (gen) | yes |
| `militech` | medium | military | — | `loc_sts_bla_ina_04` | Sunshine Motel (Militech Outpost) | Militech outpost lieutenant (gen) | yes |
| `militech` | medium | military | — | `loc_sts_bls_ina_05` | Militech Detention Center | Militech lieutenant (gen) | yes |
| `militech` | medium | economy | logistics, meeting_spot | `loc_sts_cct_dtn_05_luxury_yacht` | Gold Beach Marina party yacht (Councilwoman Cole's yacht) | Militech Marina Lieutenant (gen) | yes |
| `militech` | medium | economy | meeting_spot | `loc_sts_hey_gle_01` | Tucker Albach's Condo (Scoffield & Sinkyone, The Glen) | Militech Lieutenant (gen) | yes |
| `militech` | medium | military | — | `loc_sts_std_rcr_01` | C-Team Office, Carsten St (Rancho Coronado) | Militech Lieutenant (gen) | yes |
| `militech` | small | military | — | `hustle_bls_ina_se1_05` | bls_ina_se1_05 (Badlands) | Militech Lieutenant (gen) | yes |
| `militech` | small | economy | logistics | `hustle_cct_dtn_15` | cct_dtn_15 (Downtown) | Militech Lieutenant (gen) | yes |
| `ncpd` | large | military | — | `loc_mq062` | Night City Prison (Arroyo) — visitor center, cell block and security cortex | Ncpd Lieutenant (gen) | yes |
| `ncpd` | large | tech | — | `loc_q111_pumpstation` | Wellsprings Water Treatment Facility (Pump Station) | Ncpd Lieutenant (gen) | yes |
| `ncpd` | large | tech | — | `loc_sq021_police_lab` | NCPD Lab (The Glen) | Ncpd Lieutenant (gen) | yes |
| `ncpd` | medium | economy | meeting_spot | `loc_sq006_jefferson_residence` | Peralezes' Apartment (Charter Hill penthouse) | Ncpd Lieutenant (gen) | yes |
| `ncpd` | medium | military | logistics | `loc_sts_cct_cpz_01` | Memorial Park NCART Station (concourse and security annex) | Ncpd Lieutenant (gen) | yes |
| `ncpd` | medium | economy | meeting_spot | `loc_sts_hey_gle_03` | Gaston Slayton's Apartment (Lobos St, floor 17) | NCPD Security Lieutenant (gen) | no |
| `ncpd` | medium | tech | — | `loc_sts_std_rcr_02` | Night City Center for Psychiatric Health (Rancho Coronado) | Ncpd Lieutenant (gen) | yes |
| `ncpd` | medium | economy | meeting_spot | `loc_sts_wbr_hil_01` | Gutierrezes' Apartment (Charter Hill) | NCPD Security Lieutenant (gen) | no |
| `ncpd` | small | economy | — | `loc_q000_roadhouse_town` | Yucca | **Sheriff Jones** (lore) | yes |
| `scavs` | large | tech | — | `loc_mq306_tech_expo` | Digimmortal (Terra Cognita exhibition hall) | Scavs Lieutenant (gen) | yes |
| `scavs` | large | espionage | — | `loc_q105_braindance_studio` | Electric Corporation Power Plant (Scavenger XBD studio) | Scavs Lieutenant (gen) | yes |
| `scavs` | large | economy | logistics | `loc_sts_std_arr_03` | Kendachi Factory, El Camino Rd (Arroyo) | Scavs Lieutenant (gen) | yes |
| `scavs` | large | tech | — | `loc_sts_std_arr_10` | Cytech Factory | Scavs Lieutenant (gen) | yes |
| `scavs` | large | economy | logistics | `loc_sts_wat_kab_102_cargo` | Kabuki Docks Container Yard | Dock security lieutenant (gen) | yes |
| `scavs` | medium | tech | — | `hustle_bls_ina_se5_09` | bls_ina_se5_09 (Badlands) | Scavenger lieutenant (gen) | yes |
| `scavs` | medium | tech | — | `hustle_cct_dtn_12` | cct_dtn_12 (Corpo Plaza garage) | Scavs Lieutenant (gen) | yes |
| `scavs` | medium | economy | — | `loc_q005_notell_motel` | No-Tell Motel (Kabuki) | Scavenger Motel Lieutenant (gen) | yes |
| `scavs` | medium | tech | — | `loc_q104_power_plant` | Satwave Power Plant (Jackson Plains) | Scavenger lieutenant (gen) | yes |
| `scavs` | medium | espionage | — | `loc_sq023_braindance_studio` | Fourth Wall Studios (Japantown braindance studio) | Scavs Lieutenant (gen) | yes |
| `scavs` | medium | economy | logistics | `loc_sq027_rail_junction` | Corp-Bud Railroad Station | Scavs Lieutenant (gen) | yes |
| `scavs` | medium | economy | logistics | `loc_sts_bls_ina_11` | Warbler Lake Hazardous Waste Facility (Junk Vendor scrapyard) | Scrapyard security lieutenant (gen) | yes |
| `scavs` | medium | tech | — | `loc_sts_ep1_03` | Los Osos Motel (West Wind Estate) | Scavs Lieutenant (gen) | yes |
| `scavs` | medium | economy | — | `loc_sts_std_arr_12_motel` | Las Palapas Motel (Arroyo) | Motel security lieutenant (gen) | yes |
| `scavs` | medium | economy | — | `loc_sts_wat_nid_03_abandoned_motel` | Abandoned Motel on Martin Street | Motel security lieutenant (gen) | yes |
| `scavs` | medium | espionage | — | `loc_sts_wat_nid_12` | Old WNS Station | Media intelligence lieutenant (gen) | yes |
| `scavs` | small | tech | — | `hustle_wat_lch_01` | wat_lch_01 (Little China rooftop) | Scavenger cyberware lieutenant (gen) | yes |
| `scavs` | small | military | — | `loc_q000_scavengers` | Scavenger Den (Japantown, room 1237) | Scavenger Den Lieutenant (gen) | no |
| `scavs` | small | tech | — | `loc_sts_std_arr_12_gas_station` | Tirempire Auto Shop (Arroyo) | Scavs Lieutenant (gen) | yes |
| `scavs` | small | tech | — | `loc_sts_wat_kab_05_client_signal` | Eisenhower St. scav den and Charles Bucks' clinic (Kabuki) | Scavenger lieutenant (gen) | yes |
| `sixth_street` | large | military | — | `loc_sts_std_arr_11` | 6th Street Hideout, Megabuilding H6 (19F) **(HQ)** | 6th Street lieutenant (gen) | yes |
| `sixth_street` | medium | tech | — | `hustle_std_arr_03` | std_arr_03 (Hargreaves St, Arroyo) | Sixth Street Lieutenant (gen) | yes |
| `sixth_street` | medium | military | — | `loc_q305_netwatch_ambush` | Abandoned Hotel (West Wind Estate, Pacifica) | Sixth Street Lieutenant (gen) | yes |
| `sixth_street` | medium | tech | — | `loc_sts_hey_gle_06` | Wicked Tires Autoshop (McBride St., the Glen) | 6th Street garage lieutenant (gen) | yes |
| `sixth_street` | medium | economy | — | `loc_sts_std_arr_01` | Dewdrop Inn (Arroyo) | Sixth Street Lieutenant (gen) | yes |
| `sixth_street` | medium | tech | — | `loc_sts_std_arr_06` | Sixth Street Garage — Hargreaves St., Arroyo | Sixth Street Lieutenant (gen) | yes |
| `sixth_street` | medium | espionage | logistics | `loc_sts_std_rcr_04` | 6th Street propaganda garage, Oak St. (Rancho Coronado) | Sixth Street Lieutenant (gen) | yes |
| `sixth_street` | medium | economy | logistics | `loc_sts_wbr_hil_06` | Acorn Towers Parking Lot | Sixth Street Lieutenant (gen) | yes |
| `sixth_street` | small | tech | — | `hustle_std_rcr_08` | std_rcr_08 (Rancho Coronado) | 6th Street lieutenant (gen) | yes |
| `the_mox` | very_large | economy | multi-type | `loc_q004_lizzys_nightclub` | Lizzie's Bar **(HQ)** | **Susie Q** (lore) | yes |
| `the_mox` | medium | tech | — | `loc_sts_wat_nid_01` | Autowerks (Longshore North) | The Mox Lieutenant (gen) | yes |
| `tyger_claws` | large | economy | — | `loc_q105_jigjig_street` | Jig-Jig Street | Tyger Claws District Lieutenant (gen) | yes |
| `tyger_claws` | large | economy | — | `loc_q112_market_area` | Cherry Blossom Market (Japantown market area) | Tyger Claws Market Lieutenant (gen) | yes |
| `tyger_claws` | large | economy | — | `loc_sts_wat_kab_07` | Ho-Oh Casino (Kabuki) **(HQ)** | **Jotaro Shobo** (lore) | yes |
| `tyger_claws` | large | military | — | `loc_sts_wat_lch_03_dojo` | Deravaja Dojo | Tyger Claws Lieutenant (gen) | yes |
| `tyger_claws` | large | tech | — | `loc_sts_wat_lch_06_neon_basement` | Rovinj St. Glitter Lab (Neon Basement) | Tyger Claws lieutenant (gen) | yes |
| `tyger_claws` | medium | economy | — | `hustle_wat_lch_08` | wat_lch_08 (Drake & Cartwright, Little China) | Tyger Claws Lieutenant (gen) | yes |
| `tyger_claws` | medium | economy | — | `hustle_wbr_jpn_20` | wbr_jpn_20 (Willow St, Japantown) | Tyger Claws Lieutenant (gen) | yes |
| `tyger_claws` | medium | economy | meeting_spot | `loc_q105_dollhouse` | Clouds | **Oswald Forrest (Woodman)** (lore) | no |
| `tyger_claws` | medium | economy | meeting_spot | `loc_sq017_pachinko_lounge` | Dark Matter | Tyger Claws Lieutenant (gen) | yes |
| `tyger_claws` | medium | economy | — | `loc_sts_wat_kab_08_cop_hotel` | Kabuki Market and Motel | Tyger Claws Lieutenant (gen) | yes |
| `tyger_claws` | medium | tech | — | `loc_sts_wat_lch_01_server_room` | Megabuilding H11 Server Room | Tyger Claws Netrunner Lieutenant (gen) | yes |
| `tyger_claws` | medium | economy | logistics | `loc_sts_wat_nid_02` | Revere Courier Services Facility | Tyger Claws Lieutenant (gen) | yes |
| `tyger_claws` | medium | economy | — | `loc_sts_wbr_hil_07` | Tyger Claws Casino (Charter Hill) | Tyger Claws lieutenant (gen) | yes |
| `tyger_claws` | medium | tech | — | `loc_sts_wbr_jpn_02_monoblade_workshop` | Monokatana Workshop (Raymond St, Japantown) | Tyger Claws workshop lieutenant (gen) | yes |
| `tyger_claws` | medium | economy | — | `loc_sts_wbr_jpn_03_shrine` | Chram Denya Jinja | Tyger Claws Lieutenant (gen) | yes |
| `tyger_claws` | medium | economy | — | `loc_sts_wbr_jpn_12b` | Wired Head (Japantown) | Tyger Claws Lieutenant (gen) | yes |
| `valentinos` | large | economy | — | `loc_sts_hey_rey_06` | La Catrina Funeral Home **(HQ)** | Valentinos lieutenant (gen) | yes |
| `valentinos` | medium | economy | — | `loc_sq022_el_coyote_cojo_bar` | El Coyote Cojo | Valentinos Lieutenant (gen) | yes |
| `valentinos` | medium | economy | — | `loc_sts_hey_gle_04` | El Pinche Pollo | Valentinos Lieutenant (gen) | yes |
| `valentinos` | medium | economy | — | `loc_sts_hey_rey_02` | Dicky Twister | Valentinos Lieutenant (gen) | yes |
| `valentinos` | medium | military | logistics | `loc_sts_hey_spr_01` | Bus Depot on Benko St — Wellsprings (Valentino depot) | Valentino depot lieutenant (gen) | yes |
| `valentinos` | medium | tech | — | `loc_sts_hey_spr_03` | Valentinos Auto Shop (Russell St., Wellsprings) | Valentinos Lieutenant (gen) | yes |
| `voodoo_boys` | large | espionage | — | `loc_q110_elders_lair` | Voodoo Boys' Lair (Pacifica Serenity Bible Church basement and old maglev tunnel) | **Brigitte** (lore) | yes |
| `voodoo_boys` | large | espionage | — | `loc_q110_netrunners_den` | Voodoo Boys' Netrunners Den (Batty's Hotel / Coastview market) **(HQ)** | **Placide** (lore) | no |
| `voodoo_boys` | large | espionage | — | `loc_sts_ep1_12` | Luxor High Wellness Spa — Voodoo Boys base (Luxor Heights, Dogtown) | Voodoo Boys Lieutenant (gen) | yes |
| `voodoo_boys` | medium | economy | — | `loc_q110_chapel_of_the_black_madonna` | Pacifica Serenity Bible Church (Chapel of the Black Madonna) | Voodoo Boys lieutenant (gen) | yes |
| `voodoo_boys` | medium | espionage | — | `loc_q303_hill_park_spa` | Eventide Resort & Spa — Slider's Hideout (Dogtown, Luxor Heights) | **Slider** (lore) | no |
| `voodoo_boys` | small | espionage | — | `loc_q110_surroundings` | Coastview Relay Tower (Charon Exotics tracking station) | Voodoo Boys Lieutenant (gen) | yes |
| `wraiths` | large | military | — | `loc_sq004_raffen_shiv_camp` | Corp-Bud Cement Factory (Wraith camp) **(HQ)** | Wraith camp lieutenant (gen) | yes |
| `wraiths` | medium | military | — | `loc_q103_mine_ambush` | Corp-Bud Mine (Wraith stronghold, Rocky Ridge) | **Nash** (lore) | no |
| `wraiths` | medium | economy | — | `loc_sq021_farm_wrong` | Poppy Farm | Wraiths Lieutenant (gen) | yes |
| `wraiths` | medium | tech | — | `loc_sts_bls_ina_02` | New American Autoworks (Big Pete's Garage) | Wraiths Lieutenant (gen) | yes |
| `wraiths` | medium | espionage | logistics | `loc_sts_bls_ina_03` | Union Railroad Station (Wraiths outpost) | Wraiths Lieutenant (gen) | yes |
| `wraiths` | medium | military | — | `loc_sts_bls_ina_06` | Wraiths Outpost (Municipal Landfill) | Wraiths Lieutenant (gen) | yes |
| `wraiths` | medium | economy | logistics | `loc_sts_bls_ina_08` | Wraith Camp (Highway 101) | Wraiths Lieutenant (gen) | yes |
| `wraiths` | small | military | — | `hustle_bls_ina_se1_17` | bls_ina_se1_17 (I-9, Badlands) | Wraiths Lieutenant (gen) | yes |
| `wraiths` | small | tech | — | `hustle_bls_ina_se5_14` | bls_ina_se5_14 (Badlands) | Wraiths Lieutenant (gen) | yes |
| `wraiths` | small | economy | — | `loc_q103_ghost_town` | Rocky Ridge (Wraith-held ghost town) | Wraiths Lieutenant (gen) | yes |

## 3. Neutral Hubs (7)

| Venue ID | Display Name | Reason |
| --- | --- | --- |
| `loc_mystic_mistys_ripperdoc` | Misty's Esoterica and Viktor's Clinic | Misty & Viktor core ally / ripperdoc hub; never captured. |
| `loc_q026_judys_apartment` | Judy's Apartment (Charter Street, Kabuki) | Companion homes are protected neutral hubs. |
| `loc_q103_afterlife` | The Afterlife | Rogue’s fixer headquarters is explicitly protected and cannot be captured. |
| `loc_sq018_jackies_storage` | Jackie's Garage | Jackie Welles companion hub (owner #53: Jackie stays here when not accompanying V). |
| `loc_sq021_trailer_park` | Red Peaks Trailer Park (Kutcher's Home) | The site is protected by the neutral-hub policy. |
| `loc_sq025_delamain_garage` | Delamain Corp Headquarters | The site is protected by the neutral-hub policy. |
| `loc_sts_ep1_06` | Heavy Hearts | Fixer headquarters are protected neutral hubs. |

## 4. Civilian-Only Venues (51)

| Venue ID | Display Name | Reason |
| --- | --- | --- |
| `loc_conz_mq304_ce` | Container yard lanes below Luxor Heights (Dogtown) — mq304 city-scene ground | Keep its civilian street life and leave control to the overlapping yard. |
| `loc_hvdr_02_batty` | Batty's Hotel | Heywood (hvdr_02) Beat on the Brat rooftop, not Coastview Batty's Hotel; resolves duplicate VDB HQ and Placide conflict. |
| `loc_megabuilding_a` | Megabuilding H10 (V's home building) | Keep the home building as residential and vendor scenery. |
| `loc_mq022_ezekiel` | BuryGer diner, Arroyo (MLK & Brandon) | A small diner fails the garrison test. |
| `loc_mq030_suit_store` | Jinguji — Downtown clothing store (Senate Avenue) | Its single showroom cannot plausibly accommodate a five-person security team and boss. |
| `loc_mq303_linas_mansion` | Lina Malina's Residence (Dogtown) | Keep the residence as civilian scenery. |
| `loc_mq303_shanks_store` | Brainporium (BD shop in the Jason Exiled head, Eden Plaza, Dogtown) | The small shop fails the garrison test. |
| `loc_mq305_wanted` | Bree Whitney's Apartment (Skyline West, Wellsprings) | Retain the residents as civilian scenery. |
| `loc_mq306_boxing_ring` | Boxing Ring by Montezuma's Throne (Dogtown) | The open ring fails the security and asset test. |
| `loc_q000_underground_parking_lot` | Embers Underground Parking (The Glen) | Basement parking structure directly under Embers; keep ambient parked cars rather than a separate Scav node. |
| `loc_q004_braindance_store` | Cali Express (The Glen, Scoffield Street) | The small convenience store is civilian retail. |
| `loc_q101_landfill` | Night City Municipal Landfill | Keep the open dump as scenery without duplicating its separate outpost. |
| `loc_q105_fingers_appartment` | Fingers' Clinic, Jig-Jig Street | Keep the ordinary civilian venue because it fails the asset or garrison test. |
| `loc_q110_butcher_shop` | Rolland's Butcher Shop (Voodoo Boys front, Coastview) | The compact butcher shop fails the garrison test. |
| `loc_q112_arasaka_industrial_park_lookout` | Arasaka Industrial Park Lookout (Arroyo) | Avoid treating an ancillary lookout as a separate guarded node. |
| `loc_q112_parade_area` | Japantown Parade Route (market bridge and shrine) | Open-street parade bridge overlapping Cherry Blossom Market & Jig-Jig Street; not an independent building node. |
| `loc_q112_safe_house` | Abandoned Apartment Building, Vine Street (Vista del Rey) | Leave the intact ruin as non-node scenery. |
| `loc_q302_06_basketball` | Hillpark Basketball Court (Dogtown) | The public park is civilian scenery rather than a guarded asset. |
| `loc_q302_goodnight_charlies` | Capitán Caliente (Eden Plaza, Dogtown) | Small abandoned Eden Plaza restaurant with one squatter; fails 5+ security test. |
| `loc_q302_squat` | Rindo Hotel | Keep the squatters and exclude the crash-driven cast. |
| `loc_q303_macs_clinic` | Farida's Clinic | This small underpass shop cannot plausibly fit five guards and a lieutenant. |
| `loc_q303_nighthawks_bar` | The Moth | Small one-room Dogtown dive bar with lore-sealed NUSA backroom (owner #170); fails 5+ security test. |
| `loc_q304_songbird_meeting` | Tranquil Terrace — Luxor Heights park and basketball court | Keep the ordinary civilian venue because it fails the asset or garrison test. |
| `loc_sq012_diner` | Chubby Buffalo's BBQ (The Glen diner) | The diner fails the everyday garrison test. |
| `loc_sq017_emptystreet` | Empty Street coffee cart (Rancho Coronado) | A single coffee stand cannot support five guards and a lieutenant. |
| `loc_sq017_fast_food` | Capitán Caliente (Rancho Coronado fast-food restaurant) | The ordinary restaurant remains a civilian venue. |
| `loc_sq021_farm` | Edgewood Farm (Anthony Harris's farmstead) | The unattended farmstead lacks a convincing guarded asset. |
| `loc_sq023_glorias_house` | Gloria El-Ahmar's House | A small family home fails the garrison test. |
| `loc_sq023_resturant` | PieZ (Rancho Coronado pizza restaurant) | Its ordinary dining room is a small civilian venue without evidence of space for a dedicated garrison and boss. |
| `loc_sq030_love_shack` | Abandoned Lake Dwelling (Laguna Bend Reservoir) | The cottage fails the five-person security test. |
| `loc_sq031_drive_in_cinema` | Silver Pixel Cloud (North Oak drive-in cinema) | Owner decision #20 explicitly kept Silver Pixel Cloud open with no holding crew. |
| `loc_sts_ep1_01` | Haven Clinic | Owner call (U4): Haven Clinic stays a civilian venue (working ripperdoc hub). |
| `loc_sts_ep1_03_gunfight` | Longshore Stacks courtyard (Jason Foreman vigil site) | Keep the Stacks courtyard as civilian residential scenery. |
| `loc_sts_ep1_botanic_gardens` | Organitopia | Leave the lore-clean ruin as scenery. |
| `loc_sts_hey_gle_05` | Megabuilding H1 — basement lift-repair workshop (Gig: Going Up or Down?) | The small utility room remains part of the civilian megabuilding. |
| `loc_sts_hey_rey_01` | Gustavo Orta's Apartment | Keep ordinary neighbours and remove the residential gang crew. |
| `loc_sts_hey_rey_08` | Jacked and Coke (Karubo's bar, Vista del Rey) | Tiny corner dive bar (Jacked and Coke); fails 5+ security test. |
| `loc_sts_hey_rey_09` | 8ug8ear's Apartment Building (Salinas St.) | The small residential premises fail the security-space test. |
| `loc_sts_std_arr_05_parking` | Kendachi factory parking lot (Rancho Coronado) | Adjacent parking lot of Kendachi Factory; redundant with loc_sts_std_arr_03 as a separate node. |
| `loc_sts_std_arr_12_diner` | Kenmore Diner (Arroyo) | A small diner with six ambient staff and patrons has no demonstrated space for a security team and lieutenant. |
| `loc_sts_std_rcr_03` | Flavio dos Santos's safehouse, Mallagra St. (Rancho Coronado) | Ordinary run-down suburban house (Flavio's safehouse); not an ownable tower or 5+ security asset. |
| `loc_sts_std_rcr_05` | Horrigan Family Home (Gibson St., Rancho Coronado) | The family residence fails the security-space test. |
| `loc_sts_wat_kab_01_street_maze` | Kabuki Street Maze | Keep the ordinary civilian venue because it fails the asset or garrison test. |
| `loc_sts_wat_kab_03_stolen_meds` | Columbus St. housing block (Backs Against the Wall) | The small residential site fails the garrison test. |
| `loc_sts_wat_kab_101_slums` | Rooftop Slums near Allen St. (Kabuki) | The rooftop is residential scenery rather than a meaningful guarded asset. |
| `loc_sts_wat_nid_07b` | Aaron McCarlson's Apartment | The single flat fails the security-space test. |
| `loc_sts_wbr_jpn_01_tygerclaw_garage` | Garage on Redwood St. | Single-car lock-up garage on Redwood St. with no guards; fails 5+ security test. |
| `loc_sts_wbr_jpn_01_tygerclaw_restaurant` | Tyger Claws Diner (Japantown) | The small diner fails the full security-space test. |
| `loc_sts_wbr_jpn_05_burned_store` | Ginger Panda (Chang-Hoon Nam's netrunner den) | The small restaurant and den fail the five-guard test. |
| `loc_sts_wbr_jpn_12` | Japantown Apartments (Holly & Floyd St) — Leah Gladen's building | Ordinary Japantown residential block with one flat and one gig guard; fails 5+ security test. |
| `loc_wat_kab_gun_trainer_01` | Straight Shooters (Kabuki weapon vendor and shooting range) | Keep the ordinary civilian venue because it fails the asset or garrison test. |

## 5. Excluded (13)

| Venue ID | Display Name | Reason |
| --- | --- | --- |
| `hustle_bls_ina_se1_19` | bls_ina_se1_19 (Badlands ridge) | The exposed stash is encounter staging rather than a sustainable node. |
| `hustle_cct_cpz_16` | cct_cpz_16 (Corpo Plaza roof) | The cache is encounter staging rather than a meaningful node. |
| `hustle_hey_gle_105` | hey_gle_105 (behind Megabuilding H1) | This is a quest staging wrapper rather than a separate ownable asset. |
| `hustle_hey_gle_109` | hey_gle_109 (the Glen) | The isolated cache is too small to operate as a node. |
| `hustle_wat_nid_27` | wat_nid_27 (Northside) | The roadside stripping scene lacks a substantial physical asset. |
| `loc_mq304_bennett_meeting` | Bennett's meeting alley (Downtown back court) | It is a street staging wrapper without a meaningful ownable asset. |
| `loc_mq304_ce_2` | Longshore Stacks container yard (Dogtown) | Owner call (U11): overlaps Stacks Container Yard (loc_q301_crashsite_way_up); drop. |
| `loc_mq304_vdb_meeting` | High Peak — the Voodoo Boys' meeting ground | This is a quest staging wrapper rather than a separate ownable asset. |
| `loc_mq305_wanted_lab` | Cynosure Site D (Militech lab beneath the Kress Street hideout) | The policy explicitly excludes Cynosure bunkers. |
| `loc_q306_meeting_spot` | Downtown back-alley meeting spot (City Center, Songbird's pickup) | The empty alley fails the physical garrison and asset tests. |
| `loc_sq004_abandoned_farmhouse` | Ingalls Farm (abandoned farmhouse) | The derelict farmhouse has no established operational role and is an empty story landmark. |
| `loc_sq030_underwater_house` | Laguna Bend (submerged town) | Submerged Laguna Bend is explicitly lore-excluded. |
| `loc_sts_wbr_jpn_09_netrunner_parking_lot` | Netrunner Parking Lot (Japantown) | An empty road-side staging lot has no independent asset to restore. |
