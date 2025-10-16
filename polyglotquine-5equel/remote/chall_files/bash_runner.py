#!/usr/bin/env python3
from runner import Runner, run_script_in_sandbox


class BashRunner(Runner):
    """Runner for Bash"""

    def compile(self):
        """No compilation needed for Bash"""
        return True

    def run(self) -> bool:
        """Run Bash and check quine"""
        output, ret = run_script_in_sandbox(
            "/bin/bash", self.code, self.temp_dir, timeout=2, args=["--restricted"]
        )

        if output is None:
            print("bash code timed out")
            return False

        if ret != 0:
            print("Failed to run bash code")
            return False

        # Check if output matches input (quine check)
        if len(output) != len(self.code) or output != self.code:
            print("bash quine check failed")
            return False

        return True

    def cleanup(self):
        """No cleanup needed for Bash"""
        pass
