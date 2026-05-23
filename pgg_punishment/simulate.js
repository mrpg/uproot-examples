uproot.simulate.on("pgg_punishment/Contribute", (sim) => {
    sim.fill("contribution", sim.integer(0, 20)).submit();
});

uproot.simulate.on("pgg_punishment/Punish", (sim) => {
    const fields = document.querySelectorAll('input[type="number"]');
    const budget = 20;
    let remaining = budget;

    fields.forEach((field, i) => {
        const max = i < fields.length - 1 ? Math.min(remaining, 10) : remaining;
        const val = Math.floor(Math.random() * (max + 1));
        field.value = val;
        remaining -= val;
    });

    sim.submit();
});
