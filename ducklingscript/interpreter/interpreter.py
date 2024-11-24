from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol
from pathlib import Path

from quackinter import Interpreter as QuackInterpreter
from quackinter.commands.command import Command as QuackinterCommand
from quackinter.config import Config as QuackinterConfig

from ducklingscript import (
    DucklingCompiler,
    CompileOptions,
    WarningsObject,
    DucklingScriptError,
)
from ..compiler.compiler import Compiled

if TYPE_CHECKING:
    from quackinter.stack import Stack as QuackinterStack
    from quackinter.line import Line as QuackinterLine


class AfterCompilationHandler(Protocol):
    def __call__(
        self, warnings: WarningsObject | None, error: DucklingScriptError | None
    ) -> bool | None:
        ...


class WhileInterpretationHandler(Protocol):
    def __call__(
        self,
        line_count: int,
        total_lines: int,
        stack: "QuackinterStack",
        line: "QuackinterLine",
    ) -> bool | None:
        ...


class OnFailSafeHandler(Protocol):
    def __call__(self) -> Any:
        ...


class OnInternalError(Protocol):
    def __call__(self, error: Exception) -> Any:
        ...


class EmptyCallable(Protocol):
    """
    Provided to eliminate
    unnecessary type
    checking.
    """

    def __call__(self, *args: Any, **kwds: Any) -> None:
        return


class DucklingInterpreter:
    """
    An interpreter for the DucklingScript
    language.

    Uses chainable events and event handlers
    to let you provide feedback to users
    on progress during compilation &
    interpretation.
    """

    def __init__(
        self,
        extended_commands: list[type[QuackinterCommand]] | None = None,
        quack_config: QuackinterConfig | None = None,
        compile_options: CompileOptions | None = None,
    ) -> None:
        self._after_compilation_handler: AfterCompilationHandler | EmptyCallable = (
            lambda: None
        )
        self._while_interpretation_handler: WhileInterpretationHandler | EmptyCallable = (
            lambda: None
        )
        self._on_fail_safe_handler: OnFailSafeHandler | EmptyCallable = lambda: None
        self.compiled: Compiled | None = None
        while_tick_command = self._create_tick_interpreter_command()
        self.compiler = DucklingCompiler(options=compile_options)
        self.interpreter = QuackInterpreter(
            extended_commands=[while_tick_command]
            if extended_commands is None
            else [*extended_commands, while_tick_command],
            include_builtins=True,
            config=quack_config,
        )

    def interpret_file(self, file: Path):
        """
        Compile a file, and interpret it.
        """
        try:
            compiled = self.compiler.compile_file(file)
        except DucklingScriptError as e:
            self._after_compilation_handler(None, e)
            return
        except Exception as e:
            self._on_internal_error_handler(e)
            return

        self.compiled = compiled
        self._after_compilation_handler(compiled.warnings, None)
        try:
            return_data = self.interpreter.interpret_text("\n".join(compiled.output))
        except Exception as e:
            self._on_internal_error_handler(e)
            return

        # Sourcemaps may or may not
        # be available at this point,
        # but that doesn't matter because
        # we'll avoid using sourcemaps,
        # and we'll find the error by
        # looking at the compiled code.
        if return_data.error:
            # Ran out of time
            # Remaining: create error from self.compiled
            pass

    def _create_tick_interpreter_command(self):
        this_interpreter = self

        class InterpretTickCommand(QuackinterCommand):
            names = []

            def tick(self, stack: "QuackinterStack", line: "QuackinterLine") -> None:
                assert (
                    this_interpreter.compiled is not None
                ), "The code must be compiled before we can interpret"

                this_interpreter._while_interpretation_handler(
                    line.line_num, len(this_interpreter.compiled.output), stack, line
                )

            def execute(self, stack: "QuackinterStack", cmd: str, data: str) -> None:
                return None

        return InterpretTickCommand

    def after_compilation(
        self, handler: AfterCompilationHandler
    ) -> DucklingInterpreter:
        self._after_compilation_handler = handler
        return self

    def while_interpretation(
        self, handler: WhileInterpretationHandler
    ) -> DucklingInterpreter:
        self._while_interpretation_handler = handler
        return self

    def on_fail_safe(self, handler: OnFailSafeHandler) -> DucklingInterpreter:
        self._on_fail_safe_handler = handler
        return self

    def on_internal_error(self, handler: OnInternalError) -> DucklingInterpreter:
        self._on_internal_error_handler = handler
        return self
