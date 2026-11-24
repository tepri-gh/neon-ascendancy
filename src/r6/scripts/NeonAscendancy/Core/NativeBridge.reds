module NeonAscendancy.Core

// Native RTTI bindings exported by NeonAscendancy.dll (RED4ext + RedLib).
public native func NcCoreVersion() -> String;

public native func NcSessionBegin(
  schemaVersion: Int32,
  idHi: Uint32,
  idLo: Uint32,
  anchorRevision: Int32,
  gameSeconds: Int32
) -> Int32;

public native func NcSessionGetPlaythroughIdHi() -> Uint32;

public native func NcSessionGetPlaythroughIdLo() -> Uint32;

public native func NcSessionCurrentRevision() -> Int32;

public native func NcSessionEnd() -> Bool;

public native func NcLookupSubTerritoryAt(x: Float, y: Float) -> Int32;

public native func NcFoundGang(displayName: String, homeSubTerritoryId: Int32, gameSeconds: Int32) -> Int32;

public native func NcOfferCombatMission(
  subTerritoryId: Int32,
  controlCenterId: Int32,
  rewardEddies: Int32,
  gameSeconds: Int32
) -> Int32;

public native func NcCompleteMission(missionId: Int32, gameSeconds: Int32) -> Int64;

public native func NcAdvanceTime(currentGameSeconds: Int32) -> Int64;

