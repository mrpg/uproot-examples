# die\_roll

The die-roll honesty task (Fischbacher & Föllmi-Heusi, 2013). Participants roll a die in private and report the outcome. Reporting a 1–5 pays that amount in dollars; reporting a 6 pays nothing.

By design, the actual rolls happen entirely in the participant's browser and are **never transmitted to the server** — unobservability is the point of the paradigm. Lying can therefore only be detected at the aggregate level: the admin digest compares the distribution of reports against the uniform distribution expected under truthful reporting.

Load this app using

```python
load_config(uproot_server, config="die_roll", apps=["die_roll"])
```
