from zerorunner.models import TStep, TUiRequest
from zerorunner.models import TConfig
from zerorunner.runner_new import SessionRunner
from zerorunner.step.step import Step
from zerorunner.step.step_ui_requet import RunUiStep
from zerorunner.ext.zero_driver.driver import DriverSetting, ZeroDriver

if __name__ == '__main__':
    runner = SessionRunner()
    runner.config = TConfig(
        name="test",
    )

    step1 = TStep(
        name="test",
        step_type="ui",
        ui_request=TUiRequest(
            action="open",
            data="https://www.baidu.com"
        )
    )
    step2 = TStep(
        name="test2",
        step_type="ui",
        ui_request=TUiRequest(
            action="input",
            location_method="xpath",
            location_value="//input[@id='kw']",
            data="哈哈哈11211",
        )
    )
    step_list = [Step(RunUiStep(step1)), Step(RunUiStep(step2))]

    driver_setting = DriverSetting(
        executable_path=r'E:\fastapi\test-autotest\zerorunner\ext\zero_driver\chromedriver.exe',
        headless=False
    )
    driver_app = ZeroDriver(driver_setting)
    runner.zero_driver = driver_app
    for step in step_list:
        runner.run_step(step)
    # driver_app.get_screenshot('file', "test.png")
    # driver_app.driver.quit()
