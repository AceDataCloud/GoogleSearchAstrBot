# AstrBot 的 Google Search 插件

通过自己的 Ace Data Cloud 账号在 AstrBot 聊天中执行 Google 网页搜索。Agent 工具 `google_search` 同步返回标题、链接和摘要，无需 task ID 或轮询。

这是 **Ace Data Cloud 提供的 Google Search 独立集成**，不是 Google Search 厂商或 AstrBot 团队的官方插件。请使用自己的 Ace API Key。

[English guide](../README.md) · [Google Search API](https://platform.acedata.cloud/documents?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=googlesearchastrbot_readme_documents) · [当前价格](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=googlesearchastrbot_readme_pricing)

## 1. 查找与安装

当前上游菜单为 **插件 → 顶部插件 → 插件市场 / 已安装**；旧英文版本可能仍写 Extensions。在插件市场搜索 **Google Search**，核对 **Google Search by Ace Data Cloud**、作者 **acedatacloud** 与对应服务图标。

已有 [Cloud 正式条目](https://cloud.astrbot.app/plugin/AceDataCloud/astrbot_plugin_google_search_acedatacloud)，当前市场版本仍为 `0.1.0`。点击 **安装** 后回到 **已安装** 检查启用和加载状态。此 PR 的 `0.1.1` 是说明/图片更新，尚未发布到 Cloud，不能把源码合并当成市场包已更新。

仓库安装：**插件 → 插件 → 已安装 → 安装插件（+）→ 从链接安装**，输入 `https://github.com/AceDataCloud/GoogleSearchAstrBot`。源码已经存在；安装后核启用和加载状态。仓库/文件安装与官方市场安装分别记账。

## 2. 获取 Google Search API Key

首次使用请先注册并登录；如果应用页还没有通用应用，点击 **初始化通用应用（Initialize General Application）**，再按下面步骤管理密钥。

登录 [Ace Data Cloud Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=googlesearchastrbot_readme_api_key)，打开 **General application** 复制 Key，或在 **Manage Keys → Create** 创建 AstrBot 专用 Key。服务专用 Key 必须允许 `/serp/google`。搜索前检查当前价格和余额。

只复制 Key 本身，不加 `Bearer `，也不要使用 `platform-...` 管理 Token。不要把 Key 写入聊天消息或仓库。

### Token 图文：复制或创建专用 Key

先[注册或登录 Ace](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=googlesearchastrbot_readme_signup)，打开 **Applications → General application**；没有通用应用时先初始化。图中 **1** 复制现有 Key，**2 Manage Keys → Create** 创建专用 Key。API 限制开启时应包含 `/serp/google`，并检查账户当前权限、余额与价格。

![Ace 应用页复制 Key 或管理 Key（已脱敏）](../_assets/tutorial/get-api-key-en.png)

专用 Key 可命名为 `AstrBot Google Search`；到期和限额按需设置。下图中的 `Dify tutorial` 是旧示例名称，不需要照抄。

![创建专用 API Key（共享 Ace 页面，非 AstrBot）](../_assets/tutorial/create-api-key-en.png)

两张图于 **2026-10-19** 复用核验，原拍摄日期未知，凭据/App ID/余额均已脱敏；这是共享 Ace Applications 页面，不是 AstrBot 安装或真实调用证明。[原图来源与限制](../_assets/tutorial/sources.json)。

### 在 AstrBot 填写哪里

打开 **插件 → 插件 → 已安装**，点击 **Google Search by Ace Data Cloud** 卡片齿轮（插件配置），在 **Ace Data Cloud API key with Google Search access**（字段 `api_key`）粘贴 Key 并保存。只填 Key 本身，不加 `Bearer `；不填到模型提供商或聊天消息。界面遮罩不加密磁盘配置，请保护 AstrBot 数据目录。此处提供准确文字路径；不以假界面代替本插件最新设置截图。

## 3. 配置 AstrBot

在 **Plugins → Plugins → Installed** 点击 **Google Search by Ace Data Cloud** 的齿轮，将 Key 填入 **Ace Data Cloud API key with Google Search access** 并保存。WebUI 会遮蔽 Key，但 AstrBot 数据目录存储原值，应保护该目录。

选择支持工具调用的聊天模型，并在当前 Profile 和 Persona 中允许 `google_search`。工具未出现时检查 **Plugins → Manage Behaviors → Function Tools**。

## 4. 在聊天中搜索

向机器人发送：

> 使用 `google_search` 搜索 `site:astrbot.app plugin development`，只调用一次，返回 3 条结果及各自标题、链接和摘要。

工具调用 `/serp/google` 一次，参数为 `type=search`、`page=1`、`number=3`，同步返回 `organic` 列表。可打开链接核对来源；搜索摘要属于外部内容。这里没有生成任务需要轮询。

## 5. 核对用量与排障

在 Ace Data Cloud 应用用量中筛选 **Google SERP API**。若工具返回 trace ID，可按它精确匹配；若没有，只能结合 Key/应用、API 和时间缩小范围，不能把某条账单说成已精确对应。当前成本规则为不超过 10 条结果 0.01 Credits、11–20 条结果 0.02 Credits，账户折扣另计；使用前以线上价格为准。

| 现象 | 检查项 |
| --- | --- |
| 插件加载失败 | AstrBot 版本、**Failed to Load Plugins**、**Data & Logs → Logs**。 |
| 看不到工具 | 插件已启用；当前 Profile/Persona 允许工具；模型支持工具调用。 |
| HTTP 401/403 | Key 类型、有效期、余额、服务权限及 Allowed APIs。 |
| 网络失败 | 重试前检查请求历史；超时请求仍可能已有用量。 |

插件只向 `https://api.acedata.cloud` 发送 Key，拒绝重定向，不自动重试付费搜索。使用 Python 标准库，无新增依赖。

## 已验证的本地运行

隔离的 AstrBot `v4.28.2` 实例成功加载插件；ChatUI 对示例查询实际调用 `google_search` 一次，返回三条相关 AstrBot 插件文档结果。[脱敏证据](../tests/e2e-results.json)记录输入与结果标题。

## 已验证的市场安装

2026-10-12，[Cloud 公开卡片](https://cloud.astrbot.app/plugin/AceDataCloud/astrbot_plugin_google_search_acedatacloud)显示版本 `0.1.0`。独立的全新 AstrBot `v4.28.2` 实例通过官方市场安装，读回 `install_method: market` 与 `activated: true`。ChatUI 仅调用一次 `google_search`，返回三条搜索结果。响应没有 trace ID，因此不声称精确匹配某一条账单。[脱敏市场证据](https://github.com/AceDataCloud/Index/blob/main/plans/ecosystem-growth/agent-provider-onboarding/execution/evidence/astrbot-market-20261012.json)记录安装与调用。

## 品牌素材

`logo.png` 是未修改的当前 [Google Search 服务图标](https://cdn.acedata.cloud/27e11e555d.png)，SHA-256 为 `cf8b5ead614e5ef7aed0f0a3de1b490563a3812c00f5328ec66d8efc16a2bfc1`。
