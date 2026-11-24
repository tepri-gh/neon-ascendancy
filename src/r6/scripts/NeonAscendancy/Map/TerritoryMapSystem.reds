module NeonAscendancy.Map

import NeonAscendancy.Core.*

// Thin map adapter registering the 41 world.db control-center pins and the single
// active combat mission waypoint. All color/tooltip logic lives in C++.
public class NeonAscendancy_TerritoryMapSystem extends ScriptableSystem {
  private let m_pinsRegistered: Bool;
  private let m_pinIds: array<Uint64>;
  private let m_pinSubTerritories: array<Int32>;
  private let m_hasMissionPin: Bool;
  private let m_missionPinId: NewMappinID;
  private let m_missionPinSubTerritory: Int32;

  public func OnDetach() -> Void {
    this.ClearAllPins();
  }

  public final func SyncAllPins() -> Void {
    const game = this.GetGameInstance();
    if !GameInstance.IsValid(game) {
      return;
    }
    if !this.m_pinsRegistered {
      this.RegisterControlCenterPins(game);
    }
    this.SyncMissionWaypoint(game);
  }

  public final func SyncMissionWaypoint(game: GameInstance) -> Void {
    let ms = GameInstance.GetMappinSystem(game);
    if !IsDefined(ms) {
      return;
    }
    const activeId = NcGetActiveMissionId();
    const targetSt = NcGetActiveMissionSubTerritoryId();
    if activeId <= 0 || targetSt <= 0 {
      if this.m_hasMissionPin {
        ms.UnregisterMappin(this.m_missionPinId);
        this.m_hasMissionPin = false;
        this.m_missionPinSubTerritory = 0;
      }
      return;
    }
    if this.m_hasMissionPin && this.m_missionPinSubTerritory == targetSt {
      return;
    }
    if this.m_hasMissionPin {
      ms.UnregisterMappin(this.m_missionPinId);
      this.m_hasMissionPin = false;
    }
    let data: MappinData;
    data.mappinType = t"NeonAscendancy.MissionTargetMappin";
    data.variant = gamedataMappinVariant.DefaultQuestVariant;
    data.active = true;
    data.visibleThroughWalls = true;
    data.debugCaption = "NA_RAID";
    const pos = Vector4(
      NcGetActiveMissionTargetX(),
      NcGetActiveMissionTargetY(),
      NcGetActiveMissionTargetZ() + 1.5,
      1.0
    );
    this.m_missionPinId = ms.RegisterMappin(data, pos);
    this.m_missionPinSubTerritory = targetSt;
    this.m_hasMissionPin = true;
  }

  public final func ClearAllPins() -> Void {
    const game = this.GetGameInstance();
    if GameInstance.IsValid(game) {
      let ms = GameInstance.GetMappinSystem(game);
      if IsDefined(ms) {
        for rawId in this.m_pinIds {
          let id: NewMappinID;
          id.value = rawId;
          ms.UnregisterMappin(id);
        }
        if this.m_hasMissionPin {
          ms.UnregisterMappin(this.m_missionPinId);
        }
      }
    }
    ArrayClear(this.m_pinIds);
    ArrayClear(this.m_pinSubTerritories);
    this.m_pinsRegistered = false;
    this.m_hasMissionPin = false;
    this.m_missionPinSubTerritory = 0;
  }

  public const final func LookupSubTerritoryForMappin(id: NewMappinID) -> Int32 {
    if this.m_hasMissionPin && id.value == this.m_missionPinId.value {
      return this.m_missionPinSubTerritory;
    }
    let i = 0;
    const n = ArraySize(this.m_pinIds);
    while i < n {
      if this.m_pinIds[i] == id.value {
        return this.m_pinSubTerritories[i];
      }
      i += 1;
    }
    return 0;
  }

  public const final func IsOurMappin(id: NewMappinID) -> Bool {
    return this.LookupSubTerritoryForMappin(id) > 0;
  }

