// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

uproot.simulate.on((page) => page.startsWith("bootstrap_elements/") && page !== "bootstrap_elements/PuttingItTogether", (sim) => {
    sim.submit();
});

uproot.simulate.on("bootstrap_elements/PuttingItTogether", (sim) => {
    sim.oneOf("option", ["A", "B"]).submit();
});
