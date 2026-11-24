module NeonAscendancy.Sandbox

import NeonAscendancy.Core.*
import NeonAscendancy.Map.*

private class NeonAscendancy_SanitizerApplyCallback extends DelayCallback {
  public let m_system: wref<NeonAscendancy_SanitizerSystem>;

  public func Call() -> Void {
    if IsDefined(this.m_system) {
      this.m_system.ApplyIfSafe();
    }
  }
}

// Thin adapter that delegates era/policy decisions to C++ (NcEvaluateSanitizer)
// and applies the returned bitmask safely outside scenes.
public class NeonAscendancy_SanitizerSystem extends ScriptableSystem {
  private persistent let m_schemaVersion: Int32;
  private persistent let m_enabled: Bool;
  private persistent let m_lastEraCode: Int32;
  private let m_playerAttachedCallbackId: Uint32;
  private let m_sanctuariesSynced: Bool;

  public func OnAttach() -> Void {
    if this.m_playerAttachedCallbackId == 0u {
      const game = this.GetGameInstance();
      if GameInstance.IsValid(game) {
        this.m_playerAttachedCallbackId = GameInstance
          .GetPlayerSystem(game)
          .RegisterPlayerPuppetAttachedCallback(this, n"OnPlayerAttachedCallback");
      }
    }
  }

  public func OnRestored(saveVersion: Int32, gameVersion: Int32) -> Void {
    this.m_sanctuariesSynced = false;
    if this.m_enabled {
      this.ScheduleApply(1.0);
    }
  }

  public func OnDetach() -> Void {
    this.m_sanctuariesSynced = false;
    NcClearSafeSanctuaries();
    const game = this.GetGameInstance();
    if this.m_playerAttachedCallbackId > 0u && GameInstance.IsValid(game) {
      GameInstance
        .GetPlayerSystem(game)
        .UnregisterPlayerPuppetAttachedCallback(this.m_playerAttachedCallbackId);
      this.m_playerAttachedCallbackId = 0u;
    }
  }

  private final func OnPlayerAttachedCallback(playerPuppet: ref<GameObject>) -> Void {
    if IsDefined(playerPuppet) && this.m_enabled {
      this.ScheduleApply(1.0);
    }
  }

  public const final func IsEnabled() -> Bool {
    return this.m_enabled;
  }

  public const final func GetLastEraCode() -> Int32 {
    return this.m_lastEraCode;
  }

  public final func EnableAndApply() -> String {
    this.m_schemaVersion = NeonAscendancy_SchemaVersion();
    this.m_enabled = true;
    const eraCode = this.ApplyIfSafe();
    return NcGetEraName(eraCode);
  }

  public final func ScheduleApply(delaySeconds: Float) -> Void {
    const game = this.GetGameInstance();
    if !GameInstance.IsValid(game) {
      return;
    }
    let ds = GameInstance.GetDelaySystem(game);
    if IsDefined(ds) {
      let cb = new NeonAscendancy_SanitizerApplyCallback();
      cb.m_system = this;
      ds.DelayCallback(cb, delaySeconds, false);
    }
  }

  public final func ApplyIfSafe() -> Int32 {
    const game = this.GetGameInstance();
    if !GameInstance.IsValid(game) {
      return 0;
    }
    let qs = GameInstance.GetQuestsSystem(game);
    const factBits = NeonAscendancy_ReadEraFactsMask(qs);
    const mask = NcEvaluateSanitizer(factBits, this.m_enabled);
    const eraCode = Cast<Int32>(mask / 256u & 255u);
    this.m_lastEraCode = eraCode;

    if !this.m_enabled {
      return eraCode;
    }

    let player = GameInstance.GetPlayerSystem(game).GetLocalPlayerMainGameObject();
    if !IsDefined(player) {
      this.ScheduleApply(2.0);
      return eraCode;
    }
    let scene = GameInstance.GetSceneSystem(game).GetScriptInterface();
    if scene.IsEntityInScene(player.GetEntityID()) || scene.IsRewindableSectionActive() {
      this.ScheduleApply(2.0);
      return eraCode;
    }

    if (mask & 1u) != 0u {
      this.ApplyCityUnlock(game, qs);
    }
    if (mask & 2u) != 0u {
      this.ApplyAct2ContentUnlock(qs);
    }
    if (mask & 4u) != 0u {
      this.SuppressVanillaQuests(game);
    }
    if (mask & 8u) != 0u {
      StatusEffectHelper.RemoveStatusEffectsWithTag(player, n"JohnnySickness");
    }
    this.SyncSafeSanctuaries(game);
    this.EnforceSafeZonePolicy(game, qs, player);
    return eraCode;
  }

