// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

uproot.simulate.on("svo_slider/Allocate", (sim) => {
    for (let i = 1; i <= 6; i++) {
        sim.fill("choice_" + i, String(sim.integer(1, 9)));
    }

    sim.submit();
});
