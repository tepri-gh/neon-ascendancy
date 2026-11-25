# Faction Politics Research — Method

Status: playbook, 2026-11-25. Derived from the Maelstrom pilot
(`docs/research/factions/politics/maelstrom.md`). Use it with the location
playbook `docs/research/factions/METHOD.md` (data sources, pitfalls,
confidence tags) and the design draft `docs/design/gameplay-systems.md`.

Read `AGENTS.md` first. Do not commit. Do not launch the game. Do helper
scripting outside the repo with `python3 -I`.

## 1. Goal

For one faction, document:

1. **Leadership and ranks.** Who the player could join under, climb past,
   ally with or remove. How members advance.
2. **Internal political factions.** Cliques and blocs, their goals and
   leaders, and what drives internal conflict.
3. **External relations.** One stance toward every other faction, for wars,
   alliances and "guarantor" support when a player founds a gang.
4. **Pillar notes** against the design's archetype and faction pillars.

Output: `docs/research/factions/politics/<faction-code>.md`, where the
filename uses the hyphenated `data/factions.json` code. Use the pilot as the
worked example of depth and format.

## 1.1 Corrections from the first politics batch (override later sections)

1. **One person, several records.** Named NPCs often have alive, dead,
   holocall and braindance variants (`Character.Voodoo_Queen`,
   `q105_voodoo_queen`, `Voodoo_Queen_dead`; `Placide`, `Holocall_Placide`).
   List all of a person's records under one leader entry. Holocall/BD actors
   are not world spawns.
2. **Corps:** the `<Faction> Members` page can be empty. Follow the main
   page's `{{Main|…}}` link (Arasaka: `List of Arasaka employees`).
3. **Presence classes:** add `prologue` (lifepath intros such as
   `q000_corpo_*`: the best model for joining a corp as an employee) and mark
   canonically dead or V-dependent leaders in the `role` text.
4. **Several cells:** if a faction has separate cells (the Voodoo Boys in
   Coastview and Dogtown), name each cell's leadership in `internal_factions`
   and say which loss decapitates which cell.
5. **Current vs historical stance:** the stance is the 2077 state (Arasaka
   and Militech are `rival`, not `war`). Put history in the evidence string.
6. **Direction of `patron`/`client`:** `patron` means this faction protects
   or funds the other; `client` means this faction depends on or works for the
   other. Say which (buyer, supplier, proxy) in the evidence.
7. **Extra rows:** add `netwatch` and `nusa` rows where they matter. They are
   political actors, not territory holders. Patronage of a community that is
   not in `data/factions.json` (e.g. the Haitian diaspora) goes in prose.

## 1.2 Corrections from Valentinos and 6th Street (override later sections)

1. **Check rosters first.** Named NPCs are often in `data/sites/rosters.json`
   (capitalised name suffixes such as `Rogelio_Cruz`, `sts_std_arr_11_lucius`).
   Parse raw sectors only for the rest; only `always_loaded_1` contains
   `worldCommunityRegistryNode`.
2. **Presence classes, full list:** `ambient`, `world-activity` (gigs,
   scanner hustles, NCPD SOCA, Assault in Progress, side/minor jobs),
   `story`, `prologue`, `off-map` (alive in lore, never spawned), `mentioned`
   (named only in shards or dialogue), `historical`. Leaders with only a
   generic quest record (`mq008_6th_street_representative`) or only an
   `areas.jsonl` community count as `world-activity`/`story` by their quest,
   with `character_record_id` set to that record and tagged `[inferred]`.
3. **Record it in JSON:** each leader gets a `presence_class` field.
4. **Elimination:** when two high-rankers share a site and only one has a
   named record, the generic `*_outpost_miniboss` is the other, by
   elimination. Tag it `[inferred]`.
5. **Read the other side.** Search other factions' member pages for
   incidents involving this faction; faction pages alone miss conflicts
   (Maelstrom vs Valentinos is hostile, not neutral).