  public final func SyncSafeSanctuaries(game: GameInstance) -> Void {
    if !GameInstance.IsValid(game) {
      return;
    }
    let ms = GameInstance.GetMappinSystem(game);
    if !IsDefined(ms) {
      return;
    }
    let mappins: array<ref<IMappin>>;
    ms.GetMappins(gamemappinsMappinTargetType.Map, mappins);
    if ArraySize(mappins) == 0 {
      return;
    }
    NcClearSafeSanctuaries();
    for m in mappins {
      if IsDefined(m) {
        const pos = m.GetWorldPosition();
        NcRegisterSafeSanctuaryPin(EnumInt(m.GetVariant()), pos.X, pos.Y, pos.Z);
      }
    }
    this.m_sanctuariesSynced = true;
  }

  public final func IsAllowedSafeZoneAt(game: GameInstance, pos: Vector4) -> Bool {
    if !this.m_sanctuariesSynced {
      this.SyncSafeSanctuaries(game);
    }
    return NcIsAllowedSafeZone(pos.X, pos.Y, pos.Z);
  }

  private final func EnforceSafeZonePolicy(game: GameInstance, qs: QuestsSystem, player: ref<GameObject>) -> Void {
    const pos = player.GetWorldPosition();
    if this.IsAllowedSafeZoneAt(game, pos) {
      return;
    }
    if !StatusEffectSystem.ObjectHasStatusEffectWithTag(player, n"VehicleScene")
      && !StatusEffectSystem.ObjectHasStatusEffectWithTag(player, n"FastForward") {
      StatusEffectHelper.RemoveStatusEffectsWithTag(player, n"NoCombat");
    }
    let pp = player as PlayerPuppet;
    if IsDefined(pp) {
      pp.OnZoneFactChanged(qs.GetFact(n"CityAreaType"));
      let bbSys = GameInstance.GetBlackboardSystem(game);
      if IsDefined(bbSys) {
        let psmBB = bbSys
          .GetLocalInstanced(pp.GetEntityID(), GetAllBlackboardDefs().PlayerStateMachine);
        if IsDefined(psmBB) {
          const secVar = psmBB
            .GetVariant(GetAllBlackboardDefs().PlayerStateMachine.SecurityZoneData);
          if IsDefined(secVar) {
            let secData = FromVariant<SecurityAreaData>(secVar);
            if Equals(secData.securityAreaType, ESecurityAreaType.SAFE) {
              secData.securityAreaType = ESecurityAreaType.DISABLED;
              psmBB
                .SetVariant(
                  GetAllBlackboardDefs().PlayerStateMachine.SecurityZoneData,
                  ToVariant(secData),
                  true
                );
            }
          }
        }
      }
    }
  }

  private final func ApplyCityUnlock(game: GameInstance, qs: QuestsSystem) -> Void {
    if qs.GetFact(n"watson_prolog_lock") != 0 {
      qs.SetFact(n"watson_prolog_lock", 0);
    }
    if qs.GetFact(n"watson_prolog_unlock") == 0 {
      qs.SetFact(n"watson_prolog_unlock", 1);
    }
    let ft = GameInstance.GetScriptableSystemsContainer(game).Get(n"FastTravelSystem") as FastTravelSystem;
    if IsDefined(ft) {
      ft.QueueRequest(new RemoveAllFastTravelLocksRequest());
      let evt = new FastTravelMenuToggledEvent();
      evt.isEnabled = true;
      ft.QueueRequest(evt);
    }
  }

