#!/usr/bin/env python
"""Build the official source registry for the public welfare directory."""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path


COUNTY_SOCIAL_BUREAUS = [
    ("keelung-social", "基隆市政府社會處", "https://www.klcg.gov.tw/tw/social", "基隆市"),
    ("taipei-social", "臺北市政府社會局", "https://dosw.gov.taipei/", "臺北市"),
    ("new-taipei-social", "新北市政府社會局", "https://www.sw.ntpc.gov.tw/", "新北市"),
    ("taoyuan-social", "桃園市政府社會局", "https://sab.tycg.gov.tw/", "桃園市"),
    ("hsinchu-city-social", "新竹市政府社會處", "https://society.hccg.gov.tw/ch/index.jsp", "新竹市"),
    ("hsinchu-county-social", "新竹縣政府社會處", "https://social.hsinchu.gov.tw/", "新竹縣"),
    ("miaoli-social", "苗栗縣政府社會處", "https://www.miaoli.gov.tw/social_affairs/", "苗栗縣"),
    ("taichung-social", "臺中市政府社會局", "https://www.society.taichung.gov.tw/", "臺中市"),
    ("changhua-social", "彰化縣政府社會處", "https://social.chcg.gov.tw/00home/index1.asp", "彰化縣"),
    ("nantou-social-labor", "南投縣政府社會及勞動處", "https://www.nantou.gov.tw/big5/index.asp?dptid=376480000au130000", "南投縣"),
    ("yunlin-social", "雲林縣政府社會處", "https://social.yunlin.gov.tw/", "雲林縣"),
    ("chiayi-city-social", "嘉義市政府社會處", "https://www.chiayi.gov.tw/web/social/", "嘉義市"),
    ("chiayi-county-social", "嘉義縣政府社會局", "https://sabcc.cyhg.gov.tw/", "嘉義縣"),
    ("tainan-social", "臺南市政府社會局", "https://sab.tainan.gov.tw/Default.aspx", "臺南市"),
    ("kaohsiung-social", "高雄市政府社會局", "http://socbu.kcg.gov.tw/index.php", "高雄市"),
    ("pingtung-social", "屏東縣政府社會處", "https://www.pthg.gov.tw/planjdp/Default.aspx", "屏東縣"),
    ("yilan-social", "宜蘭縣政府社會處", "https://sntroot.e-land.gov.tw/Default.aspx", "宜蘭縣"),
    ("hualien-social", "花蓮縣政府社會處", "https://sa.hl.gov.tw/", "花蓮縣"),
    ("taitung-social", "臺東縣政府社會處", "http://taisoc.taitung.gov.tw/WebSite/Page/index.aspx", "臺東縣"),
    ("penghu-social", "澎湖縣政府社會處", "https://www.penghu.gov.tw/society/", "澎湖縣"),
    ("kinmen-social", "金門縣政府社會處", "https://social.kinmen.gov.tw/", "金門縣"),
    ("lienchiang-civil-social", "連江縣政府民政社會處", "https://www.matsu.gov.tw/Chhtml/Index/371030000A0001", "連江縣"),
]


