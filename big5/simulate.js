uproot.simulate.on("big5/Response", (sim) => {
    sim.chooseAnyRadio().submit();
});

uproot.simulate.on("big5/Results", (sim) => {
    sim.submit();
});
