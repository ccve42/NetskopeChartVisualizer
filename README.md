Data utility CLI for Netskope
============================

![graph_example](/docs/images/202009_3.7.5.png)
[More examples](/docs/images)

Installation
------------
```
pip install .
```

Usage
-----
Usage: `ns-graph <tenant> <token> [flag]`<br/>
Type `ns-graph --help` to see a list of all options.

e.g.

To grab `application` event data and make graphs of the data:
```
ns-graph <tenant> <token> --type application
```

To grab `page` event data and make graphs of the data:
```
ns-graph <tenant> <token> --type page
```

You can skip the grab process by specifing data by its file name if you
already have the data:
```
ns-graph <tenant> <token> --load-json <file name>
```

To save only data but making the graph, add --save-only. This
only saves the data and does not proceed to make the graph:
```
ns-graph <tenant> <token> --save-only --save-as-json
```

Apply queries:
```
ns-graph <tenant> <token> --query 'access_method eq Client'
```

Misc
----
This program requires Python version 3.6 or above.

PNG outputs (graphs) are saved in `png` folder.  Excel outputs are saved
in `xlsx` folder.
