from flask import Flask, requests
import logging
from flask_cors import CORS
from client import Endpoint

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

@app.route('/help', methods=['GET'])
def routes_info():
    """Show all registered routes with endpoints and methods."""
    routes = []

    rules = list(app.url_map.iter_rules())
    if not rules:
        logging.warning("No routes were registered.")
        return  {"results": routes}

    ignored_methods = set()

    rules = sorted(rules, key=lambda rule: sorted(rule.methods))  # type: ignore

    rule_methods = [
        ", ".join(sorted(rule.methods - ignored_methods))  # type: ignore
        for rule in rules
    ]

    headers = ("Endpoint", "Methods", "Rule")
    widths = (
        max(len(rule.endpoint) for rule in rules),
        max(len(methods) for methods in rule_methods),
        max(len(rule.rule) for rule in rules),
    )
    widths = [max(len(h), w) for h, w in zip(headers, widths)]
    row = "{{0:<{0}}}  {{1:<{1}}}  {{2:<{2}}}".format(*widths)

    routes.append(row.format(*headers).strip())
    routes.append(row.format(*("-" * width for width in widths)))

    for rule, methods in zip(rules, rule_methods):
        routes.append(row.format(rule.endpoint, methods, rule.rule).rstrip())
    return  {"results": routes}

@app.route('/dog')
def get_all():
    results = endpoint.get_all()
    return {'results': results}

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

if __name__ == "__main__":
    endpoint = Endpoint()
    app.run(host ='0.0.0.0', port = 5000, debug = True)
