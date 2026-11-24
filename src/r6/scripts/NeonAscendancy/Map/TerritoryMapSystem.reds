module NeonAscendancy.Map

import NeonAscendancy.Core.*

// Thin map adapter registering the 41 world.db control-center pins and the single
// active combat mission waypoint. All ownership, color, tooltip, and pin-id lookup
// state lives in C++ so WorldMap UI controllers never rely on global GetGameInstance().
public class NeonAscendancy_TerritoryMapSystem extends ScriptableSystem {
  private let m_pinsRegistered: Bool;
  private let m_pinIds: array<Uint64>;
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
        this.RebindControlCenterIds();
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
    data.mappinType = t"Mappins.QuestStaticMappinDefinition";
    data.variant = gamedataMappinVariant.CustomPositionVariant;
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
    ms.SetMappinActive(this.m_missionPinId, true);
    this.m_missionPinSubTerritory = targetSt;
    this.m_hasMissionPin = true;
    NcBindControlCenterPin(this.m_missionPinId.value, targetSt);
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
    NcClearControlCenterPins();
    this.m_pinsRegistered = false;
    this.m_hasMissionPin = false;
    this.m_missionPinSubTerritory = 0;
  }

  private final func RebindControlCenterIds() -> Void {
    NcClearControlCenterPins();
    const count = ArraySize(this.m_pinIds);
    let i = 0;
    while i < count {
      const stId = NcGetControlCenterSubTerritoryId(i);
      if stId > 0 {
        NcBindControlCenterPin(this.m_pinIds[i], stId);
      }
      i += 1;
    }
    if this.m_hasMissionPin && this.m_missionPinSubTerritory > 0 {
      NcBindControlCenterPin(this.m_missionPinId.value, this.m_missionPinSubTerritory);
    }
  }

  private final func RegisterControlCenterPins(game: GameInstance) -> Void {
    let ms = GameInstance.GetMappinSystem(game);
    if !IsDefined(ms) {
      return;
    }
    NcClearControlCenterPins();
    ArrayClear(this.m_pinIds);
    const count = NcGetControlCenterCount();
    let i = 0;
    while i < count {
      const stId = NcGetControlCenterSubTerritoryId(i);
      if stId > 0 {
        // Use vanilla DropPointStaticMappin (same path as DropPointSystem.RegisterDropPointMappin)
        // so WorldMapMenuGameController always spawns a BaseWorldMapMappinController for each dot.
        let data: MappinData;
        data.mappinType = t"Mappins.DropPointStaticMappin";
        data.variant = gamedataMappinVariant.ServicePointDropPointVariant;
        data.active = true;
        data.visibleThroughWalls = false;
        data.debugCaption = s"NA_CC_\(stId)";
        const pos = Vector4(
          NcGetControlCenterX(i),
          NcGetControlCenterY(i),
          NcGetControlCenterZ(i) + 1.0,
          1.0
        );
        const pinId = ms.RegisterMappin(data, pos);
        ms.SetMappinActive(pinId, true);
        ArrayPush(this.m_pinIds, pinId.value);
        NcBindControlCenterPin(pinId.value, stId);
      }
      i += 1;
    }
    this.m_pinsRegistered = count > 0;
    NcLogInfo(
      s"TerritoryMap: registered \(ArraySize(this.m_pinIds)) control-center pins (bound=\(NcGetBoundControlCenterPinCount()))"
    );
  }
}

public func NeonAscendancy_ResolvePinSubTerritory(mappin: wref<IMappin>) -> Int32 {
  if !IsDefined(mappin) {
    return 0;
  }
  const pinId = mappin.GetNewMappinID();
  return NcLookupControlCenterPin(pinId.value);
}

private func NeonAscendancy_ShouldHideWorldMapPin(mappin: wref<IMappin>) -> Bool {
  if !IsDefined(mappin) || !NcIsSanitizerActive() {
    return false;
  }
  if NeonAscendancy_ResolvePinSubTerritory(mappin) > 0 {
    return false;
  }
  return NcIsSuppressedVanillaMappinVariant(EnumInt(mappin.GetVariant()));
}

