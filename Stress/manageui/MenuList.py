# author: zhangran
# createTime: 2024/4/17 13:59:17
# describe: 根据不同用户操作不同菜单
import time

from Stress.manageui.DataOverview import DataOview
from Stress.manageui.LabManagement import CaseLab
from Stress.manageui.OrderManagement import Order
from Stress.manageui.ResourceMonitor import ResourceMoni
from Stress.manageui.UserManagement import Administrators


def menuListByUser(driver, username, password):
    # 超管-SuperAdmin
    if username == "SuperManager" and password == "123456":
        # Data Overview模块
        DataOview.userLabOvew(driver)

        # Resource Monitoring模块
        ResourceMoni.MirrorDatasetSource(driver, username)

        # Lab Management模块
        CaseLab.CaseLab(driver, username)

        # Order Management 模块
        Order.TrialSubscition(driver, username)

        # User Management模块
        Administrators.AdminiCoustmer(driver, username)
    # ACRC Administrators角色
    elif username == "testACRC" and password == "123456":
        # Resource Monitoring模块
        ResourceMoni.MirrorDatasetSource(driver, username)

        # Lab Management模块
        CaseLab.CaseLab(driver, username)

        # Order Management 模块
        Order.TrialSubscition(driver, username)

        # User Management模块
        Administrators.AdminiCoustmer(driver, username)
    # 系统管理员 - System Administrators
    elif username == "admin@1.com" and password == "123456":
        # Data Overview模块
        DataOview.userLabOvew(driver)

        # Resource Monitoring模块
        ResourceMoni.MirrorDatasetSource(driver, username)

        # Lab Management模块
        CaseLab.CaseLab(driver, username)

        # Order Management 模块
        Order.TrialSubscition(driver, username)

        # User Management模块
        Administrators.AdminiCoustmer(driver, username)
    #  IT Support角色
    elif username == "testIT" and password == "123456":
        # Resource Monitoring模块
        ResourceMoni.MirrorDatasetSource(driver, username)

        # Lab Management模块
        CaseLab.CaseLab(driver, username)
    else:
        print("出现其他未知角色，请确认！")
        driver.execute_script("alert('出现其他未知角色，请确认！');")
        time.sleep(5)
    driver.close()
