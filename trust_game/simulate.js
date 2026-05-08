// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

uproot.simulate.on("trust_game/Send", (sim) => {
    sim.fill("sent", "6").submit();
});

uproot.simulate.on("trust_game/Return", (sim) => {
    sim.fill("returned", "7").submit();
});