  private final func ApplyAct2ContentUnlock(qs: QuestsSystem) -> Void {
    if qs.GetFact(n"q101_enable_activities_flat") == 0 {
      qs.SetFact(n"q101_enable_activities_flat", 1);
    }
    if qs.GetFact(n"q101_enable_side_content") == 0 {
      qs.SetFact(n"q101_enable_side_content", 1);
    }
  }

  private final func SuppressVanillaQuests(game: GameInstance) -> Void {
    let jm = GameInstance.GetJournalManager(game);
    if !IsDefined(jm) {
      return;
    }
    let filter: JournalRequestStateFilter;
    filter.active = true;
    filter.inactive = false;
    filter.succeeded = false;
    filter.failed = false;

    let ctx: JournalRequestContext;
    ctx.stateFilter = filter;

    let quests: array<wref<JournalEntry>>;
    jm.GetQuests(ctx, quests);
    for q in quests {
      if IsDefined(q) {
        // JournalQuest.GetId() returns short IDs (q301_..., sq..., mq..., sts_...).
        // Suppress every vanilla active quest unless explicitly tagged na_*.
        const id = q.GetId();
        if !StrBeginsWith(id, "na_") {
          jm
            .ChangeEntryStateByHash(
              Cast<Uint32>(jm.GetEntryHash(q)),
              gameJournalEntryState.Inactive,
              JournalNotifyOption.DoNotNotify
            );
        }
      }
    }
    if IsDefined(jm.GetTrackedEntry()) {
      jm.UntrackEntry();
    }
  }
}

public func NeonAscendancy_IsSanitizerEnabled(game: GameInstance) -> Bool {
  if !GameInstance.IsValid(game) {
    return false;
  }
  const sys = GameInstance
    .GetScriptableSystemsContainer(game)
    .Get(n"NeonAscendancy.Sandbox.NeonAscendancy_SanitizerSystem") as NeonAscendancy_SanitizerSystem;
  return IsDefined(sys) && sys.IsEnabled();
}

public func NeonAscendancy_IsAllowedSafeZone(game: GameInstance, pos: Vector4) -> Bool {
  if !GameInstance.IsValid(game) {
    return false;
  }
  let sys = GameInstance
    .GetScriptableSystemsContainer(game)
    .Get(n"NeonAscendancy.Sandbox.NeonAscendancy_SanitizerSystem") as NeonAscendancy_SanitizerSystem;
  if IsDefined(sys) {
    return sys.IsAllowedSafeZoneAt(game, pos);
  }
  return NcIsAllowedSafeZone(pos.X, pos.Y, pos.Z);
}

private func NeonAscendancy_IsSuppressedVanillaMappinVariant(v: gamedataMappinVariant) -> Bool {
  switch v {
    case gamedataMappinVariant.DefaultQuestVariant:
    case gamedataMappinVariant.QuestGiverVariant:
    case gamedataMappinVariant.ExclamationMarkVariant:
    case gamedataMappinVariant.MinorActivityVariant:
    case gamedataMappinVariant.FixerVariant:
    case gamedataMappinVariant.RetrievingVariant:
    case gamedataMappinVariant.SabotageVariant:
    case gamedataMappinVariant.ThieveryVariant:
    case gamedataMappinVariant.HuntForPsychoVariant:
    case gamedataMappinVariant.ClientInDistressVariant:
    case gamedataMappinVariant.BountyHuntVariant:
    case gamedataMappinVariant.OutpostVariant:
    case gamedataMappinVariant.GangWatchVariant:
    case gamedataMappinVariant.HiddenStashVariant:
    case gamedataMappinVariant.ConvoyVariant:
    case gamedataMappinVariant.CourierVariant:
    case gamedataMappinVariant.TarotVariant:
    case gamedataMappinVariant.Zzz01_CarForPurchaseVariant:
    case gamedataMappinVariant.Zzz02_MotorcycleForPurchaseVariant:
    case gamedataMappinVariant.Zzz06_NCPDGigVariant:
    case gamedataMappinVariant.Zzz09_CourierSandboxActivityVariant:
    case gamedataMappinVariant.Zzz12_WorldEncounterVariant:
      return true;
    default:
      return false;
  }
}

