uproot.simulate.on("double_auction/RaiseHands", () => {
    uproot.invoke("set_presence", true);
});

uproot.simulate.on("double_auction/Instructions", (sim) => {
    sim.submit();
});

uproot.simulate.on("double_auction/RoundInfo", (sim) => {
    sim.submit();
});

uproot.simulate.on("double_auction/Trade", (sim) => {
    if (traded || offerAmount !== null) {
        sim.submit();
        return;
    }

    const amount = buyer ? costOrValue - tax : costOrValue + tax;
    uproot.invoke("make_offer", amount).finally(() => {
        sim.submit();
    });
});
