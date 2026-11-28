# Node Security and Staffing (design input)

Status: **open, for the design pass.** Written from the owner's node tour on
2026-11-27 (stops 13 to 86 of 163; the game hung on the teleport to stop 87).
Policy: [`venue-node-policy.md`](venue-node-policy.md). Per-venue data:
[`data/venues/classification.json`](../../data/venues/classification.json).

The owner marked 31 of the 44 stops "not right". Most of those were not bugs.
The stops were missing security detail, or needed a design call that has not
been made yet. This doc gathers those calls so a design pass can settle
them. Fix-type findings (bodies, doors, tour positions) are in
[`../tour-findings.md`](../tour-findings.md).

---

## 1. Questions for the design pass

### S1. Security detail by node size (the main question)

The policy's population rule is a placeholder: "5+ neutral-until-provoked
security garrison + 1 lieutenant boss" for every node. The owner: "we
haven't worked out small/medium/large security detail amounts."

To settle, for each size (`small`, `medium`, `large`, and `very_large` if S2
adds it):
- the headcount range;
- the role mix: guards, heavies, snipers, netrunners, drones or androids,
  and the lieutenant;
- posts against patrols (S8);
- how the counts scale with node type. A military node probably carries
  more than an economy node of the same size.

Rules already set:
- **Token vanilla guards do not count.** A node whose vanilla guards read as
  a token presence still gets the full detail (Dodger's precinct,
  `sts_ep1_10`, policy section 5).
- **A vanilla quest crowd is a fair reference.** At 7th Hell, the owner said
  the quest detail would be "okay". At Black Sapphire's approach, "check
  quest": the guards the quest puts there are the expected look.
- **Neutral until provoked** (policy section 5).

Nodes the owner called out for stronger security on this tour:

| Venue | Owner's size call | Note |
| --- | --- | --- |
| `loc_sts_ep1_10` Dodger's precinct | medium | "much stronger security detail" |
| `loc_q303_paradise` Black Sapphire | large | approach "missing many guards (check quest)"; casino and stage need large-node detail |
| `loc_sts_ep1_12` Luxor High Wellness Spa | large | netrunner den; needs a netrunner and a boss |
| `loc_q115_fancy_restaurant` Embers | small | |
| `loc_sq022_el_coyote_cojo_bar` El Coyote Cojo | medium | |
| `loc_sts_cct_cpz_01` Memorial Park NCART | medium (NCPD military) | |
| `loc_sts_cct_dtn_02_metal_club` 7th Hell | medium | "larger security detail" |
| `loc_q005_notell_motel` No-Tell Motel | medium | |
| `loc_sq017_nightclub` Riot | medium | |
| `loc_sts_wat_kab_102_cargo` Kabuki container yard | large | |
| `loc_sts_wat_lch_01_server_room` H11 server room | medium (tech) | |
| `loc_sts_wat_lch_03_dojo` Deravaja Dojo | large (military) | |
| `loc_sts_wat_lch_06_neon_basement` Glitter lab | large | |
| `loc_sq011_totentanz` Totentanz | large | |
| `loc_sts_wat_nid_01` Autowerks | medium | |
| `loc_sts_wat_nid_02` Revere Courier | medium | |
| `loc_q004_lizzys_nightclub` Lizzie's | very large (S2) | |
| `loc_arasaka_tower` Arasaka Tower | very large (S2) | "many, many security NPCs missing" |

### S2. Very large, multi-type nodes

Two venues read as bigger than `large` and as more than one node type:
- **Arasaka Tower**, a corp HQ that "might be a very large multi-node
  encompassing each type". The tower is a project of its own (S11).
- **Lizzie's**, the Mox headquarters: "multi-type node, very large, needs
  effort put into security detail".

To settle:
- whether `very_large` is a fourth size, or such places are several nodes
  (one per type) that share a site;
- how a multi-type node outputs, gets captured and shows on the map;
- which other HQs qualify. The other faction HQs in `venue-classification.md`
  are candidates: Clouds, Totentanz, the 6th Street H6 hideout, Black
  Sapphire, La Catrina and the Grand Imperial Mall.

### S3. A logistics node type?

Container yards and freight sites fold into `economy` today. The owner asks
whether they need their own `logistics` type, or should be military:
- the Kabuki docks container yard (`sts_wat_kab_102_cargo`): "could be
  military? Needs later discussion";
- Revere Courier (`sts_wat_nid_02`): "medium logistics";
- the Northside Maelstrom warehouse (`mq032_maelstrom_warehouse`): "could be
  a logistics node for containers but otherwise fairly unimportant,
  interested in ideas". Its container yard looks unreachable by vehicle;
- the Stacks container yard in Dogtown (`q301_crashsite_way_up`) is the same
  kind of place.

A fifth type touches the four-pillar model (`gameplay-systems.md` section 1)
and Culture ordering (policy section 2), so the pass should weigh it against
a logistics *tag* on economy or military nodes.

### S4. Drug labs

The Glitter lab under Rovinj St. (`sts_wat_lch_06_neon_basement`) is "a major
drug lab, large tech(?) node". The owner: settle what drug labs count as once
the rest of the node types are mapped, for balance. Other labs: the 6th
Street Hargreaves St. lab (`hustle_std_arr_03`, tech) and the Dewdrop Inn
drug lab front (`territory-node-candidates.md`).

### S5. Garages and auto shops as tech nodes

