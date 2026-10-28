**版本：v0.3（全章節定義版）｜範圍：通用 Kotlin 1.9+｜風格：適度保守**

本規範僅約束 Kotlin 程式碼本身的寫法與可讀性。以 [Kotlin 官方 Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html) 為排版與慣用語法基準；在多種合法寫法之間，優先選擇容易理解、追蹤與修改的寫法。

- **MUST（強制）**：預設必須遵守。僅在語言、互通性或明確的特殊需求使規則不適用時例外；偏離時應能說明理由。

- **SHOULD（建議）**：通常遵守。當替代寫法在當下情境更清楚，可直接選擇替代方案，不需要機械式套用。

- **Review Signal（審查警訊）**：提醒檢查可讀性，不代表違規，也不產生固定數字門檻。

- **範圍之外**：程式架構、模組及套件邊界、依賴注入、設計模式、測試策略、效能指標、CI、Lint 工具選型、團隊流程與 AI Agent 工作流程，由各專案自行決定。

如本規範未明訂格式細節，遵循 Kotlin 官方慣例與專案既有一致風格。除非明示為 MUST，本文的範例都是說明意圖，而非唯一合法寫法。

# 1. 排版與命名（Formatting & Naming）

## 1.1 排版

- **MUST** 使用 Kotlin 官方排版慣例：四個空白縮排、不使用 Tab 縮排、左大括號與宣告或控制語句同行，省略不必要的分號。

- **MUST** 不為縮短行數而犧牲排版可讀性；複雜參數、條件或呼叫應適當換行，交由官方風格的格式化器處理細節。

- **SHOULD** 避免萬用字元匯入（`import foo.*`）；讓依賴名稱可辨識。

- **SHOULD** 多行宣告與集合常值使用尾隨逗號，以降低新增項目的修改成本；呼叫處是否使用，以清晰與專案一致性為準。

```kotlin
fun createLabel(
    name: String,
    category: String,
): String {
    return "$category: $name"
}
```

## 1.2 命名

| 對象 | 規則 | 範例 |
| --- | --- | --- |
| 套件 | **MUST** 小寫、不使用底線 | `com.example.textparser` |
| 類別、介面、物件、型別別名 | **MUST** `UpperCamelCase` | `TextParser`, `ParseResult` |
| 函式、屬性、區域變數、參數 | **MUST** `lowerCamelCase` | `parseText`, `itemCount` |
| 常數 | **MUST** `const val` 及頂層或 `object` 內持有深度不可變資料的 `val` 採 `UPPER_SNAKE_CASE` | `const val MAX_RETRIES = 3` |
| 一般 `val` | **MUST** 不因為不可重新指派就使用常數命名 | `val defaultTimeout = ...` |
| 檔案 | **SHOULD** 單一主要型別與其同名；多個相關宣告使用描述性檔名 | `TextParser.kt`, `StringExtensions.kt` |

- **MUST** 名稱能表達資料意義或行為，不任意縮寫（例如 `usr`, `mgr`, `proc`）或濫用 `data`, `info`, `util` 等空泛字眼。領域通用縮寫（如 `URL`, `HTTP`, `ID`）可以保留。

- **MUST** 函式名稱與效果相符，不讓名稱暗示純查詢、實際卻修改外部狀態。

- **SHOULD** 對布林屬性使用可自然閱讀的語意，例如 `isReady`, `hasNext`；對動作函式使用動詞，對型別使用名詞。

- **SHOULD** 英文縮寫遵循官方命名慣例：兩字母縮寫可全大寫，較長縮寫按一般單字處理，例如 `IOStream`、`HttpClient`。

- **例外**：測試名稱、跨語言互通宣告、既有外部 API 的命名限制，以及用於建構物件的類別式工廠函式，可依 Kotlin 官方規範或外部契約處理。

# 2. 變數與型別（Variables & Types）

## 2.1 狀態與可變性

- **MUST** `val` 與 `var` 的使用反映「是否需要重新指派」；不要為了方便而將所有變數宣告為 `var`。

