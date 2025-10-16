#!/usr/bin/env python3
import os
import subprocess
import shutil
from abc import ABC, abstractmethod


def run_script_in_sandbox(interpreter, script_content: bytes, sandbox_dir, timeout=2, env=None, args=None, copy_dotnet=False, cs_output_dir=None):
    """Run a script with an interpreter in nsjail sandbox"""

    # Ensure sandbox_dir is traversable
    os.chmod(sandbox_dir, 0o755)

    # Copy system libraries into sandbox (only if not already done)
    lib_dest = os.path.join(sandbox_dir, "lib")
    if os.path.exists("/lib") and not os.path.exists(lib_dest):
        shutil.copytree("/lib", lib_dest, symlinks=True)
        # Make all directories and files readable by everyone
        for root, dirs, files in os.walk(lib_dest):
            for d in dirs:
                os.chmod(os.path.join(root, d), 0o755)
            for f in files:
                os.chmod(os.path.join(root, f), 0o755)

    usr_dest = os.path.join(sandbox_dir, "usr")
    usr_lib_dest = os.path.join(sandbox_dir, "usr", "lib")
    if os.path.exists("/usr/lib") and not os.path.exists(usr_lib_dest):
        os.makedirs(usr_dest, exist_ok=True)
        os.chmod(usr_dest, 0o755)
        shutil.copytree("/usr/lib", usr_lib_dest, symlinks=True)
        # Make all directories and files readable by everyone
        for root, dirs, files in os.walk(usr_lib_dest):
            for d in dirs:
                os.chmod(os.path.join(root, d), 0o755)
            for f in files:
                os.chmod(os.path.join(root, f), 0o755)

    # Copy /usr/bin for interpreters
    usr_bin_dest = os.path.join(sandbox_dir, "usr", "bin")
    if os.path.exists("/usr/bin") and not os.path.exists(usr_bin_dest):
        os.makedirs(usr_dest, exist_ok=True)
        shutil.copytree("/usr/bin", usr_bin_dest, symlinks=True)
        # Make all directories and files readable and executable by everyone
        for root, dirs, files in os.walk(usr_bin_dest):
            for d in dirs:
                try:
                    os.chmod(os.path.join(root, d), 0o755)
                except (FileNotFoundError, OSError):
                    pass  # Skip broken symlinks
            for f in files:
                fpath = os.path.join(root, f)
                try:
                    # Only chmod if the file actually exists (not a broken symlink)
                    if os.path.exists(fpath):
                        os.chmod(fpath, 0o755)
                except (FileNotFoundError, OSError):
                    pass  # Skip broken symlinks or other errors

    # Copy /bin for bash and other binaries
    bin_dest = os.path.join(sandbox_dir, "bin")
    if os.path.exists("/bin") and not os.path.exists(bin_dest):
        shutil.copytree("/bin", bin_dest, symlinks=True)
        # Make all directories and files readable and executable by everyone
        for root, dirs, files in os.walk(bin_dest):
            for d in dirs:
                try:
                    os.chmod(os.path.join(root, d), 0o755)
                except (FileNotFoundError, OSError):
                    pass  # Skip broken symlinks
            for f in files:
                fpath = os.path.join(root, f)
                try:
                    # Only chmod if the file actually exists (not a broken symlink)
                    if os.path.exists(fpath):
                        os.chmod(fpath, 0o755)
                except (FileNotFoundError, OSError):
                    pass  # Skip broken symlinks or other errors

    # Create a writable /tmp directory for the sandboxed process
    tmp_dir = os.path.join(sandbox_dir, "tmp")
    os.makedirs(tmp_dir, exist_ok=True)
    os.chmod(tmp_dir, 0o777)  # Make it world-writable so user 99999 can write to it

    # For C#, copy dotnet runtime
    dotnet_dest = os.path.join(sandbox_dir, "dotnet-bin")
    if copy_dotnet and cs_output_dir and not os.path.exists(dotnet_dest):
        shutil.copytree("/dotnet-bin", dotnet_dest, symlinks=True)
        # Make all directories and files readable by everyone
        for root, dirs, files in os.walk(dotnet_dest):
            for d in dirs:
                os.chmod(os.path.join(root, d), 0o755)
            for f in files:
                os.chmod(os.path.join(root, f), 0o755)

    nsjail_cmd = [
        "nsjail",
        "--mode", "o",
        "--user", "99999",
        "--group", "99999",
        "--disable_clone_newnet",
        "--disable_clone_newipc",
        "--disable_clone_newuts",
        "--disable_clone_newpid",
        "--disable_clone_newuser",
        "--disable_clone_newcgroup",
        "--disable_clone_newns",
        "--disable_proc",
        "--rlimit_as", "4096",
        "--rlimit_cpu", str(timeout),
        "--rlimit_fsize", "10000000",
        "--rlimit_nofile", "100",
        "--rlimit_nproc", "100",
        "--chroot", sandbox_dir,
    ]

    # Add environment variables if provided
    if env:
        for key, value in env.items():
            nsjail_cmd.extend(["--env", f"{key}={value}"])

    nsjail_cmd.extend([
        "--",
        interpreter,
    ])

    if args:
        nsjail_cmd.extend(args)

    try:
        proc = subprocess.run(
            nsjail_cmd,
            input=script_content if script_content else None,
            capture_output=True,
            timeout=timeout,
            text=False
        )
        
        return proc.stdout, proc.returncode
    except subprocess.TimeoutExpired:
        return None, -1


class Runner(ABC):
    """Base class for language runners"""

    def __init__(self, code: bytes, temp_dir: str):
        self.code = code
        self.temp_dir = temp_dir

    @abstractmethod
    def compile(self):
        """Compile the code if necessary. Returns True on success, False on failure."""
        pass

    @abstractmethod
    def run(self) -> bool:
        """Run the code and check if output matches (quine check). Returns True if passed."""
        pass

    @abstractmethod
    def cleanup(self):
        """Clean up any temporary files created during compilation/execution."""
        pass
