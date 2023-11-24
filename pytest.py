import os
import tomli
import pytest
from datetime import datetime
from playwright.sync_api import Page, expect, TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright
import utilities
import logging
now = datetime.now()
date_string = now.strftime("%Y-%m-%d %H:%M:%S").replace('-', '_').replace(':', '_').replace(' ', '_')
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

@pytest.fixture(scope='session')
def signed_in_context():
    with sync_playwright() as playwright:
        conf = g_config()
        print(conf)
        url = conf['base']['url']
        print(f'Navigated to {url}',url)
        print(f'Navigated to {conf}')
        # browser = playwright.chromium.launch(headless=True, slow_mo=1000)
        now = datetime.now()
        date_string = now.strftime("%Y-%m-%d %H:%M:%S").replace('-', '_').replace(':', '_').replace(' ', '_')
        browser = playwright.chromium.launch(headless=conf['browser']['headless'], slow_mo=1000)
        context = browser.new_context()
        page = context.new_page()
        page.goto(conf['base']['url'])
        page.screenshot(path=PATHL+date_string+"context_SI_1.jpg")
        page.wait_for_load_state('networkidle')
        expect(page).to_have_title("Emly Labs")
        page.locator("#username").fill(conf['user']['username'])
        page.locator("#password").fill(conf['user']['password'])
        page.locator("//input[@value='Sign In']").click()
        # Return the signed-in context
        page.screenshot(path=PATHL+date_string+"context_SI_2.jpg")
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        context.set_default_timeout(240000)
        utilities.restore(page)
        da = "//div[@title='Datasets']//i[@id='tab-icons']"
        page.wait_for_selector(da,timeout=240000)
        page.click(da)
        #irs = "//div[@title='isr']"
        irs = "//div[@title='"+conf['dataset']['name']+"']"
        show = page.click(irs)
        prep = "//button[normalize-space()='Prepare']"
        try:
            ex = page.wait_for_selector(prep, timeout=240000)
        except Exception as e:
            print("Not seen!")
        pre = page.click(prep)
        chk = "//span[normalize-space()='Prepare']"
        try:
            ce = page.wait_for_selector(chk,timeout=24000)
        except Exception as e:
            print("Not found!")
        yield page
        # Clean up
        context.tracing.stop(path="trace.zip")
        context.close()

# @pytest.mark.skip
def test_org_up(signed_in_context):
    page = signed_in_context
    with open(PATHL+"config.toml", mode="rb") as fp:
        config = tomli.load(fp)
    # page.goto(config['base']['url'])
    page.keyboard.press("Escape")
    now = datetime.now()
    date_string = now.strftime("%Y-%m-%d %H:%M:%S").replace('-', '_').replace(':', '_').replace(' ', '_')
    page.screenshot(path=PATHL+date_string+"set_my_org_up_1.jpg")

    print("Checking if Org is UP!")
    logging.info(f'Navigated to ORG UP 78')
    x =utilities.is_org_up(page)
    # x = page.locator(".admin-panel-title", has_text="My Applications")
    # org_up = x.is_visible()
    if x:
        # x.wait_for()
        # expect(x).to_be_visible()
        print("Org is UP now!")
    else:
        print("ORG Is Down!")
        utilities.restore(page)
        # assert False, "Fail to restore taking more than Expected 2 Mins Time!"
    # page.reload()
    page.keyboard.press("Escape")
    print("Locator Found!")
    # page.pause()
    page.screenshot(path=PATHL+date_string+"set_my_org_up_2.jpg")
    # expect(page).to_have_url(re.compile(".*orgInstance"))
    # page.close()

#@pytest.mark.skip
def test_delete_col(signed_in_context):
    conf = g_config()
    page = signed_in_context
    dop = "//button[@title='Drop Column']//img[@class='cayley-aciton-Icons']"
    try:
        dp = page.wait_for_selector(dop,timeout=240000)
    except Exception as e:
        print("Icon not found!")
    page.click(dop)
    page.screenshot(path=PATHL+date_string+"delete_col1.jpg")
    ssel = "//span[@class='multiselect-selected-text']"
    page.click(ssel)
    id = "//label[normalize-space()='"+conf['data']['del_column_name1']+"']"
    try:
        ser = page.wait_for_selector(id,timeout=240000)
    except Exception as e:
        print("Parameter not available!")
    ia = page.click(id)
    ap = "//button[@id='apply']"
    app = page.click(ap)
    col = "//div[@id='"+conf['data']['del_column_name1']+"_col_icon']"
    ad = page.locator(col).count()
    if ad!=0:
        print("Column successfully deleted!")
    else:
        print("Column not deleted!")
    page.screenshot(path=PATHL+date_string+"delete_col2.jpg")
    utilities.revert(page)

# @pytest.mark.skip
def test_sort_data(signed_in_context):
    conf = g_config()
    page = signed_in_context
    col_apply = "//button[@title='Column Apply']//img[@class='cayley-aciton-Icons']"
    pake = page.click(col_apply)
    entrysort = "//form//div/select[@class='alpaca-control form-control']"
    ent = page.locator(entrysort).select_option('SORT_DATA')
    page.screenshot(path=PATHL+date_string+"sort_data1.jpg")
    sor = "//form/div[1]/div/div[1]/div/span/div/button/span[@class='multiselect-selected-text']"
    page.click(sor)
    dot = "//label[normalize-space()='"+conf['data']['column_name3']+"']"
    try:
        page.wait_for_selector(dot,timeout=240000)
    except Exception as e:
        print("Not found!")
    page.click(dot)
    normal = "//div[@class='popupMainContainer-all-content success']"
    page.click(normal)
    asc = "//input[@name='isAscending']"
    page.click(asc)
    utilities.add(page)
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"sort_data2.jpg")
    utilities.revert(page)