CENTRAL_SOURCES = [
    {
        "id": "mohw-ebao-box",
        "name": "衛生福利e寶箱",
        "url": "https://www.mohw.gov.tw/cp-16-22219-1.html",
        "organization": "衛生福利部",
        "jurisdiction": "全國",
        "sourceType": "official-portal",
        "tags": ["中央", "主題式", "分眾", "社會福利"],
        "record": {
            "summary": "中央整合型入口，可依主題與服務對象查詢衛生醫療與社會福利資源。",
            "serviceCategories": ["入口平台", "補助查詢", "線上申辦", "社福宣導"],
            "audiences": ["兒少", "老人", "婦女", "身心障礙者", "低收入戶", "家庭照顧者"],
            "needTags": ["不知道找哪個單位", "補助", "急難救助", "身障", "老人福利", "托育"],
        },
    },
    {
        "id": "mohw-1957",
        "name": "1957福利諮詢專線",
        "url": "https://www.mohw.gov.tw/cp-16-22804-1.html",
        "organization": "衛生福利部",
        "jurisdiction": "全國",
        "sourceType": "official-hotline",
        "tags": ["中央", "1957", "福利諮詢", "社會安全網", "轉介"],
        "record": {
            "summary": "生活遭遇困難時，可撥打1957取得社會福利諮詢、通報與轉介服務。",
            "audiences": ["一般民眾", "低收入戶", "急難家庭", "街友", "照顧者"],
            "serviceCategories": ["福利諮詢", "急難轉介", "社會安全網"],
            "needTags": ["不知道找哪裡", "急難", "社工", "轉介", "1957"],
            "contact": {"phone": "1957", "website": "https://www.mohw.gov.tw/cp-16-22804-1.html"},
        },
    },
    {
        "id": "mohw-low-income",
        "name": "低收入戶及中低收入戶",
        "url": "https://www.mohw.gov.tw/cp-88-79005-1.html",
        "organization": "衛生福利部",
        "jurisdiction": "全國",
        "sourceType": "official-program",
        "tags": ["中央", "低收入戶", "中低收入戶", "社會救助", "醫療補助"],
        "record": {
            "summary": "低收入戶、中低收入戶申請說明、福利內容與常見問題官方入口。",
            "audiences": ["低收入戶", "中低收入戶", "經濟困難家庭"],
            "serviceCategories": ["現金與生活扶助", "醫療補助", "社會救助"],
            "needTags": ["低收入戶", "中低收入戶", "生活補助", "醫療補助", "1957"],
        },
    },
    {
        "id": "mohw-long-term-care-1966",
        "name": "1966長照服務專線與長照2.0",
        "url": "https://www.mohw.gov.tw/fp-16-63417-1.html",
        "organization": "衛生福利部",
        "jurisdiction": "全國",
        "sourceType": "official-program",
        "tags": ["中央", "長照", "1966", "照顧服務", "喘息", "輔具", "交通接送"],
        "record": {
            "summary": "有長照需求可撥打1966，由地方照管中心評估並連結長照2.0服務。",
            "audiences": ["老人", "失能者", "家庭照顧者", "身心障礙者"],
            "serviceCategories": ["長照", "居家照顧", "喘息服務", "輔具", "交通接送"],
            "needTags": ["1966", "長照", "失能", "喘息", "輔具", "交通接送", "照管中心"],
            "contact": {"phone": "1966", "website": "https://www.mohw.gov.tw/fp-16-63417-1.html"},
        },
    },
    {
        "id": "nhi-premium-subsidy",
        "name": "各級政府辦理保險對象健保費補助項目",
        "url": "https://data.gov.tw/dataset/106333",
        "organization": "衛生福利部中央健康保險署",
        "jurisdiction": "全國",
        "sourceType": "official-program",
        "tags": ["中央", "健保", "保費補助", "弱勢協助"],
        "record": {
            "summary": "健保署彙整各級政府辦理的保險對象健保費補助項目。",
            "audiences": ["低收入戶", "中低收入戶", "身心障礙者", "老人", "失業勞工"],
            "serviceCategories": ["醫療與健保", "保費補助"],
            "needTags": ["健保費", "保費補助", "身心障礙", "低收入戶", "中低收入戶"],
            "contact": {"website": "https://www.nhi.gov.tw/ch/cp-4721-0d598-2645-1.html"},
        },
    },
    {
        "id": "taiwanjobs",
        "name": "台灣就業通",
        "url": "https://www.taiwanjobs.gov.tw/",
        "organization": "勞動部勞動力發展署",
        "jurisdiction": "全國",
        "sourceType": "official-portal",
        "tags": ["中央", "勞動部", "就業", "職訓", "求職"],
        "record": {
            "summary": "勞動部求職、職訓、就業服務與相關就業促進資訊入口。",
            "audiences": ["求職者", "失業者", "中高齡者", "青年", "身心障礙者"],
            "serviceCategories": ["就業與職訓", "求職服務", "職業訓練"],
            "needTags": ["找工作", "職訓", "失業", "就業服務", "台灣就業通"],
        },
    },
    {
        "id": "wda-disability-employment",
        "name": "身心障礙者就業資源網",
        "url": "https://orsd.wda.gov.tw/",
        "organization": "勞動部勞動力發展署",
        "jurisdiction": "全國",
        "sourceType": "official-portal",
        "tags": ["中央", "勞動部", "身心障礙", "就業", "職業重建"],
        "record": {
            "summary": "身心障礙者職業重建、就業服務與職業訓練資源入口。",
            "audiences": ["身心障礙者", "求職者", "雇主"],
            "serviceCategories": ["就業與職訓", "身障服務", "職業重建"],
            "needTags": ["身障就業", "職業重建", "職訓", "就業服務"],
        },
    },
]


