// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

uproot.simulate.on("travellers_dilemma/Claim", (sim) => {
    sim.fill("claim", sim.integer(2, 100)).submit();
});

uproot.simulate.on("travellers_dilemma/Results", (sim) => {
    sim.submit();
});
