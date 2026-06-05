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


LOCAL_PROGRAM_SOURCES_BATCH_2 = [
    {
        "id": "taipei-low-income-rent-subsidy-115",
        "name": "115年度臺北市低收入戶承租住宅租金補貼",
        "url": "https://www.gov.taipei/News_Content.aspx?n=D0042A87C2F0270A&s=22C0CE414323E107&sms=78D644F2755ACCAA",
        "organization": "臺北市政府都市發展局",
        "jurisdiction": "臺北市",
        "sourceType": "official-local-program",
        "tags": ["地方政府", "臺北市", "低收入戶", "租金補貼", "住宅補貼", "115年度"],
        "record": {
            "summary": "臺北市115年度低收入戶承租住宅租金補貼，審查合格者每戶每月補貼1,500元。",
            "audiences": ["低收入戶", "租屋家庭"],
            "serviceCategories": ["公部門地方資源", "住宅與租金", "租金補貼", "低收入戶與中低收入戶救助"],
            "needTags": ["臺北租金補貼", "低收入戶租屋", "房租補助", "臺北市低收入戶"],
            "eligibility": "需為臺北市列冊低收入戶、在臺北市有租賃住宅事實，且符合無自有住宅及公告所列住宅、租約與補貼排除規定。",
            "conditionSourceNote": "臺北市115年度低收入戶承租住宅租金補貼公告列明租屋事實、無自有住宅、未重複領取住宅補貼等條件。",
            "applicationConditions": [
                {
                    "label": "低收入戶身分與租屋事實",
                    "requirement": "申請人需為臺北市低收入戶，且在臺北市有租賃住宅事實。",
                    "note": "同一住宅原則僅核發一戶低收入戶租金補貼。",
                    "sourceDate": "115年度",
                    "sourceUrl": "https://www.gov.taipei/News_Content.aspx?n=D0042A87C2F0270A&s=22C0CE414323E107&sms=78D644F2755ACCAA",
                },
                {
                    "label": "無自有住宅與未重複補貼",
                    "requirement": "申請人及公告列明家庭成員需符合無自有住宅規定，且未承租政府出租住宅、未接受政府住宅補貼或住宿式照顧補助。",
                    "note": "住宅用途、租約關係與出租人親屬關係也會被審查。",
                    "sourceDate": "115年度",
                    "sourceUrl": "https://www.gov.taipei/News_Content.aspx?n=D0042A87C2F0270A&s=22C0CE414323E107&sms=78D644F2755ACCAA",
                },
            ],
            "benefitSourceNote": "公告第十點列明補貼方式。",
            "benefitItems": [
                {
                    "label": "低收入戶承租住宅租金補貼",
                    "amount": "1,500元",
                    "unit": "每戶每月",
                    "note": "每月租金低於1,500元者，以實際租金核發；追溯至受理申請月份發給至當年度年底或租約有效期間止。",
                    "sourceDate": "115年度",
                    "sourceUrl": "https://www.gov.taipei/News_Content.aspx?n=D0042A87C2F0270A&s=22C0CE414323E107&sms=78D644F2755ACCAA",
                }
            ],
            "applicationMethodSourceNote": "文件不全會通知限期補正；資格以提出申請日具備條件為審查依據。",
            "howToApply": ["依公告備妥申請資料。", "向臺北市政府都市發展局公告受理窗口提出。", "審查期間若戶籍、住宅持有或租約異動，需主動補正。"],
            "documents": ["申請書", "租賃契約", "申請人指定帳戶", "家庭成員財產資料或主管機關要求文件"],
            "contact": {"website": "https://www.gov.taipei/News_Content.aspx?n=D0042A87C2F0270A&s=22C0CE414323E107&sms=78D644F2755ACCAA"},
            "freshness": {"lastChecked": dt.date.today().isoformat(), "sourceUpdatedAt": "115年度", "confidence": "source-dated", "notes": "Official Taipei 115 annual program announcement."},
        },
    },
    {
        "id": "taipei-emergency-assistance",
        "name": "臺北市急難救助",
        "url": "https://dosw.gov.taipei/cp.aspx?n=0BF751F1B9F07AA1",
        "organization": "臺北市政府社會局",
        "jurisdiction": "臺北市",
        "sourceType": "official-local-program",
        "tags": ["地方政府", "臺北市", "急難救助", "社福中心", "區公所"],
        "record": {
            "summary": "臺北市民因死亡、重病、意外、失業、服刑、帳戶凍結或重大變故導致生活陷困時，可洽社福中心或區公所申請急難救助。",
            "audiences": ["急難家庭", "一般民眾", "低收入戶", "中低收入戶"],
            "serviceCategories": ["公部門地方資源", "急難救助", "社福中心", "現金與生活扶助"],
            "needTags": ["臺北急難救助", "臨時救助", "社福中心", "區公所", "生活陷困"],
            "eligibility": "設籍臺北市市民有死亡殮葬、意外或重病、主要生計者無法工作、帳戶凍結、福利保險尚未核准或其他重大變故等情形。",
            "conditionSourceNote": "臺北市社會局頁面與急難救助金核發作業要點列明救助事由。",
            "applicationConditions": [
                {
                    "label": "生活陷於困境",
                    "requirement": "因死亡、重病、意外、失業、服刑、帳戶凍結、等待福利保險核准或其他重大變故，致生活陷於困境。",
                    "note": "社會局或區公所可訪視評估，必要時轉介其他社福、衛生、勞工或教育資源。",
                    "sourceDate": "頁面資料更新115-03-31；法規修正110-12-29",
                    "sourceUrl": "https://dosw.gov.taipei/cp.aspx?n=0BF751F1B9F07AA1",
                }
            ],
            "benefitSourceNote": "金額依臺北市急難救助金核發作業要點及給付標準表，由社會局或區公所依個案事由核定。",
            "benefitItems": [
                {
                    "label": "急難救助金",
                    "amount": "依給付標準表及個案核定",
                    "unit": "次",
                    "note": "不同急難事由金額不同，需由社會局或區公所審認。",
                    "sourceDate": "頁面資料更新115-03-31；法規修正110-12-29",
                    "sourceUrl": "https://laws.gov.taipei/Law/LawSearch/LawArticleContent/FL002892",
                }
            ],
            "applicationMethodSourceNote": "向社會局所屬社會福利服務中心或戶籍所在地區公所提出；車資救助另有特定受理窗口。",
            "howToApply": ["急迫時先洽居住地社會福利服務中心或戶籍地區公所。", "說明急難原因並檢附相關證明。", "由承辦單位評估是否核發或轉介其他資源。"],
            "documents": ["急難事由證明", "身分及戶籍資料", "收入或財產相關資料", "承辦單位要求文件"],
            "contact": {"website": "https://dosw.gov.taipei/cp.aspx?n=0BF751F1B9F07AA1"},
            "freshness": {"lastChecked": dt.date.today().isoformat(), "sourceUpdatedAt": "115-03-31", "confidence": "source-dated", "notes": "Official Taipei social welfare page checked."},
        },
    },
    {
        "id": "ntpc-low-income-application-115",
        "name": "新北市低收入戶資格申請",
        "url": "https://service.ntpc.gov.tw/eservice/CaseData.action?itemId=110017",
        "organization": "新北市政府社會局",
        "jurisdiction": "新北市",
        "sourceType": "official-local-application",
        "tags": ["地方政府", "新北市", "低收入戶", "生活扶助", "線上申辦", "115年度"],
        "record": {
            "summary": "新北市低收入戶資格申請，含115年度所得、動產、不動產標準與低收入戶生活補助金額。",
            "audiences": ["低收入戶", "經濟困難家庭", "學生", "兒少家庭"],
            "serviceCategories": ["公部門地方資源", "低收入戶與中低收入戶救助", "生活補助", "線上申辦"],
            "needTags": ["新北低收入戶", "新北生活扶助", "低收入戶申請", "新北線上申辦"],
            "eligibility": "需設籍並實際居住新北市，最近一年居住國內超過183日，且家庭收入、動產、不動產符合115年度低收入戶標準。",
            "conditionSourceNote": "新北市線上申辦案件說明列明115年度低收入戶審查標準。",
            "applicationConditions": [
                {
                    "label": "115年度低收入戶標準",
                    "requirement": "家庭總收入平均每人每月低於17,750元，動產每人每年未超過10萬元，不動產合計未超過472萬元。",
                    "note": "仍需依社會救助法計算家庭應計人口。",
                    "sourceDate": "查核日2026-06-05",
                    "sourceUrl": "https://service.ntpc.gov.tw/eservice/CaseData.action?itemId=110017",
                }
            ],
            "benefitSourceNote": "新北市線上申辦案件說明列出低收入戶各款生活扶助金額。",
            "benefitItems": [
                {"label": "一款低收入戶", "amount": "13,303元", "unit": "每人每月", "note": "戶內每人每月補助生活費。", "sourceDate": "查核日2026-06-05", "sourceUrl": "https://service.ntpc.gov.tw/eservice/CaseData.action?itemId=110017"},
                {"label": "二款低收入戶", "amount": "6,825元", "unit": "每戶每月", "note": "另戶內未滿15歲兒童每人每月3,008元。", "sourceDate": "查核日2026-06-05", "sourceUrl": "https://service.ntpc.gov.tw/eservice/CaseData.action?itemId=110017"},
                {"label": "二、三款在學生活補助", "amount": "6,825元", "unit": "每人每月", "note": "未滿25歲列冊低收入戶高中職以上在學學生，需每學期送在學證明審核。", "sourceDate": "查核日2026-06-05", "sourceUrl": "https://service.ntpc.gov.tw/eservice/CaseData.action?itemId=110017"},
            ],
            "applicationMethodSourceNote": "新北市線上申辦頁面列出書表下載與應自行檢附文件。",
            "howToApply": ["可由新北市線上申辦頁面進入案件。", "準備郵局存簿、學生證明、診斷書、租約或其他實際需要文件。", "送件後依區公所或社會局通知補件與審查。"],
            "documents": ["全戶最近1年郵局存簿內頁明細", "郵局存摺封面影本", "學生證或在學證明", "診斷書、租賃契約或其他相關證明"],
            "contact": {"website": "https://service.ntpc.gov.tw/eservice/CaseData.action?itemId=110017"},
            "freshness": {"lastChecked": dt.date.today().isoformat(), "sourceUpdatedAt": None, "confidence": "checked", "notes": "Official New Taipei online application page."},
        },
    },
    {
        "id": "ntpc-low-income-home-repair-115",
        "name": "新北市115年度低收入戶修繕住宅補助",
        "url": "https://www.planning.ntpc.gov.tw/home.jsp?act=be4f48068b2b0031&dataserno=9f2f505e1fe1dd6c351b9a407d804389&id=f57762b740db24e7",
        "organization": "新北市政府城鄉發展局",
        "jurisdiction": "新北市",
        "sourceType": "official-local-annual-program",
        "tags": ["地方政府", "新北市", "低收入戶", "住宅修繕", "115年度"],
        "record": {
            "summary": "新北市115年度低收入戶修繕住宅補助，依低收入戶款別每戶最高補助5萬至10萬元。",
            "audiences": ["低收入戶", "弱勢家庭"],
            "serviceCategories": ["公部門地方資源", "住宅與租金", "居住修繕", "低收入戶與中低收入戶救助"],
            "needTags": ["新北住宅修繕", "低收入戶修繕", "屋頂漏水", "住宅修繕補助"],
            "eligibility": "新北市列冊低收入戶，設籍且實際居住新北滿6個月，住宅建築完成10年以上，且5年內未曾接受同類修繕補助。",
            "conditionSourceNote": "新北市公告列明申請人、修繕住宅與受理期間條件。",
            "applicationConditions": [
                {"label": "申請人資格", "requirement": "新北市列冊低收入戶、設籍且實際居住新北市滿6個月。", "note": "不得居住於公有宿舍、出租國宅、社會住宅或社會福利機構。", "sourceDate": "2026-02-24", "sourceUrl": "https://www.planning.ntpc.gov.tw/home.jsp?act=be4f48068b2b0031&dataserno=9f2f505e1fe1dd6c351b9a407d804389&id=f57762b740db24e7"},
                {"label": "住宅條件", "requirement": "修繕住宅須為建築完成10年以上，且為自有或2等親以內親屬持有住宅。", "note": "5年內不得曾接受本補助或政府其他修繕住宅費用補貼。", "sourceDate": "2026-02-24", "sourceUrl": "https://www.planning.ntpc.gov.tw/home.jsp?act=be4f48068b2b0031&dataserno=9f2f505e1fe1dd6c351b9a407d804389&id=f57762b740db24e7"},
            ],
            "benefitSourceNote": "公告第五點列明各款低收入戶補助上限。",
            "benefitItems": [
                {"label": "第1款低收入戶", "amount": "最高10萬元", "unit": "每戶", "note": "依實際修繕與審查結果核定。", "sourceDate": "2026-02-24", "sourceUrl": "https://www.planning.ntpc.gov.tw/home.jsp?act=be4f48068b2b0031&dataserno=9f2f505e1fe1dd6c351b9a407d804389&id=f57762b740db24e7"},
                {"label": "第2款低收入戶", "amount": "最高7萬元", "unit": "每戶", "note": "依實際修繕與審查結果核定。", "sourceDate": "2026-02-24", "sourceUrl": "https://www.planning.ntpc.gov.tw/home.jsp?act=be4f48068b2b0031&dataserno=9f2f505e1fe1dd6c351b9a407d804389&id=f57762b740db24e7"},
                {"label": "第3款低收入戶", "amount": "最高5萬元", "unit": "每戶", "note": "依實際修繕與審查結果核定。", "sourceDate": "2026-02-24", "sourceUrl": "https://www.planning.ntpc.gov.tw/home.jsp?act=be4f48068b2b0031&dataserno=9f2f505e1fe1dd6c351b9a407d804389&id=f57762b740db24e7"},
            ],
            "applicationMethodSourceNote": "受理期間自115年3月1日至115年12月31日或經費用罄止。",
            "howToApply": ["於受理期間向新北市政府城鄉發展局或各區公所提出。", "先送申請表、權狀、估價單與施工前照片。", "核定後3個月內完成修繕，完工後送發票、照片與領據辦理撥款。"],
            "documents": ["申請表", "身分證或戶口名簿影本", "住宅所有權狀或建號", "2家廠商估價單", "施工前照片", "郵局存摺封面影本"],
            "contact": {"website": "https://www.planning.ntpc.gov.tw/home.jsp?act=be4f48068b2b0031&dataserno=9f2f505e1fe1dd6c351b9a407d804389&id=f57762b740db24e7"},
            "freshness": {"lastChecked": dt.date.today().isoformat(), "sourceUpdatedAt": "2026-02-24", "confidence": "source-dated", "notes": "Official New Taipei 115 annual program announcement."},
        },
    },
    {
        "id": "taoyuan-low-income-application-115",
        "name": "桃園市115年低收入戶與中低收入戶資格申請",
        "url": "https://www.dayuan.tycg.gov.tw/News_Content.aspx?n=7621&s=1583686&sms=12069",
        "organization": "桃園市政府社會局",
        "jurisdiction": "桃園市",
        "sourceType": "official-local-application",
        "tags": ["地方政府", "桃園市", "低收入戶", "中低收入戶", "115年度", "社會救助"],
        "record": {
            "summary": "桃園市115年度低收入戶及中低收入戶最低生活費暨家庭財產一定金額，含最低生活費、動產、不動產門檻與應備資料。",
            "audiences": ["低收入戶", "中低收入戶", "經濟困難家庭"],
            "serviceCategories": ["公部門地方資源", "低收入戶與中低收入戶救助", "申請資訊", "經濟弱勢"],
            "needTags": ["桃園低收入戶", "桃園中低收入戶", "桃園115標準", "社會救助申請"],
            "eligibility": "115年度桃園市低收入戶最低生活費為每人每月17,186元；中低收入戶為每人每月25,779元，並需同時符合動產、不動產及家庭人口審查。",
            "conditionSourceNote": "桃園市政府社會局115年資格說明列出收入、動產、不動產門檻。",
            "applicationConditions": [
                {
                    "label": "115年度低收入戶標準",
                    "requirement": "最低生活費每人每月17,186元；動產每人每年96,000元；不動產每戶470萬元。",
                    "note": "家庭應計人口、收入及財產仍由地方政府依社會救助規定審查。",
                    "sourceDate": "115年度；頁面查核日2026-06-05",
                    "sourceUrl": "https://www.dayuan.tycg.gov.tw/News_Content.aspx?n=7621&s=1583686&sms=12069",
                },
                {
                    "label": "115年度中低收入戶標準",
                    "requirement": "最低生活費1.5倍，每人每月25,779元；動產每人每年144,000元；不動產每戶564萬元。",
                    "note": "只看單一收入數字不等於一定通過，仍需看戶內人口與財產。",
                    "sourceDate": "115年度；頁面查核日2026-06-05",
                    "sourceUrl": "https://www.dayuan.tycg.gov.tw/News_Content.aspx?n=7621&s=1583686&sms=12069",
                },
            ],
            "benefitSourceNote": "本卡是資格入口；通過後依各項社會救助或福利身分核發。",
            "benefitItems": [
                {
                    "label": "資格門檻本身不核發金額",
                    "amount": "無固定金額",
                    "unit": "",
                    "note": "取得低收入戶或中低收入戶資格後，才會銜接生活扶助、醫療、教育、租金或其他補助。",
                    "sourceDate": "115年度；頁面查核日2026-06-05",
                    "sourceUrl": "https://www.dayuan.tycg.gov.tw/News_Content.aspx?n=7621&s=1583686&sms=12069",
                }
            ],
            "applicationMethodSourceNote": "桃園市頁面列出申請人與受扶助人口郵局存摺封面影本等資料提醒。",
            "howToApply": ["向戶籍所在地區公所提出申請。", "準備申請人及受扶助人口資料與郵局存摺封面影本。", "依區公所或社會局通知補件與等待審查。"],
            "documents": ["申請表", "郵局存摺封面影本", "戶籍、收入與財產相關資料", "區公所要求文件"],
            "contact": {"website": "https://www.dayuan.tycg.gov.tw/News_Content.aspx?n=7621&s=1583686&sms=12069"},
            "freshness": {"lastChecked": dt.date.today().isoformat(), "sourceUpdatedAt": "115年度", "confidence": "source-dated", "notes": "Official Taoyuan 115 annual qualification announcement mirrored by Dayuan District Office."},
        },
    },
    {
        "id": "taoyuan-low-income-living-assistance",
        "name": "桃園市低收入戶生活扶助",
        "url": "https://sab.tycg.gov.tw/home.jsp?aplistdn=ou%3Ddata%2Cou%3Dassistance%2Cou%3Dchsocial%2Cou%3Dap_root%2Co%3Dtycg%2Cc%3Dtw&dataserno=201209130004&id=30579&mcustomize=onemessages_view.jsp&parentpath=0%2C30484%2C30494&toolsflag=Y",
        "organization": "桃園市政府社會局",
        "jurisdiction": "桃園市",
        "sourceType": "official-local-program",
        "tags": ["地方政府", "桃園市", "低收入戶", "生活扶助", "兒童生活補助", "就學生活補助"],
        "record": {
            "summary": "桃園市低收入戶生活扶助，含一款、二款、兒童及高中職以上就學生活補助。",
            "audiences": ["低收入戶", "兒少家庭", "學生", "經濟困難家庭"],
            "serviceCategories": ["公部門地方資源", "低收入戶與中低收入戶救助", "生活補助", "子女就學"],
            "needTags": ["桃園生活扶助", "桃園低收補助", "兒童生活補助", "就學生活補助"],
            "eligibility": "需為桃園市列冊低收入戶，補助款別與戶內兒童、學生身分依社會局審查結果認定。",
            "conditionSourceNote": "桃園市社會局生活扶助頁面與金額調整公告列出補助對象及金額。",
            "applicationConditions": [
                {
                    "label": "列冊低收入戶",
                    "requirement": "已由桃園市審核列冊為低收入戶，並依款別、年齡或就學身分核發。",
                    "note": "福利身分異動或不符合資格時，補助可能調整或停止。",
                    "sourceDate": "頁面查核日2026-06-05",
                    "sourceUrl": "https://sab.tycg.gov.tw/home.jsp?aplistdn=ou%3Ddata%2Cou%3Dassistance%2Cou%3Dchsocial%2Cou%3Dap_root%2Co%3Dtycg%2Cc%3Dtw&dataserno=201209130004&id=30579&mcustomize=onemessages_view.jsp&parentpath=0%2C30484%2C30494&toolsflag=Y",
                }
            ],
            "benefitSourceNote": "桃園市113年度起調整低收入戶生活扶助金額，仍由社會局生活扶助頁面列為現行參考。",
            "benefitItems": [
                {"label": "第1款家庭生活補助", "amount": "13,115元", "unit": "每人每月", "note": "低收入戶第1款家庭生活補助。", "sourceDate": "113年度調整公告；查核日2026-06-05", "sourceUrl": "https://sab.tycg.gov.tw/home.jsp?aplistdn=ou%3Ddata%2Cou%3Dassistance%2Cou%3Dchsocial%2Cou%3Dap_root%2Co%3Dtycg%2Cc%3Dtw&dataserno=201209130004&id=30579&mcustomize=onemessages_view.jsp&parentpath=0%2C30484%2C30494&toolsflag=Y"},
                {"label": "第2款家庭生活補助", "amount": "6,825元", "unit": "每戶每月", "note": "低收入戶第2款家庭生活補助。", "sourceDate": "113年度調整公告；查核日2026-06-05", "sourceUrl": "https://sab.tycg.gov.tw/home.jsp?aplistdn=ou%3Ddata%2Cou%3Dassistance%2Cou%3Dchsocial%2Cou%3Dap_root%2Co%3Dtycg%2Cc%3Dtw&dataserno=201209130004&id=30579&mcustomize=onemessages_view.jsp&parentpath=0%2C30484%2C30494&toolsflag=Y"},
                {"label": "兒童生活補助", "amount": "3,008元", "unit": "每人每月", "note": "第2款及第3款低收入戶15歲以下兒童。", "sourceDate": "113年度調整公告；查核日2026-06-05", "sourceUrl": "https://sab.tycg.gov.tw/home.jsp?aplistdn=ou%3Ddata%2Cou%3Dassistance%2Cou%3Dchsocial%2Cou%3Dap_root%2Co%3Dtycg%2Cc%3Dtw&dataserno=201209130004&id=30579&mcustomize=onemessages_view.jsp&parentpath=0%2C30484%2C30494&toolsflag=Y"},
                {"label": "高中職以上就學生活補助", "amount": "6,825元", "unit": "每人每月", "note": "第2款及第3款低收入戶高中職以上學生。", "sourceDate": "113年度調整公告；查核日2026-06-05", "sourceUrl": "https://sab.tycg.gov.tw/home.jsp?aplistdn=ou%3Ddata%2Cou%3Dassistance%2Cou%3Dchsocial%2Cou%3Dap_root%2Co%3Dtycg%2Cc%3Dtw&dataserno=201209130004&id=30579&mcustomize=onemessages_view.jsp&parentpath=0%2C30484%2C30494&toolsflag=Y"},
            ],
            "applicationMethodSourceNote": "低收入戶生活扶助通常由列冊資格連動，實際核發與異動以社會局或區公所審查為準。",
            "howToApply": ["先辦理低收入戶資格申請或年度複查。", "符合款別、兒童或就學身分後，由社會局依規定核發。", "學生補助需依通知檢附在學證明或相關文件。"],
            "documents": ["低收入戶資格資料", "郵局或指定帳戶", "在學證明", "社會局或區公所要求文件"],
            "contact": {"website": "https://sab.tycg.gov.tw/home.jsp?aplistdn=ou%3Ddata%2Cou%3Dassistance%2Cou%3Dchsocial%2Cou%3Dap_root%2Co%3Dtycg%2Cc%3Dtw&dataserno=201209130004&id=30579&mcustomize=onemessages_view.jsp&parentpath=0%2C30484%2C30494&toolsflag=Y"},
            "freshness": {"lastChecked": dt.date.today().isoformat(), "sourceUpdatedAt": None, "confidence": "checked", "notes": "Official Taoyuan social bureau assistance page."},
        },
    },
    {
        "id": "taichung-low-income-standards-115",
        "name": "臺中市115年低收入戶與中低收入戶審核標準",
        "url": "https://www.society.taichung.gov.tw/13710/13735/13856/13862/3101150",
        "organization": "臺中市政府社會局",
        "jurisdiction": "臺中市",
        "sourceType": "official-local-annual-standard",
        "tags": ["地方政府", "臺中市", "低收入戶", "中低收入戶", "115年度"],
        "record": {
            "summary": "臺中市115年最低生活費、低收入戶及中低收入戶審核標準公告。",
            "audiences": ["低收入戶", "中低收入戶", "經濟困難家庭"],
            "serviceCategories": ["公部門地方資源", "年度標準", "低收入戶與中低收入戶救助", "申請資訊"],
            "needTags": ["臺中低收入戶", "臺中中低收入戶", "臺中115標準", "最低生活費"],
            "eligibility": "115年度臺中市低收入戶標準為每人每月16,431元；中低收入戶為每人每月24,647元，並需符合動產與不動產限制。",
            "conditionSourceNote": "臺中市政府社會局公告115年最低生活費及家庭財產一定金額。",
            "applicationConditions": [
                {"label": "低收入戶所得標準", "requirement": "家庭總收入平均每人每月未超過16,431元。", "note": "動產、不動產及家庭應計人口仍須一併審查。", "sourceDate": "114-09-12", "sourceUrl": "https://www.society.taichung.gov.tw/13710/13735/13856/13862/3101150"},
                {"label": "中低收入戶所得標準", "requirement": "家庭總收入平均每人每月未超過24,647元。", "note": "中低收入戶不是只看收入，仍需看財產與家庭成員。", "sourceDate": "114-09-12", "sourceUrl": "https://www.society.taichung.gov.tw/13710/13735/13856/13862/3101150"},
            ],
            "benefitSourceNote": "本卡為審核標準，不直接核發金額；低收入戶相關給付需看福利一覽表或個別申請項目。",
            "benefitItems": [
                {"label": "資格門檻本身不核發金額", "amount": "無固定金額", "unit": "", "note": "通過資格後，可能銜接生活扶助、租金、就學交通、喪葬或其他低收入戶福利。", "sourceDate": "114-09-12", "sourceUrl": "https://www.society.taichung.gov.tw/13710/13735/13856/13862/3101150"}
            ],
            "applicationMethodSourceNote": "實際申請仍由戶籍地區公所或社會局依規定審查。",
            "howToApply": ["先查看115年度標準是否大致符合。", "向戶籍地區公所提出低收入戶或中低收入戶申請。", "依通知補齊收入、財產、戶籍與其他證明文件。"],
            "documents": ["申請書", "戶籍資料", "收入與財產資料", "郵局或指定帳戶", "區公所要求文件"],
            "contact": {"website": "https://www.society.taichung.gov.tw/13710/13735/13856/13862/3101150"},
            "freshness": {"lastChecked": dt.date.today().isoformat(), "sourceUpdatedAt": "114-09-12", "confidence": "source-dated", "notes": "Official Taichung 115 annual standard announcement."},
        },
    },
    {
        "id": "taichung-low-income-benefit-overview-115",
        "name": "臺中市低收入戶福利一覽表",
        "url": "https://www.society.taichung.gov.tw/media/1333656/%E8%87%BA%E4%B8%AD%E5%B8%82%E4%BD%8E%E6%94%B6%E5%85%A5%E6%88%B6%E7%A6%8F%E5%88%A9%E4%B8%80%E8%A6%BD%E8%A1%A8.pdf",
        "organization": "臺中市政府社會局",
        "jurisdiction": "臺中市",
        "sourceType": "official-local-benefit-table",
        "tags": ["地方政府", "臺中市", "低收入戶", "福利一覽表", "租金補助", "教育補助"],
        "record": {
            "summary": "臺中市低收入戶福利一覽表，整理育兒、就學、喪葬、生育、產婦、嬰兒營養、租金與安置等補助。",
            "audiences": ["低收入戶", "兒少家庭", "學生", "租屋家庭", "經濟困難家庭"],
            "serviceCategories": ["公部門地方資源", "低收入戶與中低收入戶救助", "租金補貼", "教育補助", "兒少家庭"],
            "needTags": ["臺中低收入戶福利", "臺中租金補助", "就學交通補助", "喪葬補助", "生育補助"],
            "eligibility": "以臺中市列冊低收入戶為主要對象；各項福利另依年齡、就學、租屋、死亡或生育事實審查。",
            "conditionSourceNote": "臺中市低收入戶福利一覽表列明各補助對象與受理窗口。",
            "applicationConditions": [
                {"label": "列冊低收入戶", "requirement": "需為臺中市列冊低收入戶，並符合各補助項目所列年齡、就學、租屋或事件條件。", "note": "不同項目申請期限不同，例如就學交通、喪葬、生育相關補助各有期限。", "sourceDate": "114-11-07", "sourceUrl": "https://www.society.taichung.gov.tw/media/1333656/%E8%87%BA%E4%B8%AD%E5%B8%82%E4%BD%8E%E6%94%B6%E5%85%A5%E6%88%B6%E7%A6%8F%E5%88%A9%E4%B8%80%E8%A6%BD%E8%A1%A8.pdf"}
            ],
            "benefitSourceNote": "一覽表列出多項低收入戶常用補助金額。",
            "benefitItems": [
                {"label": "租金補助", "amount": "2,000元至5,000元", "unit": "每月", "note": "戶內1人2,000元；2至4人4,000元；5人以上5,000元。", "sourceDate": "114-11-07", "sourceUrl": "https://www.society.taichung.gov.tw/media/1333656/%E8%87%BA%E4%B8%AD%E5%B8%82%E4%BD%8E%E6%94%B6%E5%85%A5%E6%88%B6%E7%A6%8F%E5%88%A9%E4%B8%80%E8%A6%BD%E8%A1%A8.pdf"},
                {"label": "就學交通補助", "amount": "1,000元至6,000元", "unit": "每學期", "note": "國小1,000元、國中2,000元、高中職4,000元、大專6,000元；研究所不補助。", "sourceDate": "114-11-07", "sourceUrl": "https://www.society.taichung.gov.tw/media/1333656/%E8%87%BA%E4%B8%AD%E5%B8%82%E4%BD%8E%E6%94%B6%E5%85%A5%E6%88%B6%E7%A6%8F%E5%88%A9%E4%B8%80%E8%A6%BD%E8%A1%A8.pdf"},
                {"label": "喪葬補助", "amount": "最高3萬元", "unit": "次", "note": "列冊低收入戶死亡者，事實發生後3個月內申請。", "sourceDate": "114-11-07", "sourceUrl": "https://www.society.taichung.gov.tw/media/1333656/%E8%87%BA%E4%B8%AD%E5%B8%82%E4%BD%8E%E6%94%B6%E5%85%A5%E6%88%B6%E7%A6%8F%E5%88%A9%E4%B8%80%E8%A6%BD%E8%A1%A8.pdf"},
                {"label": "生育補助", "amount": "10,200元", "unit": "每胎", "note": "雙胞胎20,400元，依此類推；事實發生後3個月內申請。", "sourceDate": "114-11-07", "sourceUrl": "https://www.society.taichung.gov.tw/media/1333656/%E8%87%BA%E4%B8%AD%E5%B8%82%E4%BD%8E%E6%94%B6%E5%85%A5%E6%88%B6%E7%A6%8F%E5%88%A9%E4%B8%80%E8%A6%BD%E8%A1%A8.pdf"},
                {"label": "嬰兒營養補助", "amount": "1,800元", "unit": "每月，最多12個月", "note": "依列冊時間起算比例差額補助。", "sourceDate": "114-11-07", "sourceUrl": "https://www.society.taichung.gov.tw/media/1333656/%E8%87%BA%E4%B8%AD%E5%B8%82%E4%BD%8E%E6%94%B6%E5%85%A5%E6%88%B6%E7%A6%8F%E5%88%A9%E4%B8%80%E8%A6%BD%E8%A1%A8.pdf"},
            ],
            "applicationMethodSourceNote": "各項補助受理窗口不同，多數由戶籍地區公所辦理。",
            "howToApply": ["先確認想申請的一覽表項目與期限。", "依項目洽戶籍地區公所、學校或社會局承辦科室。", "準備身分、列冊、就學、租屋或事件證明後送件。"],
            "documents": ["低收入戶證明", "申請表", "依項目檢附就學、租約、死亡、出生或其他證明"],
            "contact": {"website": "https://www.society.taichung.gov.tw/media/1333656/%E8%87%BA%E4%B8%AD%E5%B8%82%E4%BD%8E%E6%94%B6%E5%85%A5%E6%88%B6%E7%A6%8F%E5%88%A9%E4%B8%80%E8%A6%BD%E8%A1%A8.pdf"},
            "freshness": {"lastChecked": dt.date.today().isoformat(), "sourceUpdatedAt": "114-11-07", "confidence": "source-dated", "notes": "Official Taichung low-income benefit table PDF."},
        },
    },
    {
        "id": "tainan-low-income-living-assistance",
        "name": "臺南市低收入戶家庭生活補助",
        "url": "https://sab.tainan.gov.tw/News_Content.aspx?n=21390&s=4378483",
        "organization": "臺南市政府社會局",
        "jurisdiction": "臺南市",
        "sourceType": "official-local-program",
        "tags": ["地方政府", "臺南市", "低收入戶", "生活扶助", "家庭生活補助"],
        "record": {
            "summary": "臺南市低收入戶家庭生活補助，由社會局逕撥入低收入戶指定郵政或農會帳戶。",
            "audiences": ["低收入戶", "經濟困難家庭", "兒少家庭", "學生"],
            "serviceCategories": ["公部門地方資源", "低收入戶與中低收入戶救助", "生活補助", "現金與生活扶助"],
            "needTags": ["臺南低收入戶", "臺南生活扶助", "家庭生活補助", "低收補助"],
            "eligibility": "需為臺南市列冊低收入戶，補助款別與戶內成員年齡、就學身分依社會局審查結果認定。",
            "conditionSourceNote": "臺南市社會局低收入戶家庭生活補助頁面列明補助對象與核撥方式。",
            "applicationConditions": [
                {"label": "列冊低收入戶", "requirement": "經臺南市審核列冊為低收入戶後，依款別與戶內成員情況核給生活補助。", "note": "家庭人口、款別或就學狀態異動會影響補助。", "sourceDate": "頁面查核日2026-06-05", "sourceUrl": "https://sab.tainan.gov.tw/News_Content.aspx?n=21390&s=4378483"}
            ],
            "benefitSourceNote": "臺南市屬臺灣省標準地區，低收入戶生活扶助金額可對照中央臺灣省及福建省生活扶助金額表；實際仍以臺南市核定為準。",
            "benefitItems": [
                {"label": "第1款家庭生活補助", "amount": "11,850元", "unit": "每人每月", "note": "臺灣省低收入戶生活扶助金額。", "sourceDate": "現行調整表；查核日2026-06-05", "sourceUrl": "https://www.mohw.gov.tw/dl-9691-e9b88768-ad1a-4fa4-aae6-f4df82da30f6.html"},
                {"label": "第2款家庭生活補助", "amount": "6,825元", "unit": "每戶每月", "note": "臺灣省低收入戶生活扶助金額。", "sourceDate": "現行調整表；查核日2026-06-05", "sourceUrl": "https://www.mohw.gov.tw/dl-9691-e9b88768-ad1a-4fa4-aae6-f4df82da30f6.html"},
                {"label": "兒童生活補助", "amount": "3,008元", "unit": "每人每月", "note": "第2款及第3款兒童生活補助。", "sourceDate": "現行調整表；查核日2026-06-05", "sourceUrl": "https://www.mohw.gov.tw/dl-9691-e9b88768-ad1a-4fa4-aae6-f4df82da30f6.html"},
                {"label": "高中職以上就學生活補助", "amount": "6,825元", "unit": "每人每月", "note": "第2款及第3款高中職以上就學生活補助。", "sourceDate": "現行調整表；查核日2026-06-05", "sourceUrl": "https://www.mohw.gov.tw/dl-9691-e9b88768-ad1a-4fa4-aae6-f4df82da30f6.html"},
            ],
            "applicationMethodSourceNote": "臺南市頁面說明由社會局逕撥至指定帳戶；資格申請仍洽戶籍地區公所。",
            "howToApply": ["先完成低收入戶資格申請或年度複查。", "確認郵政或農會帳戶資料正確。", "若戶內人口、就學或生活狀況異動，依區公所或社會局通知辦理。"],
            "documents": ["低收入戶資格資料", "指定郵政或農會帳戶", "在學證明", "區公所或社會局要求文件"],
            "contact": {"website": "https://sab.tainan.gov.tw/News_Content.aspx?n=21390&s=4378483"},
            "freshness": {"lastChecked": dt.date.today().isoformat(), "sourceUpdatedAt": None, "confidence": "checked", "notes": "Official Tainan social bureau assistance page."},
        },
    },
    {
        "id": "tainan-elderly-living-allowance-115",
        "name": "臺南市中低收入老人生活津貼",
        "url": "https://sab.tainan.gov.tw/News_Content.aspx?Create=1&n=21369&s=4378297",
        "organization": "臺南市政府社會局",
        "jurisdiction": "臺南市",
        "sourceType": "official-local-program",
        "tags": ["地方政府", "臺南市", "中低收入老人", "老人生活津貼", "115年度"],
        "record": {
            "summary": "臺南市中低收入老人生活津貼，115年頁面更新，依收入級距與資格審查核發。",
            "audiences": ["老人", "中低收入老人", "低收入戶", "中低收入戶"],
            "serviceCategories": ["公部門地方資源", "老人福利", "生活津貼", "經濟弱勢"],
            "needTags": ["臺南老人津貼", "中低收入老人", "老人生活津貼", "長者補助"],
            "eligibility": "年滿65歲並符合中低收入老人生活津貼規定，家庭總收入、動產、不動產及是否領取其他生活補助都需審查。",
            "conditionSourceNote": "臺南市社會局頁面列出115年度所得門檻並連結審核辦法。",
            "applicationConditions": [
                {"label": "所得門檻", "requirement": "家庭總收入平均每人每月未超過當年最低生活費15,515元的2.5倍，且未超過臺灣地區平均每人每月消費支出26,640元的1.5倍。", "note": "仍需審查動產、不動產與其他排除條件。", "sourceDate": "115-02-10", "sourceUrl": "https://sab.tainan.gov.tw/News_Content.aspx?Create=1&n=21369&s=4378297"},
                {"label": "不得重複領取部分津貼", "requirement": "領取國民年金、老農津貼、低收入戶生活津貼、榮民院外就養金等情形，可能不得重複領取。", "note": "實際排除項目以審核辦法與承辦單位認定為準。", "sourceDate": "115-02-10", "sourceUrl": "https://sab.tainan.gov.tw/News_Content.aspx?Create=1&n=21369&s=4378297"},
            ],
            "benefitSourceNote": "中低收入老人生活津貼金額依收入級距核定；臺南市區公所頁面列出低於最低生活費1.5倍者金額。",
            "benefitItems": [
                {"label": "中低收入老人生活津貼", "amount": "最高8,329元", "unit": "每人每月", "note": "依收入級距與是否領取其他生活補助核定。", "sourceDate": "115年度；查核日2026-06-05", "sourceUrl": "https://sab.tainan.gov.tw/News_Content.aspx?Create=1&n=21369&s=4378297"}
            ],
            "applicationMethodSourceNote": "通常向戶籍所在地區公所提出，社會局或區公所依審核辦法審查。",
            "howToApply": ["向戶籍所在地區公所社會課提出申請。", "檢附身分、戶籍、收入、財產及相關津貼資料。", "等待區公所或社會局審查，若有領取其他津貼需主動告知。"],
            "documents": ["申請表", "身分及戶籍資料", "收入與財產資料", "其他津貼或補助證明", "區公所要求文件"],
            "contact": {"website": "https://sab.tainan.gov.tw/News_Content.aspx?Create=1&n=21369&s=4378297"},
            "freshness": {"lastChecked": dt.date.today().isoformat(), "sourceUpdatedAt": "115-02-10", "confidence": "source-dated", "notes": "Official Tainan elderly welfare page."},
        },
    },
    {
        "id": "kaohsiung-low-income-living-assistance-115",
        "name": "高雄市低收入戶生活補助",
        "url": "https://older.kcg.gov.tw/cp.aspx?Create=1&n=EDF792DF41A20EC2",
        "organization": "高雄市政府社會局",
        "jurisdiction": "高雄市",
        "sourceType": "official-local-program",
        "tags": ["地方政府", "高雄市", "低收入戶", "生活補助", "115年度"],
        "record": {
            "summary": "高雄市低收入戶生活補助，115年更新頁面列出低收入戶資格與補助金額。",
            "audiences": ["低收入戶", "經濟困難家庭", "兒少家庭", "學生"],
            "serviceCategories": ["公部門地方資源", "低收入戶與中低收入戶救助", "生活補助", "現金與生活扶助"],
            "needTags": ["高雄低收入戶", "高雄生活補助", "低收補助", "高雄115標準"],
            "eligibility": "需符合高雄市低收入戶資格，家庭總收入、動產、不動產及家庭人口依社會局規定審查。",
            "conditionSourceNote": "高雄市政府高齡友善資訊專區頁面115-04-09更新，列出低收入戶資格條件與補助金額。",
            "applicationConditions": [
                {"label": "低收入戶資格", "requirement": "需符合115年度高雄市最低生活費及家庭財產標準，並經區公所與社會局審查列冊。", "note": "頁面列出動產每人9萬5,000元等審查資訊。", "sourceDate": "115-04-09", "sourceUrl": "https://older.kcg.gov.tw/cp.aspx?Create=1&n=EDF792DF41A20EC2"}
            ],
            "benefitSourceNote": "高雄市頁面列出低收入戶生活補助金額，實際依款別、年齡與就學身分核定。",
            "benefitItems": [
                {"label": "一款生活補助", "amount": "依高雄市公告金額核定", "unit": "每人每月", "note": "請以高雄市社會局115-04-09更新頁面及承辦單位審查為準。", "sourceDate": "115-04-09", "sourceUrl": "https://older.kcg.gov.tw/cp.aspx?Create=1&n=EDF792DF41A20EC2"},
                {"label": "兒童或就學生活補助", "amount": "依款別與身分核定", "unit": "每人每月", "note": "未成年或在學補助需依年齡、就學及款別判斷。", "sourceDate": "115-04-09", "sourceUrl": "https://older.kcg.gov.tw/cp.aspx?Create=1&n=EDF792DF41A20EC2"},
            ],
            "applicationMethodSourceNote": "通常向戶籍所在地區公所提出，實際由社會局或區公所審查。",
            "howToApply": ["向戶籍所在地區公所提出低收入戶申請。", "檢附戶籍、收入、財產及帳戶資料。", "審查通過後依款別與身分核發生活補助。"],
            "documents": ["申請表", "戶籍資料", "收入與財產資料", "帳戶資料", "區公所要求文件"],
            "contact": {"website": "https://older.kcg.gov.tw/cp.aspx?Create=1&n=EDF792DF41A20EC2"},
            "freshness": {"lastChecked": dt.date.today().isoformat(), "sourceUpdatedAt": "115-04-09", "confidence": "source-dated", "notes": "Official Kaohsiung 115 updated welfare page."},
        },
    },
    {
        "id": "kaohsiung-weak-medical-assistance-115",
        "name": "高雄市115年弱勢個案就醫補助",
        "url": "https://health.kcg.gov.tw/Content_List.aspx?n=1E202D17FB6C53C6",
        "organization": "高雄市政府衛生局",
        "jurisdiction": "高雄市",
        "sourceType": "official-local-annual-program",
        "tags": ["地方政府", "高雄市", "弱勢就醫", "醫療補助", "健保欠費", "115年度"],
        "record": {
            "summary": "高雄市115年公益彩券回饋金排除就醫障礙計畫，協助經濟弱勢個案就醫、健保欠費等費用。",
            "audiences": ["低收入戶", "中低收入戶", "經濟困難家庭", "弱勢家庭"],
            "serviceCategories": ["公部門地方資源", "醫療補助", "經濟弱勢", "健保費補助"],
            "needTags": ["高雄醫療補助", "弱勢就醫", "健保欠費", "公益彩券回饋金", "醫療費"],
            "eligibility": "設籍高雄市並符合區公所或社會局認定經濟困難者，含低收入戶、中低收入戶及其他經濟弱勢證明者。",
            "conditionSourceNote": "高雄市衛生局115年協助弱勢個案就醫補助專區列出申請資格。",
            "applicationConditions": [
                {"label": "設籍高雄市且經濟困難", "requirement": "需設籍高雄市，並符合區公所或社會局認定之經濟困難。", "note": "可包含低收入戶、中低收入戶、中低收入老人、身障生活補助、弱勢兒少或其他經濟弱勢證明。", "sourceDate": "115年度；頁面查核日2026-06-05", "sourceUrl": "https://health.kcg.gov.tw/Content_List.aspx?n=1E202D17FB6C53C6"}
            ],
            "benefitSourceNote": "115年度排除就醫障礙計畫列出醫療補助與健保欠費上限。",
            "benefitItems": [
                {"label": "醫療補助", "amount": "最高30,000元", "unit": "每人每年", "note": "以計畫補助項目與審查結果為準。", "sourceDate": "115年度；頁面查核日2026-06-05", "sourceUrl": "https://health.kcg.gov.tw/Content_List.aspx?n=1E202D17FB6C53C6"},
                {"label": "健保欠費協助", "amount": "最高3,000元", "unit": "每人每年", "note": "協助無力繳納健保費或積欠健保費者。", "sourceDate": "115年度；頁面查核日2026-06-05", "sourceUrl": "https://health.kcg.gov.tw/Content_List.aspx?n=1E202D17FB6C53C6"},
            ],
            "applicationMethodSourceNote": "衛生局專區提供計畫與文件，個案通常需由醫療院所、社政或相關窗口協助確認。",
            "howToApply": ["先確認是否有低收入戶、中低收入戶或其他經濟弱勢證明。", "洽高雄市衛生局專區、醫療院所社工或相關窗口確認可補助項目。", "依計畫檢附醫療費用、健保欠費或經濟弱勢證明文件。"],
            "documents": ["經濟弱勢證明", "醫療費用或欠費資料", "身分與戶籍資料", "承辦窗口要求文件"],
            "contact": {"website": "https://health.kcg.gov.tw/Content_List.aspx?n=1E202D17FB6C53C6"},
            "freshness": {"lastChecked": dt.date.today().isoformat(), "sourceUpdatedAt": "115年度", "confidence": "source-dated", "notes": "Official Kaohsiung Health Bureau 115 medical assistance page."},
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
    sources.extend(static_source(source) for source in LOCAL_PROGRAM_SOURCES_BATCH_2)
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
