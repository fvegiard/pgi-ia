import os

from pipeline import run


def main():
    data_dir = os.getenv("DATA_DIR", "/data")
    run(data_dir)


if __name__ == "__main__":
    main()