- **SHOULD** 預設使用 `val`；確實需要重新指派時再使用 `var`。

- **SHOULD** 僅在需要修改集合內容時使用 `MutableList`、`MutableSet`、`MutableMap`；否則以 `List`、`Set`、`Map` 表達只讀使用情境。

- **注意**：`val` 不保證物件不可變；Kotlin 的只讀集合介面也不等同深度不可變或不可被其他參照修改。

```kotlin
val items: List<String> = loadItems()
var selectedIndex = 0

selectedIndex += 1
```

## 2.2 型別的明確程度

- **SHOULD** 區域變數初始化式已清楚表達型別時使用型別推斷；初始化式或泛型推斷不易理解時明寫型別。

- **SHOULD** 對外可見的函式回傳值、屬性及容易產生語意歧義的宣告明寫型別；私有且一目了然的短函式可省略。

- **SHOULD** 避免僅為規避型別設計而廣泛使用 `Any`、未檢查的轉型或不必要的強制轉型。

- **SHOULD** 延遲初始化只在確實需要時使用 `lateinit` 或 `lazy`；一般可在宣告時初始化的值，直接初始化更清楚。

- **SHOULD** 使用最小必要的可見性，避免無意間擴大 Kotlin 宣告的可見範圍。

```kotlin
val count = records.size

fun calculateTotal(prices: List<Int>): Int =
    prices.sum()
```

# 3. 空值安全（Null Safety）

## 3.1 空值契約

- **MUST** 只有「缺少值」是合法狀態時，才將型別宣告為可空的 `T?`。不可空參數或屬性不應被任意放寬為可空型別。

- **MUST** 處理可空值時，使「有值」與「無值」的行為明確；不能依賴未驗證的非空假設。

- **MUST** 不使用 `!!` 掩蓋未確認的空值來源。若由明確且可維持的不變條件保證非空，才可例外使用，並應讓理由可從附近程式碼理解。

- **SHOULD** 優先使用 `?.`、`?:`、智慧轉型、明確的 `if` 或提早返回，選擇其中最清楚的寫法。

- **SHOULD** 安全轉型使用 `as?`；確定型別契約的強制轉型 `as` 應有可理解的前提。

- **SHOULD** 呼叫 Java API 取得平台型別（`String!`）時，在邊界依實際契約明寫為 `T` 或 `T?`，不讓未確認的空值性擴散到 Kotlin 程式碼中。

```kotlin
fun displayName(user: User?): String {
    val name = user?.name ?: return "Guest"
    return name.trim()
}
```

## 3.2 避免過度串接

- **SHOULD** 對單純空值檢查或早期返回，優先使用直接的 Elvis 運算子或 `if`，避免把 `?.let` 當作所有判斷的通用模板。

- **SHOULD** 當安全呼叫鏈混合轉換、副作用、預設值與例外時，拆成有意義的中間值。

- **SHOULD** `requireNotNull` 用於檢查呼叫端不得傳入空值的前提；`checkNotNull` 用於檢查程式目前狀態的不變條件；不要只為縮短一行而混用。

```kotlin
val session = currentSession ?: return
sendMessage(session)
```

# 4. 函式設計（Functions）

## 4.1 職責與可讀性

- **MUST** 函式名稱應準確描述它做的事；不能隱藏明顯且與名稱衝突的副作用。

- **MUST** 呼叫者需要知道的前提、回傳意義與可觀察行為，應由函式簽名、命名與必要說明清楚表達。

- **SHOULD** 一個函式完成一個容易描述的主要目的。若包含多個不相關階段，考慮拆分；若拆分只造成閱讀來回跳轉，可保留在同一函式。

- **SHOULD** 簡單且意圖清楚的單一運算使用 expression body；涉及多個步驟、分支或副作用時，使用區塊函式體。

- **SHOULD** `Unit` 回傳型別通常省略，除非型別表達或互通性需要。

- **SHOULD** 使用預設參數取代一系列只為提供預設值而重複的多載；與 Java 互通時可依契約例外。

