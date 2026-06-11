// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

uproot.simulate.on("first_price_auction/Bid", (sim) => {
    sim.fill("bid", String(Math.floor(Math.random() * 101))).submit();
});
