# Open Design Questions

Status: 2026-11-25, for owner review. Each question has context, a
suggestion, and an **Answer** section to fill in. Leave an answer blank to
accept the suggestion, or write "skip" to defer the question. Answers flow into
[`gameplay-systems.md`](gameplay-systems.md) and
[`territory-data-model.md`](territory-data-model.md).

Background: 17 faction location docs and 18 politics docs under
`docs/research/factions/`.

---

## A. Relations

### A1. Does "rival" count as Hostile or Neutral?

Research uses `rival` for ongoing competition short of open hostility.
Mapped onto the four levels, it decides how warlike the city starts
(136 territorial pairs; the 16 Scav pairs are Hostile either way):

| Rival maps to | Hostile | Neutral | Friendly |
| --- | ---: | ---: | ---: |
| Hostile | 62 | 55 | 19 |
| Neutral | 46 | 71 | 19 |

**Suggestion:** Neutral, plus a `rivalry` flag that makes coalition drift
and casus belli cheaper between the two. The city starts tense but not at
total war; wars emerge from the simulation.

**Answer:**

### A2. Attested stance beats a "neutral" placeholder

Of 37 cross-doc disagreements, 32 are one doc's `neutral` (which the method
defines as "no evidence") against the other doc's attested stance.

**Suggestion:** when one side is `neutral` and the other has evidence, use
the attested stance.

**Answer:**

### A3. The five genuine conflicts (both sides have evidence)

