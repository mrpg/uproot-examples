// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

uproot.simulate.on("dictator_game/Dictate", (sim) => {
    sim.fill("give", sim.integer(0, 10)).submit();
});

uproot.simulate.on("dictator_game/Results", (sim) => {
    sim.submit();
});
