# Rust Coding Guidelines

> 正式規範 · 2026-10-27 · 適用於 Rust 應用程式、函式庫與 Code Agent

## 1. 核心原則

以 **Idiomatic Rust、資料與函式優先、明確所有權、最小必要抽象** 為準則。首先確保正確、安全且容易閱讀，再依量測結果優化效能。不要為假設性的需求增加架構。

## 2. 語言版本與格式

- 新專案使用 **Rust 2024 Edition** 與 **Stable Toolchain**；不使用 Nightly-only 特性。
- 在 `Cargo.toml` 宣告與實際用到的功能相符的 `rust-version`（MSRV）；使用 Rust 2024 時不得低於 1.85。
- 遵循 `rustfmt` 與 Rust 官方命名慣例：型別、Trait、Enum Variant 使用 `PascalCase`；函式、變數、模組使用 `snake_case`；常數使用 `SCREAMING_SNAKE_CASE`。
- 命名應完整且可理解；不使用沒有必要的縮寫。

## 3. 資料、函式與控制流程

- 使用 `struct` 表達資料、`enum` 表達互斥狀態；獨立操作優先使用函式，與型別緊密相關的行為使用 `impl`。
- 以 Early Return、`?`、`let else`、`if let` 或清楚的 `match` 減少巢狀；不以冗長的 Iterator / Combinator 鏈犧牲可讀性。
- 預設不可變；需要修改才使用 `mut`。避免隱藏狀態與不必要的 Interior Mutability。
- 不為提前優化而增加配置技巧、複雜的型別設計或低階程式碼。

## 4. Ownership 與 Borrowing

- **借用優先，必要時持有所有權**：唯讀使用 `&T`，修改使用 `&mut T`，讀取字串使用 `&str`，讀取連續集合使用 `&[T]`。
- 函式需要保存、移交或跨生命週期持有資料時，使用 `T`、`String` 或 `Vec<T>` 等 Owned Value。
- `clone()` 可以使用，但必須具有清楚的所有權理由；不為了躲避 Borrow Checker 而任意 Clone，亦不為追求零複製製造難以維護的 Lifetime。
- Lifetime 優先採用推導；只在型別關係確實需要時明確標註。
- `Rc`、`Arc`、`RefCell`、`Mutex` 等僅在共享所有權或可變狀態需求明確時使用。

## 5. Trait 與 Generics

- **Concrete Types First**。只有存在真正的共享行為、泛用演算法、公開擴充契約或互通需求時，才引入 Trait / Generics。
- 優先實作恰當的標準 Trait（如 `From`、`TryFrom`、`AsRef`、`Debug`），不要建立重複的自訂抽象。
- 避免每個 Struct 都有對應 Trait、僅為 Mock 建立介面，或預先建立抽象層。
- 預設具體型別；需要編譯期多型時使用 Generics / `impl Trait`；確實需要執行期多型時才使用 `dyn Trait`。

## 6. 模組與公開 API

- 依功能與責任組織小型模組，不預設套用多層式架構或將專案拆成多個 Crate。
- 預設 Private；跨模組內部使用 `pub(crate)`，僅對穩定且必要的公開契約使用 `pub`。
- 公開 API 優先使用清楚的型別與易於理解的簽名，避免洩漏內部實作細節。
- 公開型別與函式應有 `///` 文件；對適用的函式記錄 `# Errors`、`# Panics`，並提供有價值的使用範例。

## 7. 錯誤處理

- 可恢復失敗使用 `Result<T, E>`；正常缺值使用 `Option<T>`；優先以 `?` 傳遞錯誤。
- **Library 使用可辨識的 Typed Error**；簡單情況使用標準函式庫，樣板程式碼較多時可使用 `thiserror`。
- **Application 在邊界提供 Error Context**；需要跨多種錯誤組合與診斷時可使用 `anyhow`，但不將其無條件暴露為 Library 的公開錯誤契約。
- 保留 Error Source；不得任意把錯誤攤平成 `String`、吞掉錯誤或使用無條件預設值掩蓋失敗。
- 不在一般正式邏輯中使用 `unwrap()`；`expect()` 僅在可證明的不變條件下使用，並寫明原因。`panic!` 不用於一般輸入或 I/O 錯誤。
- Error Enum 與錯誤轉換以實際處理需求為準，不為每個函式建立專屬型別。

## 8. Async 與 Concurrency

