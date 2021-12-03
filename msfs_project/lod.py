class MsfsLod:
    min_size: int
    model_file: str

    def __init__(self, min_size, model_file):
        self.min_size = int(min_size)
        self.model_file = model_file