| Pair | Side A | Side B | Suggestion |
| --- | --- | --- | --- |
| Tyger Claws ↔ Mox | war | rival | Hostile (the 2067 massacre; the Mox side adds a later deal) |
| Militech ↔ 6th Street | trade (former arms supplier) | hostile (Gunner's anti-corp regime) | Hostile (the trade is historical) |
| Animals ↔ Maelstrom | hostile | rival | Hostile (Maelstrom also sells them stolen drugs: a mission hook) |
| Tyger Claws ↔ Scavs | rival | hostile | Hostile (Scav rule) |
| Wraiths ↔ Scavs | rival | trade | Hostile (Scav rule) |

**Answer:**

### A4. Scav trade channels

Lore shows some Scav dealings: Barghest tolerates them for pay, Scavs sell
cyberware to the Aldecaldos, and there is a victim trade with the Tyger
Claws.

**Suggestion:** Scavs stay Hostile with everyone in the simulation; these
channels are black-market and mission flavour only.

**Answer:**

### A5. Truce / non-aggression

Lore has truces (the 2067 Tyger–Mox deal, NCPD tolerating gangs).

**Suggestion:** not a fifth relation level. A **pact** state between two
Hostile factions, like `at_war`: it blocks war declarations for a duration
and can be broken at a political cost.

**Answer:**

### A6. Relation flavour: supplier/buyer, patron/client, direction

`trade` lumps sellers and buyers together; `patron`/`client` and
`hostile` have a direction (who funds whom, aggressor vs target).

**Suggestion:** keep only the level as simulation state, plus an optional
directional `kind` (`supplier`, `buyer`, `patron`, `client`, `aggressor`)
as seed flavour for missions and the economy later.

**Answer:**

### A7. External powers

NUSA, the Chinese state (Kang Tao), SovOil (Petrochem's rival) and NetWatch
shape relations but hold no territory.

**Suggestion:** a small `external_powers` table: no territory and no
spawns, but they can act as patrons or adversaries and trigger events.
NUSA, as you planned, is the first to get mechanics; the rest stay data
only for now.

**Answer:**

---

## B. Leadership and blocs

### B1. Leadership models

The research found four shapes:

- **single** leader (most factions);
- **council** (Tyger Claws: a council of bosses, no oyabun);
- **packs** (Animals, Wraiths: independent pack/crew leaders);
- **none** (Scavs: cells only).

**Suggestion:** a `leadership_model` per faction. A council shares power
and only falls into internal war if it splits. Packs cannot be decapitated
but act together poorly. Scav cells never unify.

**Answer:**

### B2. Starting leadership states (alternate timeline)

| Faction | Suggested start |
| --- | --- |
| Maelstrom | Internal war: Royce vs Brick/Patricia |
| Valentinos | Tension: Campo jailed, Gustavo interim, crew bosses (Zoe, Rogelio, Gizmo) |
| Arasaka | Tension: Yorinobu leads; Hanako/Saburo loyalists and Michiko's board bloc |
| Barghest | Stable under Hansen; Bennett and Jago as sub-leaders |
| Tyger Claws | Council, stable |
| 6th Street | Stable under Gunner; Morton's old guard as a bloc |
| Aldecaldos | Tension: Saul vs Panam's independence bloc |
| Militech | Stable but split: serve-the-state vs own-the-state blocs |
| Voodoo Boys | Two cells (Coastview: Brigitte/Placide; Dogtown) |
| Mox | Stable: Susie Q; Judy's activist wing |
| Animals, Wraiths | Packs |
| Kang Tao, Biotechnica, Petrochem | See B3 |
| NCPD | Stable but hollow: Commissioner Fawlter (off-screen, corrupt); MaxTac as an autonomous vassal under Lt. Melissa Rory; clean-cop remnant (River Ward) vs the precinct machine |

**Answer:**

### B3. Corps with no named 2077 leader

Kang Tao and Biotechnica have no named 2077 head (Biotechnica's top named
record is regional director Joanne Koch). Petrochem's CEO, Lars Muhammad,
exists only in lore, and Night Corp's leadership is historical.

**Suggestion:** invent a Night City director for Kang Tao, Biotechnica and
Petrochem; their lore says little, so original characters are fine.
Kang Tao's director answers to China, which fits its Espionage strength.

**Answer:**

### B4. Empty flagship venues

With the campaign disabled, several flagship places have no gang staff at
all (Clouds' Tyger Claws are story-only), and nearly all named leaders are
story-only.

**Suggestion:** fold this into the deferred leader-spawning task: HQs and
major points get mod-spawned garrisons and leaders, using the faction's
own character records or its spawn template.

**Answer:**

---

## C. Territory and data

### C1. Vanilla gang lists per sub-district

The vanilla map's "gangs in this district" list (`District_Record.Gangs()`)
would sanity-check our computed starting owners.

**Suggestion:** a one-time dev CET probe dumps it to a log. You run the
game once and I parse it.

**Answer:**

### C2. Spawn templates and re-tagging

Petrochem (and any NPC-less faction) would spawn Militech-template NPCs
re-tagged at runtime into its own attitude group. The scanner would still
say Militech unless TweakXL clones the records.

**Suggestion:** Petrochem → Militech template. Do the cheap runtime
re-tag first and verify the TweakXL-clone scanner label with an in-game
probe later.

**Answer:**

### C3. Dropped factions' places

Places owned by non-modeled factions are dropped as points: Trauma Team,
Afterlife, Orbital Air (the Morro Rock spaceport), Zetatech, NetWatch, and
the fixers' offices.

**Suggestion:** drop them as influence points but keep them as world
locations (the Afterlife stays a bar, fixers stay mission givers). Confirm
nothing there should go to a modeled faction instead.

**Answer:**

### C4. Aldecaldos camp state

There is the old Mobile Camp and the new Nomad Camp (after *Riders on the
Storm*).

**Suggestion:** the old Mobile Camp, since the story never advances.

**Answer:**

### C5. Phantom Liberty content that depends on removed events

Dogtown, Barghest and Hansen stay, but some Phantom Liberty gigs and
activities are gated by story progress (e.g. *Roads to Redemption*).

**Suggestion:** keep Dogtown open-world content and its gigs available,
ungated by the removed story.

**Answer:**

### C6. Story-branch-only stances

Some stances exist only on branches the timeline removes
(Aldecaldos–Arasaka is hostile only on the Star ending; Kang Tao–Aldecaldos
comes from the Relic chain).

**Suggestion:** treat them as Neutral in the starting matrix and keep them
documented as history.

**Answer:**

### C7. Retiring the current test setup

The active-flag subset of the old grid and the separate HQ pins are a
stopgap.

**Suggestion:** remove both when the generator's influence points land;
HQ becomes a point category.

**Answer:**

---

## D. Process

### D1. Next build step

**Suggestion:**

1. Consistency pass over the politics docs (`presence_class`, timeline,
   courier-pool citations).
2. Revise the data-model spec with these answers.
3. Build the generator.
4. Publish a review map of all influence points, owners and sub-district
   holders for you to check before anything goes in game.

**Answer:**

### D2. Anything else?

Free space for questions or direction I haven't asked about.

**Answer:**
