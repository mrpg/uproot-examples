const asksContainer = I("asks");
const bidsContainer = I("bids");
const txsContainer = I("txs");

function refreshDisplay() {
    if (!traded) {
        I("not-traded").style.display = "block";
        I("traded").style.display = "none";

        if (offerAmount !== null) {
            I("current-offer").textContent = offerAmount.toFixed(2);
            document.querySelectorAll(".has-offer").forEach(el => el.style.display = "unset");
            document.querySelectorAll(".no-offer").forEach(el => el.style.display = "none");
        }
        else {
            document.querySelectorAll(".has-offer").forEach(el => el.style.display = "none");
            document.querySelectorAll(".no-offer").forEach(el => el.style.display = "unset");
        }
    }
    else {
        I("profit").textContent = profit.toFixed(2);
        I("not-traded").style.display = "none";
        I("traded").style.display = "block";
    }

    asksContainer.innerHTML = "";
    bidsContainer.innerHTML = "";
    txsContainer.innerHTML = "";

    market.asks.sort((a, b) => a.price - b.price).forEach(offer => {
        const badge = document.createElement("span");
        badge.className = "badge bg-danger me-1 mb-1";
        badge.textContent = offer.price.toFixed(2);

        if (buyer) {
            badge.onclick = () => acceptOffer(offer.id);
            badge.setAttribute("role", "button");
            badge.setAttribute("tabindex", "0");
            badge.setAttribute("aria-label", `Accept ask offer at price ${offer.price.toFixed(2)}`);
            badge.onkeypress = (e) => {
                if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    acceptOffer(offer.id);
                }
            };
        } else {
            badge.setAttribute("aria-label", `Ask price ${offer.price.toFixed(2)}`);
        }

        asksContainer.appendChild(badge);
    });

    market.bids.sort((a, b) => b.price - a.price).forEach(offer => {
        const badge = document.createElement("span");
        badge.className = "badge bg-success me-1 mb-1";
        badge.textContent = offer.price.toFixed(2);

        if (!buyer) {
            badge.onclick = () => acceptOffer(offer.id);
            badge.setAttribute("role", "button");
            badge.setAttribute("tabindex", "0");
            badge.setAttribute("aria-label", `Accept bid offer at price ${offer.price.toFixed(2)}`);
            badge.onkeypress = (e) => {
                if (e.key === "Enter" || e.key === " ") {
                    e.preventDefault();
                    acceptOffer(offer.id);
                }
            };
        } else {
            badge.setAttribute("aria-label", `Bid price ${offer.price.toFixed(2)}`);
        }

        bidsContainer.appendChild(badge);
    });

    market.txs.sort((a, b) => b.time - a.time).forEach(tx => {
        const badge = document.createElement("span");
        badge.className = "badge bg-uproot me-1 mb-1";
        badge.textContent = tx.price.toFixed(2);
        badge.setAttribute("aria-label", `Transaction completed at price ${tx.price.toFixed(2)}`);

        txsContainer.appendChild(badge);
    });
}

function makeOffer(newOffer) {
    let amount = null;

    if (newOffer) {
        amount = parseFloat(I("amount").value);
    }

    const buttons = document.querySelectorAll("#not-traded button");
    buttons.forEach(btn => btn.disabled = true);

    uproot.invoke("make_offer", amount).then((newAmount) => {
        offerAmount = newAmount;
        refreshDisplay();
    }).catch().finally(() => {
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
    }).catch().finally(() => {
        badges.forEach(badge => badge.style.pointerEvents = "");
    });
}

uproot.onCustomEvent("OffersAndTxs", event => {
    market = event.detail.data;
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
