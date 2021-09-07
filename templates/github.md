{% extends "main.md" %}
{% block content %}

Full documentation can be found at [https://v0tools.stev0.me](https://v0tools.stev0.me)

### Commands
{% for name, dval in coll.items() %}
* *[{{ name }}]({{dval["url"]}})*
    * {{dval["single"]}}
{% endfor %}

### License
See: [LICENSE](./LICENSE)
{% endblock %}
