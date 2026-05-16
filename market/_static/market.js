function priceFormatter(val) {
    const n = parseFloat(val);
    const sign = n < 0 ? "−" : "";
    return sign + "$" + Math.abs(n).toFixed(2);
}

function quantityFormatter(val) {
    const n = parseInt(val);
    const sign = n < 0 ? "−" : "";

    if (n != 1) {
        return sign + Math.abs(n) + " shares";
    }
    else {
        return sign + Math.abs(n) + " share";
    }
}

function marketApp() {
    return {
        book: { asks: [], bids: [] },
        trades: [],
        myOrders: [],
        cash: "0",
        stock: 0,
        orderType: "limit",
        orderSide: "buy",
        orderPrice: "",
        orderQty: "1",
        submitting: false,
        cancelling: null,
        error: "",

        init() {
            uproot.onReady(() => {
                uproot.invoke("get_state").then(state => {
                    this.book = state.book;
                    this.trades = state.trades;
                    this.myOrders = state.my_orders;
                    this.cash = state.cash;
                    this.stock = state.stock;
                });
            });

            uproot.onCustomEvent("MarketUpdate", event => {
                const data = event.detail.data;
                this.book = data.book;
                this.trades = data.trades;
                uproot.invoke("get_state").then(state => {
                    this.myOrders = state.my_orders;
                    this.cash = state.cash;
                    this.stock = state.stock;
                });
            });
        },

        spreadText() {
            if (this.book.asks.length > 0 && this.book.bids.length > 0) {
                const bestAsk = parseFloat(this.book.asks[0].price);
                const bestBid = parseFloat(this.book.bids[0].price);
                return "Spread: " + uproot.formatForInterface("price", (bestAsk - bestBid));
            }
            return "—";
        },

        submitOrder() {
            this.error = "";
            const qty = parseInt(this.orderQty);
            if (!qty || qty <= 0) {
                this.error = "Enter a valid quantity";
                return;
            }
            let price = null;
            if (this.orderType === "limit") {
                price = this.orderPrice;
                if (!price || parseFloat(price) <= 0) {
                    this.error = "Enter a valid price";
                    return;
                }
                price = parseFloat(price).toFixed(2);
            }

            this.submitting = true;
            uproot.invoke("submit_order", this.orderType, this.orderSide, price, qty)
                .then(result => {
                    this.cash = result.cash;
                    this.stock = result.stock;
                    this.orderPrice = "";
                    this.orderQty = "1";
                })
                .catch(err => {
                    this.error = err.message || String(err);
                })
                .finally(() => {
                    this.submitting = false;
                });
        },

        cancelOrder(orderId) {
            this.cancelling = orderId;
            uproot.invoke("cancel_order", orderId)
                .then(result => {
                    this.cash = result.cash;
                    this.stock = result.stock;
                })
                .catch(err => {
                    this.error = err.message || String(err);
                })
                .finally(() => {
                    this.cancelling = null;
                });
        }
    };
}
