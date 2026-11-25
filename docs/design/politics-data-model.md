# Politics Data Model — Factions, Blocs, Policies, Relations, Wars (spec draft)

Status: draft, 2026-11-25. Implements the politics parts of
[`gameplay-systems.md`](gameplay-systems.md). Companion to
[`territory-data-model.md`](territory-data-model.md), which owns influence
points, sub-districts and adjacency. Built from
[`docs/research/factions/politics/`](../research/factions/politics/).
Nothing here is implemented yet.

Principles (same as the territory spec): static facts in `world.db`;
mutable state in the playthrough DB; rules are pure functions in
`native/lib/sim`; one decision in one place; tunables and modifiers are data,
not code.

## 1. Concepts

| Term | Meaning |
| --- | --- |
| **Faction kind** | `territorial` (holds influence points), `political` (Night Corp, Government of Night City: no territory, acts on politics) or `external` (Chinese state, NUSA, NetWatch, SovOil: no territory, may field squads via spawn templates). One table for all kinds. |
| **Archetype** | Syndicate, Corporation, Paramilitary, Tribe, Ideological Collective (plus `special` for Scavs). Sets pillar strength/weakness, the default government and which governments are allowed. |
| **Government** | The faction's leadership model, held as a **policy** in the government slot: `autocracy` (single leader), `council`, `packs`, `collective`, `cells` (Scavs). Changeable in play. |
| **Bloc** | An internal political faction (vassal) with a leader, lieutenants and **muscle**. Never absorbed. May hold influence points. |
| **Manpower** (UI: **Muscle**) | A bloc's fighting strength. Spent defending and attacking points. Regenerates through recruitment. Data and code use `manpower`; the UI says Muscle. |
| **Demand / severity** | Every bloc's two personality parameters: how much it needs (share of influence, policies) to stay content, and how hard it escalates when unmet. MaxTac: low demand, very high severity. |
| **Policy** | An option in a slot. Slots belong to the government or to a pillar; **each pillar can have several slots** (start with one or two, expand to three or more). Options carry data-driven modifiers. |
| **Relation** | Level `allied`/`friendly`/`neutral`/`hostile` plus a `rivalry` flag. War and pacts are separate states. |
| **War** | A state between two factions, opened by a casus belli (claims). Has war goals and ends in a settlement. |
| **Pact** | A non-aggression state for a duration; breakable at a political cost. |
| **Claim** | A faction's in-progress or completed political claim (coring) on a point; completed claims give title. |

## 2. Static tables (`world.db`)

### `factions` (columns added on top of the territory spec)

`kind` (`territorial`, `political`, `external`), `archetype`,
`archetype_strength`, `archetype_weakness`, `strength_pillar`,
`weakness_pillar`, `initial_government` (nullable: defaults to the
archetype's default, set only as an override, e.g. Valentinos → `autocracy`,
Aldecaldos → `autocracy`), `spawn_template_faction_id` (nullable),
`attitude_group` (CName).

### `archetypes` and `archetype_governments`

- `archetypes`: archetype code, strength/weakness pillars, bloc-management
  modifiers (as policy-style modifier rows, §2.6).
- `archetype_governments`: `(archetype, government, is_default)`. Default
  mapping: Syndicate → council; Corporation → autocracy (CEO + board);
  Paramilitary → autocracy; Tribe → packs; Ideological → autocracy;
  special (Scavs) → cells only.

### `blocs`, `bloc_policy_preferences`, `leaders`

- `blocs`: `bloc_id`, `faction_id`, `display_name`, `goals`,
  `initial_leader_id`, `demand` (0–100), `severity` (multiplier, 1.0 =
  normal), `initial_manpower`, `traits` (e.g. MaxTac: `elite_response`).
- `bloc_policy_preferences`: `(bloc_id, option_code, weight)`, weight
  −2..+2. This is how blocs like or dislike policies.
