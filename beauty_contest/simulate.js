// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

if (uproot.currentPage == "beauty_contest/Guess") {
    I("guess").value = "33";
    uproot.submit();
}

if (uproot.currentPage == "beauty_contest/Results") {
    // uproot.submit();
}
