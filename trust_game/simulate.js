// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

if (uproot.currentPage == "trust_game/Send") {
    I("sent").value = "6";
    uproot.submit();
}

if (uproot.currentPage == "trust_game/Return") {
    I("returned").value = "7";
    uproot.submit();
}

if (uproot.currentPage == "trust_game/Results") {
    // uproot.submit();
}
