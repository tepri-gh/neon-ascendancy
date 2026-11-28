module NeonAscendancy.Dev

import NeonAscendancy.Core.*

public class NeonAscendancy_SpikeResult extends ScriptableSystemRequest {
  public let result: SpawnRequestResult;
}

public class NeonAscendancy_SpikeTimer extends DelayCallback {
  public let system: wref<NeonAscendancy_GarrisonSpike>;
  public let phase: Int32;

  public func Call() -> Void {
    if IsDefined(this.system) {
      this.system.Check(this.phase);
    }
  }
}

public class NeonAscendancy_GarrisonSpike extends ScriptableSystem {
  private let logs: array<String>;
  private let requests: array<Uint32>;
  private let records: array<TweakDBID>;
  private let units: array<wref<GameObject>>;
  private let before: Float;
  private let healthA: Float;
  private let healthB: Float;
  private let patrolOrigin: Vector4;
  private let patrolPoint: Int32;
  private let patrolSeconds: Int32;
  private let boss: EntityID;
  private let hookFired: Bool;
  private let lift: wref<LiftDevice>;
  private let liftFloor: Int32;
  private let liftCall: Int32;
  private let liftWait: Int32;
  private let liftRequests: array<Uint32>;
  private let liftUnits: array<wref<GameObject>>;
  private let liftStart: array<Float>;

  private func Log(line: String) -> Void {
    NcLogInfo(line);
    ArrayPush(this.logs, line);
  }

  public func LogCount() -> Int32 {
    return ArraySize(this.logs);
  }

  public func LogAt(i: Int32) -> String {
    if i >= 0 && i < ArraySize(this.logs) {
      return this.logs[i];
    }
    return "";
  }

  private func Timer(phase: Int32, seconds: Float) -> Void {
    let cb = new NeonAscendancy_SpikeTimer();
    cb.system = this;
    cb.phase = phase;
    GameInstance
      .GetDelaySystem(this.GetGameInstance())
      .DelayCallback(cb, seconds, false);
  }

  public func Q1() -> Void {
    let player = GameInstance
      .GetPlayerSystem(this.GetGameInstance())
      .GetLocalPlayerMainGameObject();
    if !IsDefined(player) {
      this.Log("GarrisonSpike: Q1 FAIL player unavailable");
      return;
    }
    let pos = player.GetWorldPosition() + player.GetWorldForward() * 6.0;
    let transform: WorldTransform;
    WorldTransform.SetPosition(transform, pos);
    WorldTransform.SetOrientationFromDir(transform, player.GetWorldForward());
    let spawn = GameInstance.GetPreventionSpawnSystem(this.GetGameInstance());
    let a = t"NeonAscendancy.GarrisonSpikeGuard";
    let b = t"Character.maelstrom_fast_franged2_pulsar_ma_rare";
    ArrayPush(this.requests, spawn.RequestUnitSpawn(a, transform));
    ArrayPush(this.records, a);
    ArrayPush(this.requests, spawn.RequestUnitSpawn(b, transform));
    ArrayPush(this.records, b);
    this
      .Log(
        s"GarrisonSpike: Q1 UNKNOWN requested ids=\(this.requests[ArraySize(this.requests) - 2]),\(this.requests[ArraySize(this.requests) - 1])"
      );
    this.Timer(10, 10.0);
    this.Timer(15, 15.0);
  }

  public func Owns(id: Uint32) -> Bool {
    return ArrayContains(this.requests, id);
  }

