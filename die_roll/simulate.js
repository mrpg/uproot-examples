// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

uproot.simulate.on("die_roll/Roll", (sim) => {
    I("roll-button").click();

    // Wait for the die animation to finish, then report honestly
    setTimeout(() => {
        sim.choose("report", String(sim.integer(1, 6))).submit();
    }, 1500);
});
