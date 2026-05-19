uproot.simulate.on("anchoring/Estimate", (sim) => {
    sim.choose("comparison", "more").fill("estimate", "500").submit();
});
