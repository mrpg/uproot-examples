uproot.simulate.on("custom_models/Ratings", (sim) => {
    sim.fill({ item: "Coffee", score: 8 });
    addRating();
});