6. **Filter crowd pools before co-occurrence:** respawn pools
   (`{04_NPC_Gang_Community_Area}`, `mq061_*`), customer crowds (Lizzie's)
   and time-of-day set dressing.
7. **Relations rows:** the required list plus every other
   `data/factions.json` code with an attested relation (e.g. `kendachi`).
8. **Patron/client, one definition:** `patron` = this faction funds,
   supplies or protects the other (Kendachi → 6th Street weapons line);
   `client` = this faction depends on or works for the other (Valentinos as
   Arasaka's hired crew).
9. **Don't import tabletop vocabulary** (e.g. Valentino "sets") absent from
   2077 sources.
10. **Validator:** also enforce exactly one relation per required faction and
    a `presence_class` from the list above on every leader.

## 2. Procedure

1. **Wiki first, via the API** (`action=parse&prop=wikitext&formatversion=2&redirects=1`).
   - Read the faction page's `Notable Members → Leadership` section. It is
     the only compact succession list.
   - Then read `<Faction> Members` (the best named-member table).
   - `Category:<Faction> members` pages may be empty; don't rely on them.
   - Verify red links: some leaders have no page.
2. **Named NPCs are usually not in `data/sites/rosters.json`.** Parse
   `dist/extract/raw/**/always_loaded_*.streamingsector.json` for
   `worldCommunityRegistryNode` templates and collect
   `(entryName, characterRecordId)`. Match exact entry names
   (`royce`, `brick`, `DumDum`, `sq011_patricia`).
3. **Exact record names only, never substring matching.** Tokens collide:
   `kurt`/`kurtz_*` (Barghest's Kurt Hansen), `patricia` (a 6th Street NPC),
   `aaron`, `player`.
4. **Gig/scanner NPCs: join wiki `baseid` → `sites.json` code.** If the NPC
   has no named record, use the site's single `*_miniboss`/`*_psycho`/
   `*_officer` record and tag it `[inferred]`.
5. **Presence class** from phase names and wiki behaviour, not
   `entryActiveOnStart` (it is 0 for every named NPC):
   - `story`: `q###_*`/`sq###_*` phases.
   - `world-activity`: a gig/scanner with a `baseid`.
   - `ambient`: only if the wiki says the NPC persists regardless of quests.
   - `historical`: no 2077 record.

   `open_world` is true only for ambient or world-activity NPCs that exist
   with the campaign disabled. Expect most leaders to be story-only.
6. **Joins that do not work:** `areas.jsonl.community_hash` does not equal
   the raw registry's `communityId.entityId.hash`. Join by entry names,
   marker/area positions, or site `baseid`.
7. **Do not sum overlapping quest communities.** Several `q###_*`
   communities at one place are phases of one site; use them as presence
   proxies only.
8. **Location vs character affiliation.** A location infobox's `affiliation`
   does not describe its guard (Ebunike says Maelstrom; Grayson is Arasaka).
   Use character pages for people.

## 3. Relations

There is no offline attitude matrix. `Attitude_Record.hpp` is opaque and
`Affiliation.hpp` is identity only. Judge each stance by this precedence and
tag the evidence:

1. Explicit violent event (raid, theft, killing, betrayal) → `war`,
   `hostile` or `rival`.
2. Explicit transaction (deal, favour, sale, contract) → `trade`, `client`
   or `patron`.
3. Quest-giver role against the faction → `hostile`.
4. Spatial adjacency only → `neutral` or a low-confidence `rival`, tagged
   `[inferred]`.
5. No evidence → `neutral` + `[inferred]`, stated as a placeholder, never as
   friendship.

Stance vocabulary: `war`, `hostile`, `rival`, `neutral`, `trade`, `ally`,
`patron`, `client`. One stance per row. Put the nuance in the evidence
string (e.g. "hostile with a corrupt trade channel").

Rows required: every faction in `data/factions.json` that the design names
(Tyger Claws, Valentinos, Arasaka, Militech, Kang Tao, Biotechnica,
Petrochem, Barghest, 6th Street, Aldecaldos, Wraiths, Animals, The Mox,
Maelstrom, Voodoo Boys, NCPD, Night Corp, Scavengers), the City Council, the
fixers (Regina, Wakako, Padre, El Capitán, Dakota, Dino, Rogue, Mr. Hands)
and Afterlife. Skip the row for the faction itself.

## 4. Things to look for

- **Succession patterns.** The historic leadership list shows whether
  succession is violent, external or negotiated. This matters more to the
  simulation than one 2077 snapshot.
- **"Dependent" leaders.** The wiki marks many 2077 leaders as dependent on
  V's choices. Record the branches; don't pick one silently.
- **Non-member power centres** (fixers, ripperdocs, corrupt officials,
  workshops): model them as `client`/asset, not members.
- **Neutral ground is not an alliance.** Totentanz is open to all gangs that
  obey Maelstrom's customs: that is a political asset.
- **Player-path hooks:** how one joins, rises, and could found a rival or
  splinter.

## 5. Document template

1. Leadership and ranks (chain of command, succession history, rank
   structure/initiation/advancement, named members mapped to game data, what
   spawns with the campaign disabled, player-path hooks)
2. Internal political factions (blocs; what could drive conflict in a
   simulation)
3. External relations matrix (stance vocabulary, matrix, actors outside
   `data/factions.json`, guarantor assessment)
4. Pillar notes (short, evidence-based; do not redesign)
5. Gaps and uncertainties (with sources consulted)
6. Machine-readable block

## 6. Machine-readable block

A fenced ```json block at the end:

```
{
  "faction_code": "<factions.json code>",
  "leaders": [{"name", "role", "character_record_id" (or null), "location_name" (or null),
               "presence_class", "open_world" (bool), "source", "confidence"}],
  "internal_factions": [{"name", "leader" (or null), "goals", "members_hint", "source", "confidence"}],
  "relations": [{"faction_code", "stance", "evidence", "confidence"}]
}
```

`relations[].faction_code` uses `data/factions.json` codes. Validate before
finishing: strict JSON parse; every `faction_code` exists in
`data/factions.json`; required keys present; `open_world` is a bool; every
stance is in the vocabulary; one relation per required faction.
