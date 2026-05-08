// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

uproot.simulate.on("gift_exchange_game/SetWage", (sim) => {
    sim.fill("wage", (1 + Math.random() * 9).toFixed(2)).submit();
});

uproot.simulate.on("gift_exchange_game/ChooseEffort", (sim) => {
    sim.fill("effort", sim.random([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])).submit();
});