  private func OnNeonAscendancy_SpikeResult(req: ref<NeonAscendancy_SpikeResult>) -> Void {
    let i = ArrayFindFirst(this.requests, req.result.requestID);
    if i < 0 {
      return;
    }
    let record = this.records[i];
    ArrayErase(this.requests, i);
    ArrayErase(this.records, i);
    if !req.result.success || ArraySize(req.result.spawnedObjects) == 0 {
      this
        .Log(
          s"GarrisonSpike: Q1 FAIL request=\(req.result.requestID) record=\(record) success=\(req.result.success) objects=\(ArraySize(req.result.spawnedObjects))"
        );
      return;
    }
    for unit in req.result.spawnedObjects {
      if IsDefined(unit) {
        ArrayPush(this.units, unit);
        if ArrayContains(this.liftRequests, req.result.requestID) {
          ArrayPush(this.liftUnits, unit);
        }
        this
          .Log(s"GarrisonSpike: Q1 PASS id=\(unit.GetEntityID()) record=\(record)");
      }
    }
  }

  public func Q2() -> Void {
    if ArraySize(this.units) == 0 || !IsDefined(this.units[0]) {
      this.Log("GarrisonSpike: Q2 UNKNOWN no unit");
      return;
    }
    let id = Cast<StatsObjectID>(this.units[0].GetEntityID());
    let stats = GameInstance.GetStatsSystem(this.GetGameInstance());
    this.before = stats.GetStatValue(id, gamedataStatType.PowerLevel);
    stats.RemoveAllModifiers(id, gamedataStatType.PowerLevel);
    stats
      .AddModifier(
        id,
        RPGManager
          .CreateStatModifier(gamedataStatType.PowerLevel, gameStatModifierType.Additive, 14.0)
      );
    this.Timer(2, 1.0);
  }

  public func Q3() -> Void {
    this.Log("GarrisonSpike: Q3 UNKNOWN no workspot ref");
    if ArraySize(this.units)
      < 2
      || !IsDefined(this.units[0])
      || !IsDefined(this.units[1]) {
      this.Log("GarrisonSpike: Q3 UNKNOWN need two units");
      return;
    }
    let a = this.units[0];
    let b = this.units[1];
    let player = GameInstance
      .GetPlayerSystem(this.GetGameInstance())
      .GetLocalPlayerMainGameObject();
    this
      .Log(
        s"GarrisonSpike: Q3 UNKNOWN attitudes to V=\(EnumInt(a.GetAttitudeTowards(player))),\(EnumInt(b.GetAttitudeTowards(player)))"
      );
    this.patrolOrigin = a.GetWorldPosition();
    this.patrolPoint = 0;
    this.patrolSeconds = 0;
    this.MovePatrol();
    this.Timer(30, 1.0);
  }

  private func StartCombat() -> Void {
    if ArraySize(this.units)
      < 2
      || !IsDefined(this.units[0])
      || !IsDefined(this.units[1]) {
      this.Log("GarrisonSpike: Q3 UNKNOWN combat units unavailable");
      return;
    }
    let a = this.units[0];
    let b = this.units[1];
    this.healthA = this.Health(a);
    this.healthB = this.Health(b);
    a
      .GetAttitudeAgent()
      .SetAttitudeTowards(b.GetAttitudeAgent(), EAIAttitude.AIA_Hostile);
    b
      .GetAttitudeAgent()
      .SetAttitudeTowards(a.GetAttitudeAgent(), EAIAttitude.AIA_Hostile);
    a
      .GetTargetTrackerComponent()
      .AddThreat(b, true, b.GetWorldPosition(), 1.0, -1.0, false);
    b
      .GetTargetTrackerComponent()
      .AddThreat(a, true, a.GetWorldPosition(), 1.0, -1.0, false);
    this.Timer(3, 60.0);
  }

  private func PatrolTarget() -> Vector4 {
    let pos = this.patrolOrigin;
    if this.patrolPoint == 0 {
      pos.X += 8.0;
    }
    if this.patrolPoint == 1 {
      pos.X -= 4.0;
      pos.Y += 6.928;
    }
    if this.patrolPoint == 2 {
      pos.X -= 4.0;
      pos.Y -= 6.928;
    }
    return pos;
  }

