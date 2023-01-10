import csv

from flask import Flask, render_template, request

# from fairpy imporrt fairpy
from fairpy.fairpy.items.two_players_fair_division import *


class Agents:
    agent_1 = ""
    agent_2 = ""
    num_items = 0
    items = []
    numbers = []


app = Flask(__name__)
agent = Agents()


@app.route('/use')
def form():
    return render_template('form.html', inputs=[])


@app.route('/form', methods=['POST'])
def submitted_form():
    errors = []
    if request.method == 'POST':
        num_inputs = request.form['num_items']
        agent1_name = request.form['Agent1']
        agent2_name = request.form['Agent2']
        if not agent1_name:
            errors.append('Agent 1 name is required.')
        if not agent2_name:
            errors.append('Agent 2 name is required.')
        if not errors:
            agent.num_items = int(num_inputs)
            agent.agent_1 = agent1_name
            agent.agent_2 = agent2_name
            inputs = []
            numbers = []
            for i in range(int(agent.num_items)):
                inputs.append({'name': 'input' + str(i), 'value': '', 'index': i})
                numbers.append(i + 1)
            agent.numbers = numbers
            agent.items = inputs
            return render_template('form_2.html', inputs=inputs, agent1_name=agent1_name, agent2_name=agent2_name,
                                   num_items=numbers)
        return render_template('form.html', errors=errors)


@app.route('/form_2', methods=['POST'])
def submitted_form_2():
    errors = []
    if request.method == 'POST':
        items = []
        a_scores = {}
        b_scores = {}
        a_score = 0
        b_score = 0
        for i in range(int(agent.num_items)):
            item = request.form[f'item{i}']
            if not item:
                errors.append(f'Item number {i} is missing.')
            else:
                items.append(item)
            if i in range(len(items)):
                temp_a = request.form[f'1_{i}']
                a_score += int(temp_a)
                a_scores[str(items[i])] = int(temp_a)
                temp_b = request.form[f'2_{i}']
                b_score += int(temp_b)
                b_scores[str(items[i])] = int(temp_b)
        # print(items, a_score, b_score, sum(agent.numbers))
        if a_score != sum(agent.numbers):
            errors.append(f'Agent 1 has wrong scores, each score must occur only once.')
        if b_score != sum(agent.numbers):
            errors.append(f'Agent 2 has wrong scores, each score must occur only once.')
        if not errors:
            Alice = fairpy.agents.AdditiveAgent(a_scores, name=agent.agent_1)
            George = fairpy.agents.AdditiveAgent(b_scores, name=agent.agent_2)
            res_sequential = sequential([Alice, George], items.copy())
            res_restricted_simple = restricted_simple([Alice, George], items.copy())
            res_singles_doubles = singles_doubles([Alice, George], items.copy())
            res_iterated_singles_doubles = iterated_singles_doubles([Alice, George], items.copy())
            res_s1 = s1([Alice, George], items.copy())
            res_l1 = l1([Alice, George], items.copy())
            res_top_down = top_down([Alice, George], items.copy())
            res_top_down_alternating = top_down_alternating([Alice, George], items.copy())
            res_bottom_up = bottom_up([Alice, George], items.copy())
            res_bottom_up_alternating = bottom_up_alternating([Alice, George], items.copy())
            res_trump = trump([Alice, George], items.copy())
            return render_template('submitted_form.html', agent_1=agent.agent_1, agent_2=agent.agent_2,
                                   sequential=res_sequential, restricted_simple=res_restricted_simple,
                                   singles_doubles=res_singles_doubles,
                                   iterated_singles_doubles=res_iterated_singles_doubles,
                                   s1=res_s1, l1=res_l1, top_down=res_top_down,
                                   top_down_alternating=res_top_down_alternating,
                                   bottom_up=res_bottom_up, bottom_up_alternating=res_bottom_up_alternating,
                                   trump=res_trump)
        return render_template('form_2.html', errors=errors, agent1_name=agent.agent_1, agent2_name=agent.agent_2,
                               num_items=agent.numbers, inputs=agent.items)


@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('main.html')


@app.route('/use', methods=['GET', 'POST'])
def use_page():
    return render_template('use.html')


@app.route('/about', methods=['GET', 'POST'])
def about_page():
    return render_template('about.html')


@app.route('/links', methods=['GET', 'POST'])
def links_page():
    return render_template('links.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    return render_template('upload.html')


@app.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files['file']
    # if file.filename == '':
    #     # No file was selected
    #     return 'No file selected'
    # if file and allowed_file(file.filename):
    with open(file.filename, 'r') as csv_file:
        # Read the contents of the file into a list of rows
        rows = []
        reader = csv.reader(csv_file)
        # print(reader)
        for row in reader:
            # print(row)
            rows.append(row)
        # Process the rows and do something with them
        items, Alice, George = process_rows(rows)
        res_sequential = sequential([Alice, George], items.copy())
        res_restricted_simple = restricted_simple([Alice, George], items.copy())
        res_singles_doubles = singles_doubles([Alice, George], items.copy())
        res_iterated_singles_doubles = iterated_singles_doubles([Alice, George], items.copy())
        res_s1 = s1([Alice, George], items.copy())
        res_l1 = l1([Alice, George], items.copy())
        res_top_down = top_down([Alice, George], items.copy())
        res_top_down_alternating = top_down_alternating([Alice, George], items.copy())
        res_bottom_up = bottom_up([Alice, George], items.copy())
        res_bottom_up_alternating = bottom_up_alternating([Alice, George], items.copy())
        res_trump = trump([Alice, George], items.copy())
        return render_template('submitted_form.html', agent_1=Alice.name(), agent_2=George.name(),
                               sequential=res_sequential, restricted_simple=res_restricted_simple,
                               singles_doubles=res_singles_doubles,
                               iterated_singles_doubles=res_iterated_singles_doubles,
                               s1=res_s1, l1=res_l1, top_down=res_top_down,
                               top_down_alternating=res_top_down_alternating,
                               bottom_up=res_bottom_up, bottom_up_alternating=res_bottom_up_alternating,
                               trump=res_trump)


def allowed_file(filename):
    # print(filename)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'


def process_rows(rows):
    # print(rows)
    items = rows[0][1:]
    name_a = rows[1][0]
    name_b = rows[2][0]
    agent_a_valuations = rows[1][1:]
    agent_b_valuations = rows[2][1:]
    agent_a_dict = {}
    agent_b_dict = {}
    for i in range(len(items)):
        agent_a_dict[str(items[i])] = int(agent_a_valuations[i])
        agent_b_dict[str(items[i])] = int(agent_b_valuations[i])

    Alice = fairpy.agents.AdditiveAgent(agent_a_dict, name=name_a)
    George = fairpy.agents.AdditiveAgent(agent_b_dict, name=name_b)
    return items, Alice, George


if __name__ == '__main__':
    app.run(debug=True)
