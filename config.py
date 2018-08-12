from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

#profile = webdriver.FirefoxProfile()
#profile.set_preference('network.proxy.type', 1)
#profile.set_preference('network.proxy.http', '117.127.0.205')
#profile.set_preference('network.proxy.http_port', 80)
#profile.set_preference('network.proxy.ssl', '117.127.0.205')
#profile.set_preference('network.proxy.ssl_port', 80)
#profile.update_preferences()
#browser = webdriver.Firefox(profile)

match_total = 0
def get_webdriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    return webdriver.Chrome(chrome_options=chrome_options)