@wrapMethod(WorldMapMenuGameController)
protected cb func OnInitialize() -> Bool {
  const res = wrappedMethod();
  NcLogInfo(
    s"WorldMap opened: sanitizer=\(NcIsSanitizerActive()) boundPins=\(NcGetBoundControlCenterPinCount())"
  );
  return res;
}

@addField(BaseWorldMapMappinController)
private let NeonAscendancy_cachedOwner: Int32;

@wrapMethod(BaseWorldMapMappinController)
private final func GetDesiredOpacityAndInteractivity(out opacity: Float, out interactive: Bool) -> Void {
  wrappedMethod(opacity, interactive);
  let mappin = this.GetMappin();
  if NeonAscendancy_ResolvePinSubTerritory(mappin) > 0 {
    opacity = 1.0;
    interactive = true;
    this.isVisibleInFilterAndZoom = true;
    return;
  }
  if NeonAscendancy_ShouldHideWorldMapPin(mappin) {
    opacity = 0.0;
    interactive = false;
    this.isVisibleInFilterAndZoom = false;
  }
}

@wrapMethod(BaseWorldMapMappinController)
protected func UpdateVisibility() -> Void {
  wrappedMethod();
  let mappin = this.GetMappin();
  let root = this.GetRootWidget();
  if !IsDefined(root) {
    return;
  }
  if NeonAscendancy_ResolvePinSubTerritory(mappin) > 0 {
    root.SetVisible(true);
    root.SetOpacity(1.0);
    root.SetInteractive(true);
    return;
  }
  if NeonAscendancy_ShouldHideWorldMapPin(mappin) {
    root.SetVisible(false);
    root.SetOpacity(0.0);
    root.SetInteractive(false);
  }
}

@wrapMethod(BaseWorldMapMappinController)
protected func UpdateIcon() -> Void {
  wrappedMethod();
  let mappin = this.GetMappin();
  const stId = NeonAscendancy_ResolvePinSubTerritory(mappin);
  if stId <= 0 {
    if NeonAscendancy_ShouldHideWorldMapPin(mappin) {
      let hiddenRoot = this.GetRootWidget();
      if IsDefined(hiddenRoot) {
        hiddenRoot.SetVisible(false);
        hiddenRoot.SetOpacity(0.0);
        hiddenRoot.SetInteractive(false);
      }
    }
    return;
  }
  const isRaidTarget = NcGetActiveMissionSubTerritoryId() == stId;
  // Valid ink atlas texture parts verified in mappinUtils.swift:63,91.
  inkImageRef
    .SetTexturePart(this.iconWidget, isRaidTarget ? n"map_bounty" : n"minor_quest");

  const owner = NcGetSubTerritoryOwner(stId);
  if owner
    != this.NeonAscendancy_cachedOwner
    || this.NeonAscendancy_cachedOwner == 0 {
    this.NeonAscendancy_cachedOwner = owner;
    const rgba = NcGetFactionColorRgba(owner);
    const r = Cast<Uint8>(rgba / 16777216u & 255u);
    const g = Cast<Uint8>(rgba / 65536u & 255u);
    const b = Cast<Uint8>(rgba / 256u & 255u);
    let iconW = inkWidgetRef.Get(this.iconWidget);
    if IsDefined(iconW) {
      iconW.UnbindProperty(n"tintColor");
      iconW.SetTintColor(r, g, b, Cast<Uint8>(255u));
      iconW.SetScale(Vector2(1.2, 1.2));
    }
  }
  let root = this.GetRootWidget();
  if IsDefined(root) {
    root.SetVisible(true);
    root.SetOpacity(1.0);
    root.SetInteractive(true);
  }
}

@wrapMethod(WorldMapTooltipController)
public func SetData(
  const data: script_ref<WorldMapTooltipData>,
  menu: ref<WorldMapMenuGameController>
) -> Void {
  wrappedMethod(data, menu);
  let mappin = Deref(data).mappin;
  const stId = NeonAscendancy_ResolvePinSubTerritory(mappin);
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

