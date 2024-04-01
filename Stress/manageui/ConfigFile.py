# author: zhangran
# createTime: 2024/4/1 13:47:14
# describe: 配置文件

url_path = "http://8.218.121.253/dap-manage/#/login"
driver_path = r"D:\\chromedriver_32_123\\chromedriver.exe"

no_sandbox = "--no-sandbox"
incognito = "--incognito"
disablegpu = "--disable-gpu"
maximized = "start-maximized"
automation = "enable-automation"
infobars = "--disable-infobars"
devshmusage = "--disable-dev-shm-usage"
browsernavigation = "--disable-browser-side-navigation"
NetworkServiceInProcess = "enable-features=NetworkServiceInProcess"

# 账号相关
user_name = "SuperManager"
pass_word = "123456"

# 登录
input_username = 'input[placeholder="user name"]'
input_password = 'input[placeholder="password"]'
click_btn = "el-button--primary"

# userOverview
data_body_xpath = "/html[1]/body[1]"
user_overview_xpath = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ul[1]/div[1]/div[1]/div[1]/li[1]/ul[1]/li[1]"
lab_overview_xpath = '/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ul[1]/div[1]/div[1]/div[1]/li[1]/ul[1]/li[2]'
operation_record_xpath = '/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[2]'
user_constomer_xpath = "//div[@id='tab-second']"
operation_record_cons_xpath = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]"

# LabOverview


# Resource Monitoring
resource_monitoring_xpath = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ul[1]/div[1]/div[1]/div[1]/li[2]/div[1]"
mirror_list_xpath = '/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ul[1]/div[1]/div[1]/div[1]/li[2]/ul[1]/li[1]'
dataset_list_xpath = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ul[1]/div[1]/div[1]/div[1]/li[2]/ul[1]/li[2]"
datasource_list_xpath = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ul[1]/div[1]/div[1]/div[1]/li[2]/ul[1]/li[3]"

# Lab Management
lab_management_xpath = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ul[1]/div[1]/div[1]/div[1]/li[3]/div[1]/span[1]"
case_list_xpath = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ul[1]/div[1]/div[1]/div[1]/li[3]/ul[1]/li[1]"
lab_list_xpath = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ul[1]/div[1]/div[1]/div[1]/li[3]/ul[1]/li[2]"

# Order Management
order_management_xpath = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ul[1]/div[1]/div[1]/div[1]/li[4]/div[1]"
trial_order_xpath = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ul[1]/div[1]/div[1]/div[1]/li[4]/ul[1]/li[1]"
subscription_order_xpath = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ul[1]/div[1]/div[1]/div[1]/li[4]/ul[1]/li[2]"

# User Management
user_management_xpath = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ul[1]/div[1]/div[1]/div[1]/li[5]/div[1]"
administrators_xpath = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ul[1]/div[1]/div[1]/div[1]/li[5]/ul[1]/li[1]"
customers_xpath = "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ul[1]/div[1]/div[1]/div[1]/li[5]/ul[1]/li[2]"