ECONOMIC_WEAKNESS_SOURCES = [
    {
        "id": "mohw-low-income-115-standards",
        "name": "115年度低收入戶、中低收入戶資格審核標準",
        "url": "https://dep.mohw.gov.tw/dosaasw/fp-566-84223-103.html",
        "organization": "衛生福利部社會救助及社工司",
        "jurisdiction": "全國",
        "sourceType": "official-annual-standard",
        "tags": ["中央", "低收入戶", "中低收入戶", "115年度", "資格標準", "社會救助"],
        "record": {
            "summary": "115年度低收入戶與中低收入戶資格審核標準，含各地區每人每月平均所得、動產與不動產限額。",
            "audiences": ["低收入戶", "中低收入戶", "經濟困難家庭", "一般民眾"],
            "serviceCategories": ["年度標準", "社會救助", "現金與生活扶助"],
            "needTags": ["115年低收標準", "低收入戶資格", "中低收入戶資格", "所得標準", "財產標準", "社會救助"],
            "eligibility": "需同時看家庭總收入、動產、不動產及地方政府資格審查。115年度低收入戶每人每月所得標準例：臺北市2萬744元、新北市1萬7,750元、桃園市1萬7,186元、臺中市1萬6,431元、臺南市1萬5,515元、高雄市1萬6,970元；中低收入戶標準例：臺北市2萬9,635元、新北市2萬6,625元、臺中市2萬4,647元、臺南市2萬3,273元。",
            "howToApply": ["先查看115年度標準是否大致符合", "向戶籍地或實際居住地公所/社會局處提出申請", "由地方政府依戶內人口、收入、動產、不動產及相關規定審查"],
            "documents": ["申請表", "身分證明", "戶籍資料", "收入證明", "存款或投資資料", "不動產資料", "地方政府要求文件"],
            "contact": {"website": "https://www.mohw.gov.tw/dl-97289-8c213179-3e49-4ea3-ab21-1759306d51d5.html"},
        },
    },
    {
        "id": "mohw-low-income-faq",
        "name": "低收入戶與中低收入戶申請常見問答",
        "url": "https://dep.mohw.gov.tw/dosaasw/cp-572-5035-103.html",
        "organization": "衛生福利部社會救助及社工司",
        "jurisdiction": "全國",
        "sourceType": "official-faq",
        "tags": ["中央", "低收入戶", "中低收入戶", "常見問答", "申請文件"],
        "record": {
            "summary": "低收入戶、中低收入戶資格、應備文件、申請地點、戶籍與實際居住地、審查與救濟等常見問答。",
            "audiences": ["低收入戶", "中低收入戶", "經濟困難家庭", "一般民眾"],
            "serviceCategories": ["申請資訊", "社會救助", "補助查詢"],
            "needTags": ["低收入戶怎麼申請", "中低收入戶怎麼申請", "申請文件", "資格審查", "戶籍地", "實際居住地"],
            "eligibility": "此頁不是資格表，而是申請與審查說明。資格仍需依年度標準與地方政府審查。",
            "howToApply": ["先確認戶籍或實際居住地受理規定", "準備申請文件", "向公所或社會局處送件", "如對審查結果有疑問，依頁面說明詢問或救濟"],
            "documents": ["申請書", "戶籍資料", "收入及財產證明", "其他地方政府要求文件"],
        },
    },
    {
        "id": "mohw-emergency-assistance",
        "name": "急難救助",
        "url": "https://www.mohw.gov.tw/cp-190-226-1.html",
        "organization": "衛生福利部",
        "jurisdiction": "全國",
        "sourceType": "official-program",
        "tags": ["中央", "急難救助", "社會救助", "經濟急難", "1957"],
        "record": {
            "summary": "家中主要生計者死亡、失蹤、罹患重病、失業或其他急難事故，導致生活陷困時，可查急難救助申請與轉介資訊。",
            "audiences": ["急難家庭", "低收入戶", "中低收入戶", "經濟困難家庭", "一般民眾"],
            "serviceCategories": ["急難救助", "社會救助", "現金與生活扶助", "福利諮詢"],
            "needTags": ["急難救助", "突然沒錢", "繳不出房租", "生病失業", "家庭變故", "1957"],
            "eligibility": "因死亡、失蹤、重病、失業、災害或其他急難事故導致生活陷困者，可依地方政府或相關救助規定申請或轉介。",
            "howToApply": ["急迫時先撥打1957或洽所在地社會局處/公所", "說明急難原因與目前生活困境", "依承辦窗口要求補齊證明文件"],
            "documents": ["身分證明", "急難事由證明", "收入或生活困難相關資料", "地方政府要求文件"],
            "contact": {"phone": "1957", "website": "https://www.mohw.gov.tw/cp-190-226-1.html"},
        },
    },
    {
        "id": "mohw-social-welfare-service-centers",
        "name": "社會福利服務中心與社會安全網",
        "url": "https://mohw.gov.tw/ss/cp-4530-50091-204.html",
        "organization": "衛生福利部",
        "jurisdiction": "全國",
        "sourceType": "official-service-network",
        "tags": ["中央", "社會安全網", "社福中心", "脆弱家庭", "轉介"],
        "record": {
            "summary": "當家庭同時有經濟、照顧、保護、就業或心理壓力，不知道該申請哪一項福利時，可透過社福中心與社會安全網取得評估、轉介與整合服務。",
            "audiences": ["一般民眾", "經濟困難家庭", "脆弱家庭", "急難家庭", "家庭照顧者"],
            "serviceCategories": ["社福中心", "社會安全網", "轉介服務", "福利諮詢"],
            "needTags": ["不知道找哪裡", "社福中心", "社會安全網", "脆弱家庭", "多重困難", "轉介"],
            "eligibility": "不限單一身分。當家庭遇到多重困難或需要社工評估與資源轉介時，可洽地方社福中心、社會局處或1957。",
            "howToApply": ["說明家庭目前最急迫的問題", "由社工評估需求", "依需求轉介社會救助、保護服務、照顧服務、就業或心理支持"],
            "documents": ["身分證明", "可協助說明困境的相關文件", "依轉介服務要求文件"],
            "contact": {"phone": "1957", "website": "https://mohw.gov.tw/ss/cp-4530-50091-204.html"},
        },
    },
]


