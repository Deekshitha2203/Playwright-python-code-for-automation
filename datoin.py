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
    #create_dataset(page)

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
    #delete_col(page)

    #used to start a new application and run a dataset with a given target to get appropriate results
    def create_new_application(page):
        apps = "//div[@title='My Apps']"
        doapp = page.click(apps)
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
        report = "//button[normalize-space()='View Report']"
        try:
            page.wait_for_selector(report,timeout=43200000)
            rep = page.click(report)
            print("Report is ready!")
        except Exception as e:
            print("Report making is not possible!")
        evalu = "//div[@class='Detail-label-between']"
        try:
            page.wait_for_selector(evalu,timeout=240000)
        except Exception as e:
            print("Report making is not possible!")
    #create_new_application(page)

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
    #delete_row(page)

    #to add an extra column to a given dataset with appropriate column name
    def add_column(page):
        # da = "//div[contains(text(),'Datasets')]"
        # page.click(da)
        # irs = "//div[@title='isr']"
        # show = page.click(irs)
        # prep = "//button[normalize-space()='Prepare']"
        # try:
        #     ex = page.wait_for_selector(prep, timeout=240000)
        # except Exception as e:
        #     print("Not seen!")
        # pre = page.click(prep)
        # chk = "//span[normalize-space()='Prepare']"
        # try:
        #     ce = page.wait_for_selector(chk,timeout=24000)
        # except Exception as e:
        #     print("Not found!")
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
    #add_column(page)

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
    #sort_column(page)

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
        # att = page.wait_for_selector(s,timeout=240000)

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
    #change_case(page)


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
    #missing_value_treatment(page)


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
    #number_scaling(page)


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
    #outlier_treatment(page)

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
    #rename_column(page)

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
    #round_n(page)

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
    #string_replace(page)

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
    #row_drop_outliers(page)

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
