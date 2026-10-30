# 內容結構與修改位置

## 輸入與輸出

使用者提供教材目錄即可開始盤點；可另有 project.json、課程大綱、講師資訊與風格圖。不要要求使用者先手填技術 JSON。由代理讀完整教材後生成資料及規格，讀不開的檔案列入問題。

產出專案：`project.json`、`materials/`（不公開）、`site/`、`_shots/`、`驗收報告.md`。教材來源映射及連結清單保存在 site/ 外。若使用者的素材已在別處，不必複製整份私有教材，只記對照。

`create_island.py` 只建立可運作的示意起點，不是完成教材轉製。主題由素材決定，--theme可用nature/ocean/space/halloween/custom作起點，亦可擴充其他風格。--courses使用核准的正整數，沒有固定課數範圍。裝飾與島數皆取本次diagnostics，不寫死某次場景數量。

## Markdown 解析後的資料結構（data/content.json 為快取）

| 欄位 | 契約 |
| --- | --- |
| `site` | title、slug、tagline、author、contact（沒有可空字串）、audience、language、mascot |
| `appearance` | theme、label、colors（覆寫配色）；主題裝飾由decorations模組負責，萬聖節僅一個選項 |
| `site.music` | 選用src（核准的相對音訊資產路徑）、title；不複製舊站音樂。音量記在本機，沒有src時使用手動合成音樂 |
| `center` | name、description、blocks（title/text）供中央島介紹；不要保留上一主題 AI 工具導覽 |
| `speaker` | 可為 null（未提供且不需講師區），或 name、alias、image（相對路徑）、education、teaching、administration、current[]；不得捏造資歷 |
| `courses` | 核准順序，order 從1開始、id 使用 island-01 連號，name、group、intro、goal、goalLabel、blocks、prompts、links、quiz；不要重排原始島名 |
| `blocks[]` | title/text 字串；不能用「詳見教材」代替正文。圖片、表格或公式需依素材增補渲染，保留閱讀語意 |
| `comparison` | 選用 headers[]、rows[][]；僅在教材有比較關係時使用 |
| `prompts[]` | 教材原有提示詞字串；沒有則 []，不要憑空做工具操作 |
| `links[]` | label、url、note（登入或權限提醒）；只使用核准／提供的 http(s) 網址，保留必要查詢參數，不能漏掉素材中的下載或工作台 |
| `quiz[]` | 每課4題；唯一id、question、options（4個不同id與text）、answer（選項id）、explanation。考理解而非僅背課名，避免同題改字或全課一樣 |
| `residents[]` | 14人，唯一id、name、concept；island 是存在課程id、topic 是該課 blocks 的零起算索引、text 必須能由此章節支持；名字可以虛構，概念不能捏造 |
| `editorialNote` | 實際內容來源與改寫界線；未查證現行操作時清楚說明，補寫目標標示意，自編題標自編 |

可用「透過結構化步驟與檢核提高一致性，產出仍須確認」取代素材中不可靠的保證，但涉及新教材知識變更時先讓使用者確認。不要把某次原稿的一次性敘述當成所有新課固定教材。

## 引擎修改地圖

| 檔案 | 用途與必守條件 |
| --- | --- |
| index.html / styles.css | 頁首純說明、RWD、清單、面板、主題；載入後 syncBrand 用資料更新品牌／課數／分類。部署前也由 sync_content 更新靜態標題與無JS備援 |
| js/app.mjs | 教材、清單、測驗、中央島與證書；各課數字由 courses.length 取得，品牌與作者不寫死 |
| js/core.mjs | ID判分、輪抽、資格、localStorage；資格只讀＋75%，保留最高分 |
| js/host.mjs | 本站功能FAQ、詞條與教材檢索；新主題不沿用原 AI 工具的 island-01 等語意映射；以新課 aliases 或明確課名找教材，無依據就不答 |
| js/scene.mjs | 相機、聚焦、主建築點擊、label、幾何射線驗證。建立地標前記 children.length，只標記之後的主建築；地面、岸圈、岩壁不可有 building 標記 |
| js/world.mjs | layoutFor(count)、島座標／半徑／高度、bridgeStylesFor / BRIDGE_STYLES、橋面高度profile；任意正整數依課數生成，不硬湊7課；橋型以family＋可見variant擴充，密集課數依可讀性和效能調整 |
| js/bridges.mjs | 10種起始實體橋族及可見變體；deck、階梯、扶手與人物路線共用同一profile，橋頭有島內平坦登橋區 |
| js/navigation.mjs | 連通路網、3D距離、路徑取樣；不是另造一條與視覺不合的平面路線 |
| js/residents.mjs | 14島民、多島主、步行／hover暫停、頭頂提示；行走及 pause 皆依實際 path.y，不能重設 .49 海平面 |
| js/appearance.mjs / decorations.mjs | 主題配色、主題裝飾及動態；自然／海洋／星際等可換或自訂，保留全部互動，尊重減少動態 |
| js/halloween.mjs | 只在選halloween時建立南瓜、帽、蝙蝠，其他主題不建立 |
| js/music.mjs | 手動音樂、指定音訊或合成備援、音量調整與記憶 |
| js/seascape.mjs | 水紋、船隻、遠景山林、雲與中央掃光；依地圖範圍安排航線，避免島嶼；尊重減少動態 |
| js/anime-character.mjs | 原創日系Q版動漫人物；保留各人不同髮型、衣著、名字及所有點擊標記 |
| vendor/ | 固定版本Three與controls/labels，保留授權；模板可本機運作，不靠不固定 CDN |