HIGH_DEMAND_CENTRAL_SOURCES = [
    {
        "id": "mohw-national-pension-premium-115",
        "name": "115年國民年金保險費與弱勢補助",
        "url": "https://dep.mohw.gov.tw/DOSI/cp-308-602-102.html",
        "organization": "衛生福利部社會保險司",
        "jurisdiction": "全國",
        "sourceType": "official-annual-standard",
        "tags": ["中央", "國民年金", "保費補助", "低收入戶", "中低收入戶", "身心障礙", "115年度"],
        "record": {
            "summary": "115年國民年金保險費自付金額與政府補助金額，含低收入戶、中低收入戶、所得未達一定標準及身心障礙者。",
            "audiences": ["低收入戶", "中低收入戶", "身心障礙者", "所得未達一定標準者", "國民年金被保險人"],
            "serviceCategories": ["保費補助", "國民年金", "社會保險", "經濟弱勢"],
            "needTags": ["國民年金補助", "國保保費", "低收入戶國保", "中低收入戶國保", "身障國保", "115年國民年金"],
        },
    },
    {
        "id": "mohw-special-circumstances-family",
        "name": "特殊境遇家庭扶助",
        "url": "https://dep.mohw.gov.tw/DOPS/cp-1287-14940-105.html",
        "organization": "衛生福利部保護服務司",
        "jurisdiction": "全國",
        "sourceType": "official-program",
        "tags": ["中央", "特殊境遇家庭", "單親", "家暴", "喪偶", "急難", "婦女", "兒少"],
        "record": {
            "summary": "家庭因配偶死亡、失蹤、離婚、家暴、未婚懷孕或其他重大變故而生活困難時，可查特殊境遇家庭扶助。",
            "audiences": ["特殊境遇家庭", "單親家庭", "婦女", "兒少", "急難家庭"],
            "serviceCategories": ["家庭支持", "現金與生活扶助", "子女就學", "保護服務"],
            "needTags": ["特殊境遇", "單親補助", "家暴家庭", "喪偶", "未婚懷孕", "子女生活津貼"],
        },
    },
    {
        "id": "mohw-disability-welfare",
        "name": "身心障礙福利入口",
        "url": "https://www.mohw.gov.tw/cp-88-235-1.html",
        "organization": "衛生福利部",
        "jurisdiction": "全國",
        "sourceType": "official-portal",
        "tags": ["中央", "身心障礙", "身障福利", "輔具", "照顧", "津貼"],
        "record": {
            "summary": "身心障礙者福利主題入口，可查生活補助、輔具、照顧、機構、優先採購與相關服務。",
            "audiences": ["身心障礙者", "身障家庭", "照顧者"],
            "serviceCategories": ["身障服務", "生活補助", "輔具", "照顧服務", "就業支持"],
            "needTags": ["身障補助", "身心障礙", "輔具", "身障生活補助", "身障照顧", "優先採購"],
        },
    },
    {
        "id": "mohw-childcare-services",
        "name": "托育服務與育兒支持",
        "url": "https://mohw.gov.tw/fp-88-230-1.html",
        "organization": "衛生福利部",
        "jurisdiction": "全國",
        "sourceType": "official-portal",
        "tags": ["中央", "托育", "育兒", "保母", "兒童", "家庭支持"],
        "record": {
            "summary": "托育服務主題入口，可查公共托育、居家托育、育兒津貼與兒童家庭支持相關資訊。",
            "audiences": ["嬰幼兒家庭", "父母", "照顧者", "兒童"],
            "serviceCategories": ["托育", "育兒津貼", "兒童家庭", "照顧服務"],
            "needTags": ["托育補助", "育兒津貼", "保母", "公共托育", "未滿2歲", "育兒"],
        },
    },
    {
        "id": "mohw-elderly-welfare",
        "name": "老人福利與中低收入老人生活津貼入口",
        "url": "https://www.mohw.gov.tw/cp-88-224-1.html",
        "organization": "衛生福利部",
        "jurisdiction": "全國",
        "sourceType": "official-portal",
        "tags": ["中央", "老人福利", "中低收入老人", "生活津貼", "照顧", "關懷據點"],
        "record": {
            "summary": "老人福利主題入口，可查中低收入老人生活津貼、照顧服務、關懷據點、老人福利機構與地方窗口。",
            "audiences": ["老人", "中低收入老人", "照顧者", "家庭"],
            "serviceCategories": ["老人福利", "生活津貼", "照顧服務", "社區據點"],
            "needTags": ["老人生活津貼", "中低收入老人", "老人福利", "關懷據點", "老人機構"],
        },
    },
    {
        "id": "moe-dream-aid-tuition-reduction",
        "name": "教育部圓夢助學網：學雜費減免",
        "url": "https://www.edu.tw/helpdreams/cp.aspx?n=B99F77007C45EA0F&s=4810D2C08B273D5E",
        "organization": "教育部",
        "jurisdiction": "全國",
        "sourceType": "official-program",
        "tags": ["中央", "教育部", "學雜費減免", "助學", "低收入戶", "中低收入戶", "身心障礙", "特殊境遇家庭"],
        "record": {
            "summary": "教育部圓夢助學網整理低收入戶、中低收入戶、身心障礙、原住民、特殊境遇家庭等學生學雜費減免。",
            "audiences": ["學生", "低收入戶", "中低收入戶", "身心障礙者", "原住民", "特殊境遇家庭"],
            "serviceCategories": ["助學", "學雜費減免", "教育補助"],
            "needTags": ["學雜費減免", "助學", "低收入戶學生", "中低收入戶學生", "身障學生", "特殊境遇家庭學生"],
        },
    },
    {
        "id": "wda-labor-subsidy",
        "name": "勞動部勞工補助與就業促進資源",
        "url": "https://emps.wda.gov.tw/Internet/Index/labor-subsidy.aspx",
        "organization": "勞動部勞動力發展署",
        "jurisdiction": "全國",
        "sourceType": "official-portal",
        "tags": ["中央", "勞動部", "勞工補助", "失業給付", "就業促進", "特定對象"],
        "record": {
            "summary": "勞動部勞工補助入口，包含失業給付、跨域津貼、臨工津貼、青年專案與特定對象就業資源。",
            "audiences": ["失業者", "求職者", "青年", "中高齡者", "特定對象"],
            "serviceCategories": ["就業與職訓", "失業給付", "就業獎助", "職涯支持"],
            "needTags": ["失業給付", "勞工補助", "臨工津貼", "跨域津貼", "青年就業", "特定對象就業"],
        },
    },
    {
        "id": "moi-rent-subsidy-115",
        "name": "115年300億元中央擴大租金補貼",
        "url": "https://www.gov.tw/News_Content_37_561179",
        "organization": "內政部國土管理署",
        "jurisdiction": "全國",
        "sourceType": "official-annual-program",
        "tags": ["中央", "租金補貼", "住宅補貼", "115年度", "租屋", "低收入戶", "中低收入戶"],
        "record": {
            "summary": "115年度300億元中央擴大租金補貼，協助租屋家庭減輕租金負擔，申請期間為115年1月1日至115年12月31日。",
            "audiences": ["租屋家庭", "低收入戶", "中低收入戶", "弱勢家庭", "一般民眾"],
            "serviceCategories": ["住宅與租金", "租金補貼", "經濟弱勢"],
            "needTags": ["租金補貼", "租屋補助", "300億租金補貼", "115年租金補貼", "房租", "住宅補貼"],
        },
    },
    {
        "id": "mohw-113-protection-hotline",
        "name": "113保護專線與關懷e起來",
        "url": "https://dep.mohw.gov.tw/DOPS/fp-1183-6499-105.html",
        "organization": "衛生福利部保護服務司",
        "jurisdiction": "全國",
        "sourceType": "official-hotline",
        "tags": ["中央", "113", "保護專線", "家暴", "性侵", "兒少保護", "老人保護", "身障保護"],
        "record": {
            "summary": "113保護專線提供家暴、性侵害、兒少、老人與身心障礙保護通報諮詢；敏感案件應直接洽官方專線。",
            "audiences": ["受暴者", "兒少", "老人", "身心障礙者", "一般民眾"],
            "serviceCategories": ["保護服務", "通報諮詢", "安全求助"],
            "needTags": ["113", "家暴", "性侵", "兒少保護", "老人保護", "身障保護", "通報"],
            "contact": {"phone": "113", "website": "https://dep.mohw.gov.tw/DOPS/fp-1183-6499-105.html"},
        },
    },
]