# @pytest.mark.skip
def test_change_case(signed_in_context):
    conf = g_config()
    page = signed_in_context
    col_apply = "//button[@title='Column Apply']//img[@class='cayley-aciton-Icons']"
    pake = page.click(col_apply)
    entrysort = "//form//div/select[@class='alpaca-control form-control']"
    ent = page.locator(entrysort).select_option('CHANGE_CASE')
    page.screenshot(path=PATHL+date_string+"changecase.jpg")
    colu = "//select[@name='column']"
    try:
        ex = page.wait_for_selector(colu, timeout=240000)
    except Exception as e:
         print("Not seen!")
    et = page.locator(colu)
    et.select_option(conf['data']['column_name2'],timeout=240000)
    casetype ="//select[@name='caseType']"
    try:
        ex = page.wait_for_selector(casetype, timeout=240000)
    except Exception as e:
        print("Not seen!")
    tt = page.locator(casetype)
    tt.select_option('toUpperCase',timeout=240000)
    utilities.add(page)
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"changecase2.jpg")
    utilities.revert(page)
# test_change_case(signed_in_context)

# @pytest.mark.skip
def test_missing_value_treatment(signed_in_context):
    conf = g_config()
    page = signed_in_context
    col_apply = "//button[@title='Column Apply']//img[@class='cayley-aciton-Icons']"
    pake = page.click(col_apply)
    entrysort = "//form//div/select[@class='alpaca-control form-control']"
    ent = page.locator(entrysort).select_option('MISSING_VALUE_TREATMENT')
    page.screenshot(path=PATHL+date_string+"missing_value_treatment1.jpg")
    colu = "//select[@name='column']"
    try:
        ex = page.wait_for_selector(colu, timeout=240000)
    except Exception as e:
        print("Not seen!")
    et = page.locator(colu)
    et.select_option(conf['data']['column_name2'],timeout=240000)
    casetype ="//select[@name='treatmentType']"
    try:
        ex = page.wait_for_selector(casetype, timeout=240000)
    except Exception as e:
        print("Not seen!")
    tt = page.locator(casetype)
    tt.select_option('CUSTOM_VALUE',timeout=240000)
    casetype ="//input[@name='missingString']"
    try:
        ex = page.wait_for_selector(casetype, timeout=240000)
    except Exception as e:
        print("Not seen!")
    tt = page.locator(casetype)
    tt.fill(conf['data']['replacedstring'],timeout=240000)
    page.keyboard.press('Enter')
    utilities.add(page)
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"missing_value_treatment2.jpg")
    utilities.revert(page)

# @pytest.mark.skip
def test_number_scaling(signed_in_context):
    conf = g_config()
    page = signed_in_context
    col_apply = "//button[@title='Column Apply']//img[@class='cayley-aciton-Icons']"
    pake = page.click(col_apply)
    entrysort = "//form//div/select[@class='alpaca-control form-control']"
    ent = page.locator(entrysort).select_option('NUMBER_SCALING')
    page.screenshot(path=PATHL+date_string+"numberscaling.jpg")
    colu = "//select[@name='column']"
    try:
        ex = page.wait_for_selector(colu, timeout=240000)
    except Exception as e:
        print("Not seen!")
    et = page.locator(colu)
    et.select_option(conf['data']['column_name3'],timeout=240000)
    casetype ="//select[@name='scaleType']"
    try:
        ex = page.wait_for_selector(casetype, timeout=240000)
    except Exception as e:
        print("Not seen!")
    tt = page.locator(casetype)
    tt.select_option('Standard',timeout=240000)
    utilities.add(page)
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"numberscaling2.jpg")
    utilities.revert(page)

# @pytest.mark.skip
def test_outlier_treatment(signed_in_context):
    conf = g_config()
    page = signed_in_context
    col_apply = "//button[@title='Column Apply']//img[@class='cayley-aciton-Icons']"
    pake = page.click(col_apply)
    entrysort = "//form//div/select[@class='alpaca-control form-control']"
    ent = page.locator(entrysort).select_option('OUTLIER_TREATMENT')
    page.screenshot(path=PATHL+date_string+"outliertreatment.jpg")
    colu = "//select[@name='column']"
    try:
        ex = page.wait_for_selector(colu, timeout=240000)
    except Exception as e:
        print("Not seen!")
    et = page.locator(colu)
    et.select_option(conf['data']['column_name3'],timeout=240000)
    casetype ="//select[@name='treatmentType']"
    try:
        ex = page.wait_for_selector(casetype, timeout=240000)
    except Exception as e:
        print("Not seen!")
    tt = page.locator(casetype)
    tt.select_option('AVERAGE',timeout=240000)
    utilities.add(page)
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"outliertreatment2.jpg")
    utilities.revert(page)

# @pytest.mark.skip
def test_rename_column(signed_in_context):
    conf = g_config()
    page = signed_in_context
    col_apply = "//button[@title='Column Apply']//img[@class='cayley-aciton-Icons']"
    pake = page.click(col_apply)
    entrysort = "//form//div/select[@class='alpaca-control form-control']"
    ent = page.locator(entrysort).select_option('RENAME_COLUMN')
    page.screenshot(path=PATHL+date_string+"renamecolumn.jpg")
    colu = "//select[@name='column']"
    try:
        ex = page.wait_for_selector(colu, timeout=240000)
    except Exception as e:
        print("Not seen!")
    et = page.locator(colu)
    et.select_option(conf['data']['del_column_name1'],timeout=240000)
    casetype ="//input[@name='newColumn']"
    try:
        ex = page.wait_for_selector(casetype, timeout=240000)
    except Exception as e:
        print("Not seen!")
    tt = page.locator(casetype)
    tt.fill(conf['data']['renamed_col_name'],timeout=240000)
    page.keyboard.press('Enter')
    utilities.add(page)
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"renamecolumn2.jpg")
    utilities.revert(page)
