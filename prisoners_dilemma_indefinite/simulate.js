// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

uproot.simulate.on("prisoners_dilemma_indefinite/Instructions", (sim) => {
    sim.submit();
});

uproot.simulate.on("prisoners_dilemma_indefinite/Dilemma", (sim) => {
    sim.choose("cooperate", sim.random(["True", "False"])).submit();
});

uproot.simulate.on("prisoners_dilemma_indefinite/Results", (sim) => {
    sim.submit();
});
