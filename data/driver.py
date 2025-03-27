from selenium import webdriver
from selenium.webdriver.edge.service import Service

# from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.options import Options

# service = Service(executable_path=r"C:/SeleniumDrivers/Edge/msedgedriver.exe")
options= Options()

# service = Service(executable_path=r"C:/SeleniumDrivers/chromedriver.exe")
# options= webdriver.ChromeOptions()


options.add_argument('--log-level=3')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
options.add_argument("--window-size=1920,1080")
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument("--start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# driver = webdriver.Edge(service=service, options=options)
# driver = webdriver.Chrome(service=service, options=options)

driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)