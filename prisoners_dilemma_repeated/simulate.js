// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

if (uproot.currentPage == "prisoners_dilemma_repeated/Dilemma") {
    if (Math.random() < 0.5) {
        I("cooperate-0").checked = true;
    }
    else {
        I("cooperate-1").checked = true;
    }

    uproot.submit();
}

if (uproot.currentPage == "prisoners_dilemma_repeated/Results") {
    // uproot.submit();
}