## 換科目的例子

使用者放入5份自然教材：先依檔案內容確認要5島、是否拆合，以及課名順序；規劃核准後用 --courses 5 --theme nature 建立。14個概念分配到5課，不要求每課恰好2人。中央總複習5題、5課各75%與已讀領證；頁面、FAQ、備援和證書都顯示5課。沒有講師照片時，可隱藏講師區，不拿舊講師照片補上。新專案未授權部署就留在本機驗收，等待使用者本機確認並主動提出發布要求，不主動詢問部署平台。

## Markdown 單一來源與日後更新

初建 `create_island.py` 依 N 課產生 `site/islands/<島名>/教材.md`；中央島也有自己的同名資料夾。`islands/manifest.json` 明列中央島及課程檔案的相對路徑與順序，不以資料夾排序猜順序。島名必須能安全用作資料夾名稱且不重複；遇到不合法名稱先確認，不能偷偷更改核准課名。

各檔保留 `## 資料設定` 的 JSON；課程依序有 `## 教材內容`（任意數量 `### 小節`＋正文）、`## 教材提示詞`（`### 標題`＋text程式碼區塊）、`## 延伸資源`、`## 隨堂測驗`、`## 島民概念`（後三者為JSON程式碼區塊）。中央島只有設定與教材內容。教材文字／工具操作／提示詞保留原稿；來源提供表格時放 comparison，網址、附件不遺漏。增刪小節後同步調整島民的零起算 topic；一課可有多位島民，14人總數和概念不重複。

`site/js/materials.mjs` 同時供瀏覽器與 Node 同步工具解析，瀏覽器每次載入直接讀 MD；`node site/scripts/sync-materials.mjs` 重建 JSON 快取、content.html 與靜態品牌資料。`--check` 驗證來源與快取一致、不寫檔。`--init` 僅首次把種子 JSON 轉成 MD，來源已存在時拒絕覆寫。MD 是唯一可編輯教材來源，JSON 不可反向蓋回。Markdown儲存後，`node scripts/serve.cjs` 監看並更新快取；重新整理頁面即可看見，無需重建前端套件。格式錯誤要顯示可理解的檔案／段落訊息，不能靜默改讀舊 JSON。修改檔案不會自動部署。

`資料設定` 中的 title/name/group/intro/goal/points/extra/comparison 等資料仍依下列既有 schema 使用。site、appearance、speaker、editorialNote 等全站設定位於中央島 MD；speaker 可 null；site.music 可使用新專案提供的音檔，site.certificate.sealText 可設定新站紀念鋼印，不帶前案私人資產或宣稱官方資格。中央島 blocks 在中央島的「教材內容」。新增或移除整島時，先更新核准規格、manifest、ID與order、居民指向，再驗證橋網、鏡頭、課數、進度相容性及證書；不用刪檔推測使用者想刪課，舊題庫進度不硬套新題庫。

| 新模組 | 不可退化的行為 |
| --- | --- |
| js/materials.mjs / scripts/write-materials.mjs / scripts/sync-materials.mjs | 共用解析、首次初始化保護、Markdown單一來源、無JS備援同步，不固定7課或28題 |
| js/interior.mjs | 獨立室內鏡頭，桌椅檯燈壁畫、動漫島主；教材燈箱開關不離室，實體門／返回按鈕離室；島主提示需避開門及門口標籤 |
| js/overview-labels.mjs | 依島嶼實際包圍盒及可用畫面計算最佳比例，標籤在上方、無引導線，尺寸改變重算 |
| js/scene.mjs | bestOverview先求最終位置／目標／zoom，再單段約650ms平滑插值；清掉Orbit殘留慣性，輸入可取消過場，結束恢復控制。不可逐幀強制fit造成滾輪失效；島名／人物提示是canvas同層覆蓋物，滾輪要轉交控制器，不能攔住縮放；影子快取優化不能凍結輸入或漏畫室內 |
| js/certificate.mjs | 參數化site／課數／姓名與當日日期，原創SVG內部繪圖再轉PNG下載，同圖列印，紀念而非官方認證 |
| js/progress-transfer.mjs | 匯入前完整驗證網站slug＋課題簽章、分數、姓名與課程集合；只合併已讀及最高分，錯誤不改狀態 |

正式功能來源基準：ai-teaching-island 正式版本 53c1278（2026-10-30）；僅沿用通用功能，不沿用該站教材、真人作者、音樂或萬聖節主題。更新後仍須以不同 N／非萬聖節教材實測，不以此版本紀錄代替新專案驗收。
