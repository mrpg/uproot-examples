uproot.simulate.on("prediction_market/Instructions", (sim) => {
    sim.submit();
});

uproot.simulate.on("prediction_market/Trading", (sim) => {
    let attempts = 0;
    const maxAttempts = 5;

    const interval = setInterval(() => {
        attempts += 1;
        const outcome = Math.random() < 0.5 ? "yes" : "no";
        const shares = Math.floor(Math.random() * 5) + 1;

        uproot.invoke("trade", outcome, "buy", shares).catch(() => {});

        if (attempts >= maxAttempts) {
            clearInterval(interval);
        }
    }, 800);
});

uproot.simulate.on("prediction_market/Results", (sim) => {
    sim.submit();
});