SOURCE_DOCUMENTS = [
    "C:/Users/Kevin/Downloads/民國114年12月29日，完成社福資源資料庫建置耗時17分鐘。_20251229102216631.pdf",
    "C:/Users/Kevin/Downloads/民國115年1月1日，完成社福資源資料庫建置耗時28分鐘。_20260222123907788.pdf",
    "C:/Users/Kevin/Downloads/民國115年2月7日，完成社福資源資料庫建置耗時93分鐘。_20260222123856072.pdf",
    "C:/Users/Kevin/Downloads/民國115年2月9日，完成社福資源資料庫建置耗時111分鐘。_20260222123848776.docx",
    "C:/Users/Kevin/Downloads/民國115年2月22日，完成社福資源資料庫建置耗時78分鐘。_20260223094133022.docx",
    "C:/Users/Kevin/Downloads/民國115年2月23日，完成社福資源資料庫建置耗時91分鐘。_20260223094149653.docx",
    "C:/Users/Kevin/Downloads/福利資源整理-衛福部&勞動部.docx",
    "C:/Users/Kevin/Downloads/台南市政府.docx",
    "C:/Users/Kevin/Downloads/台中市政府資源_20260328092729830.docx",
    "C:/Users/Kevin/Downloads/民間資源蒐集.pdf",
]


