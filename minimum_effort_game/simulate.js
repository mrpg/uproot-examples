// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

uproot.simulate.on("minimum_effort_game/ChooseEffort", (sim) => {
    sim.choose("effort", sim.integer(1, 7)).submit();
});
