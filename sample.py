import time
import traceback
import webbrowser

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def main():
    cloud_name = "<<cloud_url>>"
    token = "<<security_token>>"

    options = Options()
    options.platform_name = "Windows"
    options.browser_version = "latest"

    options.set_capability("perfecto:platformVersion", "10")
    options.set_capability("perfecto:location", "US East")
    options.set_capability("perfecto:resolution", "1024x768")
    options.set_capability("perfecto:securityToken", token)

    # Initialize the Selenium driver
    driver = webdriver.Remote(
        command_executor="https://" + cloud_name + ".perfectomobile.com/nexperience/perfectomobile/wd/hub",
        options=options,
    )

    # set page load timeout
    driver.set_page_load_timeout(60)

    error = None
    timeout = 30
    wait = WebDriverWait(driver, timeout)

    test_start(driver, "Selenium Python Web Sample")
    driver.get("https://www.google.com")

    ##
    #############################
    ### Your test starts here. If you test a different url, you need to modify the test steps accordingly. ###
    #############################
    ##

    search = "perfectomobile"

    try:
        step_start(driver, "Accept cookies if prompted")
        link_elements = driver.find_elements(By.LINK_TEXT, "Cookies")
        if len(link_elements) > 0:
            button_elements = driver.find_elements(By.XPATH, "//button[div[string-length(text()) > 0]]")
            if len(button_elements) > 0:
                accept_button = button_elements[len(button_elements) - 1]
                driver.execute_script("arguments[0].scrollIntoView()", accept_button)
                driver.execute_script("arguments[0].click()", accept_button)
        step_end(driver)

        step_start(driver, "Search for " + search)
        search_input = wait.until(EC.presence_of_element_located((By.NAME, "q")))
        search_input.send_keys(search)
        form = wait.until(EC.presence_of_element_located((By.XPATH, "//form[@role=\'search\']")))
        driver.execute_script("arguments[0].submit()", form)
        step_end(driver)

        step_start(driver, "Navigate to Perfecto")
        href = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href,\'www.perfecto.io\')]")))
        driver.get(href.get_attribute("href"))
        step_end(driver)

        step_start(driver, "Verify Perfecto page load")
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[@alt=\'Home\']")))
        step_end(driver)

        step_start(driver, "Press back")
        driver.back()
        time.sleep(3)
        step_end(driver)

        step_start(driver, "Verify Title")
        expected_text = search + " - Google"
        assert expected_text in driver.title
        step_end(driver)
    except AssertionError as ae:
        error = traceback.format_exc()
        step_assert(driver, error)
        step_end(driver)
    except Exception as e:
        error = traceback.format_exc()

    ##
    #############################
    ### Your test ends here. ###
    #############################
    ##

    test_end(driver, error)
    report_url = driver.capabilities.get(
        'testGridReportUrl') + "&onboardingJourney=automated&onboardingDevice=desktopWeb"

    # Quits the driver
    driver.quit()

    print("\nOpen this link to continue with the guide: " + report_url + "\n")

    # Launch browser with the Report URL
    webbrowser.open(report_url)


################################################################################
# HELPER FUNCTIONS
################################################################################

def test_start(driver, test_name):
    driver.execute_script("mobile:test:start", {"name": test_name})


def test_end(driver, error):
    params = {
        "success": False if error != None else True,
        "failureDescription": error
    }
    driver.execute_script("mobile:test:end", params)


def step_start(driver, step_name):
    driver.execute_script("mobile:step:start", {"name": step_name})


def step_end(driver):
    driver.execute_script("mobile:step:end")


def step_assert(driver, message):
    driver.execute_script("mobile:status:assert", {
        "status": False, "message": message})


################################################################################
# MAIN ENTRY POINT
################################################################################

if __name__ == '__main__':
    main()
