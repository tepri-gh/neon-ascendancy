module NeonAscendancy.Persistence

import NeonAscendancy.Core.*

private class NeonAscendancy_SessionInitCallback extends DelayCallback {
  public let m_system: wref<NeonAscendancy_AnchorSystem>;

  public func Call() -> Void {
    if IsDefined(this.m_system) {
      this.m_system.EnsureSessionInitialized();
    }
  }
}

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

  public func OnAttach() -> Void {
    // Defer initial session open by one tick so OnRestored (when loading a save)
    // always runs first with real persisted IDs instead of opening an orphan DB.
    const game = this.GetGameInstance();
    if GameInstance.IsValid(game) {
      let delaySystem = GameInstance.GetDelaySystem(game);
      if IsDefined(delaySystem) {
        let cb = new NeonAscendancy_SessionInitCallback();
        cb.m_system = this;
        delaySystem.DelayCallback(cb, 0.01, false);
      }
    }
  }

  public func OnRestored(saveVersion: Int32, gameVersion: Int32) -> Void {
    this.BeginNativeSession();
  }

  public func OnDetach() -> Void {
    if this.m_sessionReady {
      NcSessionEnd();
      this.m_sessionReady = false;
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