# test_rename_column(signed_in_context)

# @pytest.mark.skip
def test_round_n(signed_in_context):
    conf = g_config()
    page = signed_in_context
    col_apply = "//button[@title='Column Apply']//img[@class='cayley-aciton-Icons']"
    pake = page.click(col_apply)
    entrysort = "//form//div/select[@class='alpaca-control form-control']"
    ent = page.locator(entrysort).select_option('ROUND')
    page.screenshot(path=PATHL+date_string+"round.jpg")
    colu = "//select[@name='column']"
    try:
        ex = page.wait_for_selector(colu, timeout=240000)
    except Exception as e:
        print("Not seen!")
    et = page.locator(colu)
    et.select_option(conf['data']['column_name3'],timeout=240000)
    casetype ="//select[@name='roundFunctionType']"
    tt = page.locator(casetype)
    tt.select_option('ROUND',timeout=240000)
    casetY ="//input[@name='N']"
    tt = page.locator(casetY)
    tt.fill(conf['data']['round_n'],timeout=240000)
    utilities.add(page)
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"round2.jpg")
    utilities.revert(page)
# test_round_n(signed_in_context)

# @pytest.mark.skip
def test_string_replace(signed_in_context):
    conf = g_config()
    page = signed_in_context
    col_apply = "//button[@title='Column Apply']//img[@class='cayley-aciton-Icons']"
    pake = page.click(col_apply)
    entrysort = "//form//div/select[@class='alpaca-control form-control']"
    ent = page.locator(entrysort).select_option('STRING_REPLACE')
    page.screenshot(path=PATHL+date_string+"stringreplace.jpg")
    colu = "//select[@name='column']"
    try:
        ex = page.wait_for_selector(colu, timeout=240000)
    except Exception as e:
        print("Not seen!")
    et = page.locator(colu)
    et.select_option(conf['data']['column_name2'],timeout=240000)
    casetype ="//select[@name='replaceType']"
    tt = page.locator(casetype)
    tt.select_option('Text',timeout=240000)
    casetY ="//input[@name='subString']"
    tt = page.locator(casetY)
    tt.fill(conf['data']['inputstring'],timeout=240000)
    page.keyboard.press('Enter')
    cas ="//input[@name='replacement']"
    tti = page.locator(cas)
    tti.fill(conf['data']['replacedstring'],timeout=240000)
    utilities.add(page)
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"stringreplace2.jpg")
    utilities.revert(page)
# test_string_replace(signed_in_context)

# def test_done_row(signed_in_context):
#     page = signed_in_context
#     apply = "//button[@id='apply']"
#     apl = page.click(apply)
#     print("Done!")
#
# def row_start(signed_in_context):
#     page = signed_in_context
#     drop_row = "//button[@title='Drop Row']//img[@class='cayley-aciton-Icons']"
#     dpr = page.click(drop_row)

# @pytest.mark.skip
def test_row_drop_outliers(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.row_start(page)
    inpf = "//form//div//select[@name='column']"
    page.locator(inpf).select_option(conf['data']['column_name3'])
    condt = "//form//div//select[@name='condition']"
    page.locator(condt).select_option('DropOutliers')
    page.screenshot(path=PATHL+date_string+"r_d_outliers.jpg")
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"r_d_outliers2.jpg")
    utilities.revert(page)
# test_row_drop_outliers(signed_in_context)

# @pytest.mark.skip
def test_row_drop_isBetween(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.row_start(page)
    inpf = "//form//div//select[@name='column']"
    page.locator(inpf).select_option(conf['data']['column_name3'])
    condt = "//form//div//select[@name='condition']"
    page.locator(condt).select_option('IsBetween')
    page.screenshot(path=PATHL+date_string+"r_d_isbetween.jpg")
    minval = "//form//div//input[@name='minValue']"
    page.locator(minval).fill(conf['data']['row_drop_isbetween1'])
    maxval = "//form//div//input[@name='maxValue']"
    page.locator(maxval).fill(conf['data']['row_drop_isbetween2'])
    # page.keyboard.press("Enter")
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"r_d_isbetween2.jpg")
    utilities.revert(page)
# test_row_drop_isBetween(signed_in_context)

# @pytest.mark.skip
def test_row_drop_isequalto(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.row_start(page)
    inpf = "//form//div//select[@name='column']"
    page.locator(inpf).select_option(conf['data']['column_name3'])
    condt = "//form//div//select[@name='condition']"
    page.locator(condt).select_option('IsEqualTo')
    page.screenshot(path=PATHL+date_string+"r_d_isequalto.jpg")
    val = "//form//div//input[@name='value']"
    page.locator(val).fill(conf['data']['row_drop_isequalto'])
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"r_d_isequalto2.jpg")
    utilities.revert(page)
# test_row_drop_isequalto(signed_in_context)

# @pytest.mark.skip
def test_row_drop_isgreaterthan(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.row_start(page)
    inpf = "//form//div//select[@name='column']"
    page.locator(inpf).select_option(conf['data']['column_name3'])
    condt = "//form//div//select[@name='condition']"
    page.locator(condt).select_option('IsGreaterThan')
    page.screenshot(path=PATHL+date_string+"r_d_isgreaterthan.jpg")
    val = "//form//div//input[@name='value']"
    page.locator(val).fill(conf['data']['row_drop_isgreaterthan'])
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"r_d_isgreaterthan2.jpg")
    utilities.revert(page)
# test_row_drop_isgreaterthan(signed_in_context)

