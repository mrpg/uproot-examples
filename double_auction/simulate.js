uproot.simulate.on("double_auction/RaiseHands", () => {
    I("toggle-wrapper").click();
});

uproot.simulate.on("double_auction/Instructions", (sim) => {
    sim.submit();
});

uproot.simulate.on("double_auction/RoundInfo", (sim) => {
    sim.submit();
});

uproot.simulate.on("double_auction/Trade", (sim) => {
    const amount = buyer ? costOrValue - tax : costOrValue + tax;
    uproot.invoke("make_offer", amount);
});
