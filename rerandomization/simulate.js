// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

uproot.simulate.on("rerandomization/Survey", (sim) => {
    sim.fill({
        age: String(sim.integer(18, 65)),
    });
    sim.choose("econ", sim.random(["True", "False"])).submit();
});
