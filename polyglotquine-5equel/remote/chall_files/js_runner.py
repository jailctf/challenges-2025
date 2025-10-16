#!/usr/bin/env python3
from runner import Runner, run_script_in_sandbox


class JsRunner(Runner):
    """Runner for JavaScript (Node.js)"""

    def compile(self):
        """No compilation needed for JS"""
        return True

    def run(self) -> bool:
        """Run JavaScript and check quine"""
        output, ret = run_script_in_sandbox(
            "/usr/bin/node", self.code, self.temp_dir, timeout=2
        )

        if output is None:
            print("js code timed out")
            return False

        if ret != 0:
            print("Failed to run js code")
            return False

        # Check if output matches input (quine check)
        if len(output) != len(self.code) or output != self.code:
            print("js quine check failed")
            return False

        return True

    def cleanup(self):
        """No cleanup needed for JS"""
        pass