# @pytest.mark.skip
def test_row_drop_isgreaterthanorequalto(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.row_start(page)
    inpf = "//form//div//select[@name='column']"
    page.locator(inpf).select_option(conf['data']['column_name3'])
    condt = "//form//div//select[@name='condition']"
    page.locator(condt).select_option('IsGreaterThanOrEqualTo')
    page.screenshot(path=PATHL+date_string+"r_d_isgreaterthanequalto.jpg")
    val = "//form//div//input[@name='value']"
    page.locator(val).fill(conf['data']['row_drop_isgreaterthan'])
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"r_d_isgreaterthanequalto2.jpg")
    utilities.revert(page)
# test_row_drop_isgreaterthanorequalto(signed_in_context)

# @pytest.mark.skip
def test_row_drop_islessthanorequalto(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.row_start(page)
    inpf = "//form//div//select[@name='column']"
    page.locator(inpf).select_option(conf['data']['column_name3'])
    condt = "//form//div//select[@name='condition']"
    page.locator(condt).select_option('IsLessThanOrEqualTo')
    page.screenshot(path=PATHL+date_string+"r_d_islessthanequalto.jpg")
    val = "//form//div//input[@name='value']"
    page.locator(val).fill(conf['data']['islessthanorequalto'])
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"r_d_islessthanequalto2.jpg")
    utilities.revert(page)
# test_row_drop_islessthanorequalto(signed_in_context)

# @pytest.mark.skip
def test_row_drop_isnotequalto(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.row_start(page)
    inpf = "//form//div//select[@name='column']"
    page.locator(inpf).select_option(conf['data']['column_name3'])
    condt = "//form//div//select[@name='condition']"
    page.locator(condt).select_option('IsNotEqualTo')
    page.screenshot(path=PATHL+date_string+"r_d_isnotequalto.jpg")
    val = "//form//div//input[@name='value']"
    page.locator(val).fill(conf['data']['row_drop_isnotequalto'])
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"r_d_isnotequalto2.jpg")
    utilities.revert(page)
# test_row_drop_isnotequalto(signed_in_context)

# @pytest.mark.skip
def test_row_drop_if_contains(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.row_start(page)
    inpf = "//form//div//select[@name='column']"
    page.locator(inpf).select_option(conf['data']['column_name2'])
    condt = "//form//div//select[@name='condition']"
    page.locator(condt).select_option('Contains')
    page.screenshot(path=PATHL+date_string+"r_d_ifcontains.jpg")
    val = "//input[@name='subString']"
    page.locator(val).fill(conf['data']['inputstring'])
    page.keyboard.press("Enter")
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"r_d_ifcontains2.jpg")
    utilities.revert(page)
# test_row_drop_if_contains(signed_in_context)

# @pytest.mark.skip
def test_row_drop_if_endswith(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.row_start(page)
    inpf = "//form//div//select[@name='column']"
    page.locator(inpf).select_option(conf['data']['column_name2'])
    condt = "//form//div//select[@name='condition']"
    page.locator(condt).select_option('EndsWith')
    page.screenshot(path=PATHL+date_string+"r_d_ifendswith.jpg")
    val = "//input[@name='subString']"
    page.locator(val).fill(conf['data']['row_drop_endswith'])
    page.keyboard.press('Enter')
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"r_d_ifendswith2.jpg")
    utilities.revert(page)
# test_row_drop_if_endswith(signed_in_context)

# @pytest.mark.skip
def test_row_drop_if_isempty(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.row_start(page)
    inpf = "//form//div//select[@name='column']"
    page.locator(inpf).select_option(conf['data']['column_name2'])
    page.screenshot(path=PATHL+date_string+"r_d_isempty.jpg")
    condt = "//form//div//select[@name='condition']"
    page.locator(condt).select_option('IsEmpty')
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"r_d_isempty2.jpg")
    utilities.revert(page)
# test_row_drop_if_isempty(signed_in_context)

# @pytest.mark.skip
def test_row_drop_if_istextequalto(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.row_start(page)
    inpf = "//form//div//select[@name='column']"
    page.locator(inpf).select_option(conf['data']['column_name2'])
    condt = "//form//div//select[@name='condition']"
    page.locator(condt).select_option('IsTextEqualTo')
    page.screenshot(path=PATHL+date_string+"r_d_istextequalto.jpg")
    val = "//input[@name='subString']"
    page.locator(val).fill(conf['data']['inputstring'])
    page.keyboard.press('Enter')
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"r_d_istextequalto2.jpg")
    utilities.revert(page)
# test_row_drop_if_istextequalto(signed_in_context)

# @pytest.mark.skip
def test_row_drop_if_istextnotequalto(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.row_start(page)
    inpf = "//form//div//select[@name='column']"
    page.locator(inpf).select_option(conf['data']['column_name2'])
    condt = "//form//div//select[@name='condition']"
    page.locator(condt).select_option('IsTextNotEqualTo')
    page.screenshot(path=PATHL+date_string+"r_d_istextnotequalto.jpg")
    val = "//input[@name='subString']"
    page.locator(val).fill(conf['data']['inputstring'])
    page.keyboard.press('Enter')
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"r_d_istextnotequalto2.jpg")
    utilities.revert(page)
# test_row_drop_if_istextnotequalto(signed_in_context)

# @pytest.mark.skip
def test_row_drop_if_startswith(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.row_start(page)
    inpf = "//form//div//select[@name='column']"
    page.locator(inpf).select_option(conf['data']['column_name2'])
    condt = "//form//div//select[@name='condition']"
    page.locator(condt).select_option('StartsWith')
    page.screenshot(path=PATHL+date_string+"r_d_ifstartswith.jpg")
    val = "//input[@name='subString']"
    page.locator(val).fill(conf['data']['row_drop_if_startswith'])
    page.keyboard.press("Enter")
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"r_d_ifstartswith2.jpg")
    utilities.revert(page)
# test_row_drop_if_startswith(signed_in_context)

