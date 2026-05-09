// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

uproot.simulate.on("ultimatum_game/Propose", (sim) => {
    sim.fill("offer", "4").submit();
});

uproot.simulate.on("ultimatum_game/Respond", (sim) => {
    sim.choose("accept", "True").submit();
});

uproot.simulate.on("ultimatum_game/Results", (sim) => {
    sim.submit();
});
