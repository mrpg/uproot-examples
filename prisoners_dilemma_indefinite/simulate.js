uproot.simulate.on("prisoners_dilemma_indefinite/Dilemma", (sim) => {
    sim.choose("cooperate", sim.random(["True", "False"])).submit();
});

uproot.simulate.on("prisoners_dilemma_indefinite/Results", (sim) => {
    sim.submit();
});
