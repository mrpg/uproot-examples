uproot.simulate.on("blocks/Step", (sim) => {
    sim.fill("number", String(sim.integer(1, 100))).submit();
});

uproot.simulate.on("blocks/RepeatStep", (sim) => {
    sim.fill("number", String(sim.integer(1, 100))).submit();
});

uproot.simulate.on("blocks/Summary", (sim) => {
    sim.submit();
});
