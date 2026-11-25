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
// doors, and whether community spawners report spawned entities. It re-runs
// every 60 s while na_dev_venue_probe is set so an on-site check settles as the
// player moves and prefabs stream in. Never per frame.
public class NeonAscendancy_VenueProbeCallback extends DelayCallback {
  public let m_game: GameInstance;
  public let m_pass: Int32 = 1;

  public func Call() -> Void {
    NeonAscendancy_RunVenueProbe(this.m_game, this.m_pass);
    NeonAscendancy_ScheduleVenueProbe(this.m_game);
  }
}

// Resolve an authored NodeRef path to the engine's GlobalNodeRef the same way
// vanilla does: hash the path (the DLL calls RED4ext's own NodeRef::Hash, since
// redscript has no character-code primitive), then run it through the engine's
// ResolveNodeRef(local, root). The resolve step is what maps short "#name"
// community spawners and prefab-relative door refs to their global ids, exactly
// like NPCReference.GetSpawnerEntityID and the quest device managers do.
private func NeonAscendancy_ResolveProbeRef(path: String) -> GlobalNodeRef {
  if Equals(path, "") {
    return NcResolveNodeRefByHash(0ul);
  }
  const nodeRef = NcNodeRefFromHash(NcHashNodeRefPath(path));
  return ResolveNodeRef(nodeRef, Cast<GlobalNodeRef>(GlobalNodeID.GetRoot()));
}

private func NeonAscendancy_FormatDoorState(ps: ref<DoorControllerPS>) -> String {
  if !IsDefined(ps) {
    return "noPS";
  }
  return s"open=\(ps.IsOpen()) locked=\(ps.IsLocked()) sealed=\(ps.IsSealed()) disabled=\(ps.IsDisabled()) powered=\(ps.IsPowered())";
}

// Dev-only on-site repair for one door. The venue phase's device-manager actions
// fire once at bootstrap, when the player is usually still in H10 kilometres
// away, so on a fresh save they hit no streamed entity. This re-issues the same
// vanilla sequence directly against the live PS, but only when the player is
// within `range` of the door so it never touches a distant venue. Sequence
// matches vanilla: ForceEnabled -> ForcePower -> ForceUnlock -> ForceOpen
// (q303_07b_lobby_combat does ForceUnlock -> ForceOpen on the tower main door;
// ForceEnabled/ForcePower are added so a disabled/unpowered device still opens).
private func NeonAscendancy_RepairDoor(game: GameInstance, path: String, range: Float) -> String {
  if Equals(path, "") {
    return "none";
  }
  const ref = NeonAscendancy_ResolveProbeRef(path);
  if !GlobalNodeRef.IsDefined(ref) {
    return "unresolved";
  }
  const entity = GameInstance.FindEntityByID(game, Cast<EntityID>(ref));
  const device = entity as Device;
  if !IsDefined(device) {
    return "noDevice";
  }
  let player = GameInstance.GetPlayerSystem(game).GetLocalPlayerMainGameObject();
  if !IsDefined(player) {
    return "noPlayer";
  }
  if Vector4.Distance(device.GetWorldPosition(), player.GetWorldPosition()) > range {
    return "outOfRange";
  }
  let ps = device.GetDevicePS();
  if !IsDefined(ps) {
    return "noPS";
  }
  let persistency = GameInstance.GetPersistencySystem(game);
  if !IsDefined(persistency) {
    return "noPersistency";
  }
  let enabled = new QuestForceEnabled();
  enabled.clearanceLevel = 99;
  enabled.SetUp(ps);
  enabled.SetProperties();
  persistency.QueuePSDeviceEvent(enabled);
  let power = new QuestForcePower();
  power.clearanceLevel = 99;
  power.SetUp(ps);
  power.SetProperties();
  persistency.QueuePSDeviceEvent(power);
  let unlock = new QuestForceUnlock();
  unlock.clearanceLevel = 99;
  unlock.SetUp(ps);
  unlock.SetProperties();
  persistency.QueuePSDeviceEvent(unlock);
  let open = new QuestForceOpen();
  open.clearanceLevel = 99;
  open.SetUp(ps);
  open.SetProperties();
  persistency.QueuePSDeviceEvent(open);
  return "repaired";
}

private func NeonAscendancy_ProbeOneVenue(game: GameInstance, venue: NeonAscendancy_VenueProbe) -> Void {
  // 1. Does the venue's key workspot ref resolve to a node?
  let workspotResolved = false;
  if NotEquals(venue.workspot, "") {
    workspotResolved = GlobalNodeRef.IsDefined(NeonAscendancy_ResolveProbeRef(venue.workspot));
  }

  // 2. Door PS state, if the authored door ref resolves to a Device entity.
  let doorState = "skipped";
  let repair = "skipped";
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
    repair = NeonAscendancy_RepairDoor(game, venue.door, 60.0);
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
    s"VenueProbe[\(venue.code)]: workspotResolved=\(workspotResolved) door=\(doorState) repair=\(repair) communitySpawned=\(communityCount)"
  );
}

