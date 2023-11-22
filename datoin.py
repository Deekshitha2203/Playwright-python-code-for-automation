import os
from playwright.sync_api import sync_playwright
username = ' ' #Enter the username or email address
password = ' ' #Enter the password
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context ()
    page = context.new_page()
    #login page
    page.goto(' ') #Enter the website link
    un = page.locator('#username')
    un.fill(username)
    page.wait_for_selector("#username")
    pas = page.get_by_label('Password')
    pas.fill(password)
    page.get_by_role("button",name='Sign In').click()
    selector = "//p[normalize-space()='Acquire Data']"
    s = "//p[normalize-space()='Start Training']"
    h = "//p[normalize-space()='Evaluate Model']"
    try:
        element = page.wait_for_selector(selector, timeout=240000)
        try:
            ele = page.wait_for_selector(s,timeout=240000)
            try:
                el = page.wait_for_selector(h,timeout=240000)
                page.screenshot(path='screenshot.png')
                print("Login successful!")
            except Exception as e:
                print('Element is not present on the page or did not appear within the timeout.')
        except Exception as e:
                print('Element is not present on the page or did not appear within the timeout.')
    except Exception as e:
        print('Element is not present on the page or did not appear within the timeout.')
    #used upload datasets from a directory
    def create_dataset(page):
        da = "//div[contains(text(),'Datasets')]"
        page.click(da)
        page.screenshot(path='screen.png')
        ds = '//div[@class="admin-panel-title"]'
        ch = '//p[normalize-space()="Upload Dataset"]'
        fold = '//div[contains(text(),"Folders")]'
        try:
            ob = page.wait_for_selector(ds,timeout=240000)
            try:
                oob = page.wait_for_selector(ch,timeout=240000)
                try:
                    ooob = page.wait_for_selector(fold,timeout=240000)
                    print("Datasets opened successfully!")
                    page.screenshot(path='datashot.png')
                except Exception as e:
                    print('Element is not present on the page or did not appear within the timeout.')
            except Exception as e:
                    print('Element is not present on the page or did not appear within the timeout.')
        except Exception as e:
            print('Element is not present on the page or did not appear within the timeout.')
        directory_path = " " #Enter the directory path
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            upload = "//p[normalize-space()='Upload Dataset']"
            element = page.wait_for_selector(upload, state='visible')
            element.click()
            file_input = page.locator('input[type="file"]')
            file_input.set_input_files(file_path)
            drop_area = page.locator("//div[@class='filepond--drop-label']")
            drop_area_bbox = drop_area.bounding_box()
            drop_x = drop_area_bbox['x'] + drop_area_bbox['width'] / 2
            drop_y = drop_area_bbox['y'] + drop_area_bbox['height'] / 2
            page.mouse.move(drop_x, drop_y)
            page.mouse.down()
            page.mouse.move(drop_x, drop_y)
            page.mouse.up()
            page.wait_for_selector("//button[normalize-space()='Upload']")
            uploadc = page.locator("//button[normalize-space()='Upload']")
            uploadc.click()
            pau = "//button[normalize-space()='Pause All']"
            try:
                pau = page.wait_for_selector(pau, timeout=240000)
            except Exception as e:
                print("Problem in uploading!")
            upload_complete_selector = "//div[@class='button-cancel']"
            try:
                exe = page.wait_for_selector(upload_complete_selector, timeout=240000)
            except Exception as e:
                print("Problem in uploading!")
            filename=filename.replace('.csv','')
            done_selector = '//div[@title='+"'"+filename+"']"
            try:
                ex = page.wait_for_selector(done_selector, timeout=240000)
                print(filename+" uploaded successfully!")
            except Exception as e:
                print(filename+" is not uploaded!")
    create_dataset(page)

    #used to delete a column from the dataset
    def delete_col(page):
        da = "//div[contains(text(),'Datasets')]"
        page.click(da)
        irs = "//div[@title='isr']"
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
        dop = "//button[@title='Drop Column']//img[@class='cayley-aciton-Icons']"
        try:
            dp = page.wait_for_selector(dop,timeout=240000)
        except Exception as e:
            print("Icon not found!")
        du = page.click(dop)
        ssel = "//span[@class='multiselect-selected-text']"
        sel = page.click(ssel)
        ida = "//label[normalize-space()='Id']"
        try:
            ser = page.wait_for_selector(ida,timeout=240000)
        except Exception as e:
            print("Parameter not available!")
        ia = page.click(ida)
        ap = "//button[@id='apply']"
        app = page.click(ap)
        col = "//div[@id='Id_col_icon']"
        ad = page.locator(col).count()
        if ad!=0:
            print("Column successfully deleted!")
        else:
            print("Column not deleted!")
    delete_col(page)

    #used to start a new application and run a dataset with a given target to get appropriate results
    def create_new_application(page):
        new = "https://pre-app.datoin.com/4ed52767-3689-4951-85c2-0bab8b560222/7ef5d230-8dd0-471a-b180-bc83ef88efd6/apps"
        page.goto(new,wait_until="load")
        page.keyboard.press("Escape")        # apps = "//div[@title='My Apps']"
        # page.wait_for_selector(apps,timeout=240000)
        # doapp = page.click(apps)
        newapp = "//button[normalize-space()='New Application']"
        clap = page.click(newapp)
        cross = '//*[@id="___reactour"]/div[4]/div/button'
        try:
            page.wait_for_selector(cross,timeout=240000)
            page.click(cross)
        except Exception as e:
            print("Not done!")
        build = '//*[@id="scrollableDiv"]/div/div/div[2]/div/div[2]/div'
        biu = page.click(build)
        textbox = "(//input[@id='tfid-0-0'])[1]"
        fil = page.locator(textbox).fill('Iris')
        ok = "//button[normalize-space()='Start Build »']"
        try:
            buid = page.wait_for_selector(ok,timeout=240000)
        except Exception as e:
            print("Not clicked!")
        oko = page.click(ok)
        startnew = "//button[normalize-space()='Start New Experiment']"
        try:
            wit = page.wait_for_selector(startnew,timeout=240000)
        except Exception as e:
            print("Not found!")
        start = page.click(startnew)
        newex = "//h2[normalize-space()='New Experiment']"
        try:
            witho = page.wait_for_selector(newex,timeout=240000)
        except Exception as e:
            print("Not found!")
        newdata = "//button[normalize-space()='Choose dataset']"
        newd = page.click(newdata)
        plus = "//div[text()='isr' and @class='browser_item_name']/../following-sibling::div//button"
        irs = "//div[@class='browser_item_name'][normalize-space()='isr']"
        try:
            clic = page.wait_for_selector(irs,timeout=240000)
            witty = page.wait_for_selector(plus,timeout=240000)
            witty.click()
            page.screenshot(path="dataset2.png")
        except Exception as e:
            print("Not found!")
        target = "//button[normalize-space()='Choose target']"
        targ = page.click(target)
        tarsel = "//div[@class=' css-tlfecz-indicatorContainer']//*[name()='svg']"
        ast = page.click(tarsel)
        #print(ast)
        te = "//div//input"
        ex = page.locator(te)
        ex.type("Species")
        page.wait_for_timeout(500)
        ex.press('Enter')
        startsear = "//button[normalize-space()='Start Experiment']"
        try:
            page.wait_for_selector(startsear,timeout=240000)
            star = page.click(startsear)
        except Exception as e:
            print("Target not found!")
        okay = '//*[@id="___reactour"]/div[4]/div/div[2]/button[2]/span/button'
        try:
            clok = page.wait_for_selector(okay,timeout=240000)
            page.click(okay)
        except Exception as e:
            print("Done!")
        page.close()

    #to check status of the already created application. 
    def result_page(page):
        count = 0
        wb = openpyxl.load_workbook('datasheet-5.xlsx',data_only=True) #Replace 'datasheet-5.xlsx' with your excel sheet name.
        sheet = wb['sheet'] #Replace 'sheet' wwith the excel sheet you are working on.
        for row in range(2,11): #replace te range of rows you want to check.
            if sheet['F'+str(row)].value is None or sheet['F'+str(row)].value == 'Running': #In the given code snippet the letters B,E,F etc are according to the columns. So replace them according to your excel sheet columns providing the letters corresponding to the jobid link and status column.
                jobid = sheet['E'+str(row)].value
                status = sheet['F'+str(row)].value
                print(jobid)
                page.goto(jobid,wait_until="load")
                success = "//button[normalize-space()='View Report']"
                failure = "//button[normalize-space()='View Error']"
                sne = "//i[@class='fa fa-calendar']"
                page.wait_for_selector(sne,timeout=24000)
                done_v = page.is_visible(success)
                print(done_v)
                not_done = page.is_visible(failure)
                print(not_done)
                if done_v:
                    sheet['F'+str(row)].value = 'Successful'
                elif not_done:
                    sheet['F'+str(row)].value = 'Failed'
                else:
                    sheet['F'+str(row)].value = 'Running'
                    count = count+1
        print(count)
        wb.close()
        if count < 2:
                create_new_application(page)
        else:
            print("2 applications are already running. Thus wait till they complete.")
            wb.save('sheet1.xlsx')
    result_page(page)

    # used to delete a row while applying a particular parameter
    def delete_row(page): # to delete row having ID less than 5
        da = "//div[contains(text(),'Datasets')]"
        page.click(da)
        irs = "//div[@title='isr']"
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
        drop_row = "//button[@title='Drop Row']//img[@class='cayley-aciton-Icons']"
        dpr = page.click(drop_row)
        inpf = "//form//div//select[@name='column']"
        page.locator(inpf).select_option('Id')
        condt = "//form//div//select[@name='condition']"
        page.locator(condt).select_option('IsLessThan')
        val = "//form//div//input[@name='value']"
        page.locator(val).fill('5')
        apply = "//button[@id='apply']"
        apl = page.click(apply)
        print("Delete row less than 5 peration is done!")
    delete_row(page)

    #to add an extra column to a given dataset with appropriate column name
    def add_column(page):
        da = "//div[contains(text(),'Datasets')]"
        page.click(da)
        irs = "//div[@title='isr']"
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
        add_col = "//button[@title='Add Column']//img[@class='cayley-aciton-Icons']"
        page.click(add_col)
        add_new = "//form//div//select[@name='columnCreateFunction']"
        page.locator(add_new).select_option('ADD_INDEX_COLUMN')
        textadd = "//form//div//input[@name='newColumn']"
        page.locator(textadd).fill('sl_no')
        ag = "//button[normalize-space()='Add']"
        page.click(ag)
        apr = "//button[@id='apply']"
        try:
            page.wait_for_selector(apr,timeout=240000)
        except Exception as e:
            print("Not visible!")
        ap = page.click(apr)
        print("Column added!")
    add_column(page)

    #to reorder a dataset according to a given column name
    def sort_column(page):
        da = "//div[contains(text(),'Datasets')]"
        page.click(da)
        irs = "//div[@title='isr']"
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
        col_apply = "//button[@title='Column Apply']//img[@class='cayley-aciton-Icons']"
        pake = page.click(col_apply)
        entrysort = "//form//div/select[@class='alpaca-control form-control']"
        ent = page.locator(entrysort).select_option('SORT_DATA')
        sor = "//form/div[1]/div/div[1]/div/span/div/button/span[@class='multiselect-selected-text']"
        pak = page.click(sor)
        dot = "//label[normalize-space()='PetalLengthCm']"
        try:
            page.wait_for_selector(dot,timeout=240000)
        except Exception as e:
            print("Not found!")
        se = page.click(dot)
        normal = "//div[@class='popupMainContainer-all-content success']"
        norm = page.click(normal)
        asc = "//input[@name='isAscending']"
        jh = page.click(asc)
        ads = "//button[normalize-space()='Add']"
        adse = page.click(ads)
        conf = "//button[@id='apply']"
        try:
            page.wait_for_selector(conf,timeout=240000)
        except Exception as e:
            print("Not found!")
        confir = page.click(conf)
        print("Petal length is sorted in decending order!")
    sort_column(page)

    def common_dataset(page):
        da = "//div[contains(text(),'Datasets')]"
        page.click(da)
        #irs = "//div[@title='isr']"
        irs = "//div[@title='date_feild_test']"
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


    def done(page):
        ads = "//button[normalize-space()='Add']"
        adse = page.click(ads)
        conf = "//button[@id='apply']"
        try:
            page.wait_for_selector(conf,timeout=240000)
        except Exception as e:
            print("Not found!")
        confir = page.click(conf)
        print("Done!")

    def change_case(page):
        common_dataset(page)
        col_apply = "//button[@title='Column Apply']//img[@class='cayley-aciton-Icons']"
        pake = page.click(col_apply)
        entrysort = "//form//div/select[@class='alpaca-control form-control']"
        ent = page.locator(entrysort).select_option('CHANGE_CASE')
        colu = "//select[@name='column']"
        try:
            ex = page.wait_for_selector(colu, timeout=240000)
        except Exception as e:
            print("Not seen!")
        et = page.locator(colu)
        et.select_option('name',timeout=240000)
        casetype ="//select[@name='caseType']"
        try:
            ex = page.wait_for_selector(casetype, timeout=240000)
        except Exception as e:
            print("Not seen!")
        tt = page.locator(casetype)
        tt.select_option('toUpperCase',timeout=240000)
        done(page)
    change_case(page)


    def missing_value_treatment(page):
        common_dataset(page)
        col_apply = "//button[@title='Column Apply']//img[@class='cayley-aciton-Icons']"
        pake = page.click(col_apply)
        entrysort = "//form//div/select[@class='alpaca-control form-control']"
        ent = page.locator(entrysort).select_option('MISSING_VALUE_TREATMENT')
        colu = "//select[@name='column']"
        try:
            ex = page.wait_for_selector(colu, timeout=240000)
        except Exception as e:
            print("Not seen!")
        et = page.locator(colu)
        et.select_option('name',timeout=240000)
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
        tt.fill('missing_value',timeout=240000)
        done(page)
    missing_value_treatment(page)


    def number_scaling(page):
        common_dataset(page)
        col_apply = "//button[@title='Column Apply']//img[@class='cayley-aciton-Icons']"
        pake = page.click(col_apply)
        entrysort = "//form//div/select[@class='alpaca-control form-control']"
        ent = page.locator(entrysort).select_option('NUMBER_SCALING')
        colu = "//select[@name='column']"
        try:
            ex = page.wait_for_selector(colu, timeout=240000)
        except Exception as e:
            print("Not seen!")
        et = page.locator(colu)
        et.select_option('score',timeout=240000)
        casetype ="//select[@name='scaleType']"
        try:
            ex = page.wait_for_selector(casetype, timeout=240000)
        except Exception as e:
            print("Not seen!")
        tt = page.locator(casetype)
        tt.select_option('Standard',timeout=240000)
        done(page)
    number_scaling(page)


    def outlier_treatment(page):
        common_dataset(page)
        col_apply = "//button[@title='Column Apply']//img[@class='cayley-aciton-Icons']"
        pake = page.click(col_apply)
        entrysort = "//form//div/select[@class='alpaca-control form-control']"
        ent = page.locator(entrysort).select_option('OUTLIER_TREATMENT')
        colu = "//select[@name='column']"
        try:
            ex = page.wait_for_selector(colu, timeout=240000)
        except Exception as e:
            print("Not seen!")
        et = page.locator(colu)
        et.select_option('score',timeout=240000)
        casetype ="//select[@name='treatmentType']"
        try:
            ex = page.wait_for_selector(casetype, timeout=240000)
        except Exception as e:
            print("Not seen!")
        tt = page.locator(casetype)
        tt.select_option('AVERAGE',timeout=240000)
        done(page)
    outlier_treatment(page)

    def rename_column(page):
        common_dataset(page)
        col_apply = "//button[@title='Column Apply']//img[@class='cayley-aciton-Icons']"
        pake = page.click(col_apply)
        entrysort = "//form//div/select[@class='alpaca-control form-control']"
        ent = page.locator(entrysort).select_option('RENAME_COLUMN')
        colu = "//select[@name='column']"
        try:
            ex = page.wait_for_selector(colu, timeout=240000)
        except Exception as e:
            print("Not seen!")
        et = page.locator(colu)
        et.select_option('score',timeout=240000)
        casetype ="//input[@name='newColumn']"
        try:
            ex = page.wait_for_selector(casetype, timeout=240000)
        except Exception as e:
            print("Not seen!")
        tt = page.locator(casetype)
        tt.fill('marks',timeout=240000)
        done(page)
    rename_column(page)

    def round_n(page):
        common_dataset(page)
        col_apply = "//button[@title='Column Apply']//img[@class='cayley-aciton-Icons']"
        pake = page.click(col_apply)
        entrysort = "//form//div/select[@class='alpaca-control form-control']"
        ent = page.locator(entrysort).select_option('ROUND')
        colu = "//select[@name='column']"
        try:
            ex = page.wait_for_selector(colu, timeout=240000)
        except Exception as e:
            print("Not seen!")
        et = page.locator(colu)
        et.select_option('score',timeout=240000)
        casetype ="//select[@name='roundFunctionType']"
        tt = page.locator(casetype)
        tt.select_option('ROUND',timeout=240000)
        casetY ="//input[@name='N']"
        tt = page.locator(casetY)
        tt.fill('2',timeout=240000)
        done(page)
    round_n(page)

    def string_replace(page):
        common_dataset(page)
        col_apply = "//button[@title='Column Apply']//img[@class='cayley-aciton-Icons']"
        pake = page.click(col_apply)
        entrysort = "//form//div/select[@class='alpaca-control form-control']"
        ent = page.locator(entrysort).select_option('STRING_REPLACE')
        colu = "//select[@name='column']"
        try:
            ex = page.wait_for_selector(colu, timeout=240000)
        except Exception as e:
            print("Not seen!")
        et = page.locator(colu)
        et.select_option('name',timeout=240000)
        casetype ="//select[@name='replaceType']"
        tt = page.locator(casetype)
        tt.select_option('Text',timeout=240000)
        casetY ="//input[@name='subString']"
        tt = page.locator(casetY)
        tt.fill('Illuminex Limited8',timeout=240000)
        cas ="//input[@name='replacement']"
        tti = page.locator(cas)
        tti.fill('replaced',timeout=240000)
        done(page)
    string_replace(page)

    def done_row(page):
        apply = "//button[@id='apply']"
        apl = page.click(apply)
        print("Done!")
        att = page.wait_for_selector(s,timeout=240000)

    def row_start(page):
        common_dataset(page)
        drop_row = "//button[@title='Drop Row']//img[@class='cayley-aciton-Icons']"
        dpr = page.click(drop_row)

    def row_drop_outliers(page):
        row_start(page)
        inpf = "//form//div//select[@name='column']"
        page.locator(inpf).select_option('score')
        condt = "//form//div//select[@name='condition']"
        page.locator(condt).select_option('DropOutliers')
        # val = "//form//div//input[@name='value']"
        # page.locator(val).fill('5')
        done_row(page)
    row_drop_outliers(page)

    def row_drop_isBetween(page):
        row_start(page)
        inpf = "//form//div//select[@name='column']"
        page.locator(inpf).select_option('score')
        condt = "//form//div//select[@name='condition']"
        page.locator(condt).select_option('IsBetween')
        minval = "//form//div//input[@name='minValue']"
        page.locator(minval).fill('5')
        maxval = "//form//div//input[@name='maxValue']"
        page.locator(maxval).fill('30')
        done_row(page)
    row_drop_isBetween(page)

