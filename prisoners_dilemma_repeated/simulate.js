// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

uproot.simulate.on("prisoners_dilemma_repeated/Dilemma", (sim) => {
    sim.choose("cooperate", sim.random(["True", "False"])).submit();
});

uproot.simulate.on("prisoners_dilemma_repeated/Results", (sim) => {
    sim.submit();
});
