module NeonAscendancy.UI

import NeonAscendancy.Core.*

// Codeware-free "Start Ascendancy" Main Menu entry.
//
// The item is pushed through the exact same AddMenuItem / PauseMenuListItemData
// / inkListController path vanilla uses for New Game / Load Game, so focus,
// hover, keyboard, gamepad, and click behavior are identical. Activation
// dispatches OnStartAscendancy to the active MenuScenario_SingleplayerMenu
// scenario handler (the same inkMenuEventDispatcher path as vanilla OnNewGame).
@wrapMethod(SingleplayerMenuGameController)
private func PopulateMenuItemList() -> Void {
  wrappedMethod();
  const label = "Start Ascendancy";
  this.AddMenuItem(label, n"OnStartAscendancy");
  this.m_menuListController.Refresh();
}

// Skips the EP1 base-vs-PL picker while keeping the full vanilla
// Difficulty -> LifePath -> BodyType -> CharacterCustomization -> Stats ->
// Summary chain.
@addMethod(MenuScenario_SingleplayerMenu)
protected cb func OnStartAscendancy() -> Bool {
  NcSetAscendancyStartPending(true);
  this.CloseSubMenu();
  this.SwitchToScenario(n"MenuScenario_Difficulty");
}

// Returning to the main menu (or any vanilla New Game / Load Game) must never
// observe an armed .gamedef redirect.
@wrapMethod(MenuScenario_SingleplayerMenu)
protected cb func OnEnterScenario(prevScenario: CName, userData: ref<IScriptable>) -> Bool {
  NcSetAscendancyStartPending(false);
  NcDisarmAscendancyStart();
  return wrappedMethod(prevScenario, userData);
}

// Arm the native .gamedef redirect immediately before the vanilla
// FinalizeState + StartNewGame call site runs. Pending stays true until the
// world attaches so SanitizerSystem can also detect the clean-slate entry.
@wrapMethod(characterCreationSummaryMenu)
protected cb func OnOutroComplete(anim: ref<inkAnimProxy>) -> Bool {
  if NcIsAscendancyStartPending() {
    if IsDefined(this.m_characterCustomizationState) {
      this.m_characterCustomizationState.SetIsExpansionStandalone(false);
    }
    const armed = NcArmAscendancyStart();
    NcLogInfo(s"MainMenu.StartAscendancy: armed=\(armed)");
  }
  return wrappedMethod(anim);
}

