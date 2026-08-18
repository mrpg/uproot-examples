uproot.simulate.on("pgg_strategy_method/Instructions", (sim) => {
    sim.submit();
});

uproot.simulate.on("pgg_strategy_method/Unconditional", (sim) => {
    sim.fill("unconditional", sim.integer(0, 20)).submit();
});

uproot.simulate.on("pgg_strategy_method/ContributionTable", (sim) => {
    for (let i = 0; i <= 20; i++) {
        sim.fill("cond_" + i, sim.integer(0, 20));
    }
    sim.submit();
});