@wrapMethod(PhoneSystem)
private final func OnTriggerCall(request: ref<questTriggerCallRequest>) -> Void {
  if NeonAscendancy_IsSanitizerEnabled(this.GetGameInstance()) {
    // Always allow EndCall and player-initiated calls; drop unsolicited quest/fixer calls.
    if NotEquals(request.callPhase, questPhoneCallPhase.EndCall)
      && !request.isPlayerTriggered {
      return;
    }
  }
  wrappedMethod(request);
}

@wrapMethod(InteractionUIBase)
protected cb func OnDialogsData(value: Variant) -> Bool {
  const player = this.GetPlayerControlledObject();
  if IsDefined(player) && NeonAscendancy_IsSanitizerEnabled(player.GetGame()) {
    let data = FromVariant<DialogChoiceHubs>(value);
    let keptHubs: array<ListChoiceHubData>;
    for hub in data.choiceHubs {
      let keptChoices: array<ListChoiceData>;
      for choice in hub.choices {
        if !ChoiceTypeWrapper
          .IsType(choice.type, gameinteractionsChoiceType.QuestImportant) {
          ArrayPush(keptChoices, choice);
        }
      }
      if ArraySize(keptChoices) > 0 {
        hub.choices = keptChoices;
        ArrayPush(keptHubs, hub);
      }
    }
    data.choiceHubs = keptHubs;
    return wrappedMethod(ToVariant(data));
  }
  return wrappedMethod(value);
}

// Fullscreen World Map (M) mappin filter: always keep our control-center & raid
// pins, hide vanilla quest/gig/NCPD clutter, preserve shops/FT/apartments.
@wrapMethod(WorldMapMenuGameController)
public func CreateMappinUIProfile(
  mappin: wref<IMappin>,
  mappinVariant: gamedataMappinVariant,
  customData: ref<MappinControllerCustomData>
) -> MappinUIProfile {
  const game = GetGameInstance();
  if GameInstance.IsValid(game) && IsDefined(mappin) {
    const mapSys = GameInstance
      .GetScriptableSystemsContainer(game)
      .Get(n"NeonAscendancy.Map.NeonAscendancy_TerritoryMapSystem") as NeonAscendancy_TerritoryMapSystem;
    if IsDefined(mapSys) && mapSys.IsOurMappin(mappin.GetNewMappinID()) {
      return MappinUIProfile
        .Create(
          r"base\\gameplay\\gui\\fullscreen\\world_map\\mappins\\default_mappin.inkwidget",
          t"MappinUISpawnProfile.Always",
          t"MapMappinUIProfile.Default"
        );
    }
    if NeonAscendancy_IsSanitizerEnabled(game)
      && NeonAscendancy_IsSuppressedVanillaMappinVariant(mappinVariant) {
      return MappinUIProfile.None();
    }
  }
  return wrappedMethod(mappin, mappinVariant, customData);
}

// 3D in-world floating mappin filter.
@wrapMethod(WorldMappinsContainerController)
public func CreateMappinUIProfile(
  mappin: wref<IMappin>,
  mappinVariant: gamedataMappinVariant,
  customData: ref<MappinControllerCustomData>
) -> MappinUIProfile {
  const game = GetGameInstance();
  if GameInstance.IsValid(game)
    && IsDefined(mappin)
    && NeonAscendancy_IsSanitizerEnabled(game) {
    const mapSys = GameInstance
      .GetScriptableSystemsContainer(game)
      .Get(n"NeonAscendancy.Map.NeonAscendancy_TerritoryMapSystem") as NeonAscendancy_TerritoryMapSystem;
    if (!IsDefined(mapSys) || !mapSys.IsOurMappin(mappin.GetNewMappinID()))
      && NeonAscendancy_IsSuppressedVanillaMappinVariant(mappinVariant) {
      return MappinUIProfile.None();
    }
  }
  return wrappedMethod(mappin, mappinVariant, customData);
}

