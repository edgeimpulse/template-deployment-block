import argparse, json, os, shutil, zipfile, threading

# parse arguments (--metadata FILE is passed in)
parser = argparse.ArgumentParser(description='Custom deploy block demo')
parser.add_argument('--metadata', type=str)
args = parser.parse_args()

# load the metadata.json file
with open(args.metadata) as f:
  metadata = json.load(f)

# now we have two folders 'metadata.folders.input' - this is where all the SDKs etc are,
# and 'metadata.folders.output' - this is where we need to write our output
input_dir = metadata['folders']['input']
app_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'app')
output_dir = metadata['folders']['output']

print('Copying files to build directory...')

is_copying = True
def print_copy_progress():
  if (is_copying):
    threading.Timer(2.0, print_copy_progress).start()
    print("Still copying...")
print_copy_progress()

# create a build directory, the input / output folders are on network storage so might be very slow
build_dir = '/tmp/build'
if os.path.exists(build_dir):
  shutil.rmtree(build_dir)
os.makedirs(build_dir)

# copy in the data from both 'input' and 'app' folders
os.system('cp -r ' + input_dir + '/* ' + build_dir)
print(app_dir)
os.chdir(build_dir)
print(os.listdir())
os.system('cp -r ' + app_dir + '/* ' + build_dir)
print(os.listdir())

is_copying = False

print('Copying files to build directory OK')
print('')

print('Compiling application...')

is_compiling = True
def print_compile_progress():
  if (is_compiling):
    threading.Timer(2.0, print_compile_progress).start()
    print("Still compiling...")
print_compile_progress()

# then invoke Make
os.system('make -f Makefile.tflite')

is_compiling = False

print('Compiling application OK')

# ZIP the build folder up, and copy to output dir
if not os.path.exists(output_dir):
  os.makedirs(output_dir)
shutil.make_archive(os.path.join(output_dir, 'deploy'), 'zip', os.path.join(build_dir, 'build'))