def refresh_policy(normal_days: int = 14, cross_year_days: int = 3) -> dict:
    return {"normalDays": normal_days, "crossYearDays": cross_year_days}


def static_source(source: dict) -> dict:
    item = {
        **source,
        "format": "static-record",
        "crawl": True,
        "crawlDepth": 0,
        "allowInsecureSslFallback": True,
        "refreshPolicy": refresh_policy(),
    }
    item.setdefault("record", {})
    item["record"].setdefault("id", item["id"])
    item["record"].setdefault("name", item["name"])
    item["record"].setdefault("provider", item["organization"])
    item["record"].setdefault("jurisdiction", item["jurisdiction"])
    item["record"].setdefault("county", item["jurisdiction"])
    item["record"].setdefault("freshness", {
        "lastChecked": dt.date.today().isoformat(),
        "sourceUpdatedAt": None,
        "confidence": "official-entry",
        "notes": "Official source entry; specific program pages should be checked from the linked source.",
    })
    return item


def county_source(row: tuple[str, str, str, str]) -> dict:
    source_id, name, url, county = row
    return static_source({
        "id": f"county-{source_id}",
        "name": name,
        "url": url,
        "organization": name,
        "jurisdiction": county,
        "sourceType": "official-local-government",
        "tags": ["縣市政府", "社會局處", county, "社會福利", "地方窗口"],
        "record": {
            "summary": f"{county}社會福利主管機關入口，可查老人、身障、兒少、婦女、社會救助與地方補助資訊。",
            "audiences": ["一般民眾", "老人", "兒少", "婦女", "身心障礙者", "低收入戶", "家庭照顧者"],
            "serviceCategories": ["地方社福窗口", "社會救助", "老人福利", "身障服務", "兒少家庭", "補助查詢"],
            "needTags": [county, "社會局", "社會處", "補助", "急難救助", "身障", "老人福利", "托育"],
            "howToApply": ["開啟縣市社會局處網站", "依服務身分或補助類型查詢", "撥打網站提供的承辦窗口確認年度資格與文件"],
            "documents": ["身分證明", "戶籍或居住證明", "收入或財產證明", "各服務要求文件"],
        },
    })


