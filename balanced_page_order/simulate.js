uproot.simulate.on((page) => page.startsWith("balanced_page_order/") && !page.includes("End"), (sim) => {
    sim.submit();
});