```kotlin
fun isEmptyName(name: String): Boolean = name.isBlank()

fun normalizeName(name: String): String {
    val trimmed = name.trim()
    return trimmed.replace(Regex("\\s+"), " ")
}
```

## 4.2 參數與呼叫

- **MUST** 避免參數名稱與意義不符，或以位置參數製造難以辨識的呼叫。

- **SHOULD** 當呼叫包含相鄰的布林值、數字或多個同型別且意義不同的參數時，使用具名參數增進可讀性。

- **SHOULD** 避免僅靠布林參數切換差異很大的行為；可在語言 API 層面以更明確的函式名稱或型別表達。

- **SHOULD** 參數排列反映主要輸入與可選設定；可選參數通常放後面。

- **SHOULD** 公開的回傳型別保持穩定且易懂；避免讓外部程式碼依賴偶然推斷出的具體型別。

```kotlin
resizeImage(
    width = 800,
    height = 600,
    preserveAspectRatio = true,
)
```

## 4.3 審查警訊

以下**都不是違規或硬性上限**：

- 函式較長：檢查是否仍容易掌握主要目的與資料變化。

- 參數較多：檢查各參數角色是否清楚。

- 呼叫多層輔助函式：檢查抽象是否真正減少認知成本，而非只是拆成很多轉接函式。

- 一行容納過多運算：檢查是否需要具名中間值。

判斷準則是：讀者能否不費力地看出輸入、主要步驟、輸出與副作用，而不是函式有幾行。

# 5. 控制流程（Control Flow）

## 5.1 分支與迴圈

- **MUST** 使用明確、可追蹤的分支與迴圈；不得用壓縮寫法掩蓋重要副作用或控制流程。

- **SHOULD** 兩種分支使用 `if`，多種離散條件使用 `when`；不要為了遵守形式而使簡單情況更冗長。

- **SHOULD** 面對 `enum` 或 `sealed` 型別且需要完整列舉分支時，利用 `when` 的完整性檢查；不要習慣性加入吞掉新分支的 `else`。

- **SHOULD** 使用 guard clause（提前 `return`、`continue` 或 `break`）減少不必要的巢狀；若提早退出會破壞流程理解，保留結構化分支。

- **SHOULD** 有索引需求時使用 Kotlin 範圍語法，例如 `indices`、`..<` 或 `until`；不要手寫容易誤判邊界的算式。

- **SHOULD** 純粹做副作用、需 `break`/`continue` 或有複雜分支的迭代優先使用 `for`。

```kotlin
fun labelFor(status: Status): String =
    when (status) {
        Status.Pending -> "Pending"
        Status.Running -> "Running"
        Status.Done -> "Done"
    }
```

## 5.2 表達式與巢狀

- **SHOULD** `if`、`when`、`try` 作為表達式時，應能直接看出各分支產生的值。

- **SHOULD** 避免在單一表達式內堆疊巢狀條件與例外處理；必要時使用區域變數及區塊。

- **Review Signal**：巢狀層次增加時，檢查早期退出、條件拆解或資料命名是否能讓控制流程更直觀；**不設定最大巢狀深度**。

```kotlin
fun shippingLabel(order: Order): String {
    if (order.isCancelled) return "Cancelled"
    val address = order.address ?: return "Missing address"
    return "${address.city}: ${order.id}"
}
```

# 6. Lambda 與 Scope Functions

## 6.1 Lambda 的可讀性

- **MUST** Lambda 的接收者、參數與副作用不能因省略名稱而變得含糊。

- **SHOULD** 短小、單層且語意明確的 Lambda 使用 `it`；巢狀 Lambda 或同時處理多個值時，明確命名參數。

- **SHOULD** 尾隨 Lambda 與單一 Lambda 參數依官方慣例排版；若讓呼叫範圍難以辨認，改用完整的參數寫法。

- **SHOULD** 標籤返回（`return@...`）僅用於確有必要的局部控制；多個標籤交錯時，考慮改寫為一般迴圈或獨立函式。

