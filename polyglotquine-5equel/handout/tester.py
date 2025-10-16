import subprocess
import base64
import tempfile
import os

"""
NOTE: This is not the file that is being run on remote. This is only being provided for convenience.

To make the challenge as cheese-proof as possible, the real source code will not be provided.
I didn't want to have people guessing though, so I have provided this handout as a tester for your code.

If your solution **does not use any cheese strats** and works on this handout, then it should work on remote.
If it does not work on remote, open a ticket, ping @oh_word, and send your code.

For clarification, an example cheese strat would be reading the source code written on disk and printing it out.
It may work in this handout, but it will not work on remote.

A full testing environment has been provided for you in the handout Dockerfile. It has all the languages
installed and ready to use for this file.

Good luck
"""

code = base64.b64decode(input("Base64 encoded code > "))

def runner(args, language):
    global code
    TIMEOUT = 2.0

    try:
        # only stdout matters, if anything gets output to stderr it will be ignored
        proc = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=TIMEOUT
        )

        if proc.returncode != 0:
            raise subprocess.CalledProcessError(proc.returncode, args)

        # checks for full equality, beware of rogue newlines in your output
        assert proc.stdout == code
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to run {language} code")
    except subprocess.TimeoutExpired:
        print(f"{language} code timed out")
    except AssertionError:
        print(f"{language} quine check failed")
    except Exception as e:
        print(f"Unknown exception: {e}")

    return False

with tempfile.TemporaryDirectory() as temp_dir:
    prg = tempfile.NamedTemporaryFile(delete=False)
    prg.write(code)
    prg.close()

    # compile assembly
    asm_obj = f"{temp_dir}/out.o"
    asm_bin = f"{temp_dir}/asm_bin"

    nasm_ret = subprocess.call(
        ["nasm", "-f", "elf64", prg.name, "-o", asm_obj],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    if nasm_ret != 0:
        print("Failed to compile assembly")
        exit()

    ld_ret = subprocess.call(
        ["ld", "-o", asm_bin, asm_obj],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    if ld_ret != 0:
        print("Failed to link assembly output")
        exit()

    # compile C#
    cs_output_dir = f"{temp_dir}/out"
    cs_bin_name = "csbin"
    os.makedirs(cs_output_dir, exist_ok=True)

    # copy to .cs file for C# compilation (thanks microsoft for requiring this)
    cs_file = f"{temp_dir}/program.cs"
    with open(cs_file, 'wb') as f:
        f.write(code)

    dotnet_ret = subprocess.call(
        ["/dotnet-bin/dotnet", "build", "--nologo", "--no-dependencies",
         "-c", "Release", "-o", cs_output_dir,
         f"-p:AssemblyName={cs_bin_name}", cs_file],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    if dotnet_ret != 0:
        print("Failed to build C#")
        exit()

    cs_bin = f"{cs_output_dir}/{cs_bin_name}"

    if (
        runner([asm_bin], "assembly") and \
        runner([cs_bin], "C#") and \
        runner(["guile", prg.name], "scheme") and \
        runner(["node", prg.name], "js") and \
        runner(["bash", "--restricted", prg.name], "bash")
    ):
        print("You win! jail{fake_flag}")
    else:
        print("You lose!")
