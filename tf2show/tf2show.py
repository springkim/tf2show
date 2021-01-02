import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import tensorflow as tf
import openpyxl
import subprocess
import sys


def hw4show():
    if sys.platform == "linux" or sys.platform == "linux2":
        cpu_name = subprocess.check_output(f'lscpu | grep "Model name:"', shell=True).decode('utf-8').split(':')[1].strip()
        cpu_core = subprocess.check_output(f'lscpu | grep "CPU(s):"', shell=True).decode('utf-8').split('\n')[0].split(':')[1].strip()
        cpu_threads_per_core = subprocess.check_output(f'lscpu | grep "Thread(s) per core:"', shell=True).decode('utf-8').split(':')[1].strip()
        print(f"CPU: {cpu_name} {cpu_core}C/{int(cpu_core) * int(cpu_threads_per_core)}T")
        mem_size = subprocess.check_output(f'cat /proc/meminfo | grep "MemTotal:"', shell=True).decode('utf-8').split(':')[1].split()[0]
        print(f"RAM: {int(mem_size) / 1024 / 1024:.2f} GB")
    elif sys.platform == "win32":
        cpu_name = subprocess.check_output(f'wmic cpu get name | findstr CPU"', shell=True).decode('utf-8').strip()
        cpu_core = subprocess.check_output(f'wmic cpu get numberofcores', shell=True).decode('utf-8').split('\n')[1]
        cpu_threads = os.environ["NUMBER_OF_PROCESSORS"]
        print(f"CPU: {cpu_name} {int(cpu_core)}C/{int(cpu_threads)}T")
        rams = subprocess.check_output(f'wmic memorychip get capacity', shell=True).decode('utf-8').split('\n')[1:-1]
        rams = list(map(lambda x: x.strip("\r "), rams))
        total_ram = 0
        for ram in rams:
            if len(ram) != 0:
                total_ram += int(ram)
        print(f"RAM: {int(total_ram) // 1024 // 1024 // 1024 :.2f} GB")

    for device in tf.config.list_physical_devices('GPU'):
        id = device.name.split(':')[-1]
        infos = subprocess.check_output(f'nvidia-smi --query-gpu=name,memory.total --format=csv,noheader -i {id}',
                                        shell=True).decode('utf-8').split(',')
        print(f'GPU: {infos[0]}, {int(infos[1].split()[0]) / 1024:.1f} GB')


"""
CPU: Intel(R) Xeon(R) CPU @ 2.00GHz 2C/4T
RAM: 15.64 GB
GPU: Tesla P100-PCIE-16GB, 15.9 GB
"""


def tf2show(model, excel_file_name=""):
    if excel_file_name != "":
        write_wb = openpyxl.Workbook()
        write_ws = write_wb.active
    header_layer = "LAYER"
    header_name = "NAME"
    header_C = "C"
    header_H = "H"
    header_W = "W"
    header_inputs = "INPUTS"
    len_layer = len(header_layer)
    len_name = len(header_name)
    len_c = len(header_C)
    len_h = len(header_H)
    len_w = len(header_W)
    len_inputs = len(header_inputs)
    for i, l in enumerate(model.layers):
        str_layer = str(type(l)).replace("'", "").strip("<>").split('.')[-1]
        str_name = l.name
        output_shape = l.output_shape[0] if len(l.output_shape) == 1 else l.output_shape
        c = ""
        h = ""
        w = ""
        if len(output_shape) >= 3:
            c = str(output_shape[3])
            h = str(output_shape[2])
        w = str(output_shape[1])
        if type(l.input) is list:
            prevs = [pl.name.split('/')[0] for pl in l.input]
            prevs = ', '.join(map(str, prevs))
        else:
            prevs = l.input.name.split('/')[0]

        len_layer = max(len_layer, len(str_layer))
        len_name = max(len_name, len(str_name))
        len_c = max(len_c, len(c))
        len_h = max(len_h, len(h))
        len_w = max(len_w, len(w))
        len_inputs = max(len_inputs, len(prevs))
    if excel_file_name == "":
        header = f"| {header_layer:{len_layer}} | {header_name:{len_name}} | {header_C:{len_c}} | {header_H:{len_h}} | {header_W:{len_w}} | {header_inputs:{len_inputs}} |"
        print("-" * len(header))
        print(header)
        print("-" * len(header))
    for i, l in enumerate(model.layers):
        str_layer = str(type(l)).replace("'", "").strip("<>").split('.')[-1]
        str_name = l.name
        output_shape = l.output_shape[0] if len(l.output_shape) == 1 else l.output_shape
        c = ""
        h = ""
        w = ""
        if len(output_shape) >= 3:
            c = str(output_shape[3])
            h = str(output_shape[2])
        w = str(output_shape[1])
        if type(l.input) is list:
            prevs = [pl.name.split('/')[0] for pl in l.input]
            prevs = ', '.join(map(str, prevs))
        else:
            prevs = l.input.name.split('/')[0]
        if excel_file_name != "":
            write_ws.append([str_layer, str_name, c, h, w, prevs])
        else:
            print(f"| {str_layer:{len_layer}} | {str_name:{len_name}} | {c:{len_c}} | {h:{len_h}} | {w:{len_w}} | {prevs:{len_inputs}} |")
    if excel_file_name != "":
        column_widths = []
        for row in write_ws:
            for i, cell in enumerate(row):
                if len(column_widths) > i:
                    if len(cell.value) + 1 > column_widths[i]:
                        column_widths[i] = len(cell.value) + 1
                else:
                    column_widths += [len(cell.value) + 1]

        for i, column_width in enumerate(column_widths):
            write_ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = column_width
        write_wb.save(excel_file_name)
    else:
        print("-" * len(header))


if __name__ == "__main__":
    hw4show()
    sys.exit(0)
    models = [
        tf.keras.applications.DenseNet121,
        tf.keras.applications.DenseNet169,
        tf.keras.applications.DenseNet201,
        tf.keras.applications.InceptionResNetV2,
        tf.keras.applications.InceptionV3,
        tf.keras.applications.MobileNet,
        tf.keras.applications.MobileNetV2,
        tf.keras.applications.NASNetMobile,
        tf.keras.applications.NASNetLarge,
        tf.keras.applications.VGG16,
        tf.keras.applications.VGG19,
        tf.keras.applications.Xception,
        tf.keras.applications.ResNet50,
        tf.keras.applications.ResNet101,
        tf.keras.applications.ResNet152,
        tf.keras.applications.ResNet50V2,
        tf.keras.applications.ResNet101V2,
        tf.keras.applications.ResNet152V2,
        tf.keras.applications.EfficientNetB0,
        tf.keras.applications.EfficientNetB1,
        tf.keras.applications.EfficientNetB2,
        tf.keras.applications.EfficientNetB3,
        tf.keras.applications.EfficientNetB4,
        tf.keras.applications.EfficientNetB5,
        tf.keras.applications.EfficientNetB6,
        tf.keras.applications.EfficientNetB7
    ]
    # for model in models:
    #    m = model(input_shape=(512, 256, 3), include_top=True, weights=None)
    #    tf2show(m)
    m = tf.keras.applications.MobileNet(input_shape=(256, 256, 3), include_top=True, weights=None)
    m.summary()
    tf2show(m)