  private func Move(unit: ref<GameObject>, pos: Vector4) -> Void {
    let puppet = unit as ScriptedPuppet;
    if !IsDefined(puppet) {
      return;
    }
    let wp: WorldPosition;
    WorldPosition.SetVector4(wp, pos);
    let spec: AIPositionSpec;
    AIPositionSpec.SetWorldPosition(spec, wp);
    let command = new AIMoveToCommand();
    command.movementTarget = spec;
    command.finishWhenDestinationReached = true;
    command.desiredDistanceFromTarget = 1.0;
    puppet.GetAIControllerComponent().SendCommand(command);
  }

  private func MovePatrol() -> Void {
    this.Move(this.units[0], this.PatrolTarget());
  }

  public func Q5() -> Void {
    if ArraySize(this.units) == 0 || !IsDefined(this.units[0]) {
      this.Log("GarrisonSpike: Q5 UNKNOWN no unit");
      return;
    }
    this.boss = this.units[0].GetEntityID();
    this.hookFired = false;
    this.Log("GarrisonSpike: Q5 UNKNOWN check the scanner hookFired=false");
  }

  public func IsBoss(id: EntityID) -> Bool {
    return id == this.boss;
  }

  public func NameFired() -> Void {
    if !this.hookFired {
      this.hookFired = true;
      this.Log("GarrisonSpike: Q5 UNKNOWN check the scanner hookFired=true");
    }
  }

  public func CaptureLift(lift: ref<LiftDevice>) -> Void {
    this.lift = lift;
    if !IsDefined(lift) {
      this.Log("GarrisonSpike: Q4 UNKNOWN no lift found");
      return;
    }
    let ps = lift.GetDevicePS();
    let floors = ps.GetFloors();
    this
      .Log(
        s"GarrisonSpike: Q4 UNKNOWN lift=\(lift.GetEntityID()) floor=\(ps.GetActiveFloor()) count=\(ArraySize(floors))"
      );
  }

  // Calls the cab to callFloor (where the owner stands), boards the four
  // units once it has stopped there, then rides to floor and measures.
  public func LiftRide(callFloor: Int32, floor: Int32) -> Void {
    if !IsDefined(this.lift) {
      this.Log("GarrisonSpike: Q4 UNKNOWN capture lift first");
      return;
    }
    this.liftFloor = floor;
    this.liftCall = callFloor;
    this.liftWait = 0;
    ArrayClear(this.liftUnits);
    ArrayClear(this.liftRequests);
    let player = GameInstance
      .GetPlayerSystem(this.GetGameInstance())
      .GetLocalPlayerMainGameObject();
    if !IsDefined(player) {
      this.Log("GarrisonSpike: Q4 UNKNOWN no player");
      return;
    }
    let pos = player.GetWorldPosition() - player.GetWorldForward() * 2.0;
    let transform: WorldTransform;
    WorldTransform.SetPosition(transform, pos);
    let spawn = GameInstance.GetPreventionSpawnSystem(this.GetGameInstance());
    let i = 0;
    while i < 4 {
      let record = t"NeonAscendancy.GarrisonSpikeGuard";
      let id = spawn.RequestUnitSpawn(record, transform);
      ArrayPush(this.requests, id);
      ArrayPush(this.liftRequests, id);
      ArrayPush(this.records, record);
      i += 1;
    }
    this.GoToFloor(callFloor);
    this
      .Log(
        s"GarrisonSpike: Q4 UNKNOWN requested four units; cab called to floor \(callFloor)"
      );
    this.Timer(39, 2.0);
  }

  private func GoToFloor(floor: Int32) -> Void {
    let action = this.lift.GetDevicePS().ActionQuestForceGoToFloor();
    action.SetProperties(floor);
    this.lift.QueueEvent(action);
  }

  // True once the cab has stopped at floor; logs FAIL after 30 s.
  private func CabAt(floor: Int32, phase: Int32) -> Bool {
    let ps = this.lift.GetDevicePS();
    if !ps.IsMoving() && ps.GetActiveFloor() == floor {
      this.liftWait = 0;
      return true;
    }
    this.liftWait += 1;
    if this.liftWait >= 30 {
      this
        .Log(
          s"GarrisonSpike: Q4 FAIL cab not at floor \(floor) after 30s (active=\(ps.GetActiveFloor()) moving=\(ps.IsMoving()))"
        );
      this.liftWait = 0;
      return false;
    }
    this.Timer(phase, 1.0);
    return false;
  }