# @pytest.mark.skip
def test_row_drop_isdatebetween(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.row_start(page)
    inpf = "//form//div//select[@name='column']"
    page.locator(inpf).select_option(conf['data']['row_drop_date'])
    condt = "//form//div//select[@name='condition']"
    page.locator(condt).select_option('IsDateBetween')
    page.screenshot(path=PATHL+date_string+"r_d_isdatebetween.jpg")
    startval = "//input[@name='startDate']"
    page.locator(startval).fill(conf['data']['row_drop_isdatebetween1'])
    page.keyboard.press('Enter')
    endval = "//input[@name='endDate']"
    page.locator(endval).fill(conf['data']['row_drop_isdatebetween2'])
    page.keyboard.press('Enter')
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"r_d_isdatebetween2.jpg")
    utilities.revert(page)
# test_row_drop_isdatebetween(signed_in_context)

# @pytest.mark.skip
def test_row_drop_isdateequalto(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.row_start(page)
    inpf = "//form//div//select[@name='column']"
    page.locator(inpf).select_option(conf['data']['row_drop_date'])
    condt = "//form//div//select[@name='condition']"
    page.locator(condt).select_option('IsDateEqualTo')
    page.screenshot(path=PATHL+date_string+"r_d_isdateequalto.jpg")
    val = "//input[@name='customDate']"
    page.locator(val).fill(conf['data']['row_drop_isdateequalto'])
    page.keyboard.press('Enter')
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"r_d_isdateequalto2.jpg")
    utilities.revert(page)
# test_row_drop_isdateequalto(signed_in_context)

# @pytest.mark.skip
def test_row_drop_isdategreaterthan(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.row_start(page)
    inpf = "//form//div//select[@name='column']"
    page.locator(inpf).select_option(conf['data']['row_drop_date'])
    condt = "//form//div//select[@name='condition']"
    page.locator(condt).select_option('IsDateGreaterThan')
    page.screenshot(path=PATHL+date_string+"r_d_isdategreaterthan.jpg")
    val = "//input[@name='customDate']"
    page.locator(val).fill(conf['data']['row_drop_isdategreaterthan'])
    page.keyboard.press('Enter')
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"r_d_isdategreaterthan2.jpg")
    utilities.revert(page)
# test_row_drop_isdategreaterthan(signed_in_context)

# @pytest.mark.skip
def test_row_drop_isdategreaterthanorequalto(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.row_start(page)
    inpf = "//form//div//select[@name='column']"
    page.locator(inpf).select_option(conf['data']['row_drop_date'])
    condt = "//form//div//select[@name='condition']"
    page.locator(condt).select_option('IsDateGreaterThanOrEqualTo')
    page.screenshot(path=PATHL+date_string+"r_d_isdategreaterthanorequalto.jpg")
    val = "//input[@name='customDate']"
    page.locator(val).fill(conf['data']['row_drop_isdategreaterthan'])
    page.keyboard.press('Enter')
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"r_d_isdategreaterthanorequalto2.jpg")
    utilities.revert(page)
# test_row_drop_isgreaterthanorequalto(signed_in_context)

# @pytest.mark.skip
def test_row_drop_isdatelessthan(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.row_start(page)
    inpf = "//form//div//select[@name='column']"
    page.locator(inpf).select_option(conf['data']['row_drop_date'])
    condt = "//form//div//select[@name='condition']"
    page.locator(condt).select_option('IsDateLessThan')
    page.screenshot(path=PATHL+date_string+"r_d_isdatelessthan.jpg")
    val = "//input[@name='customDate']"
    page.locator(val).fill(conf['data']['row_drop_isdatelessthan'])
    page.keyboard.press('Enter')
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"r_d_isdatelessthan2.jpg")
    utilities.revert(page)
# test_row_drop_isdatelessthan(signed_in_context)

# @pytest.mark.skip
def test_row_drop_isdatelessthanorequalto(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.row_start(page)
    inpf = "//form//div//select[@name='column']"
    page.locator(inpf).select_option(conf['data']['row_drop_date'])
    condt = "//form//div//select[@name='condition']"
    page.locator(condt).select_option('IsDateLessThanOrEqualTo')
    page.screenshot(path=PATHL+date_string+"r_d_isdatelessthanorequalto.jpg")
    val = "//input[@name='customDate']"
    page.locator(val).fill(conf['data']['row_drop_isdatelessthan'])
    page.keyboard.press('Enter')
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"r_d_isdatelessthanorequalto2.jpg")
    utilities.revert(page)
# test_row_drop_isdatelessthanorequalto(signed_in_context)

# @pytest.mark.skip
def test_row_drop_isdatenotequalto(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.row_start(page)
    inpf = "//form//div//select[@name='column']"
    page.locator(inpf).select_option(conf['data']['row_drop_date'])
    condt = "//form//div//select[@name='condition']"
    page.locator(condt).select_option('IsDateNotEqualTo')
    page.screenshot(path=PATHL+date_string+"r_d_isdatenotequalto.jpg")
    val = "//input[@name='customDate']"
    page.locator(val).fill(conf['data']['row_drop_isdatenotequalto'])
    page.keyboard.press('Enter')
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"r_d_isdatenotequalto2.jpg")
    utilities.revert(page)
# test_row_drop_isdatenotequalto(signed_in_context)

# @pytest.mark.skip
def test_row_drop_matchregex(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.row_start(page)
    inpf = "//form//div//select[@name='column']"
    page.locator(inpf).select_option(conf['data']['column_name2'])
    condt = "//form//div//select[@name='condition']"
    page.locator(condt).select_option('MatchRegex')
    page.screenshot(path=PATHL+date_string+"r_d_matchregex.jpg")
    val = "//input[@name='subString']"
    page.locator(val).fill(conf['data']['row_drop_matchregex'])
    page.keyboard.press('Enter')
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"r_d_matchregex2.jpg")
    utilities.revert(page)# test_row_drop_matchregex(signed_in_context)

