#!/usr/bin/env python3
import os
import subprocess
from runner import Runner, run_script_in_sandbox


class AsmRunner(Runner):
    """Runner for x64 Assembly"""

    def __init__(self, code: bytes, temp_dir: str):
        super().__init__(code, temp_dir)
        self.code_file = os.path.join(temp_dir, "program.asm")
        self.obj_file = os.path.join(temp_dir, "out.o")
        self.bin_file = os.path.join(temp_dir, "asm_bin")

    def compile(self):
        """Compile assembly with nasm and ld"""

        # Write code to file
        with open(self.code_file, 'wb') as f:
            f.write(self.code)

        # Assemble
        nasm_ret = subprocess.run(
            ["/usr/bin/nasm", "-f", "elf64", self.code_file, "-o", self.obj_file],
            capture_output=True
        )
        if nasm_ret.returncode != 0:
            return False

        # Link
        ld_ret = subprocess.run(
            ["/usr/bin/ld", "-o", self.bin_file, self.obj_file],
            capture_output=True
        )
        if ld_ret.returncode != 0:
            return False
        
        # delete intermediate files + code
        if os.path.exists(self.obj_file):
            os.remove(self.obj_file)
        if os.path.exists(self.code_file):
            os.remove(self.code_file)

        os.chmod(self.bin_file, 0o755)
        return True

    def run(self) -> bool:
        """Run assembly binary and check quine"""
        exec_name = "/" + os.path.basename(self.bin_file)
        output, ret = run_script_in_sandbox(exec_name, None, self.temp_dir, timeout=2)

        if output is None:
            print("assembly code timed out")
            return False

        if ret != 0:
            print("Failed to run assembly code")
            return False

        # Check if output matches input (quine check)
        if len(output) != len(self.code) or output != self.code:
            print("assembly quine check failed")
            return False

        return True

    def cleanup(self):
        """Clean up files"""
        try:
            if os.path.exists(self.bin_file):
                os.remove(self.bin_file)
        except:
            pass
