import glob


from src.utils.helpers import get_filename


class DuplicateHandler(object):

    def __init__(self, out_path):
        self.out_path = out_path + "/*"
        self.processed_files = set()
        self.find_processed_files()

    def find_processed_files(self):
        for file in glob.glob(self.out_path, recursive=True):
            filename = get_filename(file)
            self.processed_files.add(filename)

    def is_duplicate(self, filename):
        if filename in self.processed_files:
            return True
        else:
            return False


def main():
    file_path = "../../files/tests/videos/**/*.mov"
    out_path = "../../../files/tests/videos/opensmile/"

    dh = DuplicateHandler(out_path)
    print(dh.processed_files)

    for file in glob.glob(file_path, recursive=True):
        print(file)

        filename = get_filename(file)

        if dh.is_duplicate(filename):
            print("file: " + filename + " is duplicate")
        else:
            print("file: " + filename + " is original")


if __name__ == "__main__":
    main()


