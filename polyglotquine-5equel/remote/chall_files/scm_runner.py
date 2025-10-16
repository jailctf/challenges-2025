#!/usr/bin/env python3
import os
import subprocess
from runner import Runner, run_script_in_sandbox


class ScmRunner(Runner):
    """Runner for Scheme (Guile)"""

    def __init__(self, code: bytes, temp_dir: str):
        super().__init__(code, temp_dir)
        self.source_file = os.path.join(temp_dir, "scheme_code.scm")
        self.compiled_file = os.path.join(temp_dir, "scheme_code.go")

    def compile(self):
        """Compile Scheme code with guild"""
        # Write code to file
        with open(self.source_file, 'wb') as f:
            f.write(self.code)

        guild_ret = subprocess.run(
            ["/usr/bin/guild", "compile", "-o", self.compiled_file, self.source_file],
            capture_output=True
        )

        if guild_ret.returncode != 0:
            return False

        # remove source file so people can't read it
        if os.path.exists(self.source_file):
            os.remove(self.source_file)

        return True

    def run(self) -> bool:
        """Run compiled Scheme and check quine"""
        output, ret = run_script_in_sandbox(
            "/usr/bin/guile", None, self.temp_dir, timeout=2,
            args=["-c", '(load-compiled "/scheme_code.go")']
        )

        if output is None:
            print("scheme code timed out")
            return False

        if ret != 0:
            print("Failed to run scheme code")
            return False

        # Check if output matches input (quine check)
        if len(output) != len(self.code) or output != self.code:
            print("scheme quine check failed")
            return False

        return True

    def cleanup(self):
        """Clean up temporary files"""
        try:
            if os.path.exists(self.compiled_file):
                os.remove(self.compiled_file)
        except:
            pass
