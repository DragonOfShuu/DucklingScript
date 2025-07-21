from .token import Token


class Variable(Token):
    def init_token_vars(self):
        if self.env is not None:
            self.vars = self.env.var.all_vars
        else:
            self.vars = {}

        self.keywords = list(self.vars.keys())
        self.init_keyword_vars()

    def set_value(self, value: str):
        potential_value = self.vars.get(value)
        if potential_value is not None:
            self.value = potential_value.value
            return self.value

        raise ValueError(
            f"String {value} was recognized as a variable, but was not one."
        )
