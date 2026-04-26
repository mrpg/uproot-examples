// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

if (uproot.currentPage == "twobytwo/Instructions") {
    uproot.submit();
}

if (uproot.currentPage == "twobytwo/Decision") {
    if (Math.random() < 0.5) {
        I("choice-0").checked = true;
    }
    else {
        I("choice-1").checked = true;
    }

    uproot.submit();
}

if (uproot.currentPage == "twobytwo/Results") {
    // uproot.submit();
}
