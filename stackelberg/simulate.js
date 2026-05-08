// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

uproot.simulate.on("stackelberg/Instructions", (sim) => {
    sim.submit();
});

uproot.simulate.on("stackelberg/LeaderDecision", (sim) => {
    sim.fill("units", "40").submit();
});

uproot.simulate.on("stackelberg/FollowerDecision", (sim) => {
    sim.fill("units", "30").submit();
});
