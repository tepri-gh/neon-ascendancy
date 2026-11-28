# Economy Data Model — Resources, Income, Upkeep, Deals (spec draft)

Status: draft, 2026-11-25. Implements the economy parts of
[`gameplay-systems.md`](gameplay-systems.md) §8b. Companion to
[`territory-data-model.md`](territory-data-model.md) (nodes) and
[`politics-data-model.md`](politics-data-model.md) (blocs, relations,
policies, modifiers). Nothing here is implemented yet.

Principles: static facts in `world.db`; mutable state in the playthrough
DB; rules are pure functions in `native/lib/sim`; every number is a tunable
in one data file (`data/economy/tunables.json`); effects go through the
politics spec's modifier registry.

## 1. Concepts

| Term | Meaning |
| --- | --- |
| **Turn** | 24 in-game hours. All income, upkeep and drift settle per turn. |
| **Resources** | Per faction: **Influence** (Politics), **Eddies** (Economy, base currency), **Intel** (Espionage), **Research** (Technology; UI R&D). Manpower (UI Muscle) is per bloc (politics spec). Culture has no currency; it acts as cultural pressure (territory spec). |
| **Materiel** | Per-faction stockpile by category (`weapons`, `vehicles`, `equipment`, `cyberware`, `drugs`) and tier (1–5). Bought with eddies; capacity tied to technology. There is no production simulation. |
| **Fielded tier** | The highest materiel tier a faction can use in a category: the lower of its tech-tree tier and its access tier. |
| **Access tier** | The highest tier a faction can buy in a category, through relations, alliances and deals. |
| **Branch budget** | A corp's per-turn subsidy from its global head office. It rises and falls with branch performance. Corps' global industry stays off-map. |
| **Deal** | A one-off or recurring contract between two factions that exchanges eddies for goods: materiel, intel, hired manpower, protection, **nodes and titles**. |
| **Upkeep** | Per-turn eddie cost of manpower and nodes; occupations cost more. |
| **Deficit** | Unpaid upkeep in a turn. Its severity drains both bloc satisfaction and node loyalty. |

## 2. Static tables (`world.db`)

- `revenue_streams`: `stream_code` (the research vocabulary in
  `docs/research/factions/METHOD.md` §7), `base_eddies`, optional
  `pillar_points` per pillar, and `discount_category` (the materiel
  category it discounts, e.g. `cyberware`, `vehicles_chop` → `vehicles`,
  `manufacturing`/`arms` → `weapons`, `drugs` → `drugs`). Production nodes
  only give a minor discount; there is no manufacturing.
- `materiel_prices`: `(category, tier) → base_price`.
- `faction_tech_start`: `(faction_id, category, tier)`, the starting
  tech-tree tier per category (e.g. Arasaka weapons 5). The full shared
  tech tree comes later; until then, tier per category is the tech state.
- `faction_budgets`: `(faction_id, base_subsidy)` for corp branches;
  absent for non-corps.

All rates (upkeep per manpower and per node, the occupation multiplier,
discount size, deficit drain curves, deal price curves, the hostile-trade
penalty) live in `data/economy/tunables.json`.

## 3. Playthrough state (mutable)

| State | Fields |
| --- | --- |
| Treasury | `(faction_id) → eddies, influence, intel, research` |
| Materiel | `(faction_id, category, tier) → quantity` |
| Tech | `(faction_id, category) → tier, research_progress` |
| Branch budget | `(faction_id) → subsidy, performance` |
| Deals | `deal_id`, `seller`, `buyer`, `good_kind` (`materiel`, `intel`, `manpower`, `protection`, `node`, `title`), `good_ref`, `quantity`, `price`, `recurring` (bool), `turns_left`, `state` |
| Node | `loyalty` (0–100, toward its controller), plus the territory spec's fields |

## 4. Rules (pure functions, settled each turn in this order)

1. **Income.** For each node: `base_eddies` of its revenue streams, scaled
   by node **size** (`small / medium / large`), title efficiency, node strength,
   loyalty, sub-district holding, policies and archetype modifiers (per-subdistrict
   scarcity scaling is deferred until simulation testing shows whether it is
   needed). Each node also produces Influence, its primary pillar output, and
   **Culture** (`economy > espionage > tech > military`). Blocs add their base
   Influence (history and leader).
2. **Branch budgets.** Corps receive their subsidy; performance (territory
   held, losses, later the stock market) moves it for the next turn.
3. **Deals.** Recurring deals settle; one-off deals execute on acceptance.
   - Price = base × relation curve × hostile penalty (hostile factions,
     Scavs included, can still trade, at worse rates).
   - A **node** deal transfers control.
   - A **title** deal transfers the legal claim only. The seller must hold
     what it sells.
4. **Upkeep.** Pay manpower and node upkeep (occupations at a multiplier).
5. **Deficit.** If eddies cannot cover upkeep:
   - severity = shortfall ÷ required;
   - bloc satisfaction and node loyalty both drain, by an amount that
     grows with severity (tunable curve, steeper at high severity).
6. **Loyalty drift.**
   - Cultural pressure from neighbouring nodes pulls each node's loyalty
     toward the pushing faction.
   - Garrison strength, eddie spending and policies resist the pull.
   - Very low loyalty risks the node flipping (to the pushing faction, or
     to Scavs).
7. **Materiel.**
   - Fielded tier = min(tech tier, access tier) per category.
   - Access comes from relations and deals; an alliance lifts the cap
     (e.g. Tyger Claws reach Arasaka-grade weapons only when allied).
   - Production nodes discount matching purchases slightly.
8. **Research.** Research points advance tech progress per category;
   Technology strength speeds it.

## 5. Open questions

1. All numbers (tunables) — set once the review map and a first sim pass
   exist.
2. The shared tech tree's structure beyond tier-per-category.
3. Intel's uses (the Espionage design).
4. The stock market's tie to branch performance and corp revenue.
5. The player org's treasury vs the in-game wallet (the TransactionSystem
   eddies V carries).
