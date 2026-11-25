module NeonAscendancy.Debug

import NeonAscendancy.Core.*

// One probed venue: the authored NodeRef paths whose resolvability and device
// state the dev-only venue-access probe reports, plus the community spawner to
// count. Paths are the exact authored strings vanilla phases/streaming sectors
// carry (see data/clean-slate/venue_phases.json probe_refs and
// docs/research/world-access.md section 5).
public struct NeonAscendancy_VenueProbe {
  public let code: String;
  public let workspot: String;
  public let door: String;
  public let community: String;
}

// Dev-only in-game venue-access probe. Reports whether Neon-authored venue
// phases make their NodeRefs resolve, the DoorControllerPS state of the probed
// doors, and whether community spawners report spawned entities.
//
// Bounded by construction: it runs once after clean-slate bootstrap (and once
// more after a short delay), never per frame and never on a timer. It is a pure
// observer - it never mutates world state.
public class NeonAscendancy_VenueProbeCallback extends DelayCallback {
  public let m_pass: Int32 = 1;

  public func Call() -> Void {
    NeonAscendancy_RunVenueProbe(this.m_pass);
  }
}

// Resolve an authored NodeRef path (full "$/03_night_city/...#name" or short
// "#name") to the engine's GlobalNodeRef. redscript cannot hash a path itself
// (no character-code primitive), so the DLL hashes with RED4ext's own
// NodeRef::Hash and returns the GlobalNodeRef.
private func NeonAscendancy_ResolveProbeRef(path: String) -> GlobalNodeRef {
  if Equals(path, "") {
    return NcResolveNodeRefByHash(0ul);
  }
  return NcResolveNodeRefByHash(NcHashNodeRefPath(path));
}

private func NeonAscendancy_FormatDoorState(ps: ref<DoorControllerPS>) -> String {
  if !IsDefined(ps) {
    return "noPS";
  }
  return s"open=\(ps.IsOpen()) locked=\(ps.IsLocked()) sealed=\(ps.IsSealed()) disabled=\(ps.IsDisabled()) powered=\(ps.IsPowered())";
}

private func NeonAscendancy_ProbeOneVenue(game: GameInstance, venue: NeonAscendancy_VenueProbe) -> Void {
  // 1. Does the venue's key workspot ref resolve to a node?
  let workspotResolved = false;
  if NotEquals(venue.workspot, "") {
    workspotResolved = GlobalNodeRef.IsDefined(NeonAscendancy_ResolveProbeRef(venue.workspot));
  }

  // 2. Door PS state, if the authored door ref resolves to a Device entity.
  let doorState = "skipped";
  if NotEquals(venue.door, "") {
    const doorRef = NeonAscendancy_ResolveProbeRef(venue.door);
    if GlobalNodeRef.IsDefined(doorRef) {
      const doorEntity = GameInstance.FindEntityByID(game, Cast<EntityID>(doorRef));
      const device = doorEntity as Device;
      if IsDefined(device) {
        let ps = device.GetDevicePS();
        doorState = "resolved " + NeonAscendancy_FormatDoorState(ps as DoorControllerPS);
      } else {
        doorState = "resolved noDevice";
      }
    } else {
      doorState = "unresolved";
    }
  }

  // 3. Does the community spawner report spawned entities?
  let communityCount = -1;
  if NotEquals(venue.community, "") {
    const comRef = NeonAscendancy_ResolveProbeRef(venue.community);
    if GlobalNodeRef.IsDefined(comRef) {
      let entries: array<CName>;
      let entityIds: array<EntityID>;
      GetFixedEntityIdsFromSpawnerEntityID(Cast<EntityID>(comRef), entries, game, entityIds);
      communityCount = ArraySize(entityIds);
    }
  }

  NcLogInfo(
    s"VenueProbe[\(venue.code)]: workspotResolved=\(workspotResolved) door=\(doorState) communitySpawned=\(communityCount)"
  );
}

