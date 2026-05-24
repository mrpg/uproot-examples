uproot.simulate.on("revise/Decision", (sim) => {
    sim.fill("number", String(Math.floor(Math.random() * 100))).submit();
});
