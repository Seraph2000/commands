import json
from pprint import pprint

global responses

coords = {}

class Commands():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.coords = {}

    def set_coords(self):
        self.coords = {"x": str(self.x), "y": str(self.y)}
        return self.coords

    def forward(self):
        y = int(coords["y"]) + 1
        self.coords.update({"y": str(y)})
        return self.coords

    def left(self):
        x = int(coords["x"]) - 1
        self.coords.update({"x": str(x)})
        return self.coords

    def right(self):
        x = int(coords["x"]) + 1
        self.coords.update({"x": str(x)})
        return self.coords

    def back_to_base(self):
        self.coords.update({"x":"0", "y":"0"})
        return self.coords

def track(index):
    if index >= 20:
        return False
    else:
        return True
       
def read_commands(command_file):
    with open(command_file) as f:
        data = json.load(f)
    rover_name = list(data.keys())[0]
    initial_position = data[rover_name][0]['position']
    commands = data[rover_name]
    commands = [command['command'] for command in commands[1:]]
    return (rover_name, initial_position, commands)
        

def write_response(file_name, data):
    with open(file_name, 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def gen_initial_response(results, response_line):
    rover_name = results[0]
    intial_coords = results[1]
    x = intial_coords["x"]
    y = intial_coords["y"]
    deploy = Commands(x, y)
    coords = deploy.set_coords()
    response = {}
    response.update({"rover-id": rover_name})
    response.update({"position": coords})
    response.update({"direction": "north"})
    response_line.write(str(response))
    response_line.write('\n')

def gen_responses(commands, responses, response_line):

    for command in commands:
        if command == 'move-forward':
            res = {}
            position = deploy.forward()
            res["rover-id"] = rover_name
            res["position"] = position
            res["direction"] = "north"
            response_line.write(str(res))
            response_line.write('\n')
        elif command == 'turn-left':
            res = {}
            position = deploy.left()
            res["rover-id"] = rover_name
            res["position"] = position
            res["direction"] = "east"
            response_line.write(str(res))
            response_line.write('\n')
        elif command == 'turn-right':
            res = {}
            r_position = deploy.right()
            res["rover-id"] = rover_name
            res["position"] = r_position
            res["direction"] = "west"
            response_line.write(str(res))
            response_line.write('\n')
        else:
            print("something went wrong!")
    response_line.close()
    return responses
    
def create_json_object(rover_name, responses):
    json_obj = {}
    json_obj = {
        rover_name: responses
    }
    return json_obj

def write_json_obj(rover_name, responses):
    json_obj = create_json_object(rover_name, responses)
    write_response(str(rover_name) + '_response.json', json_obj)


def open_write_file(rover_name):
    response_line = open(str(rover_name) + '_response.txt', 'a+')
    return response_line




if __name__ == '__main__':
    # edit initial coordinates
    deploy = Commands(3, 3)
    coords = deploy.set_coords()
    # edit command filename
    results = read_commands('1AFC_commands.json')
    rover_name = results[0]
    initial_position = results[1]
    commands = results[2]
    response_line = open_write_file(rover_name)
    responses = gen_initial_response(results, response_line)
    gen_responses(commands, responses, response_line)
    
