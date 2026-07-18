uproot.simulate.on("mind_game/Instructions", (sim) => {
    sim.submit();
});

uproot.simulate.on("mind_game/Think", (sim) => {
    sim.submit();
});

uproot.simulate.on("mind_game/Roll", (sim) => {
    I("roll-button").click();

    setTimeout(() => {
        sim.choose("reported_diceroll", String(sim.integer(1, 6)))
            .choose("correct_guess", String(sim.integer(0, 1)))
            .submit();
    }, 1500);
});
