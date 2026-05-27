uproot.simulate.on("bisection/Instructions", (sim) => {
    sim.submit();
});

uproot.simulate.on("bisection/Choice", (sim) => {
    sim.chooseAnyRadio().submit();
});
