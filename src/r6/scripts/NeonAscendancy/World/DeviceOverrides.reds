module NeonAscendancy.World

import NeonAscendancy.Core.*

// Per-device fixes for devices whose vanilla state belongs to a quest the
// clean slate never runs, listed by entity id in data/venues/ and generated
// into DoorScope.reds. Gated by na_door_policy, like the door policy.
//
// - Quest marks (device_quest_marks.json): some devices ship with markAsQuest
//   and personalLinkForced baked for a gig step; the Botanic Gardens access
//   point showed a yellow icon and jacking in froze V (tour 2026-11-26).
// - Power (device_power_overrides.json): lifts and elevator floor terminals a
//   skipped phase would enable and power (the H10 apartment lift, the
//   netrunners' den lift; sweep 2026-11-27). Doors have their own policy
//   (DoorPolicy.reds); this is the same enable and power for the lift itself.
public class NeonAscendancy_DeviceOverrideSystem extends ScriptableSystem {
  private let m_questMarks: array<String>;
  private let m_power: array<String>;
  private let m_authorization: array<String>;
  private let m_built: Bool;

  private func Build() -> Void {
    if !this.m_built {
      this.m_questMarks = NeonAscendancy_DeviceQuestMarkClears();
      this.m_power = NeonAscendancy_DevicePowerOverrides();
      this.m_authorization = NeonAscendancy_DeviceAuthorizationOverrides();
      this.m_built = true;
    }
  }

  public func ClearsQuestMark(id: String) -> Bool {
    this.Build();
    return ArrayContains(this.m_questMarks, id);
  }

  public func Powers(id: String) -> Bool {
    this.Build();
    return ArrayContains(this.m_power, id);
  }

  public func DisablesAuthorization(id: String) -> Bool {
    this.Build();
    return ArrayContains(this.m_authorization, id);
  }
}

@addMethod(ScriptableDeviceComponentPS)
public func NeonAscendancy_QueueDisconnectPersonalLink() -> Void {
  this
    .GetPersistencySystem()
    .QueuePSDeviceEvent(this.ActionQuestForceDisconnectPersonalLink());
}

// The quest actions vanilla phases queue on these lifts, in their order. Each
// handler is a no-op when the device is already in that state, so this is
// idempotent across reattaches and save loads.
@addMethod(ScriptableDeviceComponentPS)
public func NeonAscendancy_QueuePowerUp(disableAuthorization: Bool) -> Void {
  let ps = this.GetPersistencySystem();
  ps.QueuePSDeviceEvent(this.ActionQuestForceEnabled());
  ps.QueuePSDeviceEvent(this.ActionQuestForcePower());
  if disableAuthorization {
    ps.QueuePSDeviceEvent(this.ActionQuestForceAuthorizationDisabled());
  }
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
    .Get(n"NeonAscendancy.World.NeonAscendancy_DeviceOverrideSystem") as NeonAscendancy_DeviceOverrideSystem;
  if !IsDefined(sys) {
    return res;
  }
  const id = EntityID.ToDebugStringDecimal(this.GetEntityID());
  let ps = this.GetDevicePS();
  if sys.ClearsQuestMark(id) {
    // ToggleQuestImportance clears the mark and refreshes the HUD icon.
    this.ToggleQuestImportance(false);
    if IsDefined(ps) {
      ps.NeonAscendancy_QueueDisconnectPersonalLink();
    }
    NcLogInfo(s"DeviceOverride: quest mark cleared id=\(id)");
  }
  if sys.Powers(id) && IsDefined(ps) {
    const auth = sys.DisablesAuthorization(id);
    NcLogInfo(
      s"DeviceOverride: power id=\(id) disabled=\(ps.IsDisabled()) unpowered=\(ps.IsUnpowered()) authorization=\(auth)"
    );
    ps.NeonAscendancy_QueuePowerUp(auth);
  }
  return res;
}