// Run the whole probe once. `pass` distinguishes the post-bootstrap pass from the
// delayed re-check so the log shows both.
public func NeonAscendancy_RunVenueProbe(game: GameInstance, pass: Int32) -> Void {
  if !GameInstance.IsValid(game) {
    NcLogInfo(s"VenueProbe: skipped pass=\(pass) (invalid GameInstance)");
    return;
  }
  let qs = GameInstance.GetQuestsSystem(game);
  if !IsDefined(qs) || qs.GetFact(n"na_dev_venue_probe") <= 0 {
    NcLogInfo(s"VenueProbe: skipped pass=\(pass) (na_dev_venue_probe not set)");
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
      "$/03_night_city/c_watson/northside/loc_sq011_totentanz_prefabOSRVQDA/#loc_sq011_totentanz_openworld/#loc_pre_quest_totentanz/#ws_totentanz_pre_quest_crowd_bar_standing_003",
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
      "#q303_dvc_tech_warehouse_gate",
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

// Schedule the bounded repeating probe: the first pass ~2 s after bootstrap,
// then every 60 s while na_dev_venue_probe stays set. The callback re-schedules
// itself via this function, so there is exactly one live timer chain. It stops
// on its own the moment the fact is cleared.
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
  let cb = new NeonAscendancy_VenueProbeCallback();
  cb.m_game = game;
  cb.m_pass = 1;
  ds.DelayCallback(cb, 60.0, false);
}

// First pass shortly after bootstrap so the log is not empty in the first
// minute, then NeonAscendancy_ScheduleVenueProbe keeps the 60 s chain alive.
public func NeonAscendancy_StartVenueProbe(game: GameInstance) -> Void {
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
  first.m_game = game;
  first.m_pass = 1;
  ds.DelayCallback(first, 2.0, false);
}

// Dev-only door census: while the venue probe is armed, every door that streams
// in within 150 m of the player logs its global id, distance, position, the
// player position and its state. The debug name/path APIs return None for
// authored doors, so they are omitted; the player position tells us which door
// the owner is standing at, and the id is the low 32 bits of the EntityID hash
// (matches data/sites/doors.json and the raw sector extracts).
//
// De-duplication: a door can re-attach on every stream-in, so each id is logged
// at most once while this process runs. redscript has no module-scope or static
// fields, so the seen-set is one class instance stored on the PlayerPuppet via
// @addField; every door reads that same instance.
public class NeonAscendancy_VenueCensusState extends IScriptable {
  private let m_seen: array<Uint32>;

  public final func HasSeen(id: Uint32) -> Bool {
    return ArrayContains(this.m_seen, id);
  }

  public final func MarkSeen(id: Uint32) -> Void {
    if !ArrayContains(this.m_seen, id) {
      ArrayPush(this.m_seen, id);
    }
  }
}

@addField(PlayerPuppet)
public let NeonAscendancy_venueCensusState: ref<NeonAscendancy_VenueCensusState>;

private func NeonAscendancy_GetCensusState(player: ref<GameObject>) -> ref<NeonAscendancy_VenueCensusState> {
  let pp = player as PlayerPuppet;
  if !IsDefined(pp) {
    return null;
  }
  if !IsDefined(pp.NeonAscendancy_venueCensusState) {
    pp.NeonAscendancy_venueCensusState = new NeonAscendancy_VenueCensusState();
  }
  return pp.NeonAscendancy_venueCensusState;
}

@wrapMethod(Door)
protected cb func OnGameAttached() -> Bool {
  const res = wrappedMethod();
  const game = this.GetGame();
  if !GameInstance.IsValid(game) {
    return res;
  }
  let qs = GameInstance.GetQuestsSystem(game);
  if !IsDefined(qs) || qs.GetFact(n"na_dev_venue_probe") <= 0 {
    return res;
  }
  let player = GameInstance.GetPlayerSystem(game).GetLocalPlayerMainGameObject();
  if !IsDefined(player) {
    return res;
  }
  const pos = this.GetWorldPosition();
  const playerPos = player.GetWorldPosition();
  const dist = Vector4.Distance(pos, playerPos);
  if dist > 150.0 {
    return res;
  }
  const doorId = EntityID.GetHash(this.GetEntityID());
  let state = NeonAscendancy_GetCensusState(player);
  if IsDefined(state) {
    if state.HasSeen(doorId) {
      return res;
    }
    state.MarkSeen(doorId);
  }
  let ps = this.GetDevicePS();
  NcLogInfo(
    s"DoorCensus: id=\(doorId) dist=\(dist) pos=(\(pos.X),\(pos.Y),\(pos.Z)) player=(\(playerPos.X),\(playerPos.Y),\(playerPos.Z)) \(NeonAscendancy_FormatDoorState(ps))"
  );
  return res;
}

