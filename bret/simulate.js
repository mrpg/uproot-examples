// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

uproot.simulate.on("bret/Choose", (sim) => {
    const boxes = document.querySelectorAll(".bret-box");

    boxes[sim.integer(0, boxes.length - 1)].click();
    sim.submit();
});
