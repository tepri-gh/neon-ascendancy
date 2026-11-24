module NeonAscendancy.UI

import NeonAscendancy.Core.*
import NeonAscendancy.Gameplay.*
import NeonAscendancy.Sandbox.*

// Paper-thin Codeware-free Pause Menu entry. Label & action state machine live in C++.
// Decision A2: the item only exists inside an active Ascendancy run (clean-slate
// boot or an enabled sanitizer), so vanilla campaign saves stay 100% untouched.
@wrapMethod(PauseMenuGameController)
private func PopulateMenuItemList() -> Void {
  wrappedMethod();
  let qs = GameInstance.GetQuestsSystem(this.m_gameInstance);
  const cleanSlateRun = IsDefined(qs) && qs.GetFact(n"na_clean_slate") > 0;
  if cleanSlateRun || NeonAscendancy_IsSanitizerEnabled(this.m_gameInstance) {
    this.AddMenuItem(NcGetPauseMenuLabel(true), n"NeonAscendancy_PauseAction");
    this.m_menuListController.Refresh();
  }
}

@wrapMethod(PauseMenuGameController)
protected cb func OnMenuItemActivated(index: Int32, target: ref<ListItemController>) -> Bool {
  const data = target.GetData() as PauseMenuListItemData;
  if IsDefined(data) && Equals(data.eventName, n"NeonAscendancy_PauseAction") {
    this.PlaySound(n"Button", n"OnPress");
    let sys = GameInstance
      .GetScriptableSystemsContainer(this.m_gameInstance)
      .Get(n"NeonAscendancy.Gameplay.NeonAscendancy_AscendancySystem") as NeonAscendancy_AscendancySystem;
    if IsDefined(sys) {
      sys.HandlePauseMenuAction();
    }
    this.m_menuEventDispatcher.SpawnEvent(n"OnClosePauseMenu");
    return true;
  }
  return wrappedMethod(index, target);
}

