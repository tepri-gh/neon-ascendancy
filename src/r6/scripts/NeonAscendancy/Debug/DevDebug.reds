module NeonAscendancy.Debug

import NeonAscendancy.Core.*

// Dev-only playtest boost. Flip the return value to false to disable it.
public func NeonAscendancy_DevDebugEnabled() -> Bool {
  return true;
}

// Stateless, idempotent bootstrap boost: every step re-reads live state and
// only raises what is still below the target, so running it on every clean
// slate bootstrap (or repeatedly) is a no-op after the first pass. It never
// touches character Level, Street Cred, or any persisted mod field.
public func NeonAscendancy_ApplyDevDebug(game: GameInstance, player: ref<GameObject>) -> Void {
  if !GameInstance.IsValid(game) || !IsDefined(player) {
    return;
  }
  let devData = PlayerDevelopmentSystem.GetData(player);
  if !IsDefined(devData) {
    return;
  }
  const attributesApplied = NeonAscendancy_DevDebugRaiseAttributes(devData);
  const perkLevelsUpgraded = NeonAscendancy_DevDebugGrantPerks(game, devData);
  NeonAscendancy_DevDebugRefreshStatsBB(player);
  NeonAscendancy_DevDebugUnlockFastTravel(game, player);
  NeonAscendancy_DevDebugEnableVenueProbe(game);
  const doubleJump = NeonAscendancy_DevDebugGrantDoubleJump(game, player);
  // Level and Street Cred are read after the boost purely to prove they were
  // never modified: the boost only raises attributes and perk levels.
  const level = devData.GetProficiencyLevel(gamedataProficiencyType.Level);
  const streetCred = devData.GetProficiencyLevel(gamedataProficiencyType.StreetCred);
  NcLogInfo(
    s"DevDebug.Apply: attributesApplied=\(attributesApplied)/5 perkLevelsUpgraded=\(perkLevelsUpgraded) level=\(level) streetCred=\(streetCred) na_dev_unlock_all_ft=1 na_dev_venue_probe=1 doubleJump=\(doubleJump)"
  );
}

// Raise the five core attributes to 20. SetAttribute force-sets the absolute
// attribute value, so re-running with an attribute already at 20 is skipped.
private func NeonAscendancy_DevDebugRaiseAttributes(devData: ref<PlayerDevelopmentData>) -> Int32 {
  const targetAttributeValue = 20.0;
  let attributes: array<gamedataStatType> = [
    gamedataStatType.Strength,
    gamedataStatType.Reflexes,
    gamedataStatType.TechnicalAbility,
    gamedataStatType.Intelligence,
    gamedataStatType.Cool
  ];
  let applied = 0;
  for statType in attributes {
    if devData.GetAttributeValue(statType) < targetAttributeValue {
      devData.SetAttribute(statType, targetAttributeValue);
      applied += 1;
    }
  }
  return applied;
}

// Unlock and buy every 2.x new perk up to its max level. Relic/Espionage
// perks only exist with Phantom Liberty installed; when they are granted the
// ep1_tree_unlocked fact makes the Relic perk tab visible in the UI.
private func NeonAscendancy_DevDebugGrantPerks(game: GameInstance, devData: ref<PlayerDevelopmentData>) -> Int32 {
  const ep1Enabled = IsEP1();
  let upgraded = 0;
  let hasEspionagePerk = false;
  let i = 0;
  while i < EnumInt(gamedataNewPerkType.Count) {
    const perkType = IntEnum<gamedataNewPerkType>(i);
    i += 1;
    let rec = RPGManager.GetNewPerkRecord(perkType);
    if !IsDefined(rec) {
      continue;
    }
    const maxLevel = rec.GetLevelsCount();
    if maxLevel <= 0 {
      continue;
    }
    let attr = rec.Attribute();
    if !IsDefined(attr) {
      continue;
    }
    const isEspionage = Equals(attr.Type(), gamedataAttributeDataType.EspionageAttributeData);
    if isEspionage {
      if !ep1Enabled {
        continue;
      }
      hasEspionagePerk = true;
    }
    if devData.IsNewPerkBought(perkType) >= maxLevel {
      continue;
    }
    devData.UnlockNewPerk(perkType);
    while devData.IsNewPerkBought(perkType) < maxLevel {
      if !devData.BuyNewPerk(perkType, true) {
        break;
      }
      upgraded += 1;
    }
  }
  if hasEspionagePerk {
    let qs = GameInstance.GetQuestsSystem(game);
    if IsDefined(qs) && qs.GetFact(n"ep1_tree_unlocked") == 0 {
      qs.SetFact(n"ep1_tree_unlocked", 1);
    }
  }
  return upgraded;
}

