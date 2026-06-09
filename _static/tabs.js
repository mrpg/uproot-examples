(() => {
    "use strict";

    const selectors = {
        root: "[data-tabs]",
        tab: "[data-tab-target]",
        panel: "[data-tab-panel]",
        directionButton: "[data-tab-direction]",
        submit: ".tabs-page__submit",
    };

    const getTabs = (root) => Array.from(root.querySelectorAll(selectors.tab));
    const getPanels = (root) => Array.from(root.querySelectorAll(selectors.panel));

    const getActiveIndex = (tabs) => {
        const activeIndex = tabs.findIndex((tab) => tab.classList.contains("active"));

        return activeIndex === -1 ? 0 : activeIndex;
    };

    const showTab = (root, targetPanelId, focusTab = false) => {
        const tabs = getTabs(root);
        const panels = getPanels(root);
        const activeTab = tabs.find((tab) => tab.dataset.tabTarget === targetPanelId);

        if (!activeTab) {
            return;
        }

        tabs.forEach((tab) => {
            const isActive = tab === activeTab;

            tab.classList.toggle("active", isActive);
            tab.setAttribute("aria-selected", String(isActive));
            tab.tabIndex = isActive ? 0 : -1;
        });

        panels.forEach((panel) => {
            const isActive = panel.id === targetPanelId;

            panel.classList.toggle("show", isActive);
            panel.classList.toggle("active", isActive);
            panel.hidden = !isActive;
        });

        if (focusTab) {
            activeTab.focus();
        }

        window.scrollTo({ top: 0, left: 0 });
    };

    const createButton = (direction) => {
        const button = document.createElement("button");

        button.className = direction === "next" ? "btn btn-primary" : "btn btn-secondary";
        button.dataset.tabDirection = direction;
        button.type = "button";
        button.textContent = direction === "next" ? "Next" : "Back";

        return button;
    };

    const addPanelControls = (panel, index, panelCount) => {
        if (panel.querySelector(selectors.directionButton)) {
            return;
        }

        const submit = panel.querySelector(selectors.submit);

        if (submit) {
            if (index > 0) {
                submit.prepend(createButton("back"));
            }

            return;
        }

        const controls = document.createElement("div");

        controls.className = "tabs-page__controls";

        if (index > 0) {
            controls.append(createButton("back"));
        }

        if (index < panelCount - 1) {
            controls.append(createButton("next"));
        }

        if (controls.children.length > 0) {
            panel.append(controls);
        }
    };

    const showSiblingTab = (root, direction) => {
        const tabs = getTabs(root);
        const activeIndex = getActiveIndex(tabs);
        const nextIndex = direction === "next" ? activeIndex + 1 : activeIndex - 1;
        const nextTab = tabs[nextIndex];

        if (nextTab) {
            showTab(root, nextTab.dataset.tabTarget, true);
        }
    };

    const initTabs = (root) => {
        const tabs = getTabs(root);
        const panels = getPanels(root);

        if (tabs.length === 0 || panels.length === 0) {
            return;
        }

        panels.forEach((panel, index) => {
            addPanelControls(panel, index, panels.length);
        });

        tabs.forEach((tab, index) => {
            tab.tabIndex = tab.classList.contains("active") ? 0 : -1;

            tab.addEventListener("click", () => {
                showTab(root, tab.dataset.tabTarget);
            });

            tab.addEventListener("keydown", (event) => {
                if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") {
                    return;
                }

                event.preventDefault();

                const offset = event.key === "ArrowRight" ? 1 : -1;
                const nextIndex = (index + offset + tabs.length) % tabs.length;

                showTab(root, tabs[nextIndex].dataset.tabTarget, true);
            });
        });

        root.addEventListener("click", (event) => {
            const button = event.target instanceof Element
                ? event.target.closest(selectors.directionButton)
                : null;

            if (!button || !root.contains(button)) {
                return;
            }

            showSiblingTab(root, button.dataset.tabDirection);
        });

        const activeTab = tabs[getActiveIndex(tabs)];

        if (activeTab) {
            showTab(root, activeTab.dataset.tabTarget);
        }
    };

    const initAllTabs = () => {
        document.querySelectorAll(selectors.root).forEach(initTabs);
    };

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initAllTabs);
    } else {
        initAllTabs();
    }
})();
