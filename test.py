import yaml
import pprint
from config_loader import ConfigLoader

# read common values ----------------------------------------------------------

print('begin test...')

config = ConfigLoader.configure()
kp_value = config["kros"]["motor"]["pid_controller"]["kp"]
if not isinstance(kp_value, float):
    raise TypeError('kp was not a float value.')
print("\nkp: '{}'".format(kp_value))

calibrate_value = config["kros"]["motor"]["slew_limiter"]["calibrate"]
if not isinstance(calibrate_value, bool):
    raise TypeError('calibrate was not a boolean value.')
print("\ncalibrate: '{}'".format(calibrate_value))

# re-parse imported string ----------------------------------------------------
yaml_data = pprint.pretty_print(config, return_text=True)
print('\nyaml type: {}'.format(type(yaml_data)))

print('\nparse imported configuration…')
dog_food = yaml.parse(yaml_data)
print('\ndog food: {}'.format(dog_food))

# dump ------------------------------------------------------------------------
print('\ndump with indent of 4:\n')
yaml.dump(config)

_file_path = 'output.yaml'
print("\ndump to file '{}' with indent of 2:\n".format(_file_path))
yaml.dump(config, file_path=_file_path, indent=2)

print('complete.')