# @pytest.mark.skip
def test_row_drop_islessthan(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.row_start(page)
    inpf = "//form//div//select[@name='column']"
    page.locator(inpf).select_option(conf['data']['column_name3'])
    condt = "//form//div//select[@name='condition']"
    page.locator(condt).select_option('IsLessThan')
    page.screenshot(path=PATHL+date_string+"r_d_islessthan.jpg")
    val = "//form//div//input[@name='value']"
    page.locator(val).fill(conf['data']['row_drop_islessthan'])
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"r_d_islessthan2.jpg")
    utilities.revert(page)
# test_row_drop_islessthan(signed_in_context)

# def test_add_column(signed_in_context):
#     page = signed_in_context
#     add_col = "//button[@title='Add Column']//img[@class='cayley-aciton-Icons']"
#     page.click(add_col)
#
# def test_column_create_done(signed_in_context):
#     page = signed_in_context
#     ag = "//button[normalize-space()='Add']"
#     page.click(ag)
#     apr = "//button[@id='apply']"
#     try:
#         page.wait_for_selector(apr,timeout=240000)
#     except Exception as e:
#         print("Not visible!")
#     ap = page.click(apr)
#     print("Column added!")

# @pytest.mark.skip
def test_add_column_addindexcolumn(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.add_column(page)
    add_new = "//form//div//select[@name='columnCreateFunction']"
    page.locator(add_new).select_option('ADD_INDEX_COLUMN')
    page.screenshot(path=PATHL+date_string+"col_addindexcol.jpg")
    textadd = "//form//div//input[@name='newColumn']"
    page.locator(textadd).fill(conf['data']['add_column_addindexcolumn'])
    utilities.add(page)
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"col_addindexcol2.jpg")
    utilities.revert(page)
# test_add_column_addindexcolumn(signed_in_context)

# @pytest.mark.skip
def test_add_column_changecolumntype(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.add_column(page)
    add_new = "//form//div//select[@name='columnCreateFunction']"
    page.locator(add_new).select_option('CHANGE_COLUMN_TYPE')
    page.screenshot(path=PATHL+date_string+"col_changecoltype.jpg")
    current_type = "//select[@name='column']"
    page.wait_for_selector(current_type,timeout=240000)
    page.locator(current_type).select_option(conf['data']['column_name3'])
    new_data_type = "//select[@name='changeType']"
    page.locator(new_data_type).select_option('DOUBLE')
    create_new_column = "//input[@name='createNewColumn']"
    page.click(create_new_column)
    new_name = "//input[@name='newColumn']"
    page.locator(new_name).fill(conf['data']['add_column_result_name'])
    utilities.add(page)
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"col_changecoltype2.jpg")
    utilities.revert(page)
# test_add_column_changecolumntype(signed_in_context)

# @pytest.mark.skip
def test_add_column_concatwithseparator(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.add_column(page)
    add_new = "//form//div//select[@name='columnCreateFunction']"
    page.locator(add_new).select_option('CONCAT_WITH_SEPARATOR')
    page.screenshot(path=PATHL+date_string+"col_concatwithseparator.jpg")
    inp_field = "//span[@class='multiselect-selected-text']"
    page.click(inp_field)
    name = "//label[normalize-space()='"+conf['data']['column_name2']+"']"
    page.click(name)
    score = "//label[normalize-space()='"+conf['data']['column_name3']+"']"
    page.click(score)
    sep = "//input[@name='separator']"
    page.locator(sep).fill('/')
    new_col = "//input[@name='newColumn']"
    page.locator(new_col).fill(conf['data']['add_column_result_name'])
    utilities.add(page)
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"col_concatwithseparator2.jpg")
    utilities.revert(page)
# test_add_column_concatwithseparator(signed_in_context)

# @pytest.mark.skip
def test_add_column_copy(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.add_column(page)
    add_new = "//form//div//select[@name='columnCreateFunction']"
    page.locator(add_new).select_option('COPY')
    page.screenshot(path=PATHL+date_string+"col_copy.jpg")
    inp = "//select[@name='column']"
    page.locator(inp).select_option(conf['data']['column_name3'])
    new_col = "//input[@name='newColumn']"
    page.locator(new_col).fill(conf['data']['add_column_result_name'])
    page.keyboard.press('Enter')
    utilities.add(page)
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"col_copy2.jpg")
    utilities.revert(page)
# test_add_column_copy(signed_in_context)

# @pytest.mark.skip
def test_add_column_datedifference(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.add_column(page)
    add_new = "//form//div//select[@name='columnCreateFunction']"
    page.locator(add_new).select_option('DATE_DIFFERENCE')
    page.screenshot(path=PATHL+date_string+"col_datedifference.jpg")
    col1 = "//select[@name='column1']"
    page.locator(col1).select_option(conf['data']['row_drop_date'])
    col2 = "//select[@name='column2']"
    page.locator(col2).select_option(conf['data']['row_drop_date'])
    diffunit = "//select[@name='differenceUnit']"
    page.locator(diffunit).select_option(conf['data']['add_column_datedifference_unit'])
    new_col = "//input[@name='newColumn']"
    page.locator(new_col).fill(conf['data']['add_column_result_name'])
    page.keyboard.press('Enter')
    utilities.add(page)
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"col_datedifference2.jpg")
    utilities.revert(page)
# test_add_column_datedifference(signed_in_context)

