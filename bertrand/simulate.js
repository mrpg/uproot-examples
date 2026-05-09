// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

uproot.simulate.on("bertrand/Instructions", (sim) => {
    sim.submit();
});

uproot.simulate.on("bertrand/Decision", (sim) => {
    sim.fill("price", sim.integer(0, 100)).submit();
});

uproot.simulate.on("bertrand/Results", (sim) => {
    sim.submit();
});
