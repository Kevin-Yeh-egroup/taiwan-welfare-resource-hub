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
    ("taoyuan-social", "桃園市政府社會局", "http://sab.tycg.gov.tw/", "桃園市"),
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
    sources.append({
        "id": "tainan-welfare-map-dataset",
        "name": "臺南市社會福利地圖開放資料",
        "url": "https://data.tainan.gov.tw/DataSet/Detail/7227a4b1-1fe6-4bde-989b-55b072e3f66e",
        "resourceUrl": "https://data.tainan.gov.tw/Resource/93f35ae8-0e16-45ac-90d2-b0315889cf5f?handler=GoJson",
        "allowInsecureSslFallback": True,
        "organization": "臺南市政府社會局",
        "jurisdiction": "臺南市",
        "sourceType": "official-open-data",
        "format": "tainan-welfare-json",
        "crawl": True,
        "crawlDepth": 0,
        "refreshPolicy": refresh_policy(30, 3),
        "tags": ["地方政府", "開放資料", "地圖", "臺南"],
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
