module NeonAscendancy.World

import NeonAscendancy.Core.*

// Runtime door policy (docs/venue-playbook.md rule 12, owner policy
// 2026-11-25): doors are closed by default but usable. A door with an
// in-world way through (authorization such as a keycard, a lock the player
// can toggle, a skill check, a quickhack, or a terminal that controls it)
// keeps its vanilla lock. Otherwise the door is enabled, powered and, only if
// it would stay impassable, unlocked/unsealed. It is never opened.
//
// Scope: only doors vanilla quest phases drive (NeonAscendancy_DoorScopeHashes,
// generated from the venue catalogue). Set-dressing doors often open onto
// nothing. Gated by the na_door_policy fact (dev toggle first).
// What the policy needs to know about one door. Gathered from the live PS.
public struct NeonAscendancy_DoorFacts {
  public let disabled: Bool;
  public let unpowered: Bool;
  // DoorControllerPS.IsStatic(): sealed without a toggle, or locked with no
  // authorization, toggle, skill check or quickhack (doorController.swift).
  public let impassable: Bool;
  // A working keycard/password authorization or a controlling terminal: an
  // in-world way through that IsStatic() does not see. An authorization
  // module with no keycard or password configured is not a way in: it hid
  // Shank's and the Nighthawks safehouse doors (tour 2026-11-26).
  public let otherWayIn: Bool;
  public let locked: Bool;
  public let sealed: Bool;
  // An authorization module is on, valid or not.
  public let authorization: Bool;
  // A lift's own door: its lift and floor terminals open it, so the policy
  // only enables and powers it. Unlocking could leave it open on a floor the
  // car has left.
  public let liftDoor: Bool;
  // One side usable (interactive or automatic) and the other offering
  // nothing (none or remotely controlled): the door opens from one side only.
  public let oneSided: Bool;
  public let shutter: Bool;
  // Owner-flagged in data/venues/door_overrides.json: its other way in is not
  // obtainable in our timeline, so open it up regardless.
  public let overridden: Bool;
}

public struct NeonAscendancy_DoorDecision {
  public let enable: Bool;
  public let power: Bool;
  public let unlock: Bool;
  public let unseal: Bool;
  public let disableAuthorization: Bool;
  // Give both sides the usable side's type (owner overrides only).
  public let fixSides: Bool;
  // Re-evaluate the lock after enable/power lands: skill checks and quickhacks
  // only register on an enabled, powered device.
  public let recheck: Bool;
}

// Pure policy. Enabling and powering come first; the lock decision waits for
// a recheck whenever the device was disabled or unpowered.
public func NeonAscendancy_DecideDoor(f: NeonAscendancy_DoorFacts) -> NeonAscendancy_DoorDecision {
  let d: NeonAscendancy_DoorDecision;
  if f.disabled || f.unpowered {
    d.enable = f.disabled;
    d.power = f.unpowered;
    d.recheck = true;
    return d;
  }
  if f.overridden {
    // Never for shutters: one that is driven by an access point is
    // legitimately remote-only.
    d.fixSides = f.oneSided && !f.shutter;
    d.disableAuthorization = f.authorization;
    d.unlock = f.locked;
    d.unseal = f.sealed;
    return d;
  }
  // Owner overrides above still unlock a lift door (the Wellsprings lobby
  // lift); the general rule only enables and powers one.
  if f.liftDoor {
    return d;
  }
  if f.impassable {
    // A keycard, terminal or skill check gets past a lock, never a seal: only
    // quests unseal. So the other way in protects locks alone (Wilson's range
    // in H10 stayed sealed behind its auth module, tour 2026-11-26).
    d.unlock = f.locked && !f.otherWayIn;
    d.unseal = f.sealed;
  }
  return d;
}

public func NeonAscendancy_DescribeDoorDecision(d: NeonAscendancy_DoorDecision) -> String {
  if !d.enable
    && !d.power
    && !d.unlock
    && !d.unseal
    && !d.disableAuthorization
    && !d.fixSides {
    return "keep";
  }
  let parts = "";
  if d.enable {
    parts += "enable ";
  }
  if d.power {
    parts += "power ";
  }
  if d.unlock {
    parts += "unlock ";
  }
  if d.unseal {
    parts += "unseal ";
  }
  if d.disableAuthorization {
    parts += "authorize ";
  }
  if d.fixSides {
    parts += "sides ";
  }
  if d.recheck {
    parts += "recheck";
  }
  return parts;
}

// Holds the scope as engine entity-id hashes, built once from the generated
// node-path hashes.
public class NeonAscendancy_DoorPolicySystem extends ScriptableSystem {
  private let m_scope: array<Uint32>;
  private let m_built: Bool;
  private let m_overrides: array<String>;
  private let m_overridesBuilt: Bool;

  public func IsOverridden(id: EntityID) -> Bool {
    if !this.m_overridesBuilt {
      this.m_overrides = NeonAscendancy_DoorAccessOverrides();
      this.m_overridesBuilt = true;
    }
    return ArrayContains(this.m_overrides, EntityID.ToDebugStringDecimal(id));
  }

  public func InScope(id: EntityID) -> Bool {
    if !this.m_built {
      for h in NeonAscendancy_DoorScopeHashes() {
        ArrayPush(
          this.m_scope,
          EntityID.GetHash(Cast<EntityID>(NcResolveNodeRefByHash(h)))
        );
      }
      this.m_built = true;
    }
    return ArrayContains(this.m_scope, EntityID.GetHash(id));
  }
}

