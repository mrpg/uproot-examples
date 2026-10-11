uproot.simulate.on("conjoint/Choice", () => {
    // Pairs are fetched and rendered asynchronously via live methods, so poll
    // the DOM and click a card whenever a fresh pair is waiting for a choice
    const interval = setInterval(() => {
        if (I("done-area").style.display !== "none") {
            clearInterval(interval);
            I("done-area").querySelector("button").click();

            return;
        }

        const rendered = I("attrs-left").children.length > 0;
        const pending = document.querySelector(".profile-card.selected") !== null;

        if (rendered && !pending) {
            I(Math.random() < 0.5 ? "card-left" : "card-right").click();
        }
    }, 50);
});