// Run the whole probe once. `pass` distinguishes the post-bootstrap pass from the
// delayed re-check so the log shows both.
public func NeonAscendancy_RunVenueProbe(pass: Int32) -> Void {
  let game = GetGameInstance();
  if !GameInstance.IsValid(game) {
    return;
  }
  let qs = GameInstance.GetQuestsSystem(game);
  if !IsDefined(qs) || qs.GetFact(n"na_dev_venue_probe") <= 0 {
    return;
  }

  // Workspot and community paths are verified from the venue's Quest streaming
  // sector; door paths are the authored names vanilla phases address.
  let venues: array<NeonAscendancy_VenueProbe>;
  ArrayPush(
    venues,
    NeonAscendancy_VenueProbe(
      "sts_wat_kab_07",
      "$/03_night_city/c_watson/kabuki/loc_sts_wat_kab_07_casino_bar_prefab43ERUKQ/loc_sts_wat_kab_07_casino_bar_openworld_prefabAH5TG5A/#sts_wat_kab_07_streetstory/loc_sts_wat_kab_07_casino_bar_combat_prefabH3W2SIY/#kab_07_ws_bottom_guard_001",
      "#kab_07_gate_001",
      "#kab_07_com_enemies"
    )
  );
  ArrayPush(
    venues,
    NeonAscendancy_VenueProbe(
      "konpeki_plaza",
      "$/03_night_city/c_watson/arasaka_waterfront/loc_q004_q005_arasaka_hotel_prefabSAJNFOI/loc_q004_q005_arasaka_hotel_questdesign_prefabNPCBDRY/#q005_pr_arasaka/#q005_ws_concierge_during_escape",
      "#konpeki_plaza_entrance_door",
      "#q005_com_hotel_guests"
    )
  );
  ArrayPush(
    venues,
    NeonAscendancy_VenueProbe(
      "clouds",
      "$/03_night_city/c_westbrook/japan_town/loc_q105_dollhouse_prefabSOC2PJY/loc_q105_dollhouse_questdesign_prefabZ2ZMCDI/#q105_pr_dollhouse/#q105_ws_judys_van_dollhouse",
      "#q105_dvc_dollhouse_door_cabin_customer",
      "#q105_com_dollhouse"
    )
  );
  ArrayPush(
    venues,
    NeonAscendancy_VenueProbe(
      "all_foods",
      "$/03_night_city/c_watson/northside/wnid_07_prefab2UR7MHY/#loc_q003_meat_factory/loc_meat_factory_questdesign_prefabCIYNT2A/#q003_pr_quest/#q003_pr_00_base/#q003_ws_car_by_militech_ditch",
      "#q003_maelstrom_gate_entry",
      "#q003_com_main_hall"
    )
  );
  ArrayPush(
    venues,
    NeonAscendancy_VenueProbe(
      "totentanz",
      "",
      "#sq011_dvc_door_sliding_totentanz_entrance",
      "#com_totentanz"
    )
  );
  ArrayPush(
    venues,
    NeonAscendancy_VenueProbe(
      "battys_hotel",
      "$/03_night_city/#c_heywood/vista_del_rey/hvdr_02/hvdr_02_questdesign_prefabQGPW7TI/#batty_pr_roof/#batty_ws_roof",
      "",
      "#batty_com_roof"
    )
  );
  ArrayPush(
    venues,
    NeonAscendancy_VenueProbe(
      "embers",
      "$/03_night_city/#c_heywood/glen/loc_q115_fancy_restaurant_prefabMOPJDYY/loc_q115_fancy_restaurant_questdesign_prefabXXJX6OQ/#q115_pr_restaurant/#q115_ws_hanako_bodyguard_street_000",
      "#q115_dvc_embers_elevator_bottom_door",
      "#q115_com_restaurant_staff"
    )
  );
  ArrayPush(
    venues,
    NeonAscendancy_VenueProbe(
      "black_sapphire",
      "$/03_night_city/c_pacifica/combat_zone_prefabUEX7DCY/container_zone_prefab4PZIADQ/loc_q303_nighthawks_bar_prefabUYZLC4I/loc_q303_nighthawks_bar_questdesign_prefabIV4S35Q/#q303_pr_nighthawks/#q303_ws_nighthawks_customer_06",
      "#q303_dvc_ct_tunnel_entrance_door",
      "#q303_com_paradise_technical_floor_guards"
    )
  );
  ArrayPush(
    venues,
    NeonAscendancy_VenueProbe(
      "arasaka_tower",
      "$/03_night_city/#c_city_center/corpo_plaza/#loc_arasaka_tower/loc_arasaka_tower_questdesign_prefabDP2FMWA/#q113_pr_top_atrium_new/#q113_ws_propaganda_voice_atrium",
      "#q113_dvc_atrium_start_lift_door",
      "#q113_com_atrium_scenes"
    )
  );

  NcLogInfo(s"VenueProbe: start pass=\(pass) venues=\(ArraySize(venues))");
  for venue in venues {
    NeonAscendancy_ProbeOneVenue(game, venue);
  }
  NcLogInfo(s"VenueProbe: done pass=\(pass)");
}

// Schedule the bounded two-pass probe: once ~2 s after bootstrap, once ~30 s
// later to let prefab streaming and community spawns settle.
public func NeonAscendancy_ScheduleVenueProbe(game: GameInstance) -> Void {
  if !GameInstance.IsValid(game) {
    return;
  }
  let qs = GameInstance.GetQuestsSystem(game);
  if !IsDefined(qs) || qs.GetFact(n"na_dev_venue_probe") <= 0 {
    return;
  }
  let ds = GameInstance.GetDelaySystem(game);
  if !IsDefined(ds) {
    return;
  }
  let first = new NeonAscendancy_VenueProbeCallback();
  first.m_pass = 1;
  ds.DelayCallback(first, 2.0, false);
  let second = new NeonAscendancy_VenueProbeCallback();
  second.m_pass = 2;
  ds.DelayCallback(second, 30.0, false);
}

