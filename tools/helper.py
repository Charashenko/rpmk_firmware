import os, sys, argparse, subprocess, time

DISK_LABEL = "RPI-RP2"

COMMANDS = [
    "build",
    "clean",
    "install",
    "nuke",
    "repl",
    "reset",
    "run",
    "setup",
    "test",
]


def _get_dev():
    cmd = f"lsblk -fs | grep '{DISK_LABEL}' | awk " + "'{ print $1 }'"
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    return output.decode().strip()


def _mnt(directory):
    device = _get_dev()
    if not device:
        print("Device not found")
        sys.exit(1)
    print(f"Mounting device '/dev/{device}' to '{directory}'")
    if os.system(f"mount /dev/{device} {directory}"):
        print("Mounting failed")
        sys.exit(1)
    print("Successfully mounted")


def _umnt(directory):
    print(f"Unmounting directory '{directory}'")
    if os.system(f"umount {directory}"):
        print(f"Failed to umount directory '{directory}'")
        sys.exit(1)


def _arg_not_supplied(arg, cmd):
    print(f"{arg} must be supplied when running '{cmd}'")
    sys.exit(1)


def build(args):
    if not args.mpy_cross_tool:
        _arg_not_supplied("--mpy_cross_tool", args.command)
    if not args.build:
        _arg_not_supplied("-b", args.command)
    if not args.source:
        _arg_not_supplied("-s", args.command)
    print("Cleaning build directory")
    build_dir = args.build[:-1] if args.build[-1] == "/" else args.build
    source_dir = args.source[:-1] if args.source[-1] == "/" else args.source
    os.system(f"rm -rf {build_dir}/*")
    print("Creating .mpy files")
    os.system(f"python {args.mpy_cross_tool} -o {build_dir}/{source_dir} {source_dir}")


def clean(args):
    if not args.rshell_commands_dir:
        _arg_not_supplied("--rshell_commands_dir", args.command)
    print("Cleaning files")
    rshell_dir = (
        args.rshell_commands_dir[:-1]
        if args.rshell_commands_dir[-1] == "/"
        else args.rshell_commands_dir
    )
    os.system(f"rshell -f {rshell_dir}/clean.rshell")


def install(args):
    if not args.lib:
        _arg_not_supplied("-l", args.command)
    if not args.rshell_commands_dir:
        _arg_not_supplied("--rshell_commands_dir", args.command)
    clean(args)
    rshell_dir = (
        args.rshell_commands_dir[:-1]
        if args.rshell_commands_dir[-1] == "/"
        else args.rshell_commands_dir
    )
    os.system(f"rshell -f {rshell_dir}/install.rshell")


def nuke(args):
    if not args.nuke_uf2:
        _arg_not_supplied("-n", args.command)
    if not args.mount:
        _arg_not_supplied("-m", args.command)
    _mnt(args.mount)
    print("Nuking the device")
    os.system(f"cp -v {args.nuke_uf2} {args.mount}")
    print("Nuke in progress")
    while _get_dev():
        time.sleep(0.1)
    while not _get_dev():
        time.sleep(0.1)
    print("Done")
    _umnt(args.mount)


def repl(args):
    if not args.rshell_commands_dir:
        _arg_not_supplied("--rshell_commands_dir", args.command)
    rshell_dir = (
        args.rshell_commands_dir[:-1]
        if args.rshell_commands_dir[-1] == "/"
        else args.rshell_commands_dir
    )
    os.system(f"rshell -f {rshell_dir}/repl.rshell")


def reset(args):
    nuke(args)
    setup(args)
    build(args)
    install(args)


def run(args):
    if not args.rshell_commands_dir:
        _arg_not_supplied("--rshell_commands_dir", args.command)
    build(args)
    install(args)
    rshell_dir = (
        args.rshell_commands_dir[:-1]
        if args.rshell_commands_dir[-1] == "/"
        else args.rshell_commands_dir
    )
    os.system(f"rshell -f {rshell_dir}/repl.rshell")


def setup(args):
    if not args.firmware:
        _arg_not_supplied("-f", args.command)
    if not args.mount:
        _arg_not_supplied("-m", args.command)
    _mnt(args.mount)
    print(f"Flashing the device with '{args.firmware}'")
    os.system(f"cp -v {args.firmware} {args.mount}")
    print("Flashing in progress")
    while _get_dev():
        time.sleep(0.1)
    print("Done")
    _umnt(args.mount)


def test(args):
    pass


def main():
    parser = argparse.ArgumentParser(
        prog="RPMK_Helper",
        description="Small helper script to make development of RPMK faster",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Action to execute, can be:
- build = Builds .mpy files from the source folder
- clean = Cleans the device's file system (without nuking)
- install = Installs built .mpy files and main.py to the device
- nuke = Nukes the devices with specified firmware
- repl = Open REPL on the device
- reset = Reset the devices (runs: nuke, setup, build and install)
- run = Runs the 'build' and 'install' commands
- setup = Uploads the specified firmware to device

Run this script in the root directory of the project
        """,
    )

    parser.add_argument(
        "command",
        choices=COMMANDS,
        help="Action to be executed",
    )
    parser.add_argument(
        "-f",
        "--firmware",
        help="Path to the firmware to be installed",
    )
    parser.add_argument(
        "-n",
        "--nuke_uf2",
        help="Path to the nuke firmware",
    )
    parser.add_argument(
        "-l",
        "--lib",
        help="Path to the folder with libraries to be installed",
    )
    parser.add_argument(
        "-b",
        "--build",
        help="Path to directory in which build files will be saved",
    )
    parser.add_argument(
        "-m",
        "--mount",
        help="Mount point for device",
    )
    parser.add_argument(
        "--mpy_cross_tool",
        help="Path to the micropython's mpy_cross_all.py tool",
    )
    parser.add_argument(
        "-s",
        "--source",
        help="Source directory",
    )
    parser.add_argument(
        "--rshell_commands_dir",
        help="Path to the directory containing rshell instruction files",
    )

    args = parser.parse_args(sys.argv[1:])

    if args.command == "build":
        build(args)
    elif args.command == "clean":
        clean(args)
    elif args.command == "install":
        install(args)
    elif args.command == "nuke":
        nuke(args)
    elif args.command == "repl":
        repl(args)
    elif args.command == "reset":
        reset(args)
    elif args.command == "run":
        run(args)
    elif args.command == "setup":
        setup(args)
    elif args.command == "test":
        test(args)


if __name__ == "__main__":
    main()
