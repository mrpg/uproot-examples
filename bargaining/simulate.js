// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

uproot.simulate.on("bargaining/Bargain", (sim) => {
    // Demand a random share, then accept the other player's proposal after a while
    uproot.invoke("propose", sim.integer(40, 70) / 10);

    setTimeout(() => {
        uproot.invoke("accept");
    }, 3000 + sim.integer(0, 3000));
});
