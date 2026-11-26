# New Venues (planned)

Status: backlog, 2026-11-26. Places vanilla only shows as memories or
ruins, which the owner wants as working 2077 venues. These are new content,
not restores: the venue research pipeline (`docs/venue-playbook.md`)
excluded them because there is nothing in vanilla data to re-activate.

## Club Atlantis (Watson)

- **Vanilla:** a closed, signless shell with rubble across the frontage. Its
  interior and crowd exist only as Johnny's 2013 memory sets (q108 prefabs),
  and a `var_deco_present` cleanup variant marks the present-day look.
- **Needed:**
  - the memory interior shown in the present, or a reachable interior;
  - the rubble frontage cleared (no door device exists; it is geometry or a
    variant);
  - new 2077 occupants;
  - an owner (a faction or an independent).
- **Research:** `~/.cache/neon-ascendancy/extracts/venues/research/loc_q108_atlantis_club/notes.md`.

## The Hammer (Downtown)

- **Vanilla:** the club exists only as the Samurai-concert memory set (q101,
  and q108 via q110), built in an off-map backlot. The game's `District`
  enum still has `Downtown_TheHammer = 64`, and our territory research lists
  "The Hammer club" as a Downtown control centre, but no present-day building
  exists.
- **Needed:**
  - present-day geometry: place the set on the map, or build a facade and
    interior;
  - new 2077 occupants;
  - an owner.
- **Research:** `~/.cache/neon-ascendancy/extracts/venues/research/loc_q101_concert/notes.md`.

## Open questions

1. Who runs each club in 2077 (a faction node, or independent)?
2. Atlantis: can the memory interior be shown in the present through variants
   alone, or does it need new geometry?
3. Hammer: is relocating the backlot set feasible with ArchiveXL world
   additions, or is a new build needed?