The owner: "I think we turn garages into tech nodes to balance node
distribution out." Today most garages and auto shops are `economy`:
- Wicked Tires (`sts_hey_gle_06`);
- the Tirempire auto shop (`sts_std_arr_12_gas_station`, now small);
- Autowerks (`sts_wat_nid_01`);
- the Wellsprings shops (`sts_hey_spr_01`, `sts_hey_spr_03`);
- Claire's Garage;
- the q104 gas station.

The Eisenhower St. shop under Charles Bucks' clinic (`sts_wat_kab_05_client_signal`)
is already `tech`. The node counts are economy 68, military 24, tech 19 and
espionage 12, so moving garages would even them out. The pass should set
the rule and the list.

### S6. Netrunners outside espionage nodes

The owner: "netrunners aren't always at espionage nodes, in places where they
make sense we can also add them to economy/military nodes and this should
contribute to intel production." Examples: the Las Palapas Motel
(`sts_std_arr_12_motel`, economy) and Empathy (`sts_cct_dtn_03`, a netrunner
den inside a club).

To settle:
- how a netrunner in the security detail adds Intel output on top of the
  node type's pillar;
- whether that output counts per netrunner or as a flag;
- how it interacts with S1's role mix.

### S7. Civilian crowds and club activity

Several nodes are too empty for what they are:
- Empathy (`sts_cct_dtn_03`): "needs to be much more populated, large
  economy node";
- Ho-Oh (`sts_wat_kab_07`): "large economy node, needs civilian population";
- 7th Hell: "not enough civilians, use quest/gig crowd?";
- Lizzie's: empty. The bouncer says they are closed, which may be a time
  gate on the club's activity.

Clubs have no DJ and no music: Totentanz, Riot, Empathy and 7th Hell. The
fix agent is finding what drives club music, DJs and opening hours in
vanilla ([`../tour-findings.md`](../tour-findings.md)). The design calls:
- whether a node's civilian crowd scales with its size;
- whether quest or gig crowds may be reused for it;
- whether clubs keep vanilla's opening hours.

### S8. Patrols (deferred)

The owner: "Guards are just sitting in elevator, there's probably patrol
routines for a lot of these entities that we're missing" (Slayton's
apartment, `sts_hey_gle_03`). That needs a full pass on patrols. It may add
new spawns with their own patrols, sized to small, medium and large detail
(S1). Deferred until S1 is set.

### S9. Vehicle service at garages (deferred system)

The owner wants cars that drive into and out of shops to be worked on. At
the Tirempire auto shop (`sts_std_arr_12_gas_station`), NPCs work on a car.
Record their animations, workspots and positions for that later system;
the fix agents are capturing them (`tour-findings.md`). Deferred; it belongs
with the other side systems (`gameplay-systems.md`).

### S10. Tyger Claws HQ

Ho-Oh (`sts_wat_kab_07`, now large economy) "might work as Tyger Claws HQ?".
The current HQ is Clouds (`q105_dollhouse`). Settle which one, or whether
the HQ is a multi-type node (S2).

### S11. Large restoration projects

These are bigger than a fix pass:
- **Arasaka Tower** (`loc_arasaka_tower`):
  - The bottom floor is in alert mode (red lights, barriers).
  - The lifts don't reach the bottom floor, and from the atrium there is no
    lift back up to counter-intel.
  - The tour stop is the corpo-start area, which is closed after that
    prologue.
  - Many security NPCs are missing.
  - With S2, it is the reference case for a corp HQ.
- **Konpeki Plaza**, owner decision 166: lockdown dressing, staff and lifts.
- **Black Sapphire**'s approach (`q303_paradise`): it is "a mission area for
  getting into the Black Sapphire". The fix agent is listing the quest's
  guard spawns there as S1 input.

### S12. Later, maybe

The owner sees the Cynosure bunker (`q305_bunker`) as a possible unique
player base, Blackwall residue and all (owner decision 164). It stays
excluded for now.

---

## 2. Owner classifications from this tour (applied)

Applied to `classification.json` and `venue-classification.md` on
2026-11-27, each `reason` ending "Owner, tour 2026-11-27".

| Venue | Change |
| --- | --- |
| `loc_q115_fancy_restaurant` Embers | medium -> small |
| `loc_sq021_police_lab` NCPD Lab | medium -> large (NCPD tech) |
| `loc_sts_cct_cpz_01` Memorial Park NCART | tech -> military (NCPD, medium) |
| `loc_sts_cct_dtn_03` Empathy | medium -> large |
| `loc_sts_wat_kab_07` Ho-Oh | medium -> large |
| `loc_sts_wat_kab_102_cargo` Kabuki container yard | medium -> large (type waits on S3) |
| `loc_sts_wat_lch_01_server_room` H11 server room | small espionage -> medium tech; needs garrison work |
| `loc_sts_wat_lch_03_dojo` Deravaja Dojo | medium -> large (military) |
| `loc_sts_wat_lch_06_neon_basement` Glitter lab | medium -> large (type waits on S4) |
| `loc_sts_std_arr_12_gas_station` Tirempire | medium -> small (a garage, S5) |
| `loc_q004_lizzys_nightclub` Lizzie's | needs garrison work (S2) |
| `loc_q303_paradise` Black Sapphire | needs garrison work (S1) |

Confirmed unchanged:
- El Coyote Cojo: medium economy.
- No-Tell Motel: medium economy.
- La Catrina (`sts_hey_rey_06`): large.
- Totentanz: large.
- Autowerks: medium.
- Dodger's precinct: military.
- Luxor High Wellness Spa: espionage.
