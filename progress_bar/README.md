# progress\_bar

## Using a global progress bar

Copy `ProjectBody.html` into your **project's** main folder. This will globally include the progress bar in all your configs.

## Using a page-specific progress bar

Copy `ProjectBody.html` to an **app** (rename it to `Progress.html`) and, within your HTML files, do

```jinja
{% block main %}

{% include "rounds/Progress.html" %}

…

{% endblock main %}
```

where you replace `rounds` by your app’s name.
