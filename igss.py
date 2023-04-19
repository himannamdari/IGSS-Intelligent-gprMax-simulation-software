import subprocess
import os
import random

save_path = "C:\\Users\\himan\\gprMax\\user_models"
file_name = "simulation.in"
file_path = os.path.join(save_path, file_name)


def generate_file(title, x, y, z, dx, dy, dz, time_window, permittivity_range, permittivity_step, frequency, num_layers,
                  layer_depths):
    permittivity_indices = list(range(permittivity_range[0], permittivity_range[1], permittivity_step))
    p1 = random.choice(permittivity_indices)
    with open('simulation.in', 'w') as f:
        f.write(f"#title: {title}\n")
        f.write(f"#domain: {x} {y} {z}\n")
        f.write(f"#dx_dy_dz: {dx} {dy} {dz}\n")
        f.write(f"#time_window: {time_window:.2f}e-9\n")
        # f.write(f"#frequency: {frequency:.2f} Hz\n")
        f.write("#python:\n")
        f.write("import subprocess\n")
        f.write("import os\n")
        f.write("import random\n")
        f.write("from gprMax.input_cmd_funcs import *\n")
        f.write("import os\n")
        f.write("import numpy as np\n")
        f.write(f"indices = {permittivity_indices}\n")
        f.write(f"p1 = random.choice({permittivity_indices})\n")

        f.write("label_save_path = r'C:\\Users\\himan\\gprMax\\user_models\\NN'\n")
        f.write("name_of_file = 'labels'\n")
        f.write("completeName = os.path.join(label_save_path, name_of_file + '.txt')\n")
        f.write("file1 = open(completeName, 'a')\n")
        f.write("current_model_run = current_model_run\n")
        f.write("file1.write('{}: {}\\n'.format('{current_model_run}', p1))\n")

        f.write("file1.close()\n")
        f.write("#end_python:\n")
        f.write(f"#waveform: ricker 1 {frequency:.1f}e9 my_ricker\n")
        f.write(f"#hertzian_dipole: z {round((x / 2) - 0.02, 2)} {round(y - 0.15, 2)} 0 my_ricker\n")
        f.write(f"#rx: {round((x / 2) + 0.02, 2)} {round(y - 0.15, 2)} 0\n")

        for i in range(num_layers):
            if i == 0:
                f.write(f"#material: {random.choice(permittivity_indices)} 0 1 0 l{i + 1}\n")
                f.write(f"#box: 0 0 0 {x} {round(layer_depths[i],2)} {z} l{i + 1}\n")
            else:
                f.write(f"#material: {random.choice(permittivity_indices)} 0 1 0 l{i + 1}\n")
                f.write(f"#box: 0 0 0 {x} {round(sum(layer_depths[:i + 1]),2)} {z} l{i + 1}\n")


        f.write(f"#plate: 0 0 0 0 0.04 {dz} pec\n")
        f.write(f"#geometry_view: 0 0 0 {x} {y} {z} {dx} {dy} {dz} {title} n\n")
    print("Simulation file generated successfully!")
    os.system(f"start cmd /k conda activate gprMax && cd gprMax && python -m gprMax {file_path}")



def open_with_notepad(file_path):
    subprocess.Popen(["notepad.exe", file_path])
    return


from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form['title']
        x = float(request.form['x'])
        y = float(request.form['y'])
        z = float(request.form['z'])
        dx = float(request.form['dx'])
        dy = float(request.form['dy'])
        dz = float(request.form['dz'])
        time_window = float(request.form['time_window'])
        permittivity_range = [int(request.form['permittivity_range_start']),
                              int(request.form['permittivity_range_end'])]
        permittivity_step = int(request.form['permittivity_step'])
        frequency = float(request.form['frequency'])
        num_layers = int(request.form['num_layers'])
        layer_depths = [float(x) for x in request.form['layer_depths'].split(',')]
        generate_file(title, x, y, z, dx, dy, dz, time_window, permittivity_range, permittivity_step, frequency,
                      num_layers, layer_depths)
        file_path = os.path.abspath("simulation.in")
        open_with_notepad(file_path)
        return f"Thank you for using GPRMax software! Your simulation file has been saved in {file_path}"
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
