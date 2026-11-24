module NeonAscendancy.Sandbox

import NeonAscendancy.Core.*

private class NeonAscendancy_SanitizerApplyCallback extends DelayCallback {
  public let m_system: wref<NeonAscendancy_SanitizerSystem>;

  public func Call() -> Void {
    if IsDefined(this.m_system) {
      this.m_system.ApplyIfSafe();
    }
  }
}

// Thin adapter that delegates era, sanctuary, and vanilla-pin policies to C++
// and applies the results cleanly to Cyberpunk's quest/zone/UI hooks.
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
    NcSetSanitizerActive(this.m_enabled);
    if this.m_enabled {
      this.ScheduleApply(0.5);
    }
  }

  public func OnDetach() -> Void {
    this.m_sanctuariesSynced = false;
    NcSetSanitizerActive(false);
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
      NcSetSanitizerActive(true);
      this.ScheduleApply(0.5);
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
    NcSetSanitizerActive(true);
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
    NcSetSanitizerActive(this.m_enabled);
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
      this.ScheduleApply(1.0);
      return eraCode;
    }

    // Only defer quest-fact writes during locked cinematics (SceneTier >= 3).
    // Tier-1 ambient world scenes (e.g. Coastview / Dogtown approach) must NOT
    // block quest suppression or safe-zone enforcement.
    const sceneTier = this.GetPlayerSceneTier(game, player);
    if sceneTier < 3 {
      if (mask & 1u) != 0u {
        this.ApplyCityUnlock(game, qs);
      }
      if (mask & 2u) != 0u {
        this.ApplyAct2ContentUnlock(qs);
      }
    } else {
      this.ScheduleApply(2.0);
    }

    if (mask & 4u) != 0u {
      this.SuppressVanillaQuests(game);
    }
    if (mask & 8u) != 0u {
      StatusEffectHelper.RemoveStatusEffectsWithTag(player, n"JohnnySickness");
    }
    this.SyncSafeSanctuaries(game);
    this.EnforceSafeZonePolicy(game, qs, player, sceneTier);
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

  private final func GetPlayerSceneTier(game: GameInstance, player: ref<GameObject>) -> Int32 {
    let bbSys = GameInstance.GetBlackboardSystem(game);
    if !IsDefined(bbSys) {
      return 1;
    }
    let psmBB = bbSys
      .GetLocalInstanced(player.GetEntityID(), GetAllBlackboardDefs().PlayerStateMachine);
    if !IsDefined(psmBB) {
      return 1;
    }
    return psmBB.GetInt(GetAllBlackboardDefs().PlayerStateMachine.SceneTier);
  }

  private final func EnforceSafeZonePolicy(
    game: GameInstance,
    qs: QuestsSystem,
    player: ref<GameObject>,
    sceneTier: Int32
  ) -> Void {
    const pos = player.GetWorldPosition();
    const allowed = this.IsAllowedSafeZoneAt(game, pos);
    const cityAreaFact = qs.GetFact(n"CityAreaType");
    const forceEmptyFact = qs.GetFact(n"ForceEmptyHands");
    const hasNoCombat = StatusEffectSystem.ObjectHasStatusEffectWithTag(player, n"NoCombat");

    let psmZonesBefore = -1;
    let secAreaBefore = -1;
    let pp = player as PlayerPuppet;
    let bbSys = GameInstance.GetBlackboardSystem(game);
    let psmBB: ref<IBlackboard>;
    if IsDefined(bbSys) {
      psmBB = bbSys
        .GetLocalInstanced(player.GetEntityID(), GetAllBlackboardDefs().PlayerStateMachine);
      if IsDefined(psmBB) {
        psmZonesBefore = psmBB.GetInt(GetAllBlackboardDefs().PlayerStateMachine.Zones);
        const secVar = psmBB
          .GetVariant(GetAllBlackboardDefs().PlayerStateMachine.SecurityZoneData);
        if IsDefined(secVar) {
          const secData = FromVariant<SecurityAreaData>(secVar);
          secAreaBefore = EnumInt(secData.securityAreaType);
        }
      }
    }

    NcLogInfo(
      s"Sanitizer.EnforceSafeZone: tier=\(sceneTier) allowed=\(allowed) sanctuaries=\(NcGetSafeSanctuaryCount()) cityArea=\(cityAreaFact) forceEmpty=\(forceEmptyFact) noCombat=\(hasNoCombat) psmZones=\(psmZonesBefore) secArea=\(secAreaBefore)"
    );

    if allowed || sceneTier >= 3 {
      return;
    }

    if forceEmptyFact != 0 {
      qs.SetFact(n"ForceEmptyHands", 0);
    }
    if !NeonAscendancy_HasNonSafeCombatLock(player) {
      if hasNoCombat {
        StatusEffectHelper.RemoveStatusEffectsWithTag(player, n"NoCombat");
      }
      if StatusEffectSystem.ObjectHasStatusEffectWithTag(player, n"NoWeapons") {
        StatusEffectHelper.RemoveStatusEffectsWithTag(player, n"NoWeapons");
      }
      if StatusEffectSystem.ObjectHasStatusEffectWithTag(player, n"InDaClub") {
        StatusEffectHelper.RemoveStatusEffectsWithTag(player, n"InDaClub");
      }
      if StatusEffectSystem
        .ObjectHasStatusEffectWithTag(player, n"Tier2Locomotion") {
        StatusEffectHelper
          .RemoveStatusEffectsWithTag(player, n"Tier2Locomotion");
      }
      if StatusEffectSystem
        .ObjectHasStatusEffect(player, t"GameplayRestriction.NoSprint") {
        StatusEffectHelper
          .RemoveStatusEffect(player, t"GameplayRestriction.NoSprint");
      }
      const isCarrying = IsDefined(psmBB)
        && psmBB.GetBool(GetAllBlackboardDefs().PlayerStateMachine.Carrying);
      if !isCarrying
        && StatusEffectSystem
          .ObjectHasStatusEffect(player, t"GameplayRestriction.NoJump") {
        StatusEffectHelper
          .RemoveStatusEffect(player, t"GameplayRestriction.NoJump");
      }
    }
    if IsDefined(pp) {
      pp.OnZoneFactChanged(cityAreaFact);
      let clearEmptyHands = new PSMPostponedParameterBool();
      clearEmptyHands.id = n"ForceEmptyHandsByZone";
      clearEmptyHands.value = false;
      clearEmptyHands.aspect = gamestateMachineParameterAspect.Permanent;
      pp.QueueEvent(clearEmptyHands);
      let clearForceWalk = new PSMPostponedParameterBool();
      clearForceWalk.id = n"ForceWalk";
      clearForceWalk.value = false;
      clearForceWalk.aspect = gamestateMachineParameterAspect.Permanent;
      pp.QueueEvent(clearForceWalk);
      if psmZonesBefore == 2 {
        pp
          .SetBlackboardIntVariable(GetAllBlackboardDefs().PlayerStateMachine.Zones, 1);
      }
    }
    if IsDefined(psmBB) && secAreaBefore == EnumInt(ESecurityAreaType.SAFE) {
      let clearedSec: SecurityAreaData;
      clearedSec.securityAreaType = ESecurityAreaType.DISABLED;
      clearedSec.entered = false;
      psmBB
        .SetVariant(
          GetAllBlackboardDefs().PlayerStateMachine.SecurityZoneData,
          ToVariant(clearedSec),
          true
        );
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
  if NcIsSanitizerActive() {
    return true;
  }
  if !GameInstance.IsValid(game) {
    return false;
  }
  const sys = GameInstance
    .GetScriptableSystemsContainer(game)
    .Get(n"NeonAscendancy.Sandbox.NeonAscendancy_SanitizerSystem") as NeonAscendancy_SanitizerSystem;
  return IsDefined(sys) && sys.IsEnabled();
}

public func NeonAscendancy_IsAllowedSafeZone(game: GameInstance, pos: Vector4) -> Bool {
  if GameInstance.IsValid(game) {
    let sys = GameInstance
      .GetScriptableSystemsContainer(game)
      .Get(n"NeonAscendancy.Sandbox.NeonAscendancy_SanitizerSystem") as NeonAscendancy_SanitizerSystem;
    if IsDefined(sys) {
      return sys.IsAllowedSafeZoneAt(game, pos);
    }
  }
  return NcIsAllowedSafeZone(pos.X, pos.Y, pos.Z);
}

@wrapMethod(PhoneSystem)
private final func OnTriggerCall(request: ref<questTriggerCallRequest>) -> Void {
  if NeonAscendancy_IsSanitizerEnabled(this.GetGameInstance()) {
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

private func NeonAscendancy_IsOurMappin(mappin: wref<IMappin>) -> Bool {
  if !IsDefined(mappin) {
    return false;
  }
  const pinId = mappin.GetNewMappinID();
  return NcLookupControlCenterPin(pinId.value) > 0;
}

// Fullscreen World Map (M) mappin filter (uses C++ O(1) lookup, no GetGameInstance()).
@wrapMethod(WorldMapMenuGameController)
public func CreateMappinUIProfile(
  mappin: wref<IMappin>,
  mappinVariant: gamedataMappinVariant,
  customData: ref<MappinControllerCustomData>
) -> MappinUIProfile {
  if NeonAscendancy_IsOurMappin(mappin) {
    return MappinUIProfile
      .Create(
        r"base\\gameplay\\gui\\fullscreen\\world_map\\mappins\\default_mappin.inkwidget",
        t"MappinUISpawnProfile.Always",
        t"MapMappinUIProfile.Default"
      );
  }
  if NcIsSanitizerActive()
    && NcIsSuppressedVanillaMappinVariant(EnumInt(mappinVariant)) {
    return MappinUIProfile.None();
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
  if NcIsSanitizerActive()
    && !NeonAscendancy_IsOurMappin(mappin)
    && NcIsSuppressedVanillaMappinVariant(EnumInt(mappinVariant)) {
    return MappinUIProfile.None();
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
  if NcIsSanitizerActive()
    && !NeonAscendancy_IsOurMappin(mappin)
    && NcIsSuppressedVanillaMappinVariant(EnumInt(mappinVariant)) {
    return MappinUIProfile.None();
  }
  return wrappedMethod(mappin, mappinVariant, customData);
}

// --- Safe Zone Disabling (everywhere except V's apartments, stores, and ripperdocs) ---
private func NeonAscendancy_ShouldOverrideSafeZone(const owner: wref<GameObject>) -> Bool {
  if !NcIsSanitizerActive() || !IsDefined(owner) {
    return false;
  }
  const pp = owner as PlayerPuppet;
  if IsDefined(pp) {
    const psmBB = pp.GetPlayerStateMachineBlackboard();
    if IsDefined(psmBB) {
      const hl = psmBB.GetInt(GetAllBlackboardDefs().PlayerStateMachine.HighLevel);
      if hl >= 3 && hl <= 5 {
        return false;
      }
    }
  }
  const pos = owner.GetWorldPosition();
  if NcGetSafeSanctuaryCount() == 0 {
    return !NeonAscendancy_IsAllowedSafeZone(owner.GetGame(), pos);
  }
  return !NcIsAllowedSafeZone(pos.X, pos.Y, pos.Z);
}

private func NeonAscendancy_HasNonSafeCombatLock(const owner: wref<GameObject>) -> Bool {
  let ses = GameInstance.GetStatusEffectSystem(owner.GetGame());
  if !IsDefined(ses) {
    return false;
  }
  const eid = owner.GetEntityID();
  return ses.HasStatusEffectWithTag(eid, n"VehicleScene")
    || ses.HasStatusEffectWithTag(eid, n"FastForward")
    || ses.HasStatusEffectWithTag(eid, n"Braindance");
}

@wrapMethod(PlayerPuppet)
protected const final func GetCurrentZoneType(factValue: Int32) -> gameCityAreaType {
  const zoneType = wrappedMethod(factValue);
  if Equals(zoneType, gameCityAreaType.SafeZone)
    && NeonAscendancy_IsSanitizerEnabled(this.GetGame()) {
    const pos = this.GetWorldPosition();
    const allowed = NeonAscendancy_IsAllowedSafeZone(this.GetGame(), pos);
    NcLogInfo(
      s"Sanitizer.GetCurrentZoneType: SafeZone fact=\(factValue) allowed=\(allowed) pos=(\(pos.X),\(pos.Y),\(pos.Z))"
    );
    if !allowed {
      return gameCityAreaType.PublicZone;
    }
  }
  return zoneType;
}

@wrapMethod(PlayerPuppet)
private final func OnEnterSafeZone() -> Void {
  if NeonAscendancy_IsSanitizerEnabled(this.GetGame()) {
    const pos = this.GetWorldPosition();
    const allowed = NeonAscendancy_IsAllowedSafeZone(this.GetGame(), pos);
    NcLogInfo(
      s"Sanitizer.OnEnterSafeZone: allowed=\(allowed) pos=(\(pos.X),\(pos.Y),\(pos.Z))"
    );
    if !allowed {
      this.OnExitSafeZone();
      this
        .SetBlackboardIntVariable(GetAllBlackboardDefs().PlayerStateMachine.Zones, 1);
      return;
    }
  }
  wrappedMethod();
}

@wrapMethod(DefaultTransition)
protected const final func IsInSafeZone(const scriptInterface: ref<StateGameScriptInterface>) -> Bool {
  const res = wrappedMethod(scriptInterface);
  if res && NeonAscendancy_ShouldOverrideSafeZone(scriptInterface.executionOwner) {
    return false;
  }
  return res;
}

@wrapMethod(DefaultTransition)
public const final func IsEmptyHandsForced(
  const stateContext: ref<StateContext>,
  const scriptInterface: ref<StateGameScriptInterface>
) -> Bool {
  const res = wrappedMethod(stateContext, scriptInterface);
  if res
    && NeonAscendancy_ShouldOverrideSafeZone(scriptInterface.executionOwner)
    && !NeonAscendancy_HasNonSafeCombatLock(scriptInterface.executionOwner)
    && !stateContext.IsStateActive(n"HighLevel", n"minigame")
    && !stateContext.IsStateActive(n"HighLevel", n"inspection") {
    return false;
  }
  return res;
}

@wrapMethod(DefaultTransition)
public const final func IsSafeStateForced(
  const stateContext: ref<StateContext>,
  const scriptInterface: ref<StateGameScriptInterface>
) -> Bool {
  const res = wrappedMethod(stateContext, scriptInterface);
  if res
    && NeonAscendancy_ShouldOverrideSafeZone(scriptInterface.executionOwner)
    && !NeonAscendancy_HasNonSafeCombatLock(scriptInterface.executionOwner) {
    return false;
  }
  return res;
}

@wrapMethod(DefaultTransition)
protected const final func IsNoCombatActionsForced(const scriptInterface: ref<StateGameScriptInterface>) -> Bool {
  const res = wrappedMethod(scriptInterface);
  if res
    && NeonAscendancy_ShouldOverrideSafeZone(scriptInterface.executionOwner)
    && !NeonAscendancy_HasNonSafeCombatLock(scriptInterface.executionOwner) {
    return false;
  }
  return res;
}

@wrapMethod(DefaultTransition)
protected const final func IsInSafeSceneTier(const scriptInterface: ref<StateGameScriptInterface>) -> Bool {
  const res = wrappedMethod(scriptInterface);
  if res && NeonAscendancy_ShouldOverrideSafeZone(scriptInterface.executionOwner) {
    return false;
  }
  return res;
}

@wrapMethod(SceneTierIIDecisions)
protected const final func EnterCondition(
  const stateContext: ref<StateContext>,
  const scriptInterface: ref<StateGameScriptInterface>
) -> Bool {
  if NeonAscendancy_ShouldOverrideSafeZone(scriptInterface.executionOwner) {
    return false;
  }
  return wrappedMethod(stateContext, scriptInterface);
}

@wrapMethod(DefaultTransition)
protected const final func IsInTier2Locomotion(const scriptInterface: ref<StateGameScriptInterface>) -> Bool {
  const res = wrappedMethod(scriptInterface);
  if res && NeonAscendancy_ShouldOverrideSafeZone(scriptInterface.executionOwner) {
    return false;
  }
  return res;
}

@wrapMethod(ForceWalkDecisions)
protected const func EnterCondition(
  const stateContext: ref<StateContext>,
  const scriptInterface: ref<StateGameScriptInterface>
) -> Bool {
  if NeonAscendancy_ShouldOverrideSafeZone(scriptInterface.executionOwner)
    && !NeonAscendancy_HasNonSafeCombatLock(scriptInterface.executionOwner) {
    return false;
  }
  return wrappedMethod(stateContext, scriptInterface);
}

@wrapMethod(ForceWalkDecisions)
protected const final func ToStand(
  const stateContext: ref<StateContext>,
  const scriptInterface: ref<StateGameScriptInterface>
) -> Bool {
  if NeonAscendancy_ShouldOverrideSafeZone(scriptInterface.executionOwner)
    && !NeonAscendancy_HasNonSafeCombatLock(scriptInterface.executionOwner) {
    return true;
  }
  return wrappedMethod(stateContext, scriptInterface);
}

@wrapMethod(SceneTierAbstractDecisions)
protected const final func ToExploration(
  const stateContext: ref<StateContext>,
  const scriptInterface: ref<StateGameScriptInterface>
) -> Bool {
  if Equals(this.SceneTierToEnter(), GameplayTier.Tier2_StagedGameplay)
    && NeonAscendancy_ShouldOverrideSafeZone(scriptInterface.executionOwner) {
    return true;
  }
  return wrappedMethod(stateContext, scriptInterface);
}

@wrapMethod(WeaponReadyListenerTransition)
protected func UpdateWeaponReadyListenerReturnValue() -> Void {
  if !this.m_beingCreated
    && !this.m_hasStatusEffectVehicleScene
    && NeonAscendancy_ShouldOverrideSafeZone(this.m_executionOwner) {
    this.m_hasStatusEffectNoCombat = false;
    this.m_isInSafeSceneTier = false;
  }
  wrappedMethod();
}

@wrapMethod(PlayerPuppet)
protected cb func OnStatusEffectApplied(evt: ref<ApplyStatusEffectEvent>) -> Bool {
  if IsDefined(evt) && IsDefined(evt.staticData) {
    const game = this.GetGame();
    if NeonAscendancy_IsSanitizerEnabled(game) {
      let staticData = evt.staticData;
      const effectId = staticData.GetID();
      const tags = staticData.GameplayTags();
      const isNoJump = effectId
        == t"GameplayRestriction.NoJump"
        || ArrayContains(tags, n"NoJump");
      const isSafeZoneRestriction = ArrayContains(tags, n"NoCombat")
        || ArrayContains(tags, n"NoWeapons")
        || ArrayContains(tags, n"InDaClub")
        || ArrayContains(tags, n"Tier2Locomotion")
        || effectId == t"GameplayRestriction.NoSprint"
        || isNoJump;
      if isSafeZoneRestriction
        && !ArrayContains(tags, n"VehicleScene")
        && !ArrayContains(tags, n"FastForward")
        && !ArrayContains(tags, n"Braindance")
        && !ArrayContains(tags, n"NoMovement") {
        let psmBB = this.GetPlayerStateMachineBlackboard();
        const hl = IsDefined(psmBB) ? psmBB.GetInt(GetAllBlackboardDefs().PlayerStateMachine.HighLevel) : 1;
        const isCarrying = IsDefined(psmBB)
          && psmBB.GetBool(GetAllBlackboardDefs().PlayerStateMachine.Carrying);
        if isNoJump && isCarrying {
          return wrappedMethod(evt);
        }
        const pos = this.GetWorldPosition();
        const allowed = NeonAscendancy_IsAllowedSafeZone(game, pos);
        if hl < 3 || hl > 5 {
          NcLogInfo(
            s"Sanitizer.OnStatusEffectApplied: zone-lock effect=\(TDBID.ToStringDEBUG(effectId)) hl=\(hl) allowed=\(allowed) pos=(\(pos.X),\(pos.Y),\(pos.Z))"
          );
          if !allowed {
            StatusEffectHelper.RemoveStatusEffect(this, effectId);
            return true;
          }
        }
      }
    }
  }
  return wrappedMethod(evt);
}

@wrapMethod(SecurityAreaControllerPS)
public const final func GetSecurityAreaType() -> ESecurityAreaType {
  const areaType = wrappedMethod();
  if Equals(areaType, ESecurityAreaType.SAFE) && NcIsSanitizerActive() {
    const game = this.GetGameInstance();
    if GameInstance.IsValid(game) {
      const player = GameInstance.GetPlayerSystem(game).GetLocalPlayerMainGameObject();
      if IsDefined(player)
        && !NeonAscendancy_IsAllowedSafeZone(game, player.GetWorldPosition()) {
        return ESecurityAreaType.DISABLED;
      }
    }
  }
  return areaType;
}

@wrapMethod(SecurityAreaControllerPS)
private final func UpdateMiniMapRepresentation() -> Void {
  if Equals(this.m_securityAreaType, ESecurityAreaType.SAFE) && NcIsSanitizerActive() {
    const game = this.GetGameInstance();
    if GameInstance.IsValid(game) {
      const entity = this.GetOwnerEntityWeak();
      if IsDefined(entity)
        && !NeonAscendancy_IsAllowedSafeZone(game, entity.GetWorldPosition()) {
        GameInstance
          .GetMappinSystem(game)
          .OnAreaTypeChanged(
            PersistentID.ExtractEntityID(this.GetID()),
            SecurityAreaControllerPS
              .SecurityAreaTypeEnumToName(ESecurityAreaType.DISABLED)
          );
        return;
      }
    }
  }
  wrappedMethod();
}

@wrapMethod(SecuritySystemControllerPS)
private final func UpdateSecurityZoneDataBlackboard(securityAreaData: SecurityAreaData) -> Void {
  if Equals(securityAreaData.securityAreaType, ESecurityAreaType.SAFE)
    && NcIsSanitizerActive() {
    const game = this.GetGameInstance();
    if GameInstance.IsValid(game) {
      const player = GameInstance.GetPlayerSystem(game).GetLocalPlayerMainGameObject();
      if IsDefined(player) {
        const pos = player.GetWorldPosition();
        const allowed = NeonAscendancy_IsAllowedSafeZone(game, pos);
        NcLogInfo(
          s"Sanitizer.SecurityZoneBB: SAFE allowed=\(allowed) pos=(\(pos.X),\(pos.Y),\(pos.Z))"
        );
        if !allowed {
          securityAreaData.securityAreaType = ESecurityAreaType.DISABLED;
        }
      }
    }
  }
  wrappedMethod(securityAreaData);
}

@wrapMethod(MinimapContainerController)
private final func GetSecurityZoneBasedOnAreaData(securityAreaData: SecurityAreaData) -> ESecurityAreaType {
  const res = wrappedMethod(securityAreaData);
  if Equals(res, ESecurityAreaType.SAFE) && NcIsSanitizerActive() {
    const player = this.GetPlayerControlledObject();
    if IsDefined(player)
      && !NeonAscendancy_IsAllowedSafeZone(player.GetGame(), player.GetWorldPosition()) {
      return ESecurityAreaType.DISABLED;
    }
  }
  return res;
}

@wrapMethod(ZoneAlertNotificationQueue)
protected cb func OnSecurityDataChange(arg: Variant) -> Bool {
  if NcIsSanitizerActive() && IsDefined(arg) && IsDefined(this.m_playerPuppet) {
    let data = FromVariant<SecurityAreaData>(arg);
    if Equals(data.securityAreaType, ESecurityAreaType.SAFE)
      && !NeonAscendancy_IsAllowedSafeZone(this.m_playerPuppet.GetGame(), this.m_playerPuppet.GetWorldPosition()) {
      data.securityAreaType = ESecurityAreaType.DISABLED;
      return wrappedMethod(ToVariant(data));
    }
  }
  return wrappedMethod(arg);
}