  private func Health(unit: ref<GameObject>) -> Float {
    return GameInstance
      .GetStatPoolsSystem(this.GetGameInstance())
      .GetStatPoolValue(Cast<StatsObjectID>(unit.GetEntityID()), gamedataStatPoolType.Health, false);
  }

  public func Check(phase: Int32) -> Void {
    if phase == 30 && ArraySize(this.units) > 0 && IsDefined(this.units[0]) {
      this.patrolSeconds += 1;
      if Vector4.Distance(this.units[0].GetWorldPosition(), this.PatrolTarget()) <= 1.5 {
        this.patrolPoint += 1;
        this.patrolSeconds = 0;
        if this.patrolPoint == 3 {
          this.Log("GarrisonSpike: Q3 PASS patrol reached three points");
          this.StartCombat();
        } else {
          this.MovePatrol();
          this.Timer(30, 1.0);
        }
      } else {
        if this.patrolSeconds >= 20 {
          this
            .Log(
              s"GarrisonSpike: Q3 FAIL patrol point=\(this.patrolPoint) distance=\(Vector4
                .Distance(this.units[0].GetWorldPosition(), this.PatrolTarget()))"
            );
          this.StartCombat();
        } else {
          this.Timer(30, 1.0);
        }
      }
    }
    if phase == 39 && IsDefined(this.lift) && this.CabAt(this.liftCall, 39) {
      this.Timer(40, 1.5);
    }
    if phase == 40 && IsDefined(this.lift) {
      ArrayClear(this.liftStart);
      for unit in this.liftUnits {
        if IsDefined(unit) {
          let pos = unit.GetWorldPosition();
          ArrayPush(this.liftStart, pos.Z);
          this.Move(unit, this.lift.GetWorldPosition());
        }
      }
      this.Timer(41, 8.0);
    }
    if phase == 41 && IsDefined(this.lift) {
      let cab = this.lift.GetWorldPosition();
      let aboard = 0;
      for unit in this.liftUnits {
        if IsDefined(unit) && Vector4.Distance2D(unit.GetWorldPosition(), cab) <= 2.5 {
          aboard += 1;
        }
      }
      this
        .Log(
          s"GarrisonSpike: Q4 UNKNOWN boarded=\(aboard) of \(ArraySize(this.liftUnits)); riding to floor \(this.liftFloor)"
        );
      this.GoToFloor(this.liftFloor);
      this.Timer(43, 2.0);
    }
    if phase == 43 && IsDefined(this.lift) && this.CabAt(this.liftFloor, 43) {
      this.Timer(42, 3.0);
    }
    if phase == 42 {
      let moved = 0;
      let i = 0;
      for unit in this.liftUnits {
        if IsDefined(unit) && i < ArraySize(this.liftStart) {
          let pos = unit.GetWorldPosition();
          let dz = pos.Z - this.liftStart[i];
          if AbsF(dz) > 2.5 {
            moved += 1;
          }
          this
            .Log(s"GarrisonSpike: Q4 UNKNOWN unit=\(unit.GetEntityID()) dz=\(dz)");
          i += 1;
        }
      }
      if moved >= 3 {
        this.Log(s"GarrisonSpike: Q4 PASS moved=\(moved)");
      } else {
        this.Log(s"GarrisonSpike: Q4 FAIL moved=\(moved)");
      }
    }
    if phase == 10 {
      let prevention = GameInstance
        .GetScriptableSystemsContainer(this.GetGameInstance())
        .Get(n"PreventionSystem") as PreventionSystem;
      if IsDefined(prevention) {
        this
          .Log(s"GarrisonSpike: Q1 UNKNOWN wanted=\(prevention.GetHeatStageAsInt())");
      }
      this
        .Log(
          s"GarrisonSpike: Q1 UNKNOWN crowd=\(GameInstance
            .GetPreventionSpawnSystem(this.GetGameInstance())
            .GetPreventionSystemCanSpawnInCrowd())"
        );
    }
    if phase == 15 && ArraySize(this.requests) > 0 {
      this
        .Log(s"GarrisonSpike: Q1 FAIL pending=\(ArraySize(this.requests)) after 15s");
    }
    if phase == 2 && ArraySize(this.units) > 0 && IsDefined(this.units[0]) {
      let after = GameInstance
        .GetStatsSystem(this.GetGameInstance())
        .GetStatValue(
          Cast<StatsObjectID>(this.units[0].GetEntityID()),
          gamedataStatType.PowerLevel
        );
      if AbsF(after - 14.0) <= 1.0 {
        this
          .Log(s"GarrisonSpike: Q2 PASS before=\(this.before) after=\(after)");
      } else {
        this
          .Log(s"GarrisonSpike: Q2 FAIL before=\(this.before) after=\(after)");
      }
    }
    if phase
      == 3
      && ArraySize(this.units) >= 2
      && IsDefined(this.units[0])
      && IsDefined(this.units[1]) {
      let a = this.Health(this.units[0]);
      let b = this.Health(this.units[1]);
      if a < this.healthA || b < this.healthB {
        this
          .Log(
            s"GarrisonSpike: Q3 PASS combat health=\(this.healthA)->\(a),\(this.healthB)->\(b)"
          );
      } else {
        this
          .Log(
            s"GarrisonSpike: Q3 FAIL combat health=\(this.healthA)->\(a),\(this.healthB)->\(b)"
          );
      }
    }
  }

  public func Cleanup() -> Void {
    let spawn = GameInstance.GetPreventionSpawnSystem(this.GetGameInstance());
    for id in this.requests {
      spawn.CancelSpawnRequest(id);
    }
    let count = 0;
    for unit in this.units {
      if IsDefined(unit) {
        spawn.RequestDespawn(unit.GetEntityID());
        count += 1;
      }
    }
    ArrayClear(this.requests);
    ArrayClear(this.records);
    ArrayClear(this.units);
    this.Log(s"GarrisonSpike: Q1 UNKNOWN cleanup requested count=\(count)");
  }
}