// Minimap mappin filter.
@wrapMethod(MinimapContainerController)
public func CreateMappinUIProfile(
  mappin: wref<IMappin>,
  mappinVariant: gamedataMappinVariant,
  customData: ref<MappinControllerCustomData>
) -> MappinUIProfile {
  const game = GetGameInstance();
  if GameInstance.IsValid(game)
    && IsDefined(mappin)
    && NeonAscendancy_IsSanitizerEnabled(game) {
    const mapSys = GameInstance
      .GetScriptableSystemsContainer(game)
      .Get(n"NeonAscendancy.Map.NeonAscendancy_TerritoryMapSystem") as NeonAscendancy_TerritoryMapSystem;
    if (!IsDefined(mapSys) || !mapSys.IsOurMappin(mappin.GetNewMappinID()))
      && NeonAscendancy_IsSuppressedVanillaMappinVariant(mappinVariant) {
      return MappinUIProfile.None();
    }
  }
  return wrappedMethod(mappin, mappinVariant, customData);
}

// Disable vanilla Safe Zones everywhere in Sandbox Mode except V's apartments,
// stores, and ripperdocs (policy + bounds live in C++ via NcIsAllowedSafeZone).
@wrapMethod(PlayerPuppet)
protected const final func GetCurrentZoneType(factValue: Int32) -> gameCityAreaType {
  const zoneType = wrappedMethod(factValue);
  if Equals(zoneType, gameCityAreaType.SafeZone)
    && NeonAscendancy_IsSanitizerEnabled(this.GetGame())
    && !NeonAscendancy_IsAllowedSafeZone(this.GetGame(), this.GetWorldPosition()) {
    return gameCityAreaType.PublicZone;
  }
  return zoneType;
}

// Block area-applied NoCombat status effects outside apartments, stores, ripperdocs,
// and active scenes/vehicles.
@wrapMethod(PlayerPuppet)
protected cb func OnStatusEffectApplied(evt: ref<ApplyStatusEffectEvent>) -> Bool {
  if IsDefined(evt) && IsDefined(evt.staticData) {
    const game = this.GetGame();
    if NeonAscendancy_IsSanitizerEnabled(game) {
      let staticData = evt.staticData;
      const tags = staticData.GameplayTags();
      if ArrayContains(tags, n"NoCombat")
        && !ArrayContains(tags, n"VehicleScene")
        && !ArrayContains(tags, n"FastForward")
        && !NeonAscendancy_IsAllowedSafeZone(game, this.GetWorldPosition()) {
        let scene = GameInstance.GetSceneSystem(game).GetScriptInterface();
        if !scene.IsEntityInScene(this.GetEntityID())
          && !scene.IsRewindableSectionActive() {
          StatusEffectHelper.RemoveStatusEffect(this, staticData.GetID());
          return true;
        }
      }
    }
  }
  return wrappedMethod(evt);
}

// Suppress the blue "SAFE AREA" minimap badge and HUD banner outside apartments,
// stores, and ripperdocs while leaving Restricted / Dangerous security zones intact.
@wrapMethod(SecuritySystemControllerPS)
private final func UpdateSecurityZoneDataBlackboard(securityAreaData: SecurityAreaData) -> Void {
  if Equals(securityAreaData.securityAreaType, ESecurityAreaType.SAFE) {
    const game = this.GetGameInstance();
    if GameInstance.IsValid(game) && NeonAscendancy_IsSanitizerEnabled(game) {
      const player = GameInstance.GetPlayerSystem(game).GetLocalPlayerMainGameObject();
      if IsDefined(player)
        && !NeonAscendancy_IsAllowedSafeZone(game, player.GetWorldPosition()) {
        securityAreaData.securityAreaType = ESecurityAreaType.DISABLED;
      }
    }
  }
  wrappedMethod(securityAreaData);
}