def main() -> int:
    sources = []
    sources.extend(static_source(source) for source in CENTRAL_SOURCES)
    sources.extend(static_source(source) for source in ECONOMIC_WEAKNESS_SOURCES)
    sources.extend(static_source(source) for source in HIGH_DEMAND_CENTRAL_SOURCES)
    sources.append({
        "id": "sfaa-social-welfare-foundations",
        "name": "全國性財團法人社會福利基金會查詢",
        "url": "https://swft.sfaa.gov.tw/fund/fh0300#",
        "apiBase": "https://swft.sfaa.gov.tw/api",
        "apiUrl": "https://swft.sfaa.gov.tw/api/main/foundBasic/found/searchFront",
        "allowInsecureSslFallback": True,
        "organization": "衛生福利部社會及家庭署",
        "jurisdiction": "全國",
        "sourceType": "official-foundation-directory",
        "format": "sfaa-foundation-json",
        "crawl": True,
        "crawlDepth": 0,
        "pageSize": 500,
        "detailSleepSeconds": 0.04,
        "refreshPolicy": refresh_policy(14, 2),
        "tags": ["中央", "財團法人", "社會福利基金會", "民間資源", "全國性", "今年度仍在運作"],
    })
    sources.append({
        "id": "tainan-welfare-map-dataset",
        "name": "臺南市社會福利地圖開放資料",
        "url": "https://data.tainan.gov.tw/DataSet/Detail/7227a4b1-1fe6-4bde-989b-55b072e3f66e",
        "allowInsecureSslFallback": True,
        "organization": "臺南市政府社會局",
        "jurisdiction": "臺南市",
        "sourceType": "official-open-data",
        "format": "static-record",
        "crawl": True,
        "crawlDepth": 0,
        "refreshPolicy": refresh_policy(30, 3),
        "tags": ["地方政府", "開放資料", "地圖", "臺南"],
        "record": {
            "summary": "臺南市社會福利地圖開放資料入口；原始 JSON resource 端點目前受 robots.txt 限制，本專案保留入口連結供人工查核。",
            "audiences": ["一般民眾", "老人", "婦女", "兒童少年", "身心障礙者", "家庭"],
            "serviceCategories": ["開放資料", "地圖查詢", "地方社福窗口"],
            "needTags": ["臺南", "開放資料", "福利地圖", "附近據點", "社福資源"],
            "howToApply": ["開啟臺南市政府開放資料入口", "依資料集說明前往臺南市福利地圖或社會局查詢", "實際服務仍需以資源點或承辦單位確認"],
            "documents": ["依各資源點規定"],
        },
    })
    sources.append(static_source({
        "id": "tainan-welfare-map",
        "name": "臺南市福利地圖",
        "url": "https://tnsmap.tainan.gov.tw/",
        "organization": "臺南市政府社會局",
        "jurisdiction": "臺南市",
        "sourceType": "official-map",
        "tags": ["地方政府", "地圖", "臺南", "行政區"],
        "record": {
            "summary": "以服務對象、服務類別、行政區與距離查找臺南市福利資源。",
            "audiences": ["老人", "婦女", "兒童少年", "身心障礙者", "家庭", "災害需求者"],
            "serviceCategories": ["地圖查詢", "社福及社區", "長照", "災害救助"],
            "needTags": ["臺南", "地圖", "附近據點", "老人福利", "身障", "家庭福利"],
        },
    }))
    sources.append(static_source({
        "id": "taichung-welfare-network",
        "name": "臺中市社會福利服務資源網",
        "url": "https://welfare.taichung.gov.tw/",
        "organization": "臺中市政府社會局",
        "jurisdiction": "臺中市",
        "sourceType": "official-portal",
        "tags": ["地方政府", "資源網", "臺中"],
        "record": {
            "summary": "臺中市整合服務中心、社福便利站與身障便利通等入口。",
            "audiences": ["兒少", "婦女", "老人", "身心障礙者"],
            "serviceCategories": ["服務中心", "據點查詢", "身障生活", "申請資訊"],
            "needTags": ["臺中", "社福便利站", "身障便利通", "服務中心"],
        },
    }))
    sources.append(static_source({
        "id": "taipei-welfare-map",
        "name": "臺北市社福設施地圖資訊網",
        "url": "https://map.dosw.gov.taipei/",
        "organization": "臺北市政府社會局",
        "jurisdiction": "臺北市",
        "sourceType": "official-map",
        "tags": ["地方政府", "地圖", "臺北", "社福設施"],
        "record": {
            "summary": "以地圖查找臺北市各類型福利機構及設施。",
            "audiences": ["嬰幼兒", "兒童少年", "老人", "身心障礙者", "婦女", "單親", "新移民"],
            "serviceCategories": ["地圖查詢", "照顧服務", "托育", "身障機構", "樂齡學堂"],
            "needTags": ["臺北", "附近機構", "托育", "長照", "身障", "樂齡"],
        },
    }))
    sources.extend(county_source(row) for row in COUNTY_SOCIAL_BUREAUS)

    output = {
        "generatedAt": dt.date.today().isoformat(),
        "note": "Official-source registry for Taiwan welfare resource coverage. Raw Kevin-provided source documents were not available locally during generation.",
        "sourceDocuments": [{"path": path, "status": "missing"} for path in SOURCE_DOCUMENTS],
        "sources": sources,
    }
    Path("data/sources.json").write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(sources)} sources to data/sources.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
