uproot.simulate.on("n_by_n/Instructions", (sim) => {
    sim.submit();
});

uproot.simulate.on("n_by_n/Decision", (sim) => {
    const radios = document.querySelectorAll('input[name="choice"]');
    const idx = Math.floor(Math.random() * radios.length);
    radios[idx].checked = true;
    sim.submit();
});
