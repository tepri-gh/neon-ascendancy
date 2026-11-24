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
    if this.m_enabled {
      this.ScheduleApply(1.0);
    }
  }

  public func OnDetach() -> Void {
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
    return eraCode;
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
        if StrBeginsWith(id, "quests") || StrBeginsWith(id, "ep1/quest") {
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

private func NeonAscendancy_IsSuppressedVanillaMappinVariant(v: gamedataMappinVariant) -> Bool {
  switch v {
    case gamedataMappinVariant.DefaultQuestVariant:
    case gamedataMappinVariant.QuestGiverVariant:
    case gamedataMappinVariant.ExclamationMarkVariant:
    case gamedataMappinVariant.FixerVariant:
    case gamedataMappinVariant.RetrievingVariant:
    case gamedataMappinVariant.SabotageVariant:
    case gamedataMappinVariant.ThieveryVariant:
    case gamedataMappinVariant.HuntForPsychoVariant:
    case gamedataMappinVariant.ClientInDistressVariant:
    case gamedataMappinVariant.BountyHuntVariant:
    case gamedataMappinVariant.Zzz02_MotorcycleForPurchaseVariant:
    case gamedataMappinVariant.Zzz01_CarForPurchaseVariant:
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

