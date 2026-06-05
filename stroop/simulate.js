uproot.simulate.on("stroop/Instructions", (sim) => {
    sim.submit();
});

uproot.simulate.on("stroop/Stroop", (sim) => {
    sim.fill({
        response: sim.random(["red", "green", "blue", "yellow"]),
        reaction_time_ms: String(sim.integer(250, 1200)),
    }).submit();
});
