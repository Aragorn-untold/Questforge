(() => {
  const tablist = document.getElementById("campaign-detail-tabs");
  const panel = document.getElementById("campaign-tab-panel");

  if (!tablist || !panel) return;

  const tabs = () => Array.from(tablist.querySelectorAll('[role="tab"]'));

  const selectTab = (selectedTab) => {
    tabs().forEach((tab) => {
      const isSelected = tab === selectedTab;
      tab.classList.toggle("is-active", isSelected);
      tab.setAttribute("aria-selected", String(isSelected));
      tab.tabIndex = isSelected ? 0 : -1;
    });
    panel.setAttribute("aria-labelledby", selectedTab.id);
  };

  document.body.addEventListener("htmx:afterSwap", (event) => {
    if (event.detail.target !== panel) return;
    const trigger = event.detail.requestConfig?.elt;
    const selectedTab = trigger?.closest('#campaign-detail-tabs [role="tab"]');
    if (selectedTab) selectTab(selectedTab);
  });

  tablist.addEventListener("keydown", (event) => {
    const currentTab = event.target.closest('[role="tab"]');
    if (!currentTab) return;

    const allTabs = tabs();
    const currentIndex = allTabs.indexOf(currentTab);
    let nextIndex;

    if (event.key === "ArrowRight") nextIndex = (currentIndex + 1) % allTabs.length;
    else if (event.key === "ArrowLeft") nextIndex = (currentIndex - 1 + allTabs.length) % allTabs.length;
    else if (event.key === "Home") nextIndex = 0;
    else if (event.key === "End") nextIndex = allTabs.length - 1;
    else return;

    event.preventDefault();
    allTabs[nextIndex].focus();
    allTabs[nextIndex].click();
  });
})();
