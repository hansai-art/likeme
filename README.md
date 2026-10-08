# 像我本人 LikeMe

台灣繁體中文的寫作與改稿 Skill。去掉 AI 腔，校正台灣用語與全形標點，同時保住作者的聲音、事實、判斷與故事節奏，直接交可以發布的完整成稿。

[English summary](#english-summary)

## 跟一般去 AI 味工具差在哪

多數去 AI 味工具只做一件事，把稿子洗乾淨。洗得太乾淨，作者的口語、玩笑、批評也一起被磨掉，讀起來還是不像本人。

像我本人多做了三件事：

- **先問每句話在做什麼，再決定留、修或刪。** 痕跡目錄是診斷工具，不是禁詞表，「不是 A 而是 B」有真的區分就留。
- **作者聲音有獨立的設定檔。** 預設是林思翰的寫法（意思群組才用句號、不用分號與破折號、平輩口吻、一層反轉的幽默），換成你的樣本就是你的聲音。
- **改動範圍分六種模式。** 新寫、改稿、只修語氣、只整理標點、只看問題、對比說明，說「只修語氣」就不會被砍成摘要。

## 可以做什麼

- **撰寫新稿：** 社群文章、FB 貼文、課程公告、案例分析、教學、客服回覆、商務信件與產品文案。
- **修改現有內容：** 刪時代帽子、空洞結尾、「但不代表」補句與重複道理，把抽象描述寫成具體動作。
- **校正台灣用語與標點：** 視頻改影片、質量改品質，但物理的「質量」不會被誤改，半形標點換全形，URL 與程式碼保持原樣。
- **保留重要資訊：** 數字、日期、時區、上下限、網址、條件、承諾、引語與來源歸屬，改稿前後逐項核對。
- **不編故事：** 不替作者加「我愣了一下」「那一刻我才明白」這類假人味，素材沒有的經歷與成果不補。

## 改寫前後範例

### 刪掉時代帽子，第一句就給資訊

**改寫前**

> 隨著生成式 AI 快速發展，影像產業正面臨前所未有的挑戰與機遇。這次想分享我們怎麼把 AI 放進動畫流程。

**改寫後**

> 這次的 30 秒片頭，分鏡和風格測試都先丟給 AI 跑，正式動畫還是我們自己做。

### 立場真空改成作者的選擇

**改寫前**

> 用 AI 做分鏡和手繪分鏡各有優缺點，選擇哪一種取決於專案需求與個人習慣。

**改寫後**（作者給了自己的做法）

> 我現在提案一律先用 AI 出分鏡，因為客戶一小時內就能看到三個方向，定案後再手繪細修。

### 原文自然，就保留原文

> 想傳狗，就傳狗。  
> 想傳旅遊，就傳旅遊。  
> 今天吃了什麼奇怪的東西，也可以拍。  
> 總之，只要是影片都行。

這四句有畫面、有節奏，改稿時原樣交還，不會被換成「寵物、旅遊或日常生活」。

### 客服回覆不亂承諾

**素材：** 包裹漏了轉接頭，正在確認補件庫存，明天下午 3 點前回覆庫存結果，寄出時間尚未確定。

**改寫前**

> 很抱歉為您帶來不便，我們將積極處理，請放心。

**改寫後**

> 包裹漏了轉接頭，抱歉。我們正在確認補件庫存，明天下午 3 點前回覆結果，確認後再告訴你寄出時間。

「明天回覆庫存」不會被改成「明天寄出」。

## 安裝

```bash
npx skills add hansai-art/likeme --skill hans-human-writing
```

或手動把 `hans-human-writing/` 整個資料夾複製到：

| 工具 | 只給目前專案 | 這台電腦全部專案 |
| --- | --- | --- |
| Claude Code | `.claude/skills/hans-human-writing/` | `~/.claude/skills/hans-human-writing/` |
| Codex | `.agents/skills/hans-human-writing/` | `~/.agents/skills/hans-human-writing/` |
| Cursor | `.cursor/skills/hans-human-writing/` | `~/.cursor/skills/hans-human-writing/` |

Claude.ai 網頁版可以把資料夾壓成 ZIP，在設定的 Skills 上傳。完整安裝與交稿方式見 [使用教學](docs/guide.md)。

## 換成你自己的聲音

打開 `hans-human-writing/references/style-profile.md`，把林思翰的偏好換成你的。最有用的三種資料：

1. 兩三段你已經寫好、也喜歡的文字，標明「這是我的樣本」。
2. 你最在意的標點與句子習慣，例如「相連的意思用逗號，說完才加句號」。
3. 你改過 AI 稿子的具體回饋，例如「第二段把我的批評磨平了」。

不要把你不喜歡的 AI 原稿當成樣本放進去。

## 檔案結構

```
hans-human-writing/
├── SKILL.md                    流程：決定範圍、診斷、處理、保真、交稿
├── references/
│   ├── style-profile.md        作者聲音（林思翰），可換成你的
│   ├── ai-patterns.md          44 種 AI 腔痕跡，每條附誤傷邊界
│   ├── taiwan-zh.md            台灣用語與全形標點
│   ├── context-modes.md        依用途的寫法：社群、品牌、公告、信件、客服、教學
│   ├── protection-and-scenes.md 改稿前後的資訊核對
│   ├── editing-examples.md     正反例與修正方法
│   ├── youtube-case.md         產品起源文章的完整拆解
│   └── research-synthesis.md   研究來源、版本與採用邊界
└── agents/openai.yaml          Codex／ChatGPT 顯示設定
```

## 驗證

`evals/` 保存題目、每次試跑的原始輸出、技能檔案雜湊與核對結果，題目與驗收條件分開，執行者拿不到預期答案。目前結果見 [evals/results.md](evals/results.md)。

## 參考資源

- [中文維基百科：AI 生成文的特徵](https://zh.wikipedia.org/zh-tw/Wikipedia:AI%E7%94%9F%E6%88%90%E6%96%87%E7%9A%84%E7%89%B9%E5%BE%B5)：主要知識來源，收錄真實的繁中案例。
- [朱宥勳〈對「AI 腔」厭煩了嗎？分析 AI 生成文字的經典句型〉](https://www.youtube.com/watch?v=9uuX6cb81C8)：否定平行結構的觀點來源。他指出句型本身是正規的寫作動作（定義加區分），問題出在濫用造成的審美疲勞，以及讀者容易把形式正確誤判成內容正確。
- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)：英文版原始指南。
- [SEO 研究院〈什麼是 AI 味？〉](https://blog.dns.com.tw/2026/05/ai-writing.html)：「AI 起草、人工注魂」的分工框架，以及公式化開場這個痕跡。
- [Raymondhou0917/speak-human-tw](https://github.com/Raymondhou0917/speak-human-tw)：繁體中文去 AI 味的直接參考。痕跡目錄附誤傷邊界的形式、假人味的提醒、台灣在地化層都受它啟發，本專案在這個基礎上加入作者聲音設定、改動範圍模式與林思翰自己的寫法與改稿經驗。
- [MrGeDiao/shuorenhua](https://github.com/MrGeDiao/shuorenhua)：簡體中文去 AI 味的先行者，保護片段、情境分級與評測方法給了很好的參考。
- [blader/humanizer](https://github.com/blader/humanizer)、[hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop)：英文先行專案。

各來源採用與不採用的地方，以及固定的參考版本，見 [研究摘要](hans-human-writing/references/research-synthesis.md)。

所有範例句、詞表、作者偏好與情境寫法都針對繁體中文場景原創撰寫，不翻譯、不移植上述任何專案的內容。範例中的人物、數字與案子是示範用的虛構內容。

## 授權

MIT

---

## English summary

**LikeMe** is a Traditional Chinese (Taiwan) writing and editing skill for Claude Code, Codex, and Cursor. It removes AI-style writing patterns while keeping the author's own voice, facts, and judgments intact, and returns a finished draft rather than a checklist.

- A 44-item catalog of AI writing patterns, each with a "don't over-correct" boundary.
- A Taiwan localization layer: mainland vocabulary, full-width punctuation, and the author's own punctuation rules.
- A swappable author voice profile (defaults to Hans Lin's style).
- Six edit-scope modes, so "only fix the tone" never turns into a summary.
- Strict fidelity checks on numbers, dates, conditions, URLs, quotes, and source attribution, and no invented anecdotes.

Install: `npx skills add hansai-art/likeme --skill hans-human-writing`
