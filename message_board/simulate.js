uproot.simulate.on("message_board/Board", (sim) => {
    sim.fill({ body: "Hello from the simulator!" });
    addPost();
});
