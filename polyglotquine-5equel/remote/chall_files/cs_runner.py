#!/usr/bin/env python3
import os
import subprocess
import shutil
from runner import Runner, run_script_in_sandbox


class CsRunner(Runner):
    """Runner for C#"""

    def __init__(self, code: bytes, temp_dir: str):
        super().__init__(code, temp_dir)
        self.code_file = os.path.join(temp_dir, "program.cs")
        self.output_dir = os.path.join(temp_dir, "out")
        self.bin_name = "ihatecsharpsomuchwhydididothistomyself"
        self.bin_file = os.path.join(self.output_dir, self.bin_name)

    def compile(self):
        """Compile C# with dotnet"""
        # Write code to file
        with open(self.code_file, 'wb') as f:
            f.write(self.code)

        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)

        dotnet_env = {
            "DOTNET_ROOT": "/dotnet-bin",
            "DOTNET_NOLOGO": "true",
            "DOTNET_SKIP_FIRST_TIME_EXPERIENCE": "true",
            "DOTNET_CLI_TELEMETRY_OPTOUT": "true",
            "DOTNET_CLI_WORKLOAD_UPDATE_NOTIFY_DISABLE": "true",
            "DOTNET_RUNNING_IN_CONTAINER": "1",
            "DOTNET_ADD_GLOBAL_TOOLS_TO_PATH": "0",
            "DOTNET_EnableDiagnostics": "0",
            "DOTNET_EnableDiagnostics_Profiler": "0",
            "DOTNET_CLI_HOME": "/tmp/.dotnet",
            "HOME": "/tmp"
        }

        dotnet_ret = subprocess.run(
            ["/dotnet-bin/dotnet", "build", "--nologo", "--no-dependencies",
             "-c", "Release", "-o", self.output_dir,
             f"-p:AssemblyName={self.bin_name}", self.code_file],
            env=dotnet_env,
            capture_output=True
        )

        if dotnet_ret.returncode != 0:
            print("Failed to build C#")
            return False

        # delete code file so people can't read it
        if os.path.exists(self.code_file):
            os.remove(self.code_file)

        return True

    def run(self) -> bool:
        """Run C# binary and check quine"""
        exec_name = f"/out/{self.bin_name}"
        output, ret = run_script_in_sandbox(
            exec_name, None, self.temp_dir, timeout=2,
            env={"DOTNET_ROOT": "/dotnet-bin"},
            copy_dotnet=True,
            cs_output_dir=self.output_dir
        )

        if output is None:
            print("C# code timed out")
            return False

        if ret != 0:
            print("Failed to run C# code")
            return False

        # Check if output matches input (quine check)
        if len(output) != len(self.code) or output != self.code:
            print("C# quine check failed")
            return False

        return True

    def cleanup(self):
        """Clean up temporary files"""
        try:
            if os.path.exists(self.output_dir):
                shutil.rmtree(self.output_dir)
        except:
            pass