public func NeonAscendancy_DoorPolicyEnabled(game: GameInstance) -> Bool {
  if !GameInstance.IsValid(game) {
    return false;
  }
  let qs = GameInstance.GetQuestsSystem(game);
  return IsDefined(qs) && qs.GetFact(n"na_door_policy") > 0;
}

public class NeonAscendancy_DoorPolicyRecheck extends DelayCallback {
  // Strong for the one second until Call(): with a weak ref the PS was gone by
  // then and the re-check never ran (log 2026-11-26 08:11:27, enable without a
  // recheck=true line).
  public let m_ps: ref<DoorControllerPS>;
  public let m_pos: Vector4;
  public let m_overridden: Bool;

  public func Call() -> Void {
    let ps = this.m_ps;
    if IsDefined(ps) {
      ps.NeonAscendancy_ApplyDoorPolicy(true, this.m_pos, this.m_overridden);
    }
  }
}

@addMethod(DoorControllerPS)
public func NeonAscendancy_DoorFacts() -> NeonAscendancy_DoorFacts {
  let f: NeonAscendancy_DoorFacts;
  f.disabled = this.IsDisabled();
  f.unpowered = this.IsUnpowered();
  f.impassable = this.IsStatic();
  f.locked = this.IsLocked();
  f.sealed = this.IsSealed();
  f.authorization = this.IsAuthorizationModuleOn();
  f.otherWayIn = f.authorization && this.IsAuthorizationValid();
  f.liftDoor = this.IsLiftDoor();
  f.shutter = this.IsShutter();
  const one = NeonAscendancy_DoorSideUsable(this.GetDoorTypeSideOne());
  const two = NeonAscendancy_DoorSideUsable(this.GetDoorTypeSideTwo());
  f.oneSided = one != two;
  for parent in this.GetImmediateParents() {
    if IsDefined(parent as TerminalControllerPS) {
      f.otherWayIn = true;
    }
  }
  return f;
}

public func NeonAscendancy_DoorSideUsable(t: EDoorType) -> Bool {
  return Equals(t, EDoorType.INTERACTIVE) || Equals(t, EDoorType.AUTOMATIC);
}

// Evaluate and apply the policy through the same quest actions vanilla phases
// queue, so the entity and its notifier update normally. Idempotent: a door
// already enabled, powered and passable gets "keep".
@addMethod(DoorControllerPS)
public func NeonAscendancy_ApplyDoorPolicy(isRecheck: Bool, pos: Vector4, overridden: Bool) -> Void {
  let game = this.GetGameInstance();
  if !NeonAscendancy_DoorPolicyEnabled(game) {
    return;
  }
  let facts = this.NeonAscendancy_DoorFacts();
  facts.overridden = overridden;
  const d = NeonAscendancy_DecideDoor(facts);
  let ps = this.GetPersistencySystem();
  if d.enable {
    ps.QueuePSDeviceEvent(this.ActionQuestForceEnabled());
  }
  if d.power {
    ps.QueuePSDeviceEvent(this.ActionQuestForcePower());
  }
  if d.unlock {
    ps.QueuePSDeviceEvent(this.ActionQuestForceUnlock());
  }
  if d.unseal {
    ps.QueuePSDeviceEvent(this.ActionQuestForceUnseal());
  }
  if d.disableAuthorization {
    ps.QueuePSDeviceEvent(this.ActionQuestForceAuthorizationDisabled());
  }
  if d.fixSides {
    let sides = new SetDoorType();
    let usable = this.GetDoorTypeSideOne();
    if !NeonAscendancy_DoorSideUsable(usable) {
      usable = this.GetDoorTypeSideTwo();
    }
    sides.doorTypeSideOne = usable;
    sides.doorTypeSideTwo = usable;
    this.SetNewDoorType(sides);
  }
  if d.recheck && !isRecheck {
    let cb = new NeonAscendancy_DoorPolicyRecheck();
    cb.m_ps = this;
    cb.m_pos = pos;
    cb.m_overridden = overridden;
    GameInstance.GetDelaySystem(game).DelayCallback(cb, 1.0, false);
  }
  NcLogInfo(
    s"DoorPolicy: id=\(EntityID.ToDebugStringDecimal(PersistentID.ExtractEntityID(this.GetID()))) pos=(\(pos.X),\(pos.Y),\(pos.Z)) recheck=\(isRecheck) disabled=\(facts.disabled) unpowered=\(facts.unpowered) locked=\(facts.locked) sealed=\(facts.sealed) impassable=\(facts.impassable) otherWayIn=\(facts.otherWayIn) lift=\(facts.liftDoor) oneSided=\(facts.oneSided) override=\(facts.overridden) decision=\(NeonAscendancy_DescribeDoorDecision(d))"
  );
}

@wrapMethod(Door)
protected cb func OnGameAttached() -> Bool {
  const res = wrappedMethod();
  const game = this.GetGame();
  if !NeonAscendancy_DoorPolicyEnabled(game) {
    return res;
  }
  let sys = GameInstance
    .GetScriptableSystemsContainer(game)
    .Get(n"NeonAscendancy.World.NeonAscendancy_DoorPolicySystem") as NeonAscendancy_DoorPolicySystem;
  if !IsDefined(sys) {
    return res;
  }
  const overridden = sys.IsOverridden(this.GetEntityID());
  if !overridden && !sys.InScope(this.GetEntityID()) {
    return res;
  }
  let ps = this.GetDevicePS();
  if IsDefined(ps) {
    // The position lets the tour report attribute each decision to a venue.
    ps.NeonAscendancy_ApplyDoorPolicy(false, this.GetWorldPosition(), overridden);
  }
  return res;
}

