const asksContainer = I("asks");
const bidsContainer = I("bids");
const txsContainer = I("txs");

const maxBid = costOrValue - tax;
const minAsk = costOrValue + tax;

function fmt(n) {
    return Number(n).toLocaleString("en-US");
}

function checkProfitLimit(price) {
    if (buyer && price > maxBid) {
        alert("Negative profit not allowed. The price $" + fmt(price) + " is above your valuation" + (tax ? " net of the tax you must pay" : "") + " ($" + fmt(maxBid) + ").");
        return false;
    }
    if (!buyer && price < minAsk) {
        alert("Negative profit not allowed. The price $" + fmt(price) + " is below your cost" + (tax ? " including the tax you must pay" : "") + " ($" + fmt(minAsk) + ").");
        return false;
    }
    return true;
}

function refreshDisplay() {
    if (!traded) {
        I("not-traded").style.display = "block";
        I("traded").style.display = "none";

        if (offerAmount !== null) {
            I("current-offer").textContent = fmt(offerAmount);
            document.querySelectorAll(".has-offer").forEach(el => el.style.display = "unset");
            document.querySelectorAll(".no-offer").forEach(el => el.style.display = "none");
        }
        else {
            document.querySelectorAll(".has-offer").forEach(el => el.style.display = "none");
            document.querySelectorAll(".no-offer").forEach(el => el.style.display = "unset");
        }
    }
    else {
        I("profit").textContent = fmt(profit);
        I("not-traded").style.display = "none";
        I("traded").style.display = "block";
    }

    asksContainer.innerHTML = "";
    bidsContainer.innerHTML = "";
    txsContainer.innerHTML = "";

    market.asks.sort((a, b) => a.price - b.price).forEach(offer => {
        const badge = document.createElement("span");
        badge.className = "badge bg-danger me-1 mb-1";
        badge.textContent = fmt(offer.price);

        if (buyer) {
            const affordable = offer.price <= maxBid;
            if (!affordable) badge.classList.add("offer-unprofitable");
            badge.setAttribute("role", "button");
            badge.setAttribute("tabindex", "0");
            badge.setAttribute("aria-label", `Accept ask at price ${fmt(offer.price)}` + (affordable ? "" : " (too expensive)"));
            badge.onclick = () => { if (checkProfitLimit(offer.price)) acceptOffer(offer.id); };
            badge.onkeypress = (e) => {
                if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    if (checkProfitLimit(offer.price)) acceptOffer(offer.id);
                }
            };
        } else {
            badge.setAttribute("aria-label", `Ask price ${fmt(offer.price)}`);
        }

        asksContainer.appendChild(badge);
    });

    market.bids.sort((a, b) => b.price - a.price).forEach(offer => {
        const badge = document.createElement("span");
        badge.className = "badge bg-success me-1 mb-1";
        badge.textContent = fmt(offer.price);

        if (!buyer) {
            const profitable = offer.price >= minAsk;
            if (!profitable) badge.classList.add("offer-unprofitable");
            badge.setAttribute("role", "button");
            badge.setAttribute("tabindex", "0");
            badge.setAttribute("aria-label", `Accept bid at price ${fmt(offer.price)}` + (profitable ? "" : " (too low)"));
            badge.onclick = () => { if (checkProfitLimit(offer.price)) acceptOffer(offer.id); };
            badge.onkeypress = (e) => {
                if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    if (checkProfitLimit(offer.price)) acceptOffer(offer.id);
                }
            };
        } else {
            badge.setAttribute("aria-label", `Bid price ${fmt(offer.price)}`);
        }

        bidsContainer.appendChild(badge);
    });

    [...market.txs].reverse().forEach(tx => {
        const badge = document.createElement("span");
        badge.className = "badge bg-uproot me-1 mb-1";
        badge.textContent = fmt(tx.price);
        badge.setAttribute("aria-label", `Transaction completed at price ${fmt(tx.price)}`);

        txsContainer.appendChild(badge);
    });
}

function makeOffer(newOffer) {
    let amount = null;

    if (newOffer) {
        const raw = I("amount").value.trim();
        if (raw === "") {
            alert("Please enter a price.");
            return;
        }
        amount = parseInt(raw, 10);
        if (isNaN(amount)) {
            alert("Please enter a valid price.");
            return;
        }
        if (!checkProfitLimit(amount)) return;
    }

    const buttons = document.querySelectorAll("#not-traded button");
    buttons.forEach(btn => btn.disabled = true);

    uproot.invoke("make_offer", amount).then((newAmount) => {
        offerAmount = newAmount;
        refreshDisplay();
    }).catch(err => console.error(err)).finally(() => {
        buttons.forEach(btn => btn.disabled = false);
    });
}

function acceptOffer(id) {
    const badges = document.querySelectorAll('[role="button"]');
    badges.forEach(badge => badge.style.pointerEvents = "none");

    uproot.invoke("accept_offer", id).then((profit_) => {
        traded = true;
        profit = profit_;
        refreshDisplay();
    }).catch(err => console.error(err)).finally(() => {
        badges.forEach(badge => badge.style.pointerEvents = "");
    });
}

uproot.onCustomEvent("MarketDiff", event => {
    const diff = event.detail.data;
    const removeSet = new Set(diff.remove.map(id => String(id)));
    market.asks = market.asks.filter(o => !removeSet.has(String(o.id)));
    market.bids = market.bids.filter(o => !removeSet.has(String(o.id)));
    for (const offer of diff.add) {
        (offer.buy ? market.bids : market.asks).push({id: offer.id, price: offer.price});
    }
    for (const tx of diff.txs) {
        market.txs.push(tx);
    }
    refreshDisplay();
});

uproot.onCustomEvent("OfferAccepted", event => {
    [traded, profit] = event.detail.data;
    refreshDisplay();
});

uproot.onReady(() => {
    uproot.invoke("get_market").then(newMarket => {
        market = newMarket;
        refreshDisplay();
    });

    // Prevent default form submission on Enter key in amount input
    const amountInput = I("amount");
    amountInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            makeOffer(true);
        }
    });
});
