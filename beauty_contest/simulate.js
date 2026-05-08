// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

uproot.simulate.on("beauty_contest/Guess", (sim) => {
    sim.fill("guess", "33").submit();
});