```kotlin
val names = users.map { user -> user.name }

val activeNames = users
    .filter { it.isActive }
    .map { it.name }
```

## 6.2 Scope Function 的用途

| 函式 | 常見用途 | 區塊內主要參照 | 回傳 |
| --- | --- | --- | --- |
| `let` | 轉換值、對非空值做運算 | `it` | Lambda 結果 |
| `run` | 對接收者計算結果 | `this` | Lambda 結果 |
| `with` | 對既有物件進行一組相關操作 | `this` | Lambda 結果 |
| `apply` | 設定、初始化物件 | `this` | 物件本身 |
| `also` | 觀察、記錄或額外副作用 | `it` | 物件本身 |

- **MUST** 選用 Scope Function 時，讓「操作對象」與「回傳值」符合讀者可預期的語意。

- **SHOULD** 不為了使用語法糖而使用 Scope Function；普通的區域變數或敘述如果更清楚，就直接使用。

- **SHOULD** 避免混用多層隱式 `this` / `it`，尤其在巢狀 `apply`、`run`、`let` 時。

- **Review Signal**：Scope Function 的連用、巢狀或數量增加時，檢查接收者切換、回傳值與副作用是否仍直觀；**不設定最多幾個**。

```kotlin
val request = Request().apply {
    timeoutMillis = 3_000
    followRedirects = true
}

// 若轉換與錯誤處理開始混雜，拆成有名稱的步驟。
val rawName = user?.name ?: return
val normalizedName = rawName.trim()
saveName(normalizedName)
```

# 7. 集合與 Kotlin 語法糖（Collections & Idioms）

## 7.1 集合處理

- **MUST** 集合運算的結果與副作用應可辨識，不得讓延遲執行或多次遍歷的行為變得意外。

- **SHOULD** 表示資料轉換或篩選時使用 `map`、`filter`、`associate`、`groupBy` 等語意明確的標準操作。

- **SHOULD** 主要目的為修改外部狀態、需提早中斷或控制流程較複雜時，使用 `for`，不強求 `forEach`。

- **SHOULD** 集合鏈保持每一步容易理解；當鏈結混合多重轉換、副作用及條件分支時，拆成具名中間結果或一般迴圈。

- **SHOULD** 只有在資料量、延遲求值或避免中間集合確有價值時使用 `Sequence`；它不是預設的「更 Kotlin」寫法。

```kotlin
val activeUserNames = users
    .filter { it.isActive }
    .map { it.name }

for (user in users) {
    if (!user.isActive) continue
    notifyUser(user)
}
```

## 7.2 語法糖的取捨

- **MUST** 不使用會讓正常閱讀者誤解行為的運算子多載、`infix` 或隱晦的擴充函式名稱。

- **SHOULD** 使用字串模板取代單純的字串串接；多行文字可視需要用 `trimIndent()` 或 `trimMargin()`。

- **SHOULD** 解構宣告只在元件意義清楚時使用；若 `componentN` 的意義需要猜測，明確存取屬性。

- **SHOULD** 擴充函式用於語意上確實屬於接收者的操作；避免建立與既有成員函式相似卻行為不同的 API。

- **SHOULD** `typealias` 用來替重複且不易讀的型別取名，不把每個普通型別都再包一層別名。

- **SHOULD** 只有符合領域直覺的運算才使用運算子多載；可預期性優先於表面簡短。

- **SHOULD** 善用 Kotlin 的 `data class`、字串模板、範圍與智慧轉型等常見語言能力，但不將「語法越短」當作品質指標。

```kotlin
val message = "Hello, ${user.name}"

val (key, value) = entry // Pair 或 Map.Entry：元件意義明確
```

# 8. 類別與例外（Classes & Exceptions）

## 8.1 類別與宣告形式

- **MUST** 類別的宣告形式與語意相符；不要因語法簡短就使用會產生不適當行為的宣告形式。

- **SHOULD** 對主要表示資料值且適合結構性比較的型別使用 `data class`；理解 `equals`、`hashCode`、`toString`、`copy` 主要依主建構子屬性生成。

