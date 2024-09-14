import typing
from ..models import TStep
from ..runner_new import SessionRunner
from ..step.step_api_requet import RunRequestStep
from ..models import TRequest
from ..step.step_loop_requet import RunLoopStep
from zerorunner.step.step_ui_requet import RunUiStep


class Step(object):
    def __init__(
            self,
            step: typing.Union[
                RunRequestStep,
                RunLoopStep,
                RunUiStep
            ],
    ):
        self.__step = step

    @property
    def request(self) -> TRequest:
        return self.__step.struct().request

    @property
    def retry_times(self) -> int:
        return self.__step.struct().retry_times

    @property
    def retry_interval(self) -> int:
        return self.__step.struct().retry_interval

    def struct(self) -> TStep:
        return self.__step.struct()

    @property
    def name(self) -> str:
        return self.__step.name()

    def type(self) -> str:
        return self.__step.type()

    def run(self, runner: SessionRunner, **kwargs):
        return self.__step.run(runner, **kwargs)
