// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

uproot.simulate.on("ping/Ping", async (sim) => {
    await ping(1000);

    if (document.getElementById("timeslength").innerText === "1000") {
        sim.submit();
    }
});