// Push the raised attributes into the player-stats blackboard so HUD/menus
// show them without reopening the inventory.
private func NeonAscendancy_DevDebugRefreshStatsBB(player: ref<GameObject>) -> Void {
  const devSystem = PlayerDevelopmentSystem.GetInstance(player);
  if !IsDefined(devSystem) {
    return;
  }
  let req = new RequestStatsBB();
  req.Set(player);
  devSystem.QueueRequest(req);
}

// Clear fast-travel blocks; the fact gate lets the clean-slate archive
// register and unlock every fast travel point on the map.
private func NeonAscendancy_DevDebugUnlockFastTravel(game: GameInstance, player: ref<GameObject>) -> Void {
  StatusEffectHelper.RemoveStatusEffectsWithTag(player, n"BlockFastTravel");
  FastTravelSystem.RemoveAllFastTravelLocks(game);
  let qs = GameInstance.GetQuestsSystem(game);
  if IsDefined(qs) && qs.GetFact(n"na_dev_unlock_all_ft") == 0 {
    qs.SetFact(n"na_dev_unlock_all_ft", 1);
  }
}

// Arm the venue-access probe. Setting na_dev_venue_probe lets the clean-slate
// archive's gated venue_probe.questphase start, then schedules the bounded
// two-pass log check. Never runs unless dev debug is enabled.
private func NeonAscendancy_DevDebugEnableVenueProbe(game: GameInstance) -> Void {
  let qs = GameInstance.GetQuestsSystem(game);
  if !IsDefined(qs) {
    return;
  }
  if qs.GetFact(n"na_dev_venue_probe") == 0 {
    qs.SetFact(n"na_dev_venue_probe", 1);
  }
  NeonAscendancy_StartVenueProbe(game);
}

// Dev boost: install and equip Reinforced Tendons, the double-jump leg
// cyberware (HasDoubleJump, checked by locomotionTransitions.swift:3951).
// In TweakDB, Reinforced Tendons is the BoostedTendons family; JenkinsTendons
// is the different Jenkins' Tendons cyberware (the owner confirmed in-game
// that the Jenkins record is not the double-jump one).
//
// Mirrors a ripperdoc install: grant the item, then call
// EquipCyberwareByTDBID, which queues the same EquipRequest the ripperdoc UI
// uses (ripperdoc.swift EquipCyberware). Idempotent - the equipped leg slots are
// scanned by record id first, and the item is only granted when the player does
// not already own one, so repeated bootstraps add nothing. Returns a short
// status string for the Apply log line.
private func NeonAscendancy_DevDebugGrantDoubleJump(game: GameInstance, player: ref<GameObject>) -> String {
  const tendonTdbId = t"Items.AdvancedBoostedTendonsLegendary";
  let equipData = EquipmentSystem.GetData(player);
  if !IsDefined(equipData) {
    return "noEquipmentData";
  }
  // Idempotency: ItemID carries a per-instance seed, so compare on the record id
  // and scan the equipped leg slots rather than relying on IsEquipped alone.
  const slotCount = equipData.GetNumberOfSlots(gamedataEquipmentArea.LegsCW);
  let i = 0;
  while i < slotCount {
    const equipped = equipData.GetItemInEquipSlot(gamedataEquipmentArea.LegsCW, i);
    if ItemID.IsValid(equipped) && ItemID.GetTDBID(equipped) == tendonTdbId {
      return "alreadyEquipped";
    }
    i += 1;
  }
  let transactionSystem = GameInstance.GetTransactionSystem(game);
  if !IsDefined(transactionSystem) {
    return "noTransactionSystem";
  }
  if !IsDefined(transactionSystem.GetItemDataByTDBID(player, tendonTdbId)) {
    transactionSystem.GiveItem(player, ItemID.FromTDBID(tendonTdbId), 1);
  }
  const equipmentSystem = EquipmentSystem.GetInstance(player);
  if !IsDefined(equipmentSystem) {
    return "noEquipmentSystem";
  }
  let puppet = player as PlayerPuppet;
  if !IsDefined(puppet) {
    return "noPlayerPuppet";
  }
  // Same call a ripperdoc install ends in (ripperdoc.swift EquipCyberware ->
  // EquipRequest; EquipCyberwareByTDBID wraps exactly that request).
  equipmentSystem.EquipCyberwareByTDBID(puppet, tendonTdbId);
  return "equipped";
}

