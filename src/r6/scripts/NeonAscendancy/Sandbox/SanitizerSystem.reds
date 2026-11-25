module NeonAscendancy.Sandbox

import NeonAscendancy.Core.*
import NeonAscendancy.Gameplay.*

private class NeonAscendancy_SanitizerApplyCallback extends DelayCallback {
  public let m_system: wref<NeonAscendancy_SanitizerSystem>;

  public func Call() -> Void {
    if IsDefined(this.m_system) {
      this.m_system.ApplyIfSafe();
    }
  }
}

private class NeonAscendancy_CleanSlateBootstrapCallback extends DelayCallback {
  public let m_system: wref<NeonAscendancy_SanitizerSystem>;

  public func Call() -> Void {
    if IsDefined(this.m_system) {
      this.m_system.RunCleanSlateBootstrap();
    }
  }
}

private class NeonAscendancy_SafeZoneStripCallback extends DelayCallback {
  public let m_system: wref<NeonAscendancy_SanitizerSystem>;
  public let m_allowFollowUp: Bool;

  public func Call() -> Void {
    if IsDefined(this.m_system) {
      this.m_system.RunDelayedSafeZoneStrip(this.m_allowFollowUp);
    }
  }
}

// Thin adapter that delegates era, sanctuary, and vanilla-pin policies to C++
// and applies the results cleanly to Cyberpunk's quest/zone/UI hooks.
public class NeonAscendancy_SanitizerSystem extends ScriptableSystem {
  private persistent let m_schemaVersion: Int32;
  private persistent let m_enabled: Bool;
  private persistent let m_lastEraCode: Int32;
  private persistent let m_starterKitGranted: Bool;
  private let m_playerAttachedCallbackId: Uint32;
  private let m_sanctuariesSynced: Bool;
  private let m_stripPending: Bool;
  private let m_bootstrapPending: Bool;

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
    this.m_stripPending = false;
    const game = this.GetGameInstance();
    let cleanSlate = false;
    if GameInstance.IsValid(game) {
      let qs = GameInstance.GetQuestsSystem(game);
      cleanSlate = IsDefined(qs) && qs.GetFact(n"na_clean_slate") > 0;
    }
    if cleanSlate {
      // Never leave a redirect armed across a save load.
      NcSetAscendancyStartPending(false);
      NcDisarmAscendancyStart();
      if !this.m_enabled {
        this.m_enabled = true;
        this.m_schemaVersion = NeonAscendancy_SchemaVersion();
      }
    }
    NcSetSanitizerActive(this.m_enabled);
    if this.m_enabled {
      this.ScheduleApply(0.5);
    }
    if cleanSlate {
      this.ScheduleCleanSlateBootstrap(1.0);
    }
  }

  public func OnDetach() -> Void {
    this.m_sanctuariesSynced = false;
    this.m_stripPending = false;
    this.m_bootstrapPending = false;
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
    if !IsDefined(playerPuppet) {
      return;
    }
    const game = this.GetGameInstance();
    if !GameInstance.IsValid(game) {
      return;
    }
    let qs = GameInstance.GetQuestsSystem(game);
    const cleanSlate = IsDefined(qs) && qs.GetFact(n"na_clean_slate") > 0;
    const wasPending = NcIsAscendancyStartPending();
    if cleanSlate || wasPending {
      NcLogInfo(
        s"Sanitizer.OnPlayerAttached: cleanSlate=\(cleanSlate) pending=\(wasPending)"
      );
      // Clean-slate world attached: consume the arm/pending handshake, then
      // auto-enable the sanitizer so a clean-slate run is never unmanaged.
      NcSetAscendancyStartPending(false);
      NcDisarmAscendancyStart();
      if !this.m_enabled {
        this.m_enabled = true;
        this.m_schemaVersion = NeonAscendancy_SchemaVersion();
      }
    }
    if this.m_enabled {
      NcSetSanitizerActive(true);
      this.ScheduleApply(0.5);
    }
    if cleanSlate || wasPending {
      this.ScheduleCleanSlateBootstrap(1.0);
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

  public final func ScheduleSafeZoneStrip(delaySeconds: Float, allowFollowUp: Bool) -> Void {
    if this.m_stripPending {
      return;
    }
    const game = this.GetGameInstance();
    if !GameInstance.IsValid(game) {
      return;
    }
    let ds = GameInstance.GetDelaySystem(game);
    if IsDefined(ds) {
      this.m_stripPending = true;
      let cb = new NeonAscendancy_SafeZoneStripCallback();
      cb.m_system = this;
      cb.m_allowFollowUp = allowFollowUp;
      ds.DelayCallback(cb, delaySeconds, false);
    }
  }

  public final func RunDelayedSafeZoneStrip(allowFollowUp: Bool) -> Void {
    this.m_stripPending = false;
    if !this.m_enabled {
      return;
    }
    const game = this.GetGameInstance();
    if !GameInstance.IsValid(game) {
      return;
    }
    let player = GameInstance.GetPlayerSystem(game).GetLocalPlayerMainGameObject();
    if !IsDefined(player) {
      return;
    }
    const pos = player.GetWorldPosition();
    const allowed = this.IsAllowedSafeZoneAt(game, pos);
    let bbSys = GameInstance.GetBlackboardSystem(game);
    let psmBB: ref<IBlackboard>;
    let hl = 1;
    let isCarrying = false;
    if IsDefined(bbSys) {
      psmBB = bbSys
        .GetLocalInstanced(player.GetEntityID(), GetAllBlackboardDefs().PlayerStateMachine);
      if IsDefined(psmBB) {
        hl = psmBB.GetInt(GetAllBlackboardDefs().PlayerStateMachine.HighLevel);
        isCarrying = psmBB.GetBool(GetAllBlackboardDefs().PlayerStateMachine.Carrying);
      }
    }
    let stripped = 0;
    if !allowed && (hl < 3 || hl > 5) && !NeonAscendancy_HasNonSafeCombatLock(player) {
      stripped = NeonAscendancy_StripAllSafeZoneRestrictions(player, isCarrying);
      NeonAscendancy_ClearSafeZonePsmParams(player, psmBB);
      PlayerGameplayRestrictions.PushForceRefreshInputHintsEventToPSM(player);
    }
    NeonAscendancy_LogSafeZoneDiagnostics(game, player, psmBB, allowed, stripped);
    if allowFollowUp && stripped > 0 && !allowed && (hl < 3 || hl > 5) {
      this.ScheduleSafeZoneStrip(0.25, false);
    }
  }

  // --- Clean-Slate Bootstrap -------------------------------------------------
  //
  // Runs on the na_clean_slate fact (set by the custom root quest phase) for
  // both a fresh "Start Ascendancy" boot and clean-slate save loads. Fact
  // application and the Ascendancy session boot are idempotent and re-run every
  // load; the Level-1 Mercenary starter kit is granted exactly once per
  // character via the persisted m_starterKitGranted flag.
  public final func ScheduleCleanSlateBootstrap(delaySeconds: Float) -> Void {
    if this.m_bootstrapPending {
      return;
    }
    const game = this.GetGameInstance();
    if !GameInstance.IsValid(game) {
      return;
    }
    let ds = GameInstance.GetDelaySystem(game);
    if IsDefined(ds) {
      this.m_bootstrapPending = true;
      let cb = new NeonAscendancy_CleanSlateBootstrapCallback();
      cb.m_system = this;
      ds.DelayCallback(cb, delaySeconds, false);
    }
  }

  public final func RunCleanSlateBootstrap() -> Void {
    this.m_bootstrapPending = false;
    const game = this.GetGameInstance();
    if !GameInstance.IsValid(game) {
      return;
    }
    let qs = GameInstance.GetQuestsSystem(game);
    if !IsDefined(qs) || qs.GetFact(n"na_clean_slate") == 0 {
      NcLogInfo("Sanitizer.CleanSlateBootstrap: skipped (na_clean_slate=0)");
      return;
    }
    let player = GameInstance.GetPlayerSystem(game).GetLocalPlayerMainGameObject();
    if !IsDefined(player) {
      this.ScheduleCleanSlateBootstrap(1.0);
      return;
    }
    this.ApplyCleanSlateFacts(qs);
    if !this.m_starterKitGranted {
      this.GrantCleanSlateStarterKit(game, player);
    }
    this.BootAscendancySystems(game);
  }

  // Mandatory usability facts for a clean-slate run (HUD, map, phone/car
  // summoning, full RPG progression, tutorials off, apartment, open city).
  // NEVER story-completion facts.
  private final func ApplyCleanSlateFacts(qs: QuestsSystem) -> Void {
    qs.SetFact(n"unlock_phone_hud_dpad", 1);
    qs.SetFact(n"unlock_car_hud_dpad", 1);
    qs.SetFact(n"q000_started", 1);
    qs.SetFact(n"dpad_hints_visibility_enabled", 1);
    qs.SetFact(n"initial_gadget_picked", 1);
    qs.SetFact(n"map_blocked", 0);
    qs.SetFact(n"full_rpg_progression_on", 1);
    qs.SetFact(n"q000_patch_2_0_new_game", 1);
    qs.SetFact(n"disable_tutorials", 1);
    qs.SetFact(n"apartment_on", 1);
    qs.SetFact(n"watson_prolog_lock", 0);
    qs.SetFact(n"watson_prolog_unlock", 1);
    qs.SetFact(n"q101_enable_activities_flat", 1);
    qs.SetFact(n"q101_enable_side_content", 1);
    // Mark Wilson's gun-shop intro/tutorial already seen so wat_lch_gunsmith_01.scene
    // opens directly as a normal gunsmith vendor without activating sq_q001_wilson ("The Gun").
    qs.SetFact(n"wilson_met", 1);
    qs.SetFact(n"wat_lch_gun_01_met", 1);
    qs.SetFact(n"q001_wilson_shop_tutorial_seen", 1);
  }

  // Level-1 Mercenary Starter Kit: Paraline cyberdeck + Kiroshi + Power Grip +
  // Boring Plating, V's Unity + ammo, Q001 outfit, starter car, 2,500 eb, and
  // basic crafting mats. Every grant is guarded so the whole kit is idempotent.
  // Placement in V's H10 apartment is handled natively by ascendancy.gamedef's
  // spawnPointTags (mq000_spwn_player) with full streaming before fade-in.
  private final func GrantCleanSlateStarterKit(game: GameInstance, player: ref<GameObject>) -> Void {
    let ts = GameInstance.GetTransactionSystem(game);
    if !IsDefined(ts) {
      this.ScheduleCleanSlateBootstrap(1.0);
      return;
    }

    // Money: top up to 2,500 eb cleanly (never overshoot, never take away).
    const money = ts.GetItemQuantity(player, MarketSystem.Money());
    if money < 2500 {
      ts.GiveItem(player, MarketSystem.Money(), 2500 - money);
    }

    // Starter car (Archer Hella is the canonical starter vehicle).
    let vs = GameInstance.GetVehicleSystem(game);
    if IsDefined(vs) {
      vs
        .EnablePlayerVehicle("Vehicle.v_standard2_archer_hella_player", true, false);
    }

    // Cyberware (give + equip into their slots via EquipmentSystem request queue).
    this.GrantAndEquipItem(game, ts, player, t"Items.KiroshiOptics");
    this
      .GrantAndEquipItem(game, ts, player, t"Items.AdvancedMilitechParalineMKICommon");
    this.GrantAndEquipItem(game, ts, player, t"Items.PowerGripRare");
    this
      .GrantAndEquipItem(game, ts, player, t"Items.AdvancedBoringPlating_Q001");

    // Weapon & ammo.
    this.GrantAndEquipItem(game, ts, player, t"Items.Preset_V_Unity");
    this.GrantItem(ts, player, t"Ammo.HandgunAmmo", 60);

    // Outfit.
    this.GrantAndEquipItem(game, ts, player, t"Items.Q001_TShirt");
    this.GrantAndEquipItem(game, ts, player, t"Items.Q001_Pants");
    this.GrantAndEquipItem(game, ts, player, t"Items.Q001_Shoes");

    // Basic crafting mats.
    this.GrantItem(ts, player, t"Items.CommonMaterial1", 50);

    this.m_starterKitGranted = true;
    const posAfter = player.GetWorldPosition();
    NcLogInfo(
      s"Sanitizer.CleanSlateBootstrap: granted starter kit (Paraline + car + 2500 eb) pos=(\(posAfter.X),\(posAfter.Y),\(posAfter.Z))"
    );
    let autosave = GameInstance.GetAutoSaveSystem(game);
    if IsDefined(autosave) {
      autosave.RequestCheckpoint();
    }
    NeonAscendancy_ShowHudNotice(
      game,
      "Neon Ascendancy \u{2014} Clean-Slate Night City. Open Pause Menu to found your gang."
    );
  }

  private final func GrantAndEquipItem(
    game: GameInstance,
    ts: TransactionSystem,
    player: ref<GameObject>,
    tdbid: TweakDBID
  ) -> Void {
    const itemId = ItemID.FromTDBID(tdbid);
    const hasAny = ts.HasItem(player, ItemID.CreateQuery(tdbid));
    let es = GameInstance.GetScriptableSystemsContainer(game).Get(n"EquipmentSystem") as EquipmentSystem;
    if IsDefined(es) {
      let req = new EquipRequest();
      req.owner = player;
      req.itemID = itemId;
      req.addToInventory = !hasAny;
      es.QueueRequest(req);
    } else if !hasAny {
      ts.GiveItem(player, itemId, 1);
    }
  }

  private final func GrantItem(
    ts: TransactionSystem,
    player: ref<GameObject>,
    tdbid: TweakDBID,
    amount: Int32
  ) -> Void {
    const itemId = ItemID.FromTDBID(tdbid);
    const have = ts.GetItemQuantity(player, itemId);
    if have < amount {
      ts.GiveItem(player, itemId, amount - have);
    }
  }

  // Ensure the Ascendancy session/pins boot automatically on a clean-slate run.
  private final func BootAscendancySystems(game: GameInstance) -> Void {
    let sys = GameInstance
      .GetScriptableSystemsContainer(game)
      .Get(n"NeonAscendancy.Gameplay.NeonAscendancy_AscendancySystem") as NeonAscendancy_AscendancySystem;
    if IsDefined(sys) {
      sys.BootCleanSlateSession();
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

    const cleanSlateFact = IsDefined(qs) ? qs.GetFact(n"na_clean_slate") : -1;
    NcLogInfo(
      s"Sanitizer.EnforceSafeZone: tier=\(sceneTier) cleanSlate=\(cleanSlateFact) allowed=\(allowed) sanctuaries=\(NcGetSafeSanctuaryCount()) cityArea=\(cityAreaFact) forceEmpty=\(forceEmptyFact) noCombat=\(hasNoCombat) psmZones=\(psmZonesBefore) secArea=\(secAreaBefore)"
    );

    if allowed || sceneTier >= 3 {
      return;
    }

    if forceEmptyFact != 0 {
      qs.SetFact(n"ForceEmptyHands", 0);
    }
    if !NeonAscendancy_HasNonSafeCombatLock(player) {
      const isCarrying = IsDefined(psmBB)
        && psmBB.GetBool(GetAllBlackboardDefs().PlayerStateMachine.Carrying);
      NeonAscendancy_StripAllSafeZoneRestrictions(player, isCarrying);
    }
    if IsDefined(pp) {
      pp.OnZoneFactChanged(cityAreaFact);
    }
    NeonAscendancy_ClearSafeZonePsmParams(player, psmBB);
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
    || ses.HasStatusEffectWithTag(eid, n"Braindance")
    || ses.HasStatusEffectWithTag(eid, n"FistFight")
    || ses.HasStatusEffectWithTag(eid, n"ShootingRangeCompetition")
    || ses.HasStatusEffectWithTag(eid, n"Cyberspace")
    || ses.HasStatusEffectWithTag(eid, n"MetroRide")
    || ses.HasStatusEffectWithTag(eid, n"SpaceShuttleInterior");
}

private func NeonAscendancy_IsSafeZoneRestriction(effectId: TweakDBID, const tags: [CName], isCarrying: Bool) -> Bool {
  if ArrayContains(tags, n"VehicleScene")
    || ArrayContains(tags, n"FastForward")
    || ArrayContains(tags, n"Braindance")
    || ArrayContains(tags, n"NoMovement")
    || ArrayContains(tags, n"FistFight")
    || ArrayContains(tags, n"ShootingRangeCompetition")
    || ArrayContains(tags, n"Firearms")
    || ArrayContains(tags, n"Melee")
    || ArrayContains(tags, n"Cyberspace")
    || ArrayContains(tags, n"MetroRide")
    || ArrayContains(tags, n"SpaceShuttleInterior")
    || ArrayContains(tags, n"SandstormLocomotion")
    || ArrayContains(tags, n"FocusModeLocomotion")
    || ArrayContains(tags, n"ForceCrouch")
    || ArrayContains(tags, n"ForceStand")
    || ArrayContains(tags, n"BodyCarryingGeneric")
    || ArrayContains(tags, n"BodyCarryingFriendly")
    || ArrayContains(tags, n"BodyCarryingWoundedSoldier")
    || ArrayContains(tags, n"BodyCarryingCanSprint")
    || ArrayContains(tags, n"BodyCarryingBodyMasterPerk5")
    || effectId == t"GameplayRestriction.CinematicCamera"
    || effectId == t"GameplayRestriction.BinocularView" {
    return false;
  }
  const isNoJump = effectId == t"GameplayRestriction.NoJump" || ArrayContains(tags, n"NoJump");
  if isNoJump {
    return !isCarrying;
  }
  return ArrayContains(tags, n"NoCombat")
    || ArrayContains(tags, n"NoWeapons")
    || ArrayContains(tags, n"InDaClub")
    || ArrayContains(tags, n"Tier2Locomotion")
    || ArrayContains(tags, n"NoWeaponWheel")
    || ArrayContains(tags, n"NoQuickHacks")
    || ArrayContains(tags, n"NoGrenadeOrGadget")
    || effectId == t"GameplayRestriction.NoSprint"
    || effectId == t"GameplayRestriction.NoCombat"
    || effectId == t"GameplayRestriction.InDaClub"
    || effectId == t"GameplayRestriction.NoWeapons"
    || effectId == t"GameplayRestriction.NoCyberware"
    || effectId == t"GameplayRestriction.NoDangerousCyberware"
    || effectId == t"GameplayRestriction.NoDangerousPerks"
    || effectId == t"GameplayRestriction.NoCombatWithQuickhacks";
}

private func NeonAscendancy_StripEffectHard(player: GameObject, effectId: TweakDBID, staticData: wref<StatusEffect_Record>) -> Bool {
  const game = player.GetGame();
  if !GameInstance.IsValid(game) {
    return false;
  }
  let ses = GameInstance.GetStatusEffectSystem(game);
  if !IsDefined(ses) {
    return false;
  }
  const eid = player.GetEntityID();
  let matches: array<ref<StatusEffect>>;
  ses.GetAppliedEffectsWithID(eid, effectId, matches);
  let totalStacks: Uint32 = 0u;
  for m in matches {
    if IsDefined(m) {
      totalStacks += m.GetStackCount();
    }
  }
  if totalStacks == 0u {
    totalStacks = 1u;
  }
  let removed = ses.RemoveStatusEffect(eid, effectId, totalStacks);
  if ses.HasStatusEffect(eid, effectId) {
    removed = ses.RemoveStatusEffect(eid, effectId, 999u) || removed;
  }
  if ses.HasStatusEffect(eid, effectId) {
    removed = ses.RemoveStatusEffect(eid, effectId) || removed;
  }

  let es = GameInstance.GetEffectorSystem(game);
  let glps = GameInstance.GetGameplayLogicPackageSystem(game);
  const stillActive = ses.HasStatusEffect(eid, effectId);
  let appliedPkgs: array<TweakDBID>;
  if stillActive && IsDefined(glps) {
    glps.GetAppliedPackages(player, appliedPkgs);
  }
  if IsDefined(staticData) {
    const pkgCount = staticData.GetPackagesCount();
    let p = 0;
    while p < pkgCount {
      let pkg = staticData.GetPackagesItem(p);
      if IsDefined(pkg) {
        if IsDefined(es) {
          const effCount = pkg.GetEffectorsCount();
          let e = 0;
          while e < effCount {
            let eff = pkg.GetEffectorsItem(e);
            if IsDefined(eff) {
              es.RemoveEffectorsByID(eid, eff.GetID());
              let applyEff = eff as ApplyEffectorEffector_Record;
              if IsDefined(applyEff) {
                let inner = applyEff.EffectorToApply();
                if IsDefined(inner) {
                  es.RemoveEffectorsByID(eid, inner.GetID());
                }
              }
            }
            e += 1;
          }
        }
        if stillActive && IsDefined(glps) {
          const pkgId = pkg.GetID();
          if ArrayContains(appliedPkgs, pkgId) {
            glps.RemovePackages(player, pkgId, 999u);
          }
        }
      }
      p += 1;
    }
  }
  return removed;
}

private func NeonAscendancy_StripAllSafeZoneRestrictions(player: GameObject, isCarrying: Bool) -> Int32 {
  const game = player.GetGame();
  if !GameInstance.IsValid(game) {
    return 0;
  }
  let ses = GameInstance.GetStatusEffectSystem(game);
  if !IsDefined(ses) {
    return 0;
  }
  let applied: array<ref<StatusEffect>>;
  ses.GetAppliedEffects(player.GetEntityID(), applied);
  let stripped = 0;
  for eff in applied {
    if IsDefined(eff) {
      let rec = eff.GetRecord();
      if IsDefined(rec) {
        const effectId = rec.GetID();
        const tags = rec.GameplayTags();
        if NeonAscendancy_IsSafeZoneRestriction(effectId, tags, isCarrying) {
          NeonAscendancy_StripEffectHard(player, effectId, rec);
          stripped += 1;
        }
      }
    }
  }
  return stripped;
}

private func NeonAscendancy_QueueClearPsmBool(pp: PlayerPuppet, paramId: CName) -> Void {
  let evt = new PSMPostponedParameterBool();
  evt.id = paramId;
  evt.value = false;
  evt.aspect = gamestateMachineParameterAspect.Permanent;
  pp.QueueEvent(evt);
}

private func NeonAscendancy_ClearSafeZonePsmParams(player: GameObject, psmBB: ref<IBlackboard>) -> Void {
  let pp = player as PlayerPuppet;
  if IsDefined(pp) {
    NeonAscendancy_QueueClearPsmBool(pp, n"ForceEmptyHandsByZone");
    NeonAscendancy_QueueClearPsmBool(pp, n"ForceSafeStateByZone");
    NeonAscendancy_QueueClearPsmBool(pp, n"ForceEmptyHands");
    NeonAscendancy_QueueClearPsmBool(pp, n"ForceSafeState");
    NeonAscendancy_QueueClearPsmBool(pp, n"ForceWalk");
    if IsDefined(psmBB)
      && psmBB.GetInt(GetAllBlackboardDefs().PlayerStateMachine.Zones) == 2 {
      pp
        .SetBlackboardIntVariable(GetAllBlackboardDefs().PlayerStateMachine.Zones, 1);
    }
  }
  if IsDefined(psmBB) {
    const secVar = psmBB.GetVariant(GetAllBlackboardDefs().PlayerStateMachine.SecurityZoneData);
    if IsDefined(secVar) {
      const secData = FromVariant<SecurityAreaData>(secVar);
      if Equals(secData.securityAreaType, ESecurityAreaType.SAFE) {
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
  }
}

private func NeonAscendancy_LogSafeZoneDiagnostics(
  game: GameInstance,
  player: GameObject,
  psmBB: ref<IBlackboard>,
  allowed: Bool,
  stripped: Int32
) -> Void {
  const pos = player.GetWorldPosition();
  const eid = player.GetEntityID();
  const statsId = Cast<StatsObjectID>(eid);
  let stats = GameInstance.GetStatsSystem(game);
  let canSprint = false;
  let hasDodge = false;
  let canJump = false;
  let hasDoubleJump = false;
  let hasChargeJump = false;
  let hasSandy = false;
  let maxSpeed = 0.0;
  if IsDefined(stats) {
    canSprint = stats.GetStatBoolValue(statsId, gamedataStatType.CanSprint);
    hasDodge = stats.GetStatBoolValue(statsId, gamedataStatType.HasDodge);
    canJump = stats.GetStatBoolValue(statsId, gamedataStatType.CanJump);
    hasDoubleJump = stats.GetStatBoolValue(statsId, gamedataStatType.HasDoubleJump);
    hasChargeJump = stats.GetStatBoolValue(statsId, gamedataStatType.HasChargeJump);
    hasSandy = stats.GetStatBoolValue(statsId, gamedataStatType.HasSandevistan);
    maxSpeed = stats.GetStatValue(statsId, gamedataStatType.MaxSpeed);
  }
  let hl = -1;
  let zones = -1;
  let upper = -1;
  let loco = -1;
  let secArea = -1;
  if IsDefined(psmBB) {
    hl = psmBB.GetInt(GetAllBlackboardDefs().PlayerStateMachine.HighLevel);
    zones = psmBB.GetInt(GetAllBlackboardDefs().PlayerStateMachine.Zones);
    upper = psmBB.GetInt(GetAllBlackboardDefs().PlayerStateMachine.UpperBody);
    loco = psmBB.GetInt(GetAllBlackboardDefs().PlayerStateMachine.Locomotion);
    const secVar = psmBB.GetVariant(GetAllBlackboardDefs().PlayerStateMachine.SecurityZoneData);
    if IsDefined(secVar) {
      const secData = FromVariant<SecurityAreaData>(secVar);
      secArea = EnumInt(secData.securityAreaType);
    }
  }
  let effectList = "";
  let ses = GameInstance.GetStatusEffectSystem(game);
  if IsDefined(ses) {
    let applied: array<ref<StatusEffect>>;
    ses.GetAppliedEffects(eid, applied);
    for eff in applied {
      if IsDefined(eff) && IsDefined(eff.GetRecord()) {
        if StrLen(effectList) > 0 {
          effectList += ",";
        }
        effectList
          += s"\(TDBID.ToStringDEBUG(eff.GetRecord().GetID()))(x\(eff.GetStackCount()))";
      }
    }
  }
  NcLogInfo(
    s"Sanitizer.PostStrip: stripped=\(stripped) allowed=\(allowed) hl=\(hl) zones=\(zones) secArea=\(secArea) upper=\(upper) loco=\(loco) canSprint=\(canSprint) hasDodge=\(hasDodge) canJump=\(canJump) hasDoubleJump=\(hasDoubleJump) hasChargeJump=\(hasChargeJump) hasSandy=\(hasSandy) maxSpeed=\(maxSpeed) pos=(\(pos.X),\(pos.Y),\(pos.Z)) effects=[\(effectList)]"
  );
}

private func NeonAscendancy_ScheduleSafeZoneStrip(game: GameInstance, delaySeconds: Float) -> Void {
  if !GameInstance.IsValid(game) {
    return;
  }
  let sys = GameInstance
    .GetScriptableSystemsContainer(game)
    .Get(n"NeonAscendancy.Sandbox.NeonAscendancy_SanitizerSystem") as NeonAscendancy_SanitizerSystem;
  if IsDefined(sys) {
    sys.ScheduleSafeZoneStrip(delaySeconds, true);
  }
}

private func NeonAscendancy_IsSafeZoneBlockedStat(statType: gamedataStatType) -> Bool {
  return Equals(statType, gamedataStatType.CanSprint)
    || Equals(statType, gamedataStatType.HasDodge)
    || Equals(statType, gamedataStatType.HasDodgeAir)
    || Equals(statType, gamedataStatType.HasChargeJump)
    || Equals(statType, gamedataStatType.HasDoubleJump)
    || Equals(statType, gamedataStatType.CanJump)
    || Equals(statType, gamedataStatType.HasSandevistan)
    || Equals(statType, gamedataStatType.HasBerserk)
    || Equals(statType, gamedataStatType.HasKerenzikov)
    || Equals(statType, gamedataStatType.CanUseOverclock);
}

// Block nested ApplyStatGroupEffector payloads (e.g. GameplayRestriction.InDaClub
// and GameplayRestriction.NoSprint -> ApplyEffectorOnPlayer -> ApplyStatGroupOnPlayer)
// from zeroing movement/cyberware stats outside allowed sanctuaries.
@wrapMethod(ApplyStatGroupEffector)
public final func ApplyModifierGroup() -> Void {
  if IsDefined(this.m_owner)
    && this.m_owner.IsPlayer()
    && NeonAscendancy_ShouldOverrideSafeZone(this.m_owner)
    && !NeonAscendancy_HasNonSafeCombatLock(this.m_owner)
    && !StatusEffectSystem
      .ObjectHasStatusEffect(this.m_owner, t"BaseStatusEffect.Encumbered") {
    let blockedByPlayerState = false;
    const pp = this.m_owner as PlayerPuppet;
    if IsDefined(pp) {
      const psmBB = pp.GetPlayerStateMachineBlackboard();
      if IsDefined(psmBB) {
        blockedByPlayerState = psmBB.GetBool(GetAllBlackboardDefs().PlayerStateMachine.Carrying)
          || psmBB
            .GetBool(GetAllBlackboardDefs().PlayerStateMachine.MountedToVehicle)
          || psmBB.GetInt(GetAllBlackboardDefs().PlayerStateMachine.Vision) == 1;
      }
    }
    if !blockedByPlayerState {
      let groupRec = TweakDBInterface.GetStatModifierGroupRecord(this.m_record);
      if IsDefined(groupRec) {
        const modCount = groupRec.GetStatModifiersCount();
        let i = 0;
        while i < modCount {
          let modRec = groupRec.GetStatModifiersItem(i) as ConstantStatModifier_Record;
          if IsDefined(modRec)
            && Equals(modRec.ModifierType(), n"Multiplier")
            && modRec.Value() <= 0.0 {
            let statRec = modRec.StatType();
            if IsDefined(statRec)
              && NeonAscendancy_IsSafeZoneBlockedStat(statRec.StatType()) {
              NcLogInfo(
                s"Sanitizer.BlockStatGroup: group=\(TDBID.ToStringDEBUG(this.m_record)) stat=\(statRec.EnumName())"
              );
              return;
            }
          }
          i += 1;
        }
      }
    }
  }
  wrappedMethod();
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
      let psmBB = this.GetPlayerStateMachineBlackboard();
      const hl = IsDefined(psmBB) ? psmBB.GetInt(GetAllBlackboardDefs().PlayerStateMachine.HighLevel) : 1;
      const isCarrying = IsDefined(psmBB)
        && psmBB.GetBool(GetAllBlackboardDefs().PlayerStateMachine.Carrying);
      if NeonAscendancy_IsSafeZoneRestriction(effectId, tags, isCarrying) {
        const pos = this.GetWorldPosition();
        const allowed = NeonAscendancy_IsAllowedSafeZone(game, pos);
        if hl < 3 || hl > 5 {
          if !allowed {
            const removed = NeonAscendancy_StripEffectHard(this, effectId, staticData);
            let ses = GameInstance.GetStatusEffectSystem(game);
            const still = IsDefined(ses) && ses.HasStatusEffect(this.GetEntityID(), effectId);
            NcLogInfo(
              s"Sanitizer.OnStatusEffectApplied: zone-lock effect=\(TDBID.ToStringDEBUG(effectId)) hl=\(hl) allowed=\(allowed) removed=\(removed) still=\(still) pos=(\(pos.X),\(pos.Y),\(pos.Z))"
            );
            NeonAscendancy_ScheduleSafeZoneStrip(game, 0.05);
            return true;
          }
          NcLogInfo(
            s"Sanitizer.OnStatusEffectApplied: sanctuary-allowed effect=\(TDBID.ToStringDEBUG(effectId)) hl=\(hl) pos=(\(pos.X),\(pos.Y),\(pos.Z))"
          );
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