def row_drop_isequalto(page):
        row_start(page)
        inpf = "//form//div//select[@name='column']"
        page.locator(inpf).select_option('score')
        condt = "//form//div//select[@name='condition']"
        page.locator(condt).select_option('IsEqualTo')
        val = "//form//div//input[@name='value']"
        page.locator(val).fill('35')
        done_row(page)
    row_drop_isequalto(page)

    def row_drop_isgreaterthan(page):
        row_start(page)
        inpf = "//form//div//select[@name='column']"
        page.locator(inpf).select_option('score')
        condt = "//form//div//select[@name='condition']"
        page.locator(condt).select_option('IsGreaterThan')
        val = "//form//div//input[@name='value']"
        page.locator(val).fill('25')
        done_row(page)
    row_drop_isgreaterthan(page)

    def row_drop_isgreaterthanorequalto(page):
        row_start(page)
        inpf = "//form//div//select[@name='column']"
        page.locator(inpf).select_option('score')
        condt = "//form//div//select[@name='condition']"
        page.locator(condt).select_option('IsGreaterThanOrEqualTo')
        val = "//form//div//input[@name='value']"
        page.locator(val).fill('25')
        done_row(page)
    row_drop_isgreaterthanorequalto(page)

    def row_drop_islessthanorequalto(page):
        row_start(page)
        inpf = "//form//div//select[@name='column']"
        page.locator(inpf).select_option('score')
        condt = "//form//div//select[@name='condition']"
        page.locator(condt).select_option('IsLessThanOrEqualTo')
        val = "//form//div//input[@name='value']"
        page.locator(val).fill('25')
        done_row(page)
    row_drop_islessthanorequalto(page)

    def row_drop_isnotequalto(page):
        row_start(page)
        inpf = "//form//div//select[@name='column']"
        page.locator(inpf).select_option('score')
        condt = "//form//div//select[@name='condition']"
        page.locator(condt).select_option('IsNotEqualTo')
        val = "//form//div//input[@name='value']"
        page.locator(val).fill('35')
        done_row(page)
    row_drop_isnotequalto(page)

    def row_drop_if_contains(page):
        row_start(page)
        inpf = "//form//div//select[@name='column']"
        page.locator(inpf).select_option('name')
        condt = "//form//div//select[@name='condition']"
        page.locator(condt).select_option('Contains')
        val = "//input[@name='subString']"
        page.locator(val).fill('Illuminex Limited8')
        done_row(page)
    row_drop_if_contains(page)

    def row_drop_if_endswith(page):
        row_start(page)
        inpf = "//form//div//select[@name='column']"
        page.locator(inpf).select_option('name')
        condt = "//form//div//select[@name='condition']"
        page.locator(condt).select_option('EndsWith')
        val = "//input[@name='subString']"
        page.locator(val).fill('8')
        done_row(page)
    row_drop_if_endswith(page)

    def row_drop_if_isempty(page):
        row_start(page)
        inpf = "//form//div//select[@name='column']"
        page.locator(inpf).select_option('name')
        condt = "//form//div//select[@name='condition']"
        page.locator(condt).select_option('IsEmpty')
        done_row(page)
    row_drop_if_isempty(page)

    def row_drop_if_istextequalto(page):
        row_start(page)
        inpf = "//form//div//select[@name='column']"
        page.locator(inpf).select_option('name')
        condt = "//form//div//select[@name='condition']"
        page.locator(condt).select_option('IsTextEqualTo')
        val = "//input[@name='subString']"
        page.locator(val).fill('Illuminex Limited8')
        done_row(page)
    row_drop_if_istextequalto(page)

    def row_drop_if_istextnotequalto(page):
        row_start(page)
        inpf = "//form//div//select[@name='column']"
        page.locator(inpf).select_option('name')
        condt = "//form//div//select[@name='condition']"
        page.locator(condt).select_option('IsTextNotEqualTo')
        val = "//input[@name='subString']"
        page.locator(val).fill('Illuminex Limited8')
        done_row(page)
    row_drop_if_istextnotequalto(page)

    def row_drop_if_startswith(page):
        row_start(page)
        inpf = "//form//div//select[@name='column']"
        page.locator(inpf).select_option('name')
        condt = "//form//div//select[@name='condition']"
        page.locator(condt).select_option('StartsWith')
        val = "//input[@name='subString']"
        page.locator(val).fill('i')
        done_row(page)
    row_drop_if_startswith(page)

    def row_drop_if_istextequalto(page):
        row_start(page)
        inpf = "//form//div//select[@name='column']"
        page.locator(inpf).select_option('name')
        condt = "//form//div//select[@name='condition']"
        page.locator(condt).select_option('IsTextEqualTo')
        val = "//input[@name='subString']"
        page.locator(val).fill('Illuminex Limited8')
        done_row(page)
    row_drop_if_istextequalto(page)

    def row_drop_isdatebetween(page):
        row_start(page)
        inpf = "//form//div//select[@name='column']"
        page.locator(inpf).select_option('isoFormaWrong')
        condt = "//form//div//select[@name='condition']"
        page.locator(condt).select_option('IsDateBetween')
        startval = "//input[@name='startDate']"
        page.locator(startval).fill('2000-10-31 01:30:00.000000000')
        page.keyboard.press('Enter')
        endval = "//input[@name='endDate']"
        page.locator(endval).fill('2000-11-01 01:30:00.000000000')
        page.keyboard.press('Enter')
        done_row(page)
    row_drop_isdatebetween(page)

    def row_drop_isdateequalto(page):
        row_start(page)
        inpf = "//form//div//select[@name='column']"
        page.locator(inpf).select_option('isoFormaWrong')
        condt = "//form//div//select[@name='condition']"
        page.locator(condt).select_option('IsDateEqualTo')
        val = "//input[@name='customDate']"
        page.locator(val).fill('2000-10-31 01:30:00.000000000')
        page.keyboard.press('Enter')
        done_row(page)
    row_drop_isdateequalto(page)

    def row_drop_isdategreaterthan(page):
        row_start(page)
        inpf = "//form//div//select[@name='column']"
        page.locator(inpf).select_option('isoFormaWrong')
        condt = "//form//div//select[@name='condition']"
        page.locator(condt).select_option('IsDateGreaterThan')
        val = "//input[@name='customDate']"
        page.locator(val).fill('2000-10-31 01:30:00.000000000')
        page.keyboard.press('Enter')
        done_row(page)
    row_drop_isdategreaterthan(page)

    def row_drop_isdategreaterthanorequalto(page):
        row_start(page)
        inpf = "//form//div//select[@name='column']"
        page.locator(inpf).select_option('isoFormaWrong')
        condt = "//form//div//select[@name='condition']"
        page.locator(condt).select_option('IsDateGreaterThanOrEqualTo')
        val = "//input[@name='customDate']"
        page.locator(val).fill('2000-10-31 01:30:00.000000000')
        page.keyboard.press('Enter')
        done_row(page)
    row_drop_isgreaterthanorequalto(page)

    def row_drop_isdatelessthan(page):
        row_start(page)
        inpf = "//form//div//select[@name='column']"
        page.locator(inpf).select_option('isoFormaWrong')
        condt = "//form//div//select[@name='condition']"
        page.locator(condt).select_option('IsDateLessThan')
        val = "//input[@name='customDate']"
        page.locator(val).fill('2000-10-31 01:30:00.000000000')
        page.keyboard.press('Enter')
        done_row(page)
    row_drop_isdatelessthan(page)

    def row_drop_isdatelessthanorequalto(page):
        row_start(page)
        inpf = "//form//div//select[@name='column']"
        page.locator(inpf).select_option('isoFormaWrong')
        condt = "//form//div//select[@name='condition']"
        page.locator(condt).select_option('IsDateLessThanOrEqualTo')
        val = "//input[@name='customDate']"
        page.locator(val).fill('2000-10-31 01:30:00.000000000')
        page.keyboard.press('Enter')
        done_row(page)
    row_drop_isdatelessthanorequalto(page)

    def row_drop_isdatenotequalto(page):
        row_start(page)
        inpf = "//form//div//select[@name='column']"
        page.locator(inpf).select_option('isoFormaWrong')
        condt = "//form//div//select[@name='condition']"
        page.locator(condt).select_option('IsDateNotEqualTo')
        val = "//input[@name='customDate']"
        page.locator(val).fill('2000-10-31 01:30:00.000000000')
        page.keyboard.press('Enter')
        done_row(page)
    row_drop_isdatenotequalto(page)

    def row_drop_matchregex(page):
        row_start(page)
        inpf = "//form//div//select[@name='column']"
        page.locator(inpf).select_option('name')
        condt = "//form//div//select[@name='condition']"
        page.locator(condt).select_option('MatchRegex')
        val = "//input[@name='subString']"
        page.locator(val).fill('owl*')
        done_row(page)
    row_drop_matchregex(page)

    def add_column(page):
        common_dataset(page)
        add_col = "//button[@title='Add Column']//img[@class='cayley-aciton-Icons']"
        page.click(add_col)

    def column_create_done(page):
        ag = "//button[normalize-space()='Add']"
        page.click(ag)
        apr = "//button[@id='apply']"
        try:
            page.wait_for_selector(apr,timeout=240000)
        except Exception as e:
            print("Not visible!")
        ap = page.click(apr)
        print("Column added!")

    def add_column_changecolumntype(page):
        add_column(page)
        add_new = "//form//div//select[@name='columnCreateFunction']"
        page.locator(add_new).select_option('CHANGE_COLUMN_TYPE')
        current_type = "//select[@name='column']"
        page.wait_for_selector(current_type,timeout=240000)
        page.locator(current_type).select_option('score')
        new_data_type = "//select[@name='changeType']"
        page.locator(new_data_type).select_option('DOUBLE')
        create_new_column = "//input[@name='createNewColumn']"
        page.click(create_new_column)
        new_name = "//input[@name='newColumn']"
        page.locator(new_name).fill("New_Column")
        column_create_done(page)
    add_column_changecolumntype(page)

    def add_column_concatwithseparator(page):
        add_column(page)
        add_new = "//form//div//select[@name='columnCreateFunction']"
        page.locator(add_new).select_option('CONCAT_WITH_SEPARATOR')
        inp_field = "//span[@class='multiselect-selected-text']"
        page.click(inp_field)
        name = "//label[normalize-space()='name']"
        page.click(name)
        score = "//label[normalize-space()='score']"
        page.click(score)
        sep = "//input[@name='separator']"
        page.locator(sep).fill('/')
        new_col = "//input[@name='newColumn']"
        page.locator(new_col).fill("Result")
        column_create_done(page)
    add_column_concatwithseparator(page)

    def add_column_copy(page):
        add_column(page)
        add_new = "//form//div//select[@name='columnCreateFunction']"
        page.locator(add_new).select_option('COPY')
        inp = "//select[@name='column']"
        page.locator(inp).select_option('score')
        new_col = "//input[@name='newColumn']"
        page.locator(new_col).fill("Result")
        column_create_done(page)
    add_column_copy(page)

    def add_column_datedifference(page):
        add_column(page)
        add_new = "//form//div//select[@name='columnCreateFunction']"
        page.locator(add_new).select_option('DATE_DIFFERENCE')
        col1 = "//select[@name='column1']"
        page.locator(col1).select_option('isoFormaWrong')
        col2 = "//select[@name='column2']"
        page.locator(col2).select_option('isoFormaWrong')
        diffunit = "//select[@name='differenceUnit']"
        page.locator(diffunit).select_option('DAY')
        new_col = "//input[@name='newColumn']"
        page.locator(new_col).fill("Result")
        column_create_done(page)
    add_column_datedifference(page)

    def add_column_datefrequency(page):
        add_column(page)
        add_new = "//form//div//select[@name='columnCreateFunction']"
        page.locator(add_new).select_option('DATE_FREQUENCY')
        inp = "//select[@name='column']"
        page.locator(inp).select_option('isoFormaWrong')
        frequnit = "//select[@name='frequencyUnit']"
        page.locator(frequnit).select_option('DAY')
        grp = "//b[@class='caret']"
        page.click(grp)
        date = "//input[@value='Date']"
        page.click(date)
        new_col = "//input[@name='newColumn']"
        page.locator(new_col).fill("Result")
        column_create_done(page)
    add_column_datefrequency(page)

    def add_column_extractdatefeatures(page):
        add_column(page)
        add_new = "//form//div//select[@name='columnCreateFunction']"
        page.locator(add_new).select_option('EXTRACT_DATE_FEATURES')
        inp = "//select[@name='column']"
        page.locator(inp).select_option('isoFormaWrong')
        grp = "//b[@class='caret']"
        page.click(grp)
        day = "//input[@value='DAY']"
        page.click(day)
        res = "//input[@name='prefix']"
        page.locator(res).fill("Result")
        column_create_done(page)
    add_column_extractdatefeatures(page)

    def add_column_metricfunction(page):
        add_column(page)
        add_new = "//form//div//select[@name='columnCreateFunction']"
        page.locator(add_new).select_option('METRIC_FUNCTION')
        inp = "//select[@name='column']"
        page.locator(inp).select_option('score')
        metric = "//select[@name='metricFunctionType']"
        page.locator(metric).select_option('COUNT')
        grp = "//span[normalize-space()='None selected']"
        page.click(grp)
        date = "//input[@value='Date']"
        page.click(date)
        new_col = "//input[@name='newColumn']"
        page.locator(new_col).fill("Result")
        column_create_done(page)
    add_column_metricfunction(page)

    def add_column_numberbucketing(page):
        add_column(page)
        add_new = "//form//div//select[@name='columnCreateFunction']"
        page.locator(add_new).select_option('NUMBER_BUCKETING')
        inp = "//select[@name='column']"
        page.locator(inp).select_option('score')
        bucket = "//select[@name='bucketType']"
        page.locator(bucket).select_option('AutoBucketing')
        no_of_bucks = "//input[@name='numberOfBuckets']"
        page.locator(no_of_bucks).fill('3')
        lab_prefix = "//input[@name='labelPrefix']"
        page.locator(lab_prefix).fill('res')
        new_col = "//input[@name='newColumn']"
        page.locator(new_col).fill("Result")
        column_create_done(page)
    add_column_numberbucketing(page)

    def add_column_stringcondition(page):
        add_column(page)
        add_new = "//form//div//select[@name='columnCreateFunction']"
        page.locator(add_new).select_option('STRING_CONDITION')
        inp = "//select[@name='column']"
        page.locator(inp).select_option('name')
        cont = "//select[@name='condition']"
        page.locator(cont).select_option('Contains')
        substring = "//input[@name='subString']"
        page.locator(substring).fill('Illuminex')
        new_col = "//input[@name='newColumn']"
        page.locator(new_col).fill("Result")
        column_create_done(page)
    add_column_stringcondition(page)

    def add_column_stringcountmatches(page):
        add_column(page)
        add_new = "//form//div//select[@name='columnCreateFunction']"
        page.locator(add_new).select_option('STRING_COUNT_MATCHES')
        inp = "//select[@name='column']"
        page.locator(inp).select_option('name')
        subs = "//input[@name='regex']"
        page.locator(subs).fill('Illuminex')
        new_col = "//input[@name='newColumn']"
        page.locator(new_col).fill("Result")
        column_create_done(page)
    add_column_stringcountmatches(page)

    def add_column_stringlength(page):
        add_column(page)
        add_new = "//form//div//select[@name='columnCreateFunction']"
        page.locator(add_new).select_option('STRING_LENGTH')
        inp = "//select[@name='column']"
        page.locator(inp).select_option('name')
        new_col = "//input[@name='newColumn']"
        page.locator(new_col).fill("Result")
        column_create_done(page)
    add_column_stringlength(page)

    def add_column_stringsplit(page):
        add_column(page)
        add_new = "//form//div//select[@name='columnCreateFunction']"
        page.locator(add_new).select_option('STRING_SPLIT')
        inp = "//select[@name='column']"
        page.locator(inp).select_option('isoFormatRight')
        splittype = "//select[@name='splitType']"
        page.locator(splittype).select_option('splitByText')
        deli = "//input[@name='delimiter']"
        page.locator(deli).fill('T')
        prefix = "//input[@name='prefix']"
        page.locator(prefix).fill("Result")
        column_create_done(page)
    add_column_stringsplit(page)

    def add_column_substring(page):
        add_column(page)
        add_new = "//form//div//select[@name='columnCreateFunction']"
        page.locator(add_new).select_option('SUB_STRING')
        inp = "//select[@name='column']"
        page.locator(inp).select_option('name')
        substring_type = "//select[@name='SubStringType']"
        page.locator(substring_type).select_option("FIRST_N_CHARACTER")
        len = "//input[@name='length']"
        page.locator(len).fill('10')
        new_col = "//input[@name='newColumn']"
        page.locator(new_col).fill("Result")
        column_create_done(page)
    add_column_substring(page)

    def grouping_data_concatenate(page):
        common_dataset(page)
        grp_data = "//button[@title='Group Data']//img[@class='cayley-aciton-Icons']"
        page.locator(grp_data).click()
        select = "//span[@class='multiselect-selected-text']"
        page.click(select)
        date = "//input[@value='Date']"
        page.click(date)
        click = "//div[@class='alpaca-array-toolbar alpaca-array-toolbar-position-bottom']"
        page.click(click)
        add_funct = "//button[normalize-space()='Add Function']"
        page.click(add_funct)
        met_funct = "//select[@name='metricFunctions_0']"
        page.locator(met_funct).select_option('CONCATENATE')
        inp = "//select[@name='column']"
        page.locator(inp).select_option('name')
        deli = "//input[@name='delimiter']"
        page.locator(deli).fill('-')
        new_col = "//input[@name='newColumn']"
        page.locator(new_col).fill("Result")
        column_create_done(page)
    grouping_data_concatenate(page)

    def grouping_data_mean(page):
        common_dataset(page)
        grp_data = "//button[@title='Group Data']//img[@class='cayley-aciton-Icons']"
        page.locator(grp_data).click()
        select = "//span[@class='multiselect-selected-text']"
        page.click(select)
        score = "//label[normalize-space()='score']"
        page.click(score)
        click = "//div[@class='alpaca-array-toolbar alpaca-array-toolbar-position-bottom']"
        page.click(click)
        add_funct = "//button[normalize-space()='Add Function']"
        page.click(add_funct)
        met_funct = "//select[@name='metricFunctions_0']"
        page.locator(met_funct).select_option('MEAN')
        inp = "//select[@name='column']"
        page.locator(inp).select_option('score')
        new_col = "//input[@name='newColumn']"
        page.locator(new_col).fill("Result")
        column_create_done(page)
    grouping_data_mean(page)

    def show_hide(page):
        common_dataset(page)
        show = "//button[@title='Show/Hide Columns']//img[@class='cayley-aciton-Icons']"
        page.click(show)
        score = "//div[@role='rowgroup']//div[1]//div[1]//span[1]//span[1]"
        page.click(score)
        name = "//input[@id='checkbox-name']"
        page.click(name)
        leftpannel = "//div[@class='LeftSidePanel']"
        page.click(leftpannel)
    show_hide(page)

    def common_dataset_insight(page):
        da = "//div[contains(text(),'Datasets')]"
        page.click(da)
        irs = "//div[@title='caley_test_feilds_modified']"
        page.click(irs)
        chk = "//button[normalize-space()='Insights']"
        try:
            page.wait_for_selector(chk,timeout=24000)
            page.click(chk)
        except Exception as e:
            print("Not found!")
        summary = "//button[@id='first']"
        try:
            page.wait_for_selector(summary,timeout=240)
            page.click(summary)
            print("Summary found!")
        except Exception as e:
            print("Not found!")
        sum_test = "//div[contains(text(),'High positive co-relation sum points')]"
        try:
            page.wait_for_selector(sum_test,timeout=24000)
            print("Summary successfully generated!")
        except Exception as e:
            print("Not found!")
        characteristics = "//button[@id='last']"
        page.click(characteristics)
        char_check = "//div[normalize-space()='No of columns : 18']"
        try:
            page.wait_for_selector(char_check,timeout=24000)
            print("Characteristics successfully loaded!")
        except Exception as e:
            print('Not done!')
        contribution = "//button[normalize-space()='contributions']"
        try:
            page.wait_for_selector(contribution,timeout=2400000)
            page.click(contribution)
        except Exception as e:
            print("Not found!")
        metric_col = "//div[@class='options metrix emly-mc']//div[@class='select__indicator select__dropdown-indicator css-tlfecz-indicatorContainer']//*[name()='svg']"
        page.click(metric_col)
        te = "//div[@class='options metrix emly-mc']//div[@class='select__input']//div"
        ex = page.locator(te)
        ex.type("score")
        page.wait_for_timeout(500)
        ex.press('Enter')
        player_col = "//div[@class='options player contribution emly-mc']//div[@class='select__indicator select__dropdown-indicator css-tlfecz-indicatorContainer']//*[name()='svg']"
        page.click(player_col)
        pc = "//div[@class='options player contribution emly-mc']//div[@class='select__input']//div"
        xe = page.locator(pc)
        xe.type("date_1")
        page.wait_for_timeout(500)
        xe.press('Enter')
        analyze = "//button[normalize-space()='Analyze']"
        page.click(analyze)
        checking = "//div[contains(text(),'paretos_insights')]"
        try:
            page.wait_for_selector(checking,timeout=240000)
            print("Contribution successful!")
        except Exception as e:
            print('Not done!')
        outliers = "//button[normalize-space()='outliers']"
        page.click(outliers)
        page.click(outliers)
        sumary_points = "//div[@class='lbl']"
        try:
            page.wait_for_selector(sumary_points,timeout=240000)
            print("Outliers successful!")
        except Exception as e:
            print('Not done!')
        paradoxes = "//button[normalize-space()='paradoxes']"
        page.click(paradoxes)
        metric_col = "//div[@class='options metrix emly-mc']//div[@class='select__indicator select__dropdown-indicator css-tlfecz-indicatorContainer']//*[name()='svg']"
        page.click(metric_col)
        te = "//div[@class='options metrix emly-mc']//div[@class='select__input']//div"
        ex = page.locator(te)
        ex.type("score")
        page.wait_for_timeout(500)
        ex.press('Enter')
        player_col = "//div[@class='options player paradoxes emly-mc']//div[@class='select__indicator select__dropdown-indicator css-tlfecz-indicatorContainer']//*[name()='svg']"
        page.click(player_col)
        pc = "//div[@class='options player paradoxes emly-mc']//div[@class='select__input']//div"
        xe = page.locator(pc)
        xe.type("date_1")
        page.wait_for_timeout(500)
        xe.press('Enter')
        pc = "//div[@class='options player paradoxes emly-mc']//div[@class='select__input']//div"
        xe = page.locator(pc)
        xe.type("date_2")
        page.wait_for_timeout(500)
        xe.press('Enter')
        analyze = "//button[normalize-space()='Analyze']"
        page.click(analyze)
        s_analysis = "//div[contains(text(),'Simpsons Analysis')]"
        try:
            page.wait_for_selector(s_analysis,timeout=24000)
            print("Paradoxes done!")
        except Exception as e:
            print("Not done!")
        characteristics = "//button[@id='last']"
        page.click(characteristics)
    common_dataset_insight(page)
