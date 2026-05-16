if (uproot.currentPage === "Trading") {
    let attempts = 0;
    const maxAttempts = 8;

    const interval = setInterval(() => {
        attempts += 1;
        const side = Math.random() < 0.5 ? "buy" : "sell";
        const price = (5 + Math.random() * 10).toFixed(2);
        const quantity = Math.floor(Math.random() * 5) + 1;
        const type = Math.random() < 0.7 ? "limit" : "market";
        let request;

        if (type === "limit") {
            request = uproot.invoke("submit_order", "limit", side, price, quantity);
        } else {
            request = uproot.invoke("submit_order", "market", side, null, quantity);
        }

        request.catch(() => {
            // Empty books and self-trade rejections are expected during simulation.
        });

        if (attempts >= maxAttempts) {
            clearInterval(interval);
            setTimeout(() => uproot.submit(), 500);
        }
    }, 1000);
}
