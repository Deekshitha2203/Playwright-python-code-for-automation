from playwright.sync_api import Page
import os
import logging
import tomli
from datetime import datetime
def restore(page: Page):

    PATHL=os.getcwd()+"/"
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d %H:%M:%S").replace('-', '_').replace(':', '_').replace(' ', '_')
    print("Restoring ORG Utilit 9!")
    try:
        button_restore = page.locator(".restore-button", has_text="Restore Instance")
        button_restore_page = page.locator(".restore", has_text="Restore")
        print("Org is Down: ", button_restore.is_visible())
        page.screenshot(path=PATHL+date_string+"restore_1.jpg")
        page.keyboard.press("Escape")
        org_down = button_restore.is_visible()
        org_down_p = button_restore_page.is_visible()
        if org_down:
            button_restore.click()
            page.screenshot(path=PATHL+date_string+"restore_2.jpg")
            print("Clicked Button Restore  ", button_restore.is_visible())
            confirm_restore = page.locator(".successInvite", has_text="Restore")
            if confirm_restore.is_visible():
                confirm_restore.click()
                page.screenshot(path=PATHL+date_string+"restore_3.jpg")
        elif org_down_p:
            page.keyboard.press("Escape")
            button_restore_page.click()
            page.screenshot(path=PATHL+date_string+"restore_4.jpg")
            print("Clicked Button Restore  ", button_restore_page.is_visible())
            confirm_restore = page.locator(".successInvite", has_text="Restore")
            if confirm_restore.is_visible():
                confirm_restore.click()
                page.screenshot(path=PATHL+date_string+"restore_5.jpg")
                page.wait_for_selector("//i[@class='fa fa-check-circle ']", state='visible', timeout=6000)
                spin_checker = page.locator("//i[@class='fa fa-check-circle ']")
                if spin_checker.count() > 0:
                    print("SPINNER CHECK is: ", spin_checker.is_visible())
                    print("SPINNER CHECK Completing ", spin_checker.count())
        spin_checker = page.locator("//i[@class='fa fa-check-circle ']")
        if spin_checker.count() > 0:
            print("SPINNER CHECK Count", spin_checker.count())
        print("SPINNER CHECK is: ", spin_checker.is_visible())
        print("SPINNER CHECK Compleating ", spin_checker.count())
        #TODO check if org is UP sucessfully
        try:
            my_button = page.wait_for_selector("//p[normalize-space()='My Projects']", state='visible', timeout=120000)
        except Exception as ex:
            page.screenshot(path=PATHL+date_string+"utils_51.jpg")
            print("Error in Deploy App in 2 Mins: " + str(ex))
        if my_button.is_visible():
            print("Org is restored!")
        page.screenshot(path=PATHL+date_string+"restore_6.jpg")
    except Exception as ex:
        page.screenshot(path=PATHL+date_string+"utils_7.jpg")
        print("Unable to find button Util 31: " + str(ex))

def is_org_up(page: Page):
    rest = page.get_by_role("button", name="Restore")
    if rest.is_visible():
        if rest.is_enabled():
            return False
    return True


def is_org_down(page: Page):
    restore_org = page.get_by_role("button", name="Restore")
    if restore_org.is_visible():
        if restore_org.is_enabled():
            return True
    return False

try:
    logging.basicConfig(filename='playwright.log', level=logging.INFO)
except Exception as e:
    print(f"Error occurred during logging setup: {e}")
PATHL=os.getcwd()+"/"


def g_config():
    with open(PATHL+"config.toml", mode="rb") as fp:
        config_file = tomli.load(fp)
        print(config_file)
    return config_file

def add(page):
    ads = "//button[normalize-space()='Add']"
    page.click(ads)
    print("Add done!")

def apply(page):
    apply = "//button[@id='apply']"
    page.wait_for_selector(apply,timeout=240000)
    apl = page.click(apply)
    print("Apply done!")

def row_start(signed_in_context):
    page = signed_in_context
    drop_row = "//button[@title='Drop Row']//img[@class='cayley-aciton-Icons']"
    dpr = page.click(drop_row)

def add_column(page):
    add_col = "//button[@title='Add Column']//img[@class='cayley-aciton-Icons']"
    page.click(add_col)

def revert(page):
    revert = "//button[@title='Revert']//img[@class='cayley-aciton-Icons']"
    page.wait_for_selector(revert,timeout=240000)
    page.click(revert)
