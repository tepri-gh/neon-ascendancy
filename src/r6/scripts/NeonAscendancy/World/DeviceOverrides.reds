module NeonAscendancy.World

import NeonAscendancy.Core.*

// Device-level rules for devices whose vanilla state belongs to a quest the
// clean slate never runs. Gated by na_door_policy, like the door policy.
//
// - Lifts work (owner decision 58, 2026-11-27): every lift car
//   (LiftDevice) and floor terminal (ElevatorFloorTerminal) is enabled and
//   powered, and its authorization is turned off, so every floor it serves
//   is open. Floor access comes from the floor terminals
//   (LiftControllerPS.GetFloorAuthorizationFromSlaves). The only exceptions
//   are lift groups in places sealed for lore (excluded and deferred venues,
//   data/venues/lift_exclusions.json), listed in
//   NeonAscendancy_LiftExclusions. Their lift doors follow the door policy
//   (DoorPolicy.reds).
// - Quest marks (data/venues/device_quest_marks.json): some devices ship with
//   markAsQuest and personalLinkForced baked for a gig step; the Botanic
//   Gardens access point showed a yellow icon and jacking in froze V (tour
//   2026-11-26).
public class NeonAscendancy_DeviceOverrideSystem extends ScriptableSystem {
  private let m_questMarks: array<String>;
  private let m_liftExclusions: array<String>;
  private let m_built: Bool;

  private func Build() -> Void {
    if !this.m_built {
      this.m_questMarks = NeonAscendancy_DeviceQuestMarkClears();
      this.m_liftExclusions = NeonAscendancy_LiftExclusions();
      this.m_built = true;
    }
  }

  public func ClearsQuestMark(id: String) -> Bool {
    this.Build();
    return ArrayContains(this.m_questMarks, id);
  }

  public func LiftExcluded(id: String) -> Bool {
    this.Build();
    return ArrayContains(this.m_liftExclusions, id);
  }
}

@addMethod(ScriptableDeviceComponentPS)
public func NeonAscendancy_QueueDisconnectPersonalLink() -> Void {
  this
    .GetPersistencySystem()
    .QueuePSDeviceEvent(this.ActionQuestForceDisconnectPersonalLink());
}

// The quest actions vanilla phases queue on lifts, in their order. ForceON
// matters: a car only moves when it is ON (LiftControllerPS GoToFloor fails
// "Unpowered, Disabled or Off"), and ForceEnabled on a disabled car leaves it
// OFF, which ForcePower then skips as already powered. Each handler is a
// no-op when the device is already in that state, so this is idempotent
// across reattaches and save loads.
@addMethod(ScriptableDeviceComponentPS)
public func NeonAscendancy_QueueLiftAccess() -> Void {
  let ps = this.GetPersistencySystem();
  ps.QueuePSDeviceEvent(this.ActionQuestForceEnabled());
  ps.QueuePSDeviceEvent(this.ActionQuestForcePower());
  ps.QueuePSDeviceEvent(this.ActionQuestForceON());
  ps.QueuePSDeviceEvent(this.ActionQuestForceAuthorizationDisabled());
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
  let ps = this.GetDevicePS();
  if !IsDefined(sys) || !IsDefined(ps) {
    return res;
  }
  const id = EntityID.ToDebugStringDecimal(this.GetEntityID());
  if sys.ClearsQuestMark(id) {
    // ToggleQuestImportance clears the mark and refreshes the HUD icon.
    this.ToggleQuestImportance(false);
    ps.NeonAscendancy_QueueDisconnectPersonalLink();
    NcLogInfo(s"DeviceOverride: quest mark cleared id=\(id)");
  }
  const lift = IsDefined(this as LiftDevice) || IsDefined(this as ElevatorFloorTerminal);
  if lift && (!ps.IsON() || ps.IsAuthorizationModuleOn()) {
    if sys.LiftExcluded(id) {
      NcLogInfo(s"LiftPolicy: id=\(id) excluded (lore-sealed area), kept vanilla");
    } else {
      const pos = this.GetWorldPosition();
      NcLogInfo(
        s"LiftPolicy: id=\(id) pos=(\(pos.X),\(pos.Y),\(pos.Z)) disabled=\(ps.IsDisabled()) unpowered=\(ps.IsUnpowered()) on=\(ps.IsON()) authorization=\(ps.IsAuthorizationModuleOn())"
      );
      ps.NeonAscendancy_QueueLiftAccess();
    }
  }
  return res;
}

