/*
 * A small guided tour, built only on Bootstrap’s own Popover component.
 *
 * Usage:
 *
 *     Tour.start([
 *         { target: "#some-element", title: "Title", content: "Text", placement: "bottom" },
 *         ...
 *     ]);
 *
 * Each step highlights its target with a “spotlight” (a box with a huge shadow
 * that dims the rest of the page) and attaches a popover with Back/Next buttons
 * to it. Keyboard: ← and → navigate, Esc ends the tour. Steps whose target does
 * not exist or is invisible are skipped. Content is inserted as text, never as HTML.
 */

window.Tour = (() => {
    "use strict";

    const PADDING = 8;  // Space between target and spotlight edge in pixels
    const OFFSET = 12;  // Space between spotlight and popover in pixels
    const SIDES = ["top", "right", "bottom", "left"];

    let steps = [];
    let index = 0;
    let backdrop = null;
    let spotlight = null;
    let popover = null;
    let returnFocus = null;
    let frame = 0;

    const isVisible = (el) => el !== null && el.getClientRects().length > 0;

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

        el.type = "button";  // Never submit uproot’s form
        el.addEventListener("click", onClick);

        return el;
    };

    // Move the spotlight over the current target (in page coordinates, so it scrolls along)
    const placeSpotlight = () => {
        const rect = document.querySelector(steps[index].target).getBoundingClientRect();

        spotlight.style.top = `${rect.top + window.scrollY - PADDING}px`;
        spotlight.style.left = `${rect.left + window.scrollX - PADDING}px`;
        spotlight.style.width = `${rect.width + 2 * PADDING}px`;
        spotlight.style.height = `${rect.height + 2 * PADDING}px`;
    };

    // Choose the popover’s side once, from the target’s final position in the window: the
    // step’s own placement if the popover fits there, otherwise the side with the most room
    const chooseSide = (step, rect, tip) => {
        const room = {
            top: rect.top - tip.offsetHeight,
            right: window.innerWidth - rect.right - tip.offsetWidth,
            bottom: window.innerHeight - rect.bottom - tip.offsetHeight,
            left: rect.left - tip.offsetWidth,
        };

        if (room[step.placement] >= PADDING + OFFSET) {
            return step.placement;
        }

        return SIDES.reduce((best, side) => (room[side] > room[best] ? side : best));
    };

    // While the spotlight glides to a new target, re-align the popover with it on every frame
    const follow = () => {
        popover?.update();
        frame = spotlight.getAnimations().length > 0 ? requestAnimationFrame(follow) : 0;
    };

    const header = (step) => {
        const el = element("div", "d-flex align-items-center justify-content-between gap-3");

        el.append(
            element("span", "", step.title),
            button("btn-close", undefined, end),
        );
        el.lastChild.setAttribute("aria-label", "End tour");

        return el;
    };

    const body = (step) => {
        const el = element("div", "");
        const footer = element("div", "d-flex align-items-center justify-content-between gap-2 mt-3");
        const controls = element("div", "d-flex gap-2");
        const last = index === steps.length - 1;

        if (index > 0) {
            controls.append(button("btn btn-sm btn-outline-secondary", "Back", () => show(index - 1)));
        }

        controls.append(
            button("btn btn-sm btn-primary", last ? "Done" : "Next", () => (last ? end() : show(index + 1))),
        );

        footer.append(element("small", "text-body-secondary", `${index + 1} of ${steps.length}`), controls);
        el.append(element("div", "", step.content), footer);

        return el;
    };

    const show = (newIndex) => {
        index = newIndex;

        const step = steps[index];
        const target = document.querySelector(step.target);

        if (popover !== null) {
            popover.dispose();
        }

        // Center small targets; show tall ones from their top
        const tall = target.getBoundingClientRect().height > 0.6 * window.innerHeight;
        const block = tall ? "start" : "center";
        const { scrollX, scrollY } = window;

        // Find out where the target ends up by scrolling there instantly and back again
        // (nothing is drawn in between), then let the page scroll there smoothly
        target.scrollIntoView({ block, behavior: "instant" });
        const rect = target.getBoundingClientRect();
        window.scrollTo({ left: scrollX, top: scrollY, behavior: "instant" });

        target.scrollIntoView({ block });
        placeSpotlight();

        // The popover is attached to the spotlight, not to the target, so that the
        // target’s own tooltips or popovers (if any) are left untouched
        popover = new bootstrap.Popover(spotlight, {
            container: "body",
            content: body(step),
            customClass: "tour-popover",
            html: true,  // Allows passing DOM elements; their text is still set via textContent
            offset: [0, OFFSET],
            placement: (_, tip) => chooseSide(step, rect, tip),
            // Never switch sides while gliding, and keep the popover inside the window,
            // even if it then overlaps a tall target
            popperConfig: (config) => ({
                ...config,
                modifiers: [
                    ...config.modifiers,
                    { name: "flip", enabled: false },
                    { name: "preventOverflow", options: { altAxis: true, padding: 8, tether: false } },
                ],
            }),
            title: header(step),
            trigger: "manual",
        });
        popover.show();

        cancelAnimationFrame(frame);
        frame = requestAnimationFrame(follow);
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
    };

    const onResize = () => {
        placeSpotlight();
        popover.update();
    };

    // Focus the main button of each step, so that keyboard users can simply press Enter
    const onShown = () => {
        document.querySelector(".tour-popover .btn-primary")?.focus({ preventScroll: true });
    };

    const end = () => {
        if (popover === null) {
            return;
        }

        cancelAnimationFrame(frame);
        popover.dispose();
        popover = null;
        spotlight.remove();
        backdrop.remove();
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

        // The backdrop catches clicks on the dimmed page (ending the tour)
        backdrop = element("div", "tour-backdrop");
        backdrop.addEventListener("click", end);
        spotlight = element("div", "tour-spotlight");
        spotlight.addEventListener("shown.bs.popover", onShown);
        document.body.append(backdrop, spotlight);

        document.addEventListener("keydown", onKeydown);
        window.addEventListener("resize", onResize);

        show(0);
    };

    return { start, end };
})();
