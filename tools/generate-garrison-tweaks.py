#!/usr/bin/env python3
"""Generate deterministic TweakXL faction garrison templates from data/garrison/faction_templates.json.

Outputs:
  src/r6/tweaks/NeonAscendancy/GarrisonTemplates.yaml

Design invariants (docs/design/node-garrison-and-assault.md §3 & §4):
  - Every generated Character.NA_* record strips Character.ScaleToPlayerLevel so
    garrisons never auto-scale to V's player level; explicit simulation PowerLevel
    is applied on spawn.
  - Covers all 17 territorial factions plus Afterlife Mercs (18 total):
      * 6 combat roles x 3 gear brackets (Low=T1-2, Mid=T3, High=T4-5) = 324 unit records
      * 3 generated boss archetypes x 2 boss tiers (Elite for small, Boss for medium+) = 108 boss records
  - Reusable NPCEquipmentItem + NPCEquipmentGroup records are emitted once per weapon
    preset to avoid duplication.
  - Optional --verify-tweakdb hashes every vanilla TweakDB reference directly against
    Cyberpunk 2077 2.5 EP1 tweakdb_ep1.bin so typos or nonexistent base records fail fast.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
import sys
import zlib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
SPEC_PATH = ROOT / "data" / "garrison" / "faction_templates.json"
DEFAULT_OUT = ROOT / "src" / "r6" / "tweaks" / "NeonAscendancy" / "GarrisonTemplates.yaml"
DEFAULT_TWEAKDB = Path("/home/suvikyi/Games/Cyberpunk 2077/r6/cache/tweakdb_ep1.bin")

MELEE_WEAPONS = frozenset({
    "Items.Preset_Katana_Default",
    "Items.Preset_Machete_Default",
    "Items.Preset_Knife_Default",
    "Items.Preset_Baseball_Bat_Default",
    "Items.Preset_Baton_Alpha",
    "Items.Preset_Baton_Beta",
    "Items.Preset_Hammer_Default",
    "Items.Preset_Crowbar_Default",
    "Items.Preset_Pipe_Wrench_Default",
})

# Role + GearBracket -> (ArchetypeData, NPCRarity, VisualLvlTag, Abilities)
ROLE_ARCHETYPES: dict[tuple[str, str], tuple[str, str, str, list[str]]] = {
    ("GuardRanged", "Low"):  ("ArchetypeData.GenericRangedT1", "NPCRarity.Normal", "Lvl1", ["Ability.IsTier1Archetype"]),
    ("GuardRanged", "Mid"):  ("ArchetypeData.GenericRangedT2", "NPCRarity.Normal", "Lvl2", ["Ability.IsTier2Archetype"]),
    ("GuardRanged", "High"): ("ArchetypeData.GenericRangedT3", "NPCRarity.Normal", "Lvl3", ["Ability.IsTier3Archetype", "Ability.CanDash"]),
    ("GuardMelee", "Low"):   ("ArchetypeData.GenericMeleeT1",  "NPCRarity.Normal", "Lvl1", ["Ability.IsTier1Archetype"]),
    ("GuardMelee", "Mid"):   ("ArchetypeData.GenericMeleeT2",  "NPCRarity.Normal", "Lvl2", ["Ability.IsTier2Archetype", "Ability.CanSprint"]),
    ("GuardMelee", "High"):  ("ArchetypeData.FastMeleeT3",     "NPCRarity.Normal", "Lvl3", ["Ability.IsTier3Archetype", "Ability.CanDash", "Ability.HasKerenzikov"]),
    ("Heavy", "Low"):        ("ArchetypeData.ShotgunnerT2",    "NPCRarity.Rare",   "Lvl1", ["Ability.IsTier2Archetype"]),
    ("Heavy", "Mid"):        ("ArchetypeData.HeavyRangedT2",   "NPCRarity.Rare",   "Lvl2", ["Ability.IsTier2Archetype"]),
    ("Heavy", "High"):       ("ArchetypeData.HeavyRangedT3",   "NPCRarity.Rare",   "Lvl3", ["Ability.IsTier3Archetype", "Ability.CanUseCombatStims"]),
    ("Sniper", "Low"):       ("ArchetypeData.SniperT2",        "NPCRarity.Rare",   "Lvl1", ["Ability.IsTier2Archetype"]),
    ("Sniper", "Mid"):       ("ArchetypeData.SniperT2",        "NPCRarity.Rare",   "Lvl2", ["Ability.IsTier2Archetype", "Ability.HasKerenzikov"]),
    ("Sniper", "High"):      ("ArchetypeData.FastSniperT3",    "NPCRarity.Rare",   "Lvl3", ["Ability.IsTier3Archetype", "Ability.HasKerenzikov", "Ability.CanDash"]),
    ("Netrunner", "Low"):    ("ArchetypeData.NetrunnerT1",     "NPCRarity.Rare",   "Lvl1", ["Ability.IsTier1Archetype", "Ability.IsNetrunnerArchetype", "Ability.HasCyberdeck", "Ability.CanQuickhack"]),
    ("Netrunner", "Mid"):    ("ArchetypeData.NetrunnerT2",     "NPCRarity.Rare",   "Lvl2", ["Ability.IsTier2Archetype", "Ability.IsNetrunnerArchetype", "Ability.HasCyberdeck", "Ability.CanQuickhack"]),
    ("Netrunner", "High"):   ("ArchetypeData.NetrunnerT3",     "NPCRarity.Rare",   "Lvl3", ["Ability.IsTier3Archetype", "Ability.IsNetrunnerArchetype", "Ability.HasCyberdeck", "Ability.CanQuickhack", "Ability.HasKerenzikov"]),
    ("Elite", "Low"):        ("ArchetypeData.FastRangedT2",    "NPCRarity.Elite",  "Lvl2", ["Ability.IsTier2Archetype", "Ability.CanDash"]),
    ("Elite", "Mid"):        ("ArchetypeData.FastRangedT3",    "NPCRarity.Elite",  "Lvl3", ["Ability.IsTier3Archetype", "Ability.HasKerenzikov", "Ability.CanDash"]),
    ("Elite", "High"):       ("ArchetypeData.FastMeleeT3",     "NPCRarity.Elite",  "Lvl3", ["Ability.IsTier3Archetype", "Ability.HasSandevistan", "Ability.HasKerenzikov", "Ability.CanDash"]),
}

# Boss archetype -> (base_role_key, ArchetypeData, extra_abilities)
BOSS_SPECS: dict[str, tuple[str, str, list[str]]] = {
    "Enforcer":  ("Heavy",     "ArchetypeData.HeavyRangedT3", ["Ability.IsTier3Archetype", "Ability.CanUseCombatStims"]),
    "Netrunner": ("Netrunner", "ArchetypeData.NetrunnerT3",   ["Ability.IsTier3Archetype", "Ability.IsNetrunnerArchetype", "Ability.HasCyberdeck", "Ability.CanQuickhack", "Ability.HasKerenzikov"]),
    "Vanguard":  ("Elite",     "ArchetypeData.FastMeleeT3",   ["Ability.IsTier3Archetype", "Ability.HasSandevistan", "Ability.HasKerenzikov", "Ability.CanDash"]),
}


def weapon_slug(preset_id: str) -> str:
    return preset_id.replace("Items.Preset_", "").replace("_Default", "")


def load_tweakdb_records(tdb_path: Path) -> set[int]:
    data = tdb_path.read_bytes()
    _, _, _, _, _, recs_off, _, _ = struct.unpack_from("<IIIIIIII", data, 0)
    (rec_count,) = struct.unpack_from("<I", data, recs_off)
    out: set[int] = set()
    pos = recs_off + 4
    for _ in range(rec_count):
        (tdbid,) = struct.unpack_from("<Q", data, pos)
        out.add(tdbid)
        pos += 12
    return out


def tdbid_of(name: str) -> int:
    b = name.encode("ascii")
    return (len(b) << 32) | (zlib.crc32(b) & 0xFFFFFFFF)


def collect_vanilla_refs(spec: dict[str, Any]) -> set[str]:
    refs: set[str] = {
        "Character.ScaleToPlayerLevel",
        "TargetTracking.BossPreset",
        "AttachmentSlots.WeaponRight",
        "AttachmentSlots.ItemSlotGenericRanged",
        "AttachmentSlots.ItemSlotGenericMelee",
        "NPCRarity.Normal",
        "NPCRarity.Rare",
        "NPCRarity.Elite",
        "NPCRarity.Boss",
        "NPCStatPreset.HighHealth",
    }
    for arch, rarity, _, abilities in ROLE_ARCHETYPES.values():
        refs.add(arch)
        refs.add(rarity)
        refs.update(abilities)
    for _, arch, abilities in BOSS_SPECS.values():
        refs.add(arch)
        refs.update(abilities)
    for fac in spec["factions"]:
        if fac.get("custom_affiliation_base"):
            refs.add(fac["custom_affiliation_base"])
        else:
            refs.add(fac["affiliation"])
        refs.update(fac["bases"].values())
        for wlist in fac["weapons"].values():
            refs.update(wlist)
        refs.update(fac["boss_weapons"].values())
    return refs


def render_yaml(spec: dict[str, Any]) -> str:
    lines: list[str] = [
        "# GENERATED FILE — DO NOT EDIT BY HAND.",
        "# Source: data/garrison/faction_templates.json",
        "# Generator: tools/generate-garrison-tweaks.py",
        "#",
        "# Neon Ascendancy §4 TweakXL Faction Garrison Template Matrix.",
        "# Separate from Dev/garrison_spike.yaml. Every record strips",
        "# Character.ScaleToPlayerLevel so simulation-owned PowerLevel governs scaling.",
        "",
    ]

    # 1. Custom affiliations (Petrochem clones UnaffiliatedCorpo so scanner & AI stay valid).
    custom_affs = [f for f in spec["factions"] if f.get("custom_affiliation_base")]
    if custom_affs:
        lines.append("# --- Custom Faction Affiliations ---")
        for fac in sorted(custom_affs, key=lambda f: f["pascal"]):
            lines.extend([
                f"{fac['affiliation']}:",
                f"  $base: {fac['custom_affiliation_base']}",
                f"  enumName: {fac['pascal']}",
                "",
            ])

    # 2. Shared weapon NPCEquipmentItem + NPCEquipmentGroup records (deduplicated).
    all_weapons: set[str] = set()
    for fac in spec["factions"]:
        for wlist in fac["weapons"].values():
            all_weapons.update(wlist)
        all_weapons.update(fac["boss_weapons"].values())

    lines.append("# --- Shared Weapon Equipment Groups ---")
    for preset in sorted(all_weapons):
        slug = weapon_slug(preset)
        on_body = (
            "AttachmentSlots.ItemSlotGenericMelee"
            if preset in MELEE_WEAPONS
            else "AttachmentSlots.ItemSlotGenericRanged"
        )
        lines.extend([
            f"EquipmentItem.NA_{slug}:",
            "  $type: gamedataNPCEquipmentItem_Record",
            f"  item: {preset}",
            "  equipSlot: AttachmentSlots.WeaponRight",
            f"  onBodySlot: {on_body}",
            "",
            f"Equipment.NA_{slug}:",
            "  $type: gamedataNPCEquipmentGroup_Record",
            "  equipmentItems:",
            f"    - EquipmentItem.NA_{slug}",
            "",
        ])

    # 3. Per-faction combat roles x 3 gear brackets + 3 boss archetypes x 2 tiers.
    roles: list[str] = spec["roles"]
    brackets: list[str] = spec["gear_brackets"]
    boss_archetypes: list[str] = spec["boss_archetypes"]

    for fac in spec["factions"]:
        pascal = fac["pascal"]
        aff = fac["affiliation"]
        att = fac["attitude_group"]
        override_aff = bool(fac.get("override_affiliation", False))
        vtags_override: list[str] | None = fac.get("visual_tags_override")

        lines.append(f"# === {pascal} ({fac['code']}, faction_id={fac['faction_id']}) ===")
        for role in roles:
            base_rec = fac["bases"][role]
            role_weapons = fac["weapons"][role]
            if len(role_weapons) != len(brackets):
                raise ValueError(f"{pascal}.{role} must specify {len(brackets)} bracket weapons")
            for bi, bracket in enumerate(brackets):
                preset = role_weapons[bi]
                eq_group = f"Equipment.NA_{weapon_slug(preset)}"
                arch, rarity, lvl_tag, abilities = ROLE_ARCHETYPES[(role, bracket)]
                # Match ranged vs melee archetype if a faction's High-bracket Elite uses a gun.
                if role == "Elite" and bracket == "High" and preset not in MELEE_WEAPONS:
                    arch = "ArchetypeData.FastRangedT3"
                rec_name = f"Character.NA_{pascal}_{role}_{bracket}"
                lines.extend([
                    f"{rec_name}:",
                    f"  $base: {base_rec}",
                    f"  archetypeData: {arch}",
                    f"  rarity: {rarity}",
                    f"  primaryEquipment: {eq_group}",
                    f"  baseAttitudeGroup: {att}",
                    "  isCrowd: false",
                    "  statModifierGroups:",
                    "    - !remove Character.ScaleToPlayerLevel",
                ])
                if override_aff:
                    lines.append(f"  affiliation: {aff}")
                if vtags_override:
                    lines.append("  visualTags:")
                    for tag in vtags_override:
                        lines.append(f"    - {tag}")
                    lines.append(f"    - {lvl_tag}")
                else:
                    lines.append("  visualTags:")
                    lines.append(f"    - !append-once {lvl_tag}")
                if abilities:
                    lines.append("  abilities:")
                    for ab in abilities:
                        lines.append(f"    - !append-once {ab}")
                lines.append("")

        # Generated Lieutenant Boss templates: Elite tier (small nodes) + Boss tier (medium+ nodes).
        for b_arch in boss_archetypes:
            base_role, arch_data, extra_ab = BOSS_SPECS[b_arch]
            base_rec = fac["bases"][base_role]
            preset = fac["boss_weapons"][b_arch]
            eq_group = f"Equipment.NA_{weapon_slug(preset)}"
            if b_arch == "Vanguard" and preset not in MELEE_WEAPONS:
                arch_data = "ArchetypeData.FastRangedT3"
            for tier_label, rarity_rec, is_full_boss in (
                ("Elite", "NPCRarity.Elite", False),
                ("Boss", "NPCRarity.Boss", True),
            ):
                rec_name = f"Character.NA_Boss_{pascal}_{b_arch}_{tier_label}"
                abilities = list(extra_ab)
                lines.extend([
                    f"{rec_name}:",
                    f"  $base: {base_rec}",
                    f"  archetypeData: {arch_data}",
                    f"  rarity: {rarity_rec}",
                    f"  primaryEquipment: {eq_group}",
                    f"  baseAttitudeGroup: {att}",
                    "  isCrowd: false",
                    "  statModifierGroups:",
                    "    - !remove Character.ScaleToPlayerLevel",
                ])
                if is_full_boss:
                    lines.extend([
                        "    - !append-once NPCStatPreset.HighHealth",
                        "  threatTrackingPreset: TargetTracking.BossPreset",
                        "  bossHealthBarThresholds:",
                        "    - 0.66",
                        "    - 0.33",
                    ])
                if override_aff:
                    lines.append(f"  affiliation: {aff}")
                if vtags_override:
                    lines.append("  visualTags:")
                    for tag in vtags_override:
                        lines.append(f"    - {tag}")
                    lines.append("    - Lvl3")
                else:
                    lines.append("  visualTags:")
                    lines.append("    - !append-once Lvl3")
                lines.append("  abilities:")
                for ab in abilities:
                    lines.append(f"    - !append-once {ab}")
                lines.append("")

    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate & verify Neon Ascendancy TweakXL garrison templates.")
    ap.add_argument("-o", "--output", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--check", action="store_true", help="Verify generated YAML matches output on disk.")
    ap.add_argument("--verify-tweakdb", action="store_true", help="Verify every vanilla record ref exists in tweakdb_ep1.bin.")
    ap.add_argument("--tweakdb", type=Path, default=DEFAULT_TWEAKDB)
    args = ap.parse_args()

    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    refs = collect_vanilla_refs(spec)

    if args.verify_tweakdb:
        if not args.tweakdb.is_file():
            raise FileNotFoundError(f"Missing tweakdb_ep1.bin at {args.tweakdb}")
        tdb = load_tweakdb_records(args.tweakdb)
        missing = sorted(r for r in refs if tdbid_of(r) not in tdb)
        if missing:
            print(f"ERROR: {len(missing)} vanilla TweakDB reference(s) missing from {args.tweakdb}:", file=sys.stderr)
            for m in missing:
                print(f"  MISSING: {m}", file=sys.stderr)
            return 1
        print(f"TweakDB check OK: all {len(refs)} vanilla references verified in {args.tweakdb.name}")

    yaml_text = render_yaml(spec)
    sha = hashlib.sha256(yaml_text.encode("utf-8")).hexdigest()

    if args.check:
        if not args.output.is_file():
            print(f"ERROR: missing {args.output}", file=sys.stderr)
            return 1
        existing = args.output.read_text(encoding="utf-8")
        if existing != yaml_text:
            print(f"ERROR: {args.output} is out of date; re-run tools/generate-garrison-tweaks.py", file=sys.stderr)
            return 1
        print(f"GarrisonTemplates.yaml deterministic OK (sha256={sha[:16]}...)")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(yaml_text, encoding="utf-8")

    n_fac = len(spec["factions"])
    n_units = n_fac * len(spec["roles"]) * len(spec["gear_brackets"])
    n_bosses = n_fac * len(spec["boss_archetypes"]) * 2
    print(
        f"Generated {args.output} ({len(yaml_text)} B, sha256={sha[:16]}..., "
        f"{n_fac} factions, {n_units} unit templates, {n_bosses} boss templates, "
        f"{len(refs)} vanilla refs)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
