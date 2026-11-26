# Hustle sites: crime areas, encounters and nodes

Status: **direction agreed, details open** (owner, 2026-11-26). Needs an
in-depth design discussion before implementation. Core simulation first
(see `docs/roadmap.md`).

Vanilla's NCPD scanner hustles (`loc_ma_*`, 333 sites in the venue
catalogue) are staged crime spots: Assault in Progress, Reported Crime,
Suspected Organized Crime Activity and similar. Each one has spawners,
workspots, attitudes and sometimes loot. The clean slate does not run them,
and they are not restored as ordinary venues. They get three roles instead.

## 1. Node candidates (Organized Crime hideouts)

Some hustle sites are real places that deserve to be territory nodes: drug
manufacturing sites, chop shops, prominent or large gang hangouts. Organized
Crime sites are the likeliest. A research pass classifies all 333 sites and
proposes the node-worthy ones with evidence (see
`~/.cache/neon-ascendancy/extracts/venues/research/hustles/BRIEF.md`).
Accepted ones join `territory-node-candidates.md` and get venue entries like
any other node.

## 2. Encounter and spawn data

Sites not chosen as nodes become spawn and encounter data for the
simulation, so territory between venues does not look dead. A faction's
territory shows its people at these spots, and they add flavour (a deal, a
mugging, a crew on a corner).

Open idea for the war system: kills at encounter sites count toward a
gang's attrition (depleting its muscle) in the simulation, so a war feels
like a campaign across the district rather than clearing one venue. Needs
the in-depth discussion.

## 3. Active crime areas for the NCPD path

If the player joins the NCPD, hustle sites can serve as active crime areas:
being a beat cop is the natural starting path toward a "restore order"
arc for NCPD and MaxTac (see `gameplay-systems.md`).

- **At peace:** NCPD still patrols, so police presence stays visible across
  the city, and crime areas offer beat-cop work.
- **At war:** crime areas inside war zones must not trigger, so a hustle
  never fires in the middle of a gang war. Needs a rule tying hustle
  activation to the territory and war state.

## Open questions

- How encounter-site kills feed attrition, and at what rate.
- How crime areas are selected (district, faction, heat, NCPD strength).
- Whether non-NCPD players ever see crime areas, or only the factions'
  presence at those spots.
- How MaxTac differs from ordinary NCPD work in this arc.
