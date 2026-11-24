module NeonAscendancy.Gameplay

import NeonAscendancy.Core.*
import NeonAscendancy.Map.*
import NeonAscendancy.Persistence.*
import NeonAscendancy.Sandbox.*

private class NeonAscendancy_IncomeTickCallback extends DelayCallback {
  public let m_system: wref<NeonAscendancy_AscendancySystem>;

  public func Call() -> Void {
    if IsDefined(this.m_system) {
      this.m_system.OnIncomeTick();
    }
  }
}

// Paper-thin coordinator wiring Pause Menu actions, low-frequency GameTime ticks,
// NPC takedown events, and TransactionSystem eddie payouts into the C++20 core.
public class NeonAscendancy_AscendancySystem extends ScriptableSystem {
  private let m_tickerRunning: Bool;
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
    if this.IsAscendancyActive() {
      this.SyncMapAndStartTicker();
    }
  }

  public func OnDetach() -> Void {
    this.m_tickerRunning = false;
    const game = this.GetGameInstance();
    if this.m_playerAttachedCallbackId > 0u && GameInstance.IsValid(game) {
      GameInstance
        .GetPlayerSystem(game)
        .UnregisterPlayerPuppetAttachedCallback(this.m_playerAttachedCallbackId);
      this.m_playerAttachedCallbackId = 0u;
    }
  }

  private final func OnPlayerAttachedCallback(playerPuppet: ref<GameObject>) -> Void {
    if IsDefined(playerPuppet) && this.IsAscendancyActive() {
      this.SyncMapAndStartTicker();
    }
  }

  public const final func IsAscendancyActive() -> Bool {
    return NeonAscendancy_IsSanitizerEnabled(this.GetGameInstance());
  }

  public final func HandlePauseMenuAction() -> Void {
    const game = this.GetGameInstance();
    if !GameInstance.IsValid(game) {
      return;
    }
    const action = NcGetPauseMenuActionCode(this.IsAscendancyActive());
    switch action {
      case 1:
        this.ActivateAscendancy();
        break;
      case 2:
        this.FoundGangHere("Neon Vipers");
        break;
      case 3:
        this.LaunchNearestRivalRaid();
        break;
      case 4:
        NeonAscendancy_ShowHudNotice(game, NcFormatStatusSummary());
        break;
      default:
        break;
    }
  }

  public final func ActivateAscendancy() -> Void {
    const game = this.GetGameInstance();
    if !GameInstance.IsValid(game) {
      return;
    }
    let anchor = GameInstance
      .GetScriptableSystemsContainer(game)
      .Get(n"NeonAscendancy.Persistence.NeonAscendancy_AnchorSystem") as NeonAscendancy_AnchorSystem;
    if IsDefined(anchor) {
      anchor.EnsureSessionInitialized();
    }
    let sanitizer = GameInstance
      .GetScriptableSystemsContainer(game)
      .Get(n"NeonAscendancy.Sandbox.NeonAscendancy_SanitizerSystem") as NeonAscendancy_SanitizerSystem;
    let eraName = "Unknown";
    if IsDefined(sanitizer) {
      eraName = sanitizer.EnableAndApply();
    }
    this.SyncMapAndStartTicker();
    NeonAscendancy_ShowHudNotice(game, s"NEON ASCENDANCY ACTIVE (\(eraName)) | Open Pause Menu to Found Gang");
  }

  public final func FoundGangHere(gangName: String) -> Void {
    const game = this.GetGameInstance();
    const player = GameInstance.GetPlayerSystem(game).GetLocalPlayerMainGameObject();
    if !IsDefined(player) {
      return;
    }
    let anchor = GameInstance
      .GetScriptableSystemsContainer(game)
      .Get(n"NeonAscendancy.Persistence.NeonAscendancy_AnchorSystem") as NeonAscendancy_AnchorSystem;
    if IsDefined(anchor) {
      anchor.EnsureSessionInitialized();
    }
    const pos = player.GetWorldPosition();
    const stId = NcFindBestSubTerritoryAt(pos.X, pos.Y);
    const gameSeconds = GameTime.GetSeconds(GameInstance.GetTimeSystem(game).GetGameTime());
    const rev = NcFoundGang(gangName, stId, gameSeconds);
    if rev > 0 {
      NcOfferNearestRivalMission(pos.X, pos.Y, gameSeconds);
      if IsDefined(anchor) {
        anchor.SyncPublishedRevision();
      }
      this.SyncMapAndStartTicker();
      NeonAscendancy_DrainHudNotices(game);
    }
  }

  public final func LaunchNearestRivalRaid() -> Void {
    const game = this.GetGameInstance();
    const player = GameInstance.GetPlayerSystem(game).GetLocalPlayerMainGameObject();
    if !IsDefined(player) {
      return;
    }
    const pos = player.GetWorldPosition();
    const gameSeconds = GameTime.GetSeconds(GameInstance.GetTimeSystem(game).GetGameTime());
    const missionId = NcOfferNearestRivalMission(pos.X, pos.Y, gameSeconds);
    if missionId > 0 {
      let anchor = GameInstance
        .GetScriptableSystemsContainer(game)
        .Get(n"NeonAscendancy.Persistence.NeonAscendancy_AnchorSystem") as NeonAscendancy_AnchorSystem;
      if IsDefined(anchor) {
        anchor.SyncPublishedRevision();
      }
      this.SyncMapAndStartTicker();
    }
    NeonAscendancy_DrainHudNotices(game);
  }

  public final func OnNpcIncapacitated(puppet: wref<ScriptedPuppet>) -> Void {
    if !IsDefined(puppet) || puppet.IsPlayer() || !this.IsAscendancyActive() {
      return;
    }
    const isCrowd = puppet.IsCrowd();
    const isCivilian = puppet.IsCivilian() || puppet.IsCharacterCivilian();
    const isVendor = puppet.IsVendor();
    if isCrowd || isCivilian || isVendor {
      return;
    }
    const game = this.GetGameInstance();
    if !GameInstance.IsValid(game) {
      return;
    }
    let player = GameInstance.GetPlayerSystem(game).GetLocalPlayerMainGameObject();
    const isHostile = IsDefined(player)
      && Equals(GameObject.GetAttitudeTowards(puppet, player), EAIAttitude.AIA_Hostile);
    let affEnum = -1;
    let rec = puppet.GetRecord();
    if IsDefined(rec) {
      let aff = rec.Affiliation();
      if IsDefined(aff) {
        affEnum = EnumInt(aff.Type());
      }
    }
    const pos = puppet.GetWorldPosition();
    const entityHash = Cast<Uint64>(EntityID.GetHash(puppet.GetEntityID()));
    const gameSeconds = GameTime.GetSeconds(GameInstance.GetTimeSystem(game).GetGameTime());
    const payout = NcOnNpcIncapacitated(
      entityHash,
      affEnum,
      isCrowd,
      isCivilian,
      isVendor,
      isHostile,
      pos.X,
      pos.Y,
      pos.Z,
      gameSeconds
    );
    if payout > 0l {
      this.GrantPlayerEddies(game, payout);
      let anchor = GameInstance
        .GetScriptableSystemsContainer(game)
        .Get(n"NeonAscendancy.Persistence.NeonAscendancy_AnchorSystem") as NeonAscendancy_AnchorSystem;
      if IsDefined(anchor) {
        anchor.SyncPublishedRevision();
      }
      this.SyncMapAndStartTicker();
    }
    NeonAscendancy_DrainHudNotices(game);
  }

  public final func OnIncomeTick() -> Void {
    this.m_tickerRunning = false;
    const game = this.GetGameInstance();
    if !GameInstance.IsValid(game) || !this.IsAscendancyActive() {
      return;
    }
    const gameSeconds = GameTime.GetSeconds(GameInstance.GetTimeSystem(game).GetGameTime());
    const payout = NcAdvanceTime(gameSeconds);
    if payout > 0l {
      this.GrantPlayerEddies(game, payout);
      let anchor = GameInstance
        .GetScriptableSystemsContainer(game)
        .Get(n"NeonAscendancy.Persistence.NeonAscendancy_AnchorSystem") as NeonAscendancy_AnchorSystem;
      if IsDefined(anchor) {
        anchor.SyncPublishedRevision();
      }
      NeonAscendancy_DrainHudNotices(game);
    }
    this.ScheduleNextIncomeTick();
  }

  private final func SyncMapAndStartTicker() -> Void {
    const game = this.GetGameInstance();
    if !GameInstance.IsValid(game) {
      return;
    }
    let mapSys = GameInstance
      .GetScriptableSystemsContainer(game)
      .Get(n"NeonAscendancy.Map.NeonAscendancy_TerritoryMapSystem") as NeonAscendancy_TerritoryMapSystem;
    if IsDefined(mapSys) {
      mapSys.SyncAllPins();
    }
    if !this.m_tickerRunning {
      this.ScheduleNextIncomeTick();
    }
  }

  private final func ScheduleNextIncomeTick() -> Void {
    const game = this.GetGameInstance();
    if !GameInstance.IsValid(game) {
      return;
    }
    let ds = GameInstance.GetDelaySystem(game);
    if IsDefined(ds) {
      let cb = new NeonAscendancy_IncomeTickCallback();
      cb.m_system = this;
      ds.DelayCallback(cb, 10.0, false);
      this.m_tickerRunning = true;
    }
  }

  private final func GrantPlayerEddies(game: GameInstance, amount: Int64) -> Void {
    if amount <= 0l {
      return;
    }
    let player = GameInstance.GetPlayerSystem(game).GetLocalPlayerMainGameObject();
    if !IsDefined(player) {
      return;
    }
    let ts = GameInstance.GetTransactionSystem(game);
    if IsDefined(ts) {
      ts.GiveItem(player, MarketSystem.Money(), Cast<Int32>(amount));
    }
  }
}

@wrapMethod(ScriptedPuppet)
protected func OnDied() -> Void {
  wrappedMethod();
  let sys = GameInstance
    .GetScriptableSystemsContainer(this.GetGame())
    .Get(n"NeonAscendancy.Gameplay.NeonAscendancy_AscendancySystem") as NeonAscendancy_AscendancySystem;
  if IsDefined(sys) {
    sys.OnNpcIncapacitated(this);
  }
}

@wrapMethod(ScriptedPuppet)
protected cb func OnDefeated(evt: ref<DefeatedEvent>) -> Bool {
  const res = wrappedMethod(evt);
  let sys = GameInstance
    .GetScriptableSystemsContainer(this.GetGame())
    .Get(n"NeonAscendancy.Gameplay.NeonAscendancy_AscendancySystem") as NeonAscendancy_AscendancySystem;
  if IsDefined(sys) {
    sys.OnNpcIncapacitated(this);
  }
  return res;
}