# @pytest.mark.skip
def test_add_column_datefrequency(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.add_column(page)
    add_new = "//form//div//select[@name='columnCreateFunction']"
    page.locator(add_new).select_option('DATE_FREQUENCY')
    page.screenshot(path=PATHL+date_string+"col_datefrequency.jpg")
    inp = "//select[@name='column']"
    page.locator(inp).select_option(conf['data']['row_drop_date'])
    frequnit = "//select[@name='frequencyUnit']"
    page.locator(frequnit).select_option(conf['data']['add_column_datefrequency_unit'])
    grp = "//b[@class='caret']"
    page.click(grp)
    date = "//input[@value='"+conf['data']['add_column_datefrequency_date']+"']"
    page.click(date)
    new_col = "//input[@name='newColumn']"
    page.locator(new_col).fill(conf['data']['add_column_result_name'])
    page.keyboard.press('Enter')
    utilities.add(page)
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"col_datefrequency2.jpg")
    utilities.revert(page)
# test_add_column_datefrequency(signed_in_context)

# @pytest.mark.skip
def test_add_column_extractdatefeatures(signed_in_context):
    conf = g_config()
    page = page = signed_in_context
    utilities.add_column(page)
    add_new = "//form//div//select[@name='columnCreateFunction']"
    page.locator(add_new).select_option('EXTRACT_DATE_FEATURES')
    page.screenshot(path=PATHL+date_string+"col_extractdatefeatures.jpg")
    inp = "//select[@name='column']"
    page.locator(inp).select_option(conf['data']['row_drop_date'])
    grp = "//b[@class='caret']"
    page.click(grp)
    day = "//input[@value='"+conf['data']['add_column_extractdatefeatures_unit']+"']"
    page.click(day)
    res = "//input[@name='prefix']"
    page.locator(res).fill(conf['data']['add_column_result_name'])
    utilities.add(page)
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"col_extractdatefeatures2.jpg")
    utilities.revert(page)
# test_add_column_extractdatefeatures(signed_in_context)

# @pytest.mark.skip
def test_add_column_metricfunction(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.add_column(page)
    add_new = "//form//div//select[@name='columnCreateFunction']"
    page.locator(add_new).select_option('METRIC_FUNCTION')
    page.screenshot(path=PATHL+date_string+"col_metricfunction.jpg")
    inp = "//select[@name='column']"
    page.locator(inp).select_option(conf['data']['column_name3'])
    metric = "//select[@name='metricFunctionType']"
    page.locator(metric).select_option('COUNT')
    grp = "//span[normalize-space()='None selected']"
    page.click(grp)
    date = "//input[@value='"+conf['data']['add_column_metricfunction_date']+"']"
    page.click(date)
    new_col = "//input[@name='newColumn']"
    page.locator(new_col).fill(conf['data']['add_column_result_name'])
    page.keyboard.press('Enter')
    utilities.add(page)
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"col_metricfunction2.jpg")
    utilities.revert(page)
# test_add_column_metricfunction(signed_in_context)

# @pytest.mark.skip
def test_add_column_numberbucketing(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.add_column(page)
    add_new = "//form//div//select[@name='columnCreateFunction']"
    page.locator(add_new).select_option('NUMBER_BUCKETING')
    page.screenshot(path=PATHL+date_string+"col_numberbucketing.jpg")
    inp = "//select[@name='column']"
    page.locator(inp).select_option(conf['data']['column_name3'])
    bucket = "//select[@name='bucketType']"
    page.locator(bucket).select_option('AutoBucketing')
    no_of_bucks = "//input[@name='numberOfBuckets']"
    page.locator(no_of_bucks).fill(conf['data']['add_column_numberbucketing'])
    lab_prefix = "//input[@name='labelPrefix']"
    page.locator(lab_prefix).fill(conf['data']['add_column_numberbucketing_prefix'])
    new_col = "//input[@name='newColumn']"
    page.locator(new_col).fill(conf['data']['add_column_result_name'])
    page.keyboard.press('Enter')
    utilities.add(page)
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"col_numberbucketing2.jpg")
    utilities.revert(page)
# test_add_column_numberbucketing(signed_in_context)

# @pytest.mark.skip
def test_add_column_stringcondition(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.add_column(page)
    add_new = "//form//div//select[@name='columnCreateFunction']"
    page.locator(add_new).select_option('STRING_CONDITION')
    page.screenshot(path=PATHL+date_string+"col_stringcondition.jpg")
    inp = "//select[@name='column']"
    page.locator(inp).select_option(conf['data']['column_name2'])
    cont = "//select[@name='condition']"
    page.locator(cont).select_option('Contains')
    substring = "//input[@name='subString']"
    page.locator(substring).fill(conf['data']['add_column_stringcondition_substring'])
    new_col = "//input[@name='newColumn']"
    page.locator(new_col).fill(conf['data']['add_column_result_name'])
    utilities.add(page)
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"col_stringcondition2.jpg")
    utilities.revert(page)
# test_add_column_stringcondition(signed_in_context)

# @pytest.mark.skip
def test_add_column_stringcountmatches(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.add_column(page)
    add_new = "//form//div//select[@name='columnCreateFunction']"
    page.locator(add_new).select_option('STRING_COUNT_MATCHES')
    page.screenshot(path=PATHL+date_string+"col_stringcountmatches.jpg")
    inp = "//select[@name='column']"
    page.locator(inp).select_option(conf['data']['column_name2'])
    subs = "//input[@name='regex']"
    page.locator(subs).fill(conf['data']['add_column_stringcountmatches_substring'])
    new_col = "//input[@name='newColumn']"
    page.locator(new_col).fill(conf['data']['add_column_result_name'])
    # page.keyboard.press('Enter')
    utilities.add(page)
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"col_stringcountmatches2.jpg")
    utilities.revert(page)
# test_add_column_stringcountmatches(signed_in_context)

