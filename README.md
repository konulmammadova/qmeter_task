### Code Cleanup and Execution

- Ensure type checking and correct import order.
- Clean up the code for readability.
- Run the `py` file after checking for any errors.

### Example HTML Template

```html
{% for branch in data %}
    <tr>
        <td rowspan="{{ branch.services|length }}">{{ branch.branch_name|default_if_none:"Branch name doesn't exist!" }}</td>
        {% if branch.services %}
            <tr>
                <td>{{ branch.services.0.service_name }}</td>
                <td>100*({{ branch.services.0.ones }}*10 + {{ branch.services.0.twos }}*5 + {{ branch.services.0.threes }}*0 + {{ branch.services.0.fours }}*-5 + {{ branch.services.0.fives }}*10)</td>
            </tr>
        {% endif %}
    </tr>
{% endfor %}
