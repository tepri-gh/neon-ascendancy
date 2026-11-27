module NeonAscendancy.World

import NeonAscendancy.Core.*

// Clears a dead quest marking on listed devices (data/venues/device_quest_marks.json,
// generated into NeonAscendancy_DeviceQuestMarkClears). Some devices ship with
// markAsQuest and personalLinkForced baked for a gig step the clean slate never
// runs: the Botanic Gardens access point showed a yellow icon and jacking in
// froze V (tour 2026-11-26). Gated by na_door_policy, like the door policy.
public class NeonAscendancy_DeviceQuestMarkSystem extends ScriptableSystem {
  private let m_ids: array<String>;
  private let m_built: Bool;

  public func IsListed(id: EntityID) -> Bool {
    if !this.m_built {
      this.m_ids = NeonAscendancy_DeviceQuestMarkClears();
      this.m_built = true;
    }
    return ArraySize(this.m_ids)
      > 0
      && ArrayContains(this.m_ids, EntityID.ToDebugStringDecimal(id));
  }
}

@addMethod(ScriptableDeviceComponentPS)
public func NeonAscendancy_QueueDisconnectPersonalLink() -> Void {
  this
    .GetPersistencySystem()
    .QueuePSDeviceEvent(this.ActionQuestForceDisconnectPersonalLink());
}

@wrapMethod(Device)
protected cb func OnGameAttached() -> Bool {
  const res = wrappedMethod();
  const game = this.GetGame();
  if !NeonAscendancy_DoorPolicyEnabled(game) {
    return res;
  }
  let sys = GameInstance
    .GetScriptableSystemsContainer(game)
    .Get(n"NeonAscendancy.World.NeonAscendancy_DeviceQuestMarkSystem") as NeonAscendancy_DeviceQuestMarkSystem;
  if !IsDefined(sys) || !sys.IsListed(this.GetEntityID()) {
    return res;
  }
  // ToggleQuestImportance clears the mark and refreshes the HUD icon.
  this.ToggleQuestImportance(false);
  let ps = this.GetDevicePS();
  if IsDefined(ps) {
    ps.NeonAscendancy_QueueDisconnectPersonalLink();
  }
  NcLogInfo(
    s"DeviceQuestMark: cleared id=\(EntityID.ToDebugStringDecimal(this.GetEntityID()))"
  );
  return res;
}

