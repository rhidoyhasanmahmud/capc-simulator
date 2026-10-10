from capc_sim.cli import main

if __name__ == "__main__":
    raise SystemExit(main(["pilot", *__import__("sys").argv[1:]]))