@wrapMethod(PreventionSpawnSystem)
protected final func SpawnRequestFinished(requestResult: SpawnRequestResult) -> Void {
  let system = GameInstance
    .GetScriptableSystemsContainer(GetGameInstance())
    .Get(n"NeonAscendancy.Dev.NeonAscendancy_GarrisonSpike") as NeonAscendancy_GarrisonSpike;
  if IsDefined(system) && system.Owns(requestResult.requestID) {
    let req = new NeonAscendancy_SpikeResult();
    req.result = requestResult;
    system.QueueRequest(req);
    return;
  }
  wrappedMethod(requestResult);
}

@wrapMethod(NPCPuppet)
public const func CompileScannerChunks() -> Bool {
  let result = wrappedMethod();
  let system = GameInstance
    .GetScriptableSystemsContainer(this.GetGame())
    .Get(n"NeonAscendancy.Dev.NeonAscendancy_GarrisonSpike") as NeonAscendancy_GarrisonSpike;
  if IsDefined(system) && system.IsBoss(this.GetEntityID()) {
    let chunk = new ScannerName();
    chunk.Set("NA Spike Boss (Lieutenant)");
    let bb = GameInstance
      .GetBlackboardSystem(this.GetGame())
      .Get(GetAllBlackboardDefs().UI_ScannerModules);
    if IsDefined(bb) {
      bb
        .SetVariant(GetAllBlackboardDefs().UI_ScannerModules.ScannerName, ToVariant(chunk));
      system.NameFired();
    }
  }
  return result;
}