- 依工作性質選擇：一般操作保持同步；大量等待 I/O 時使用 Async；CPU 密集型工作使用適合的平行執行模型。
- **Runtime 由 Application 管理**；Library 不無故自行建立 Runtime，盡可能保持核心邏輯與特定 Runtime 解耦。
- 所有背景任務都需明確管理完成、取消、錯誤及資源回收；禁止無管理的任務無限增加。
- 使用有界 Channel、Semaphore 或其他明確策略限制併發與背壓。
- 優先資料所有權轉移或訊息傳遞；只在必要時共享可變狀態，不將 `Arc<Mutex<T>>` 視為預設方案。
- 避免在 `.await` 跨越期間持有同步鎖；不得長時間阻塞 Async Executor。必要時將阻塞工作交給適當的專用執行資源。

## 9. Unsafe

- 預設 Safe Rust。僅在 FFI、底層資料結構或經過論證的效能等需求下允許 `unsafe`。
- 每個 `unsafe` Block 應縮小範圍，並使用 `// SAFETY:` 說明相關前提與其成立理由；`unsafe fn` 使用 `# Safety` 文件說明呼叫端責任。
- 不使用 `unsafe`、Raw Pointer 或 `transmute` 迴避正常的所有權／型別設計問題。
- Unsafe 變更必須有針對不變條件的測試與人工審查；不可僅憑註解宣稱安全。

## 10. 測試

- 以 `#[cfg(test)]` 撰寫貼近功能的 Unit Test；以 `tests/` 驗證公開 API 和關鍵整合流程；公開範例適合時使用 Doc Test。
- 每項行為變更至少驗證成功路徑、重要失敗路徑與邊界條件；修復 Bug 應增加回歸測試。
- Async / Concurrency 測試應涵蓋取消、逾時、任務完成及受限資源；避免依賴不穩定時間順序。
- 測試應可重複、彼此獨立；不強制追求任意的覆蓋率百分比，也不為測試而重塑正式架構。

## 11. 依賴管理

- 先評估標準函式庫；增加 Crate 前，確認必要性、維護狀態、安全性、授權、MSRV、Feature 與傳遞依賴成本。
- 依賴只開啟需要的 Feature；避免不受控的 Git / Path Dependency、萬用版本與重複功能的 Crate。
- 對可交付專案提交 `Cargo.lock`；Library 也預設提交以利維護與 CI 重現，但必須另外驗證相容的依賴更新情境；不要手動編輯 Lockfile。
- 相依版本與 Features 更新應經過測試。避免不必要的新增依賴與大範圍升級。

## 12. 程式碼品質與 CI

基本檢查：

```bash
cargo fmt --all -- --check
cargo clippy --workspace --all-targets -- -D warnings
cargo test --workspace
cargo doc --workspace --no-deps
```

- 若專案使用 Cargo Features，另行測試實際支援的 Feature 組合；僅在所有 Features 可以同時啟用時使用 `--all-features`。
- 公開 Library 應驗證宣告的 MSRV；特殊平台或 `no_std` 支援依專案需要加上對應檢查。
- 對確有理由的 Clippy 例外，允許小範圍 `#[allow(...)]` 並註明原因；不得全面關閉警告以通過 CI。
- 以量測資料決定效能優化，不以直覺宣稱某種寫法較快。

## 13. Code Agent 強制要求

1. **先理解現有結構**，沿用既有 API、模組、命名和抽象；不擅自大規模重構。
2. **只修改任務所需範圍**；不增加推測性的 Feature、Trait、泛型或架構層。
3. **命名完整清楚**；避免過度縮寫、過深巢狀、冗長鏈式呼叫及壓縮式難讀程式碼。
4. **尊重 Ownership**；不得以大量 Clone、共享鎖或 Unsafe 草率消除編譯器錯誤。
5. **嚴格處理 Result / Option**；不得吞錯、不合理 Panic 或掩蓋失敗。
6. **沒有需求不引入 Async 或 Runtime**；使用 Async 時必須控制併發及任務生命週期。
7. **未經合理性說明不得加入依賴或 Unsafe**；Unsafe 必須具備安全前提與審查。
8. **附上適當測試並執行可用檢查**；無法驗證時清楚回報，不可宣稱已通過。
9. **以最少、清晰、可維護的程式碼完成需求**；可讀性與正確性優先於技巧性。

## 參考

- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- [Rust Style Guide](https://doc.rust-lang.org/stable/style-guide/)
- [Rust Edition Guide](https://doc.rust-lang.org/stable/edition-guide/rust-2024/)
- [The Rust Programming Language — Tests](https://doc.rust-lang.org/book/ch11-00-testing.html)
- [Cargo Book](https://doc.rust-lang.org/stable/cargo/)
- [Clippy Documentation](https://doc.rust-lang.org/stable/clippy/)
- [Rustonomicon](https://doc.rust-lang.org/stable/nomicon/)
