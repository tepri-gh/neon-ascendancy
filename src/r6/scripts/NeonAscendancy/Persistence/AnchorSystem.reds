module NeonAscendancy.Persistence

import NeonAscendancy.Core.*

// 20-byte durable revision-watermark anchor persisted per save file.
// Never store large simulation tables here; external SQLite checkpoints are
// keyed by (m_playthroughIdHi, m_playthroughIdLo, m_saveGeneration).
public class NeonAscendancy_AnchorSystem extends ScriptableSystem {
  private persistent let m_schemaVersion: Int32;
  private persistent let m_playthroughIdHi: Uint32;
  private persistent let m_playthroughIdLo: Uint32;
  private persistent let m_saveGeneration: Int32;
  private persistent let m_flags: Uint32;
  private let m_sessionReady: Bool;
  private let m_playerAttachedCallbackId: Uint32;

  public func OnAttach() -> Void {
    // Only open a fresh session once a real PlayerPuppet attaches in-world
    // (avoids creating an empty playthrough DB on the main menu / char creator).
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
    this.BeginNativeSession();
  }

  public func OnDetach() -> Void {
    const game = this.GetGameInstance();
    if this.m_playerAttachedCallbackId > 0u && GameInstance.IsValid(game) {
      GameInstance
        .GetPlayerSystem(game)
        .UnregisterPlayerPuppetAttachedCallback(this.m_playerAttachedCallbackId);
      this.m_playerAttachedCallbackId = 0u;
    }
    if this.m_sessionReady {
      NcSessionEnd();
      this.m_sessionReady = false;
    }
  }

  private final func OnPlayerAttachedCallback(playerPuppet: ref<GameObject>) -> Void {
    if IsDefined(playerPuppet) && !this.m_sessionReady {
      this.BeginNativeSession();
    }
  }

  public final func EnsureSessionInitialized() -> Void {
    if !this.m_sessionReady {
      this.BeginNativeSession();
    }
  }

  public const final func IsSessionReady() -> Bool {
    return this.m_sessionReady;
  }

  public const final func GetDurableRevision() -> Int32 {
    return this.m_saveGeneration;
  }

  public final func SyncPublishedRevision() -> Void {
    if !this.m_sessionReady {
      return;
    }
    const rev = NcSessionCurrentRevision();
    if rev > 0 {
      this.m_saveGeneration = rev;
    }
  }

  private final func BeginNativeSession() -> Void {
    const game = this.GetGameInstance();
    if !GameInstance.IsValid(game) {
      return;
    }
    const gameSeconds = GameTime.GetSeconds(GameInstance.GetTimeSystem(game).GetGameTime());
    const rev = NcSessionBegin(
      this.m_schemaVersion,
      this.m_playthroughIdHi,
      this.m_playthroughIdLo,
      this.m_saveGeneration,
      gameSeconds
    );
    if rev < 0 {
      this.m_sessionReady = false;
      return;
    }
    this.m_schemaVersion = NeonAscendancy_SchemaVersion();
    this.m_playthroughIdHi = NcSessionGetPlaythroughIdHi();
    this.m_playthroughIdLo = NcSessionGetPlaythroughIdLo();
    this.m_saveGeneration = rev;
    this.m_sessionReady = true;
  }
}