  private final func RegisterControlCenterPins(game: GameInstance) -> Void {
    let ms = GameInstance.GetMappinSystem(game);
    if !IsDefined(ms) {
      return;
    }
    const count = NcGetControlCenterCount();
    let i = 0;
    while i < count {
      const stId = NcGetControlCenterSubTerritoryId(i);
      if stId > 0 {
        let data: MappinData;
        data.mappinType = t"NeonAscendancy.ControlCenterMappin";
        data.variant = gamedataMappinVariant.DefaultQuestVariant;
        data.active = true;
        data.visibleThroughWalls = true;
        data.debugCaption = s"NA_CC_\(stId)";
        const pos = Vector4(
          NcGetControlCenterX(i),
          NcGetControlCenterY(i),
          NcGetControlCenterZ(i) + 1.0,
          1.0
        );
        const pinId = ms.RegisterMappin(data, pos);
        ArrayPush(this.m_pinIds, pinId.value);
        ArrayPush(this.m_pinSubTerritories, stId);
      }
      i += 1;
    }
    this.m_pinsRegistered = count > 0;
  }
}

@addField(BaseWorldMapMappinController)
private let NeonAscendancy_cachedOwner: Int32;

@wrapMethod(BaseWorldMapMappinController)
protected func UpdateIcon() -> Void {
  wrappedMethod();
  let mappin = this.GetMappin();
  if !IsDefined(mappin) {
    return;
  }
  const game = GetGameInstance();
  if !GameInstance.IsValid(game) {
    return;
  }
  const mapSys = GameInstance
    .GetScriptableSystemsContainer(game)
    .Get(n"NeonAscendancy.Map.NeonAscendancy_TerritoryMapSystem") as NeonAscendancy_TerritoryMapSystem;
  if !IsDefined(mapSys) {
    return;
  }
  const stId = mapSys.LookupSubTerritoryForMappin(mappin.GetNewMappinID());
  if stId <= 0 {
    return;
  }
  const owner = NcGetSubTerritoryOwner(stId);
  if owner
    != this.NeonAscendancy_cachedOwner
    || this.NeonAscendancy_cachedOwner == 0 {
    this.NeonAscendancy_cachedOwner = owner;
    const rgba = NcGetFactionColorRgba(owner);
    const r = Cast<Uint8>(rgba / 16777216u & 255u);
    const g = Cast<Uint8>(rgba / 65536u & 255u);
    const b = Cast<Uint8>(rgba / 256u & 255u);
    const a = Cast<Uint8>(rgba & 255u);
    let iconW = inkWidgetRef.Get(this.iconWidget);
    if IsDefined(iconW) {
      iconW.UnbindProperty(n"tintColor");
      iconW.SetTintColor(r, g, b, a);
    }
  }
}

@wrapMethod(WorldMapTooltipController)
public func SetData(
  const data: script_ref<WorldMapTooltipData>,
  menu: ref<WorldMapMenuGameController>
) -> Void {
  wrappedMethod(data, menu);
  let mappin = Deref(data).mappin;
  if !IsDefined(mappin) {
    return;
  }
  const game = GetGameInstance();
  if !GameInstance.IsValid(game) {
    return;
  }
  const mapSys = GameInstance
    .GetScriptableSystemsContainer(game)
    .Get(n"NeonAscendancy.Map.NeonAscendancy_TerritoryMapSystem") as NeonAscendancy_TerritoryMapSystem;
  if !IsDefined(mapSys) {
    return;
  }
  const stId = mapSys.LookupSubTerritoryForMappin(mappin.GetNewMappinID());
  if stId <= 0 {
    return;
  }
  inkTextRef.SetText(this.m_titleText, NcGetControlCenterTooltipTitle(stId));
  inkWidgetRef.SetVisible(this.m_descText, true);
  inkTextRef.SetText(this.m_descText, NcGetControlCenterTooltipDesc(stId));
  inkWidgetRef.SetVisible(this.m_warningText, false);
  inkWidgetRef.SetVisible(this.m_threatLevelPanel, false);
  inkWidgetRef.SetVisible(this.m_fixerPanel, false);
  inkWidgetRef.SetVisible(this.m_travelCostContainer, false);
}