- **注意**：`data class.copy()` 是淺拷貝；內含可變參照時，不代表複製了其內部資料。

- **SHOULD** 有限且互斥的狀態族群可用 `sealed class` / `sealed interface` 表達；單純固定常數集合可使用 `enum class`。不因為存在多種狀態就強制建立類別階層。

- **SHOULD** 需要單一物件實例時使用 `object`；無狀態行為也可直接使用頂層函式，不為了「面向物件」而硬加包裝類別。

- **SHOULD** 主建構子、屬性初始化與 `init` 區塊保持容易追蹤；初始化邏輯複雜時優先讓中間值語意明確。

```kotlin
data class Point(val x: Int, val y: Int)

sealed interface LoadState {
    data object Loading : LoadState
    data class Loaded(val count: Int) : LoadState
    data class Failed(val reason: String) : LoadState
}
```

## 8.2 例外與前提檢查

- **MUST** 不靜默吞掉例外；若捕捉後不再拋出，程式碼必須有明確且合理的處理方式。

- **MUST** 例外代表的失敗情境應與實際問題相符，不以不相關的例外型別掩蓋真正原因。

- **MUST** 在 coroutine 中不吞掉 `CancellationException`；`catch (e: Exception)`、`catch (e: Throwable)` 或 `runCatching` 會一併捕捉取消，必須重新拋出，以維持結構化併發的取消語意。

- **SHOULD** 以 `require` / `requireNotNull` 檢查呼叫端輸入的前提；以 `check` / `checkNotNull` 檢查執行時狀態的不變條件。

- **SHOULD** 優先捕捉能實際處理的特定例外；避免無條件捕捉所有例外後回傳模糊的預設值。

- **SHOULD** 空值或找不到資料若屬正常結果，使用明確的可空回傳或其他合適的 Kotlin 型別；不要無故以例外代表正常分支。

- **SHOULD** 在單一值的計算中可使用 `try` 表達式；當清理、分支或副作用較多，使用清楚的區塊。

- **不強制** 所有函式統一回傳 `Result<T>`、自訂例外或某一種錯誤模型；那是 API 契約與專案設計的選擇。

```kotlin
fun updateProgress(percent: Int) {
    require(percent in 0..100) { "percent must be between 0 and 100" }
    progress = percent
}

fun takeNext(): Item {
    check(queue.isNotEmpty()) { "Queue is empty" }
    return queue.removeFirst()
}

suspend fun loadProfileOrNull(id: String): Profile? =
    try {
        api.fetchProfile(id)
    } catch (e: CancellationException) {
        throw e
    } catch (e: IOException) {
        null
    }
```

# Code Review 的共同判斷準則

以下四個面向**只作為警訊，不設定數字門檻，也不自動判定違規**：

| 面向 | 該問的問題 |
| --- | --- |
| 函式行數 | 函式目的、資料流與副作用是否仍容易理解？ |
| 巢狀深度 | 是否能用清楚的條件、提早退出或區域變數降低閱讀負擔？ |
| Scope Function 數量 | `this` / `it` 指向何者、結果與副作用是否一眼可辨？ |
| 抽象層數 | 新增的一層有無真正承載語意，還是徒增跳轉？ |

**判準：**「這段程式碼是否讓下一位讀者容易理解與修改？」優先於「是否使用最多 Kotlin 語法糖」或「是否符合某個行數」。

# 參考依據

- [Kotlin Coding Conventions（官方）](https://kotlinlang.org/docs/coding-conventions.html)

- [Null Safety（官方）](https://kotlinlang.org/docs/null-safety.html)

- [Scope Functions（官方）](https://kotlinlang.org/docs/scope-functions.html)

- [Idioms（官方）](https://kotlinlang.org/docs/idioms.html)

- [Exceptions（官方）](https://kotlinlang.org/docs/exceptions.html)

**文件狀態：**完整章節定義版；仍可依實際 Kotlin 程式碼案例對個別 MUST / SHOULD 進行校準。本規範不取代各專案自行制定的架構與工程實踐。