- `leaders`: `leader_id`, `faction_id`, `bloc_id` (nullable), `display_name`,
  `rank` (`leader`, `sub_leader`, `lieutenant`), `character_record_id`
  (nullable), `presence_class`, `home_point_id` (nullable),
  `is_original` (true for mod-invented directors such as Kang Tao's).

### `faction_relations` and `initial_pacts`

- `faction_relations`: `faction_a < faction_b`, `initial_level`
  (`friendly`/`neutral`/`hostile`; the build rejects `allied`), `rivalry`
  (bool), `evidence`, `confidence`. Symmetric. Build rules: an attested
  stance beats a no-evidence neutral; removed-branch stances are neutral;
  Scavs are hostile to all; unresolved conflicts fail the build until an
  override settles them.
- `initial_pacts`: `(faction_a, faction_b, duration_cycles, reason)`, e.g.
  Tyger Claws–Mox (the 2067 deal).

### `policy_slots`, `policy_options`, `policy_modifiers`, `faction_initial_policies`

- `policy_slots`: `slot_code`, `group` (`government` or a pillar), `index`
  (supports many slots per pillar), `display_name`.
- `policy_options`: `option_code`, `slot_code`, `display_name`,
  `adoption_cost` (political influence), `cooldown_cycles`; child table
  `policy_option_archetypes` restricts which archetypes may adopt it.
- `policy_modifiers`: `(option_code, target, op, value)`. `op` is `add` or
  `mul`. `target` comes from one registry of modifiable quantities in
  `native/lib/sim` (e.g. `bloc.demand`, `bloc.severity`,
  `bloc.manpower_regen`, `pillar.<pillar>.output`, `point.strength`,
  `war.support_threshold`, `trade.hostile_penalty`). The registry is the
  single list of what can be modified; the build rejects unknown targets.
- `faction_initial_policies`: `(faction_id, slot_code, option_code)`.

Archetype and bloc-management effects use the same modifier rows, so there
is one modifier mechanism for everything.

## 3. Playthrough state (mutable)

| State | Fields |
| --- | --- |
| Faction | `leader_id`, `leadership_state` (`stable`, `tension`, `internal_war`), `political_influence` (balance) |
| Faction policies | `(faction_id, slot_code) → option_code, adopted_cycle` (the government slot gives the leadership model) |
| Bloc | `leader_id`, `satisfaction` (0–100), `manpower`, `escalation` (`content`, `demanding`, `refusing`, `revolt`) |
| Relation | `level`, `rivalry` per pair |
| Pacts | `(faction_a, faction_b, kind, start_cycle, end_cycle, origin)` (`origin`: peace, deal, initial) |
| Wars | `war_id`, `attacker`, `defender`, `start_cycle`, `end_cycle`, `outcome`; `war_goals (war_id, point_id, claimant)` |
| Claims | `(faction_id, point_id, progress, completed_cycle)` |

Derived, not stored: war support, faction influence totals, the leadership
model, effective modifiers.

## 4. Rules (pure functions)

1. **Government and leadership model.** The government slot's option is the
   leadership model. A faction starts with its `initial_government` or its
   archetype default.
   - **Changing government** needs blocs holding ≥ 50% of the faction's
     influence to support it (same rule as sub-district holding). The
     change sets `tension`.
2. **Bloc satisfaction** moves with:
   - influence share vs effective demand;
   - losses or threats to the bloc's own points;
   - lieutenant deaths;
   - **manpower losses**, weighted heavier when spent defending another
     bloc's points;
   - preferences for the faction's current policies;
   - influence points the leader grants.
3. **Escalation ladder:** when satisfaction stays below the bloc's
   threshold, escalation steps `content → demanding → refusing → revolt`.
   - The step speed and the effects scale with `severity`.
   - `refusing` withholds the bloc's manpower and traits (MaxTac refusing
     means NCPD loses its elite response).
   - `revolt` is an internal turf war, or secession as its own faction.
4. **Leadership state:** a bloc holding ≥ 50% of the faction's influence,
   with a living leader, leads (`stable`).
   - A rival bloc above a threshold, or a revolting bloc, means `tension`.
   - No bloc at 50%, or a dead leader with no successor, means
     `internal_war`, which ends when a bloc passes 50% and keeps it.
5. **War support** = influence-weighted satisfaction of the faction's blocs.
   - Below the (modifiable) threshold, the leader must sue for peace or risk
     a revolt.
   - The winner's support caps how harsh its terms can be.
6. **Peace settlement:**
   - War goals the winner holds transfer title to the winner.
   - Other points captured in the war revert by default.
   - The winner may keep some as untitled occupations if its war support
     allows. Occupations bring reduced strength, upkeep and bloc drain, and
     the original owner keeps a ready claim.
   - Peace starts an automatic non-aggression pact.
   - No claim progress during an active war, or only at a heavy penalty.
7. **Policy adoption** costs political influence, respects cooldowns and
   archetype restrictions, and shifts bloc satisfaction through
   preferences.
8. **Relations:**
   - Trade is allowed at every level; hostility penalises it (via the
     economy design).
   - Rivalry makes casus belli and coalition drift cheaper.
   - Anti-snowball drift pushes nearby factions toward hostile against a
     fast grower.
   - No `allied` at game start.
9. **Player sub-leader grant:** as in `gameplay-systems.md` §5 (from the
   strongest bloc unless that breaks its control; then the second;
   seeded-RNG roll on ties).

## 5. Seed sources

- `factions` kind/archetype/pillars: `gameplay-systems.md` §1 plus overrides.
- Blocs and leaders: the politics research JSON blocks
  (`internal_factions`, `leaders`), mapped through
  `data/politics/overrides.json` (owner decisions: the alternate timeline,
  original directors, demand/severity values, MaxTac as an NCPD bloc).
- Relations: the research `relations` rows, reconciled per §2 (the
  reconciliation already found 99 agreeing pairs, 32 placeholder overrides
  and 5 owner-settled conflicts).
- Policies: a small hand-written catalogue in `data/politics/policies.json`.

## 6. Decided since the draft

- **Political influence** is earned every turn (24 in-game hours): each
  influence point grants a set amount, plus a base amount per bloc derived
  from its historical value and its leader.
- **Alliances** are military: allies may refuse a call to an offensive war
  but must join defensive wars. An alliance also unlocks trade in more
  advanced equipment (e.g. Tyger Claws allied with Arasaka can buy weapon
  tiers above their normal cap).

## 7. Open questions

1. **Starting policy catalogue** — **deferred** until the basics of the
   Economy, Military, Espionage, Technology and Culture systems exist. The
   slot/option/modifier architecture above stays in place for it.
2. **Renaming influence points** (candidate: "sectors").