# @pytest.mark.skip
def test_add_column_stringlength(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.add_column(page)
    add_new = "//form//div//select[@name='columnCreateFunction']"
    page.locator(add_new).select_option('STRING_LENGTH')
    page.screenshot(path=PATHL+date_string+"col_stringlength.jpg")
    inp = "//select[@name='column']"
    page.locator(inp).select_option(conf['data']['column_name2'])
    new_col = "//input[@name='newColumn']"
    page.locator(new_col).fill(conf['data']['add_column_result_name'])
    page.keyboard.press("Enter")
    utilities.add(page)
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"col_stringlength2.jpg")
    utilities.revert(page)
# test_add_column_stringlength(signed_in_context)

# @pytest.mark.skip
def test_add_column_stringsplit(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.add_column(page)
    add_new = "//form//div//select[@name='columnCreateFunction']"
    page.locator(add_new).select_option('STRING_SPLIT')
    page.screenshot(path=PATHL+date_string+"col_stringsplit.jpg")
    inp = "//select[@name='column']"
    page.locator(inp).select_option(conf['data']['add_column_stringsplit_inputdate'])
    splittype = "//select[@name='splitType']"
    page.locator(splittype).select_option('splitByText')
    deli = "//input[@name='delimiter']"
    page.locator(deli).fill(conf['data']['add_column_stringsplit_delimeter'])
    prefix = "//input[@name='prefix']"
    page.locator(prefix).fill(conf['data']['add_column_result_name'])
    utilities.add(page)
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"col_stringsplit2.jpg")
    utilities.revert(page)
# test_add_column_stringsplit(signed_in_context)

# @pytest.mark.skip
def test_add_column_substring(signed_in_context):
    conf = g_config()
    page = signed_in_context
    utilities.add_column(page)
    add_new = "//form//div//select[@name='columnCreateFunction']"
    page.locator(add_new).select_option('SUB_STRING')
    page.screenshot(path=PATHL+date_string+"col_substring.jpg")
    inp = "//select[@name='column']"
    page.locator(inp).select_option(conf['data']['column_name2'])
    substring_type = "//select[@name='SubStringType']"
    page.locator(substring_type).select_option("FIRST_N_CHARACTER")
    len = "//input[@name='length']"
    page.locator(len).fill(conf['data']['add_column_substring_length'])
    new_col = "//input[@name='newColumn']"
    page.locator(new_col).fill(conf['data']['add_column_result_name'])
    utilities.add(page)
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"col_substring2.jpg")
    utilities.revert(page)
# test_add_column_substring(signed_in_context)

# @pytest.mark.skip
def test_grouping_data_concatenate(signed_in_context):
    conf = g_config()
    page = signed_in_context
    grp_data = "//button[@title='Group Data']//img[@class='cayley-aciton-Icons']"
    page.locator(grp_data).click()
    select = "//span[@class='multiselect-selected-text']"
    page.click(select)
    date = "//input[@value='"+conf['data']['grouping_data_concatenate_date']+"']"
    page.click(date)
    click = "//div[@class='alpaca-array-toolbar alpaca-array-toolbar-position-bottom']"
    page.click(click)
    add_funct = "//button[normalize-space()='Add Function']"
    page.click(add_funct)
    met_funct = "//select[@name='metricFunctions_0']"
    page.locator(met_funct).select_option(conf['data']['grouping_data1'])
    page.screenshot(path=PATHL+date_string+"group_data_concat.jpg")
    inp = "//select[@name='column']"
    page.locator(inp).select_option(conf['data']['column_name2'])
    deli = "//input[@name='delimiter']"
    page.locator(deli).fill(conf['data']['grouping_data_concatenate_delimeter'])
    new_col = "//input[@name='newColumn']"
    page.locator(new_col).fill(conf['data']['add_column_result_name'])
    utilities.add(page)
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"group_data_concat2.jpg")
    utilities.revert(page)
# test_grouping_data_concatenate(signed_in_context)

# @pytest.mark.skip
def test_grouping_data_mean(signed_in_context):
    conf = g_config()
    page = signed_in_context
    grp_data = "//button[@title='Group Data']//img[@class='cayley-aciton-Icons']"
    page.locator(grp_data).click()
    select = "//span[@class='multiselect-selected-text']"
    page.click(select)
    score = "//label[normalize-space()='"+conf['data']['column_name3']+"']"
    page.click(score)
    click = "//div[@class='alpaca-array-toolbar alpaca-array-toolbar-position-bottom']"
    page.click(click)
    add_funct = "//button[normalize-space()='Add Function']"
    page.click(add_funct)
    met_funct = "//select[@name='metricFunctions_0']"
    page.locator(met_funct).select_option(conf['data']['grouping_data'])
    page.screenshot(path=PATHL+date_string+"group_data_mean.jpg")
    inp = "//select[@name='column']"
    page.locator(inp).select_option(conf['data']['column_name3'])
    new_col = "//input[@name='newColumn']"
    page.locator(new_col).fill(conf['data']['add_column_result_name'])
    page.keyboard.press('Enter')
    utilities.add(page)
    utilities.apply(page)
    page.screenshot(path=PATHL+date_string+"group_data_mean2.jpg")
    utilities.revert(page)
# test_grouping_data_mean(signed_in_context)

# @pytest.mark.skip
def test_show_hide(signed_in_context):
    conf = g_config()
    page = signed_in_context
    show = "//button[@title='Show/Hide Columns']//img[@class='cayley-aciton-Icons']"
    page.click(show)
    page.screenshot(path=PATHL+date_string+"showorhide.jpg")
    score = "//div[@role='rowgroup']//div[1]//div[1]//span[1]//span[1]"
    page.click(score)
    name = "//input[@id='checkbox-name']"
    page.click(name)
    leftpannel = "//div[@class='LeftSidePanel']"
    page.click(leftpannel)
    page.screenshot(path=PATHL+date_string+"showorhide2.jpg")
# test_show_hide(signed_in_context)
