module NeonAscendancy.Core

// Native RTTI bindings exported by NeonAscendancy.dll (RED4ext + RedLib).
public native func NcCoreVersion() -> String;

public native func NcPopHudNotice() -> String;

public native func NcEvaluateSanitizer(factBits: Uint32, enabled: Bool) -> Uint32;

public native func NcGetEraName(eraCode: Int32) -> String;

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

public native func NcGetControlCenterCount() -> Int32;

public native func NcGetControlCenterSubTerritoryId(index: Int32) -> Int32;

public native func NcGetControlCenterId(index: Int32) -> Int32;

public native func NcGetControlCenterX(index: Int32) -> Float;

public native func NcGetControlCenterY(index: Int32) -> Float;

public native func NcGetControlCenterZ(index: Int32) -> Float;

public native func NcGetSubTerritoryOwner(subTerritoryId: Int32) -> Int32;

public native func NcGetFactionColorRgba(factionId: Int32) -> Uint32;

public native func NcGetControlCenterTooltipTitle(subTerritoryId: Int32) -> String;

public native func NcGetControlCenterTooltipDesc(subTerritoryId: Int32) -> String;

public native func NcLookupSubTerritoryAt(x: Float, y: Float) -> Int32;

public native func NcFindBestSubTerritoryAt(x: Float, y: Float) -> Int32;

public native func NcHasPlayerOrg() -> Bool;

public native func NcGetPlayerOrgName() -> String;

public native func NcGetPlayerOwnedCount() -> Int32;

public native func NcGetPlayerCycleIncome() -> Int64;

public native func NcGetPlayerTreasury() -> Int64;

public native func NcFoundGang(displayName: String, homeSubTerritoryId: Int32, gameSeconds: Int32) -> Int32;

public native func NcOfferCombatMission(
  subTerritoryId: Int32,
  controlCenterId: Int32,
  rewardEddies: Int32,
  gameSeconds: Int32
) -> Int32;

public native func NcOfferNearestRivalMission(x: Float, y: Float, gameSeconds: Int32) -> Int32;

public native func NcCompleteMission(missionId: Int32, gameSeconds: Int32) -> Int64;

public native func NcOnNpcIncapacitated(
  entityHash: Uint64,
  affiliationEnum: Int32,
  isCrowd: Bool,
  isCivilian: Bool,
  isVendor: Bool,
  isHostile: Bool,
  x: Float,
  y: Float,
  z: Float,
  gameSeconds: Int32
) -> Int64;

public native func NcAdvanceTime(currentGameSeconds: Int32) -> Int64;

public native func NcGetActiveMissionId() -> Int32;

public native func NcGetActiveMissionSubTerritoryId() -> Int32;

public native func NcGetActiveMissionTargetX() -> Float;

public native func NcGetActiveMissionTargetY() -> Float;

public native func NcGetActiveMissionTargetZ() -> Float;

public native func NcGetPauseMenuActionCode(ascendancyEnabled: Bool) -> Int32;

public native func NcGetPauseMenuLabel(ascendancyEnabled: Bool) -> String;

public native func NcFormatStatusSummary() -> String;

