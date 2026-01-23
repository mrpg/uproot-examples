# sumhunt

Load this app using

```python
load_config(uproot_server, config="sumhunt", apps=["sumhunt"])
```

This app implements a real effort task similar to the one described in:

> Thomas Buser, Muriel Niederle, Hessel Oosterbeek; [Can Competitiveness Predict Education and Labor Market Outcomes? Evidence from Incentivized Choice and Survey Measures.](https://direct.mit.edu/rest/article/doi/10.1162/rest_a_01439/120192/Can-Competitiveness-Predict-Education-and-Labor) The Review of Economics and Statistics, 2024.

Among other things, the grid size (default: 3x3), target number (default: 100), and number of terms (default: 2) are configurable.

*Note*: Incorrect submissions do not advance participants to the next matrix.

*Note*: All participants see the same matrices over time (though the matrices themselves are generated on the fly). This is possible thanks to [a special feature](https://github.com/mrpg/uproot/commit/b493f6e00ed0b25a3012ca30e6d6d083055a6ae3) in uproot that allows you to save a `random.Random` object in a player field. Thanks, uproot.
