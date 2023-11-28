import subprocess
import re

class Connector:
    def __init__(self):
        pass

    # Usage: pass a path to ovpn file as string
    def connect(self, profile):
        if (profile != ''):
            self._run_command(f"openvpn3 session-start --config {profile}")

    # Usage: pass a path to ovpn file as string
    def disconnect(self, profile):
        if (profile != ''):
            self._run_command(f"openvpn3 session-manage --config {profile} --disconnect")

    # Usage: pass a path to ovpn file as string
    def get_stats(self, profile):
        if (profile != ''):
            result = self._run_command(f"openvpn3 session-stats --config {profile}")
            stats = {'BYTES_IN': None, 'BYTES_OUT': None, 'PACKETS_IN': None, 'PACKETS_OUT': None}
            if 'Connection statistics:' in result:
                for name in ['BYTES_IN', 'BYTES_OUT', 'PACKETS_IN', 'PACKETS_OUT']:
                    stats[name] = self._search_and_extract(name, result)
            return stats

    # @internal
    def _search_and_extract(self, name, search):
        pattern = r'{}\.+([0-9]+)'.format(re.escape(name))
        match = re.search(pattern, search)
        if match:
            return int(match.group(1))
        else:
            return None

    # @internal
    def _run_command(self, command):
        try:
            result = subprocess.run(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                # No log yet
                return f"Error: {result.stderr.strip()}"
        except Exception as e:
            # No log yet
            return f"Exception: {str(e)}"
