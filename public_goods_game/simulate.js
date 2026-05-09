// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

uproot.simulate.on("public_goods_game/Contribute", (sim) => {
    sim.fill("contribution", "5").submit();
});

uproot.simulate.on("public_goods_game/Results", (sim) => {
    sim.submit();
});
