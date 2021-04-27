class C32:
    state = 'A'
    def chat(self):
        if self.state == 'A':
            self.state = 'E'
            return 1
        elif self.state == 'B':
            self.state = 'C'
            return 3

        elif self.state == 'C':
            raise RuntimeError
        elif self.state == 'D':
            raise RuntimeError
        elif self.state == 'E':
            raise RuntimeError
        elif self.state == 'F':
            raise RuntimeError
        elif self.state == 'G':
            raise RuntimeError
        elif self.state == 'H':
            raise RuntimeError

    def coast(self):
        if self.state == 'A':
            self.state = 'B'
            return 0
        elif self.state == 'B':
            raise RuntimeError
        elif self.state == 'C':
            self.state = 'D'
            return 4
        elif self.state == 'D':
            self.state = 'E'
            return 5
        elif self.state == 'E':
            self.state = 'F'
            return 7
        elif self.state == 'F':
            self.state = 'F'
            return 10
        elif self.state == 'G':
            raise RuntimeError
        elif self.state == 'H':
            raise RuntimeError

    def fetch(self):
        if self.state == 'A':
            self.state = 'D'
            return 2
        elif self.state == 'B':
            raise RuntimeError
        elif self.state == 'C':
            raise RuntimeError
        elif self.state == 'D':
            self.state = 'G'
            return 6
        elif self.state == 'E':
            self.state = 'G'
            return 8
        elif self.state == 'F':
            self.state = 'G'
            return 9
        elif self.state == 'G':
            self.state = 'H'
            return 11
        elif self.state == 'H':
            raise RuntimeError