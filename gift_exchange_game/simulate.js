// The use of this file is optional. What you write here will run whenever
// player pages load in sessions created with the "Simulate responses" option
// enabled, allowing you to check whether your experiment works as intended.

if (uproot.currentPage == "gift_exchange_game/SetWage") {
    var wage = (1 + Math.random() * 9).toFixed(2);
    I("wage").value = wage;
    uproot.submit();
}

if (uproot.currentPage == "gift_exchange_game/ChooseEffort") {
    var efforts = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0];
    var effort = efforts[Math.floor(Math.random() * efforts.length)];
    I("effort").value = effort;
    uproot.submit();
}

if (uproot.currentPage == "gift_exchange_game/Results") {
    // uproot.submit();
}
