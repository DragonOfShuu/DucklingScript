from .token import Token


class Variable(Token):
    def init_token_vars(self):
        self.vars = self.environ.all_vars
        self.keywords = list(self.vars.keys())
        self.init_keyword_vars()

    def set_value(self, value: str):
        if value not in self.vars:
            raise ValueError(
                f"String {value} was recognized as a variable, but was not one."
            )
        self.value = self.vars.get(value)
