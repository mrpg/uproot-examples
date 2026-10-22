/*
 * A small guided tour, styled with Bootstrap’s popover classes.
 *
 * Usage:
 *
 *     Tour.start([
 *         { target: "#some-element", title: "Title", content: "Text", placement: "bottom" },
 *         ...
 *     ]);
 *
 * Each step highlights its target with a “spotlight” (a box with a huge shadow
 * that dims the rest of the page) and explains it in a popover with Back and
 * Next buttons. Before anything moves, the tour works out where the page will
 * scroll to and where the popover ends up: on the step’s placement if it fits
 * there, otherwise on the side with the most room. Spotlight and popover then
 * glide there together.
 *
 * While the tour runs, the rest of the page is inert. Keyboard: ← and → navigate,
 * Esc ends the tour. Steps whose target does not exist or is invisible are
 * skipped. Content is inserted as text, never as HTML.
 */

window.Tour = (() => {
    "use strict";

    const PADDING = 8;  // Space between target and spotlight edge in pixels
    const GAP = 12;  // Space between spotlight and popover, leaving room for the arrow
    const MARGIN = 8;  // Minimum space between popover and window edge
    const SIDES = ["top", "right", "bottom", "left"];

    let steps = [];
    let index = 0;
    let backdrop = null;
    let spotlight = null;
    let popover = null;
    let parts = null;  // The popover’s arrow, texts, and buttons
    let inert = [];  // Page elements made inert while the tour runs
    let returnFocus = null;

    const isVisible = (el) => el !== null && el.getClientRects().length > 0;

    const clamp = (value, min, max) => Math.max(min, Math.min(value, max));

    const element = (tag, className, text) => {
        const el = document.createElement(tag);

        el.className = className;

        if (text !== undefined) {
            el.textContent = text;
        }

        return el;
    };

    const button = (className, text, onClick) => {
        const el = element("button", className, text);

        el.type = "button";  // Never submit a form
        el.addEventListener("click", onClick);

        return el;
    };

    // Build the popover once, with Bootstrap’s markup; each step only changes its texts
    const createPopover = () => {
        const el = element("div", "popover bs-popover-auto tour-popover");
        const header = element("div", "popover-header d-flex align-items-center justify-content-between gap-5");
        const body = element("div", "popover-body");
        const footer = element("div", "d-flex align-items-center justify-content-between gap-3 mt-5");
        const controls = element("div", "d-flex gap-3");
        const close = button("btn-close", undefined, end);

        parts = {
            arrow: element("div", "popover-arrow"),
            title: element("span", "fw-semibold"),
            text: element("p", "mb-0"),
            counter: element("small", "fg-2"),
            back: button("btn-outline theme-secondary btn-sm", "Back", () => show(index - 1)),
            next: button("btn-solid theme-primary btn-sm", "Next", () => (index < steps.length - 1 ? show(index + 1) : end())),
        };

        parts.title.id = "tour-step-title";
        parts.text.id = "tour-step-text";
        parts.text.setAttribute("aria-live", "polite");  // Screen readers announce each new step
        close.setAttribute("aria-label", "End tour");

        el.setAttribute("role", "dialog");
        el.setAttribute("aria-modal", "true");
        el.setAttribute("aria-labelledby", parts.title.id);
        el.setAttribute("aria-describedby", parts.text.id);

        header.append(parts.title, close);
        controls.append(parts.back, parts.next);
        footer.append(parts.counter, controls);
        body.append(parts.text, footer);
        el.append(parts.arrow, header, body);

        return el;
    };

    // The spotlight around a target, in page coordinates (which do not change when the page scrolls)
    const spotlightRect = (target) => {
        const rect = target.getBoundingClientRect();

        return new DOMRect(
            rect.left + window.scrollX - PADDING,
            rect.top + window.scrollY - PADDING,
            rect.width + 2 * PADDING,
            rect.height + 2 * PADDING,
        );
    };

    // Where the page should scroll to: center the spotlight, but show tall ones from their top
    const scrollTopFor = (spot) => {
        const { clientHeight, scrollHeight } = document.documentElement;
        const top = spot.height > 0.6 * clientHeight ? spot.top - MARGIN : spot.top - (clientHeight - spot.height) / 2;

        return clamp(top, 0, scrollHeight - clientHeight);
    };

    // Choose a side from the spotlight’s position in the window once the page has scrolled to
    // scrollTop: the step’s own placement if the popover fits there, otherwise the side with
    // the most room
    const chooseSide = (step, spot, scrollTop) => {
        const { clientWidth, clientHeight } = document.documentElement;
        const top = spot.top - scrollTop;
        const left = spot.left - window.scrollX;
        const room = {
            top: top - popover.offsetHeight,
            right: clientWidth - left - spot.width - popover.offsetWidth,
            bottom: clientHeight - top - spot.height - popover.offsetHeight,
            left: left - popover.offsetWidth,
        };

        if (room[step.placement] >= GAP + MARGIN) {
            return step.placement;
        }

        return SIDES.reduce((best, side) => (room[side] > room[best] ? side : best));
    };

    const placeSpotlight = (spot) => {
        Object.assign(spotlight.style, {
            top: `${spot.top}px`,
            left: `${spot.left}px`,
            width: `${spot.width}px`,
            height: `${spot.height}px`,
        });
    };

    // Put the popover next to the spotlight, on the chosen side, but always inside the window
    const placePopover = (step, spot, scrollTop) => {
        const { clientWidth, clientHeight } = document.documentElement;
        const { offsetWidth: width, offsetHeight: height } = popover;
        const side = chooseSide(step, spot, scrollTop);
        const vertical = side === "top" || side === "bottom";
        const centerX = spot.left + spot.width / 2;
        const centerY = spot.top + spot.height / 2;
        const [x, y] = {
            top: [centerX - width / 2, spot.top - GAP - height],
            right: [spot.right + GAP, centerY - height / 2],
            bottom: [centerX - width / 2, spot.bottom + GAP],
            left: [spot.left - GAP - width, centerY - height / 2],
        }[side];
        const left = clamp(x, window.scrollX + MARGIN, window.scrollX + clientWidth - MARGIN - width);
        const top = clamp(y, scrollTop + MARGIN, scrollTop + clientHeight - MARGIN - height);
        const { arrow } = parts;

        popover.dataset.bsPlacement = side;  // Bootstrap’s CSS draws the arrow on this side
        popover.style.left = `${left}px`;
        popover.style.top = `${top}px`;

        // The arrow points at the spotlight’s center, unless the popover had to cover the target
        arrow.hidden = vertical ? top !== y : left !== x;

        if (arrow.hidden) {
            return;
        }

        // The arrow is positioned within the popover’s border, and kept clear of its rounded corners
        const radius = parseFloat(getComputedStyle(popover).borderTopLeftRadius);

        if (vertical) {
            arrow.style.left = `${clamp(centerX - left - popover.clientLeft - arrow.offsetWidth / 2, radius, popover.clientWidth - radius - arrow.offsetWidth)}px`;
            arrow.style.top = "";
        }
        else {
            arrow.style.left = "";
            arrow.style.top = `${clamp(centerY - top - popover.clientTop - arrow.offsetHeight / 2, radius, popover.clientHeight - radius - arrow.offsetHeight)}px`;
        }
    };

    // Position spotlight and popover for the current step, scrolling the page there if asked to
    const layout = (scroll) => {
        const step = steps[index];
        const spot = spotlightRect(document.querySelector(step.target));
        const scrollTop = scroll ? scrollTopFor(spot) : window.scrollY;

        placeSpotlight(spot);
        placePopover(step, spot, scrollTop);

        if (scroll) {
            // Bootstrap makes this smooth, unless the participant prefers reduced motion
            window.scrollTo({ top: scrollTop });
        }
    };

    const show = (newIndex) => {
        index = newIndex;

        const step = steps[index];

        parts.title.textContent = step.title;
        parts.text.textContent = step.content;
        parts.counter.textContent = `${index + 1} of ${steps.length}`;
        parts.back.hidden = index === 0;
        parts.next.textContent = index === steps.length - 1 ? "Done" : "Next";

        layout(true);

        // Focus the main button of each step, so that keyboard users can simply press Enter
        parts.next.focus({ preventScroll: true });
    };

    const onKeydown = (event) => {
        if (event.key === "Escape") {
            end();
        }
        else if (event.key === "ArrowRight" && index < steps.length - 1) {
            show(index + 1);
        }
        else if (event.key === "ArrowLeft" && index > 0) {
            show(index - 1);
        }
        else {
            return;
        }

        event.preventDefault();
    };

    const onResize = () => {
        layout(false);
    };

    const end = () => {
        if (popover === null) {
            return;
        }

        backdrop.remove();
        spotlight.remove();
        popover.remove();
        backdrop = spotlight = popover = parts = null;

        for (const el of inert) {
            el.inert = false;
        }

        inert = [];
        document.removeEventListener("keydown", onKeydown);
        window.removeEventListener("resize", onResize);
        returnFocus?.focus();
    };

    const start = (allSteps) => {
        end();  // In case a tour is already running

        steps = allSteps.filter((step) => isVisible(document.querySelector(step.target)));

        if (steps.length === 0) {
            return;
        }

        returnFocus = document.activeElement;

        // While the tour runs, the page can be neither clicked nor focused, and screen readers skip it
        inert = [...document.body.children].filter((el) => !el.inert);

        for (const el of inert) {
            el.inert = true;
        }

        // The backdrop catches clicks on the dimmed page (ending the tour)
        backdrop = element("div", "tour-backdrop");
        backdrop.addEventListener("click", end);
        spotlight = element("div", "tour-spotlight");
        popover = createPopover();
        document.body.append(backdrop, spotlight, popover);

        document.addEventListener("keydown", onKeydown);
        window.addEventListener("resize", onResize);

        show(0);

        // Commit the first position before turning on the transitions, so that spotlight and
        // popover glide from step to step, but do not glide in from the corner of the page
        popover.getBoundingClientRect();
        spotlight.classList.add("tour-glide");
        popover.classList.add("tour-glide", "show");  // .show fades the popover in
    };

    return { start, end };
})();
