uproot.simulate.on("ramsey_economy/Instructions", (sim) => {
    sim.submit();
});

uproot.simulate.on("ramsey_economy/LaborTask", (sim) => {
    const effort = sim.integer(1, 10);

    uproot.invoke("set_effort", effort).then(() => {
        uproot.submit();
    });
});

uproot.simulate.on("ramsey_economy/ConsumptionChoice", (sim) => {
    const maxField = document.querySelector('[name="consumption"]');
    const max = parseFloat(maxField?.max || "20");
    const consumption = (Math.random() * max * 0.8 + max * 0.1).toFixed(2);

    sim.fill("consumption", consumption).submit();
});

uproot.simulate.on("ramsey_economy/RoundResults", (sim) => {
    sim.submit();
});
