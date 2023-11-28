import os
import shutil
import json

class Profiler:
    def __init__(self):
        self.profiles = []
        self._config_folder_path = os.path.expanduser(f"~/.config/wolfopenvpnclient/")
        self._configs_folder_path = os.path.join(self._config_folder_path, 'configs')
        self._configs_file_path = os.path.join(self._config_folder_path, 'configs.json')
        self._check_config_folder()
        # Read the 'configs.json' file and load profiles on init
        try:
            with open(self._configs_file_path, 'r') as config_file:
                self.profiles = json.load(config_file)
        except FileNotFoundError:
            pass

    # @internal
    # Ensure that config structure exist, or create it
    def _check_config_folder(self):
        os.makedirs(self._config_folder_path, exist_ok=True)
        os.makedirs(self._configs_folder_path, exist_ok=True)
        if not os.path.isfile(self._configs_file_path):
            with open(self._configs_file_path, 'w') as config_file:
                json.dump([], config_file)

    # Returns profiles list of dictionaries {name='str', path='path/to/ovpn'}
    def get_profiles(self):
        return self.profiles

    # Saves profile {name='str', path='path/to/ovpn'} by copy the ovpn file
    # to config folder and add this dict to configs.json
    def save_profile(self, profile):
        # copy the config to the app configs folder
        file_name = os.path.basename(profile['path'])
        destination_path = os.path.join(self._configs_folder_path, file_name)
        shutil.copyfile(profile['path'], destination_path)
        # assign new profile
        new_profile = {"name": profile['name'], "path": destination_path}
        self.profiles.append(new_profile)
        # saving profiles to configs.json
        with open(self._configs_file_path, 'w') as config_file:
            json.dump(self.profiles, config_file, indent=2)

    # Delete a profile by its name from the self.profiles, configs.json and  removes according config file
    def delete_profile_by_name(self, profile_name):
        for profile in self.profiles:
            if profile["name"] == profile_name:
                # removing file from configs folder
                file_path = profile["path"]
                if os.path.isfile(file_path):
                    os.remove(file_path)
                # removing profile from list and save updated list to configs.json
                self.profiles.remove(profile)
                with open(self._configs_file_path, 'w') as config_file:
                    json.dump(self.profiles, config_file, indent=2)
                return
        print(f"Profile with name '{profile_name}' not found.")

    # Returns profile {name='str', path='path/to/ovpn'} by provided name or return None if not found
    def get_profile_by_name(self, profile_name):
        for profile in self.profiles:
            if profile['name'] == profile_name:
                return profile
        return None
