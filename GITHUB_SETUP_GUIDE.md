# GitHub 注册与项目上传指南

> 适用项目：`Energy_Data_Project`（Python 能源数据分析）
>
> 目标：注册 GitHub 账号，把已经准备好的本地仓库推送到 GitHub。

---

## 一、我已经完成的部分

| 项目 | 状态 |
|---|---|
| Git 安装 | 已安装 Git 2.55.0 |
| GitHub CLI | 已安装 `gh` 2.102.0 |
| 本地仓库 | 已在 `Energy_Data_Project` 中初始化 |
| 分支 | `main` |
| 提交 | 已有两次提交，工作区干净 |
| `.gitignore` | 已排除 `.venv/`、`__pycache__/`、`.ipynb_checkpoints/` |
| 跟踪文件 | 24 个，不包含 `.venv` |
| 图表位置 | `output/charts/energy_trend.png`、`yoy_growth.png` |

当前本地 Git 身份是临时占位：

```text
user.name  = Lenovo
user.email = lenovo@local
```

创建 GitHub 账号后，需要改成你自己的用户名和邮箱（见第五节）。

---

## 二、你需要做的部分

### 第 1 步：注册 GitHub 账号

1. 打开 <https://github.com/signup>。
2. 输入邮箱、密码、用户名。
3. 到邮箱里完成验证。
4. 开启两步验证：右上角头像 → **Settings** → **Password and authentication** → **Two-factor authentication**。
   - 推荐用手机验证器 App。
   - 保存好恢复代码，丢失后可能无法登录。
5. 建议补全个人资料：姓名、头像、学校（Jiangsu University）。
6. 记下两样东西：
   - GitHub 用户名，例如 `lenovo-ujs`。
   - 注册邮箱。

注意：GitHub 注册、邮箱验证、两步验证必须由你本人完成，AI 不能替代。

### 第 2 步：创建远程仓库

**网页方式（最简单）**

1. 登录 GitHub，点击右上角 **+** → **New repository**。
2. Repository name 填 `energy-data-analysis`。
3. Description 可以填：`Python energy data analysis: cleaning, trends, YoY growth and charts`。
4. 选择 **Public**（推荐）或 **Private**。
5. 不要勾选 **Add a README file**、**Add .gitignore**、**Choose a license**，因为本地仓库已经有这些文件。
6. 点击 **Create repository**。
7. 复制页面上显示的 HTTPS 地址：

```text
https://github.com/你的用户名/energy-data-analysis.git
```

**GitHub CLI 方式（更省事，需要先登录）**

```bash
gh repo create energy-data-analysis --public --source "C:\Users\Lenovo\Documents\New project\Three_Year_Plan_2026_2029\Energy_Data_Project" --push
```

### 第 3 步：登录和认证（二选一）

**方式 A：GitHub CLI（推荐）**

在 PowerShell 里运行：

```bash
gh auth login
```

依次选择：

1. **GitHub.com**
2. **HTTPS**
3. **Login with a web browser**
4. 复制一次性验证码，在浏览器里粘贴并授权

完成后检查：

```bash
gh auth status
```

看到 `Logged in to github.com` 即成功。

**方式 B：HTTPS + Personal Access Token**

1. GitHub → 头像 → **Settings** → **Developer settings**。
2. **Personal access tokens** → **Tokens (classic)** → **Generate new token (classic)**。
3. Note 填 `energy-data-project`，Expiration 选 90 天。
4. 勾选 **repo** 权限。
5. 生成后复制 token（以 `ghp_` 开头），只显示一次，务必保存。
6. 以后 `git push` 提示输入密码时：
   - 用户名：你的 GitHub 用户名。
   - 密码：粘贴这个 token。

注意：GitHub 不再接受账号登录密码作为 git 密码；只能用 token 或 `gh auth login`。

### 第 4 步：更新 Git 身份

在项目目录执行：

```bash
cd "C:\Users\Lenovo\Documents\New project\Three_Year_Plan_2026_2029\Energy_Data_Project"
git config user.name "你的GitHub用户名"
git config user.email "你的GitHub注册邮箱"
git commit --amend --reset-author --no-edit
```

如果想隐藏邮箱，用 GitHub 的 noreply 地址：

1. GitHub → **Settings** → **Emails**。
2. 勾选 **Keep my email addresses private**。
3. 复制形如 `12345678+用户名@users.noreply.github.com` 的地址。
4. 把它作为 `git config user.email` 的值。

如果想让第一次提交也用你的身份，可以重建一个只有一次提交的干净历史：

```bash
git checkout --orphan main-clean
git add .
git commit -m "Initial commit: energy data analysis project"
git branch -M main-clean main
```

### 第 5 步：推送代码

如果第 2 步用网页方式建了空仓库：

```bash
cd "C:\Users\Lenovo\Documents\New project\Three_Year_Plan_2026_2029\Energy_Data_Project"
git remote add origin https://github.com/你的用户名/energy-data-analysis.git
git push -u origin main
```

如果提示 remote 已存在：

```bash
git remote set-url origin https://github.com/你的用户名/energy-data-analysis.git
git push -u origin main
```

如果第 2 步使用 `gh repo create`，它已经自动推送，不需要再执行上面的命令。

### 第 6 步：验证上传结果

1. 刷新 GitHub 仓库页面。
2. 确认能看到：
   - `README.md`
   - `energy_all_in_one.py`
   - `output/charts/energy_trend.png`
   - `output/charts/yoy_growth.png`
   - `report_template.md`
3. 点开两张 PNG，确认能正常显示。
4. 点开 commits，确认提交作者是你的用户名。

---

## 三、认证之后我还能帮你做什么

你完成 `gh auth login` 后，把 GitHub 用户名和仓库名告诉我，我可以继续帮你：

1. 更新本地 Git 身份。
2. 用 `gh repo create` 创建远程仓库。
3. 执行 `git push` 并处理报错。
4. 给仓库加 LICENSE、topics、GitHub Pages。
5. 优化 README，加入两张图和数据来源说明。

我不能替你注册账号、输入密码、完成两步验证，也不能替你提供真实数据。

---

## 四、安全与合规

1. 不要把 GitHub 密码或 token 发给任何人，包括 AI。
2. 开启两步验证，并保存恢复代码。
3. 如果 token 曾经出现在聊天、截图或代码里，立刻去 GitHub 撤销并重新生成。
4. 不要上传 `.venv`、个人隐私数据或敏感数据；`.gitignore` 已经排除 `.venv`。
5. 使用真实数据时写清来源；不确定能否公开的数据就先放私有仓库。
6. 遵守江苏大学和比赛的 AI 使用规定，确保自己能讲清楚项目内容。

---

## 五、常见问题

| 问题 | 解决方法 |
|---|---|
| `gh` 命令找不到 | 重启终端，或用完整路径 `C:\Program Files\GitHub CLI\gh.exe` |
| `git push` 要求输入密码 | GitHub 已不接受账号密码，改用 token 或 `gh auth login` |
| 提示 remote origin already exists | 用 `git remote set-url origin ...` 改地址 |
| 推送被拒绝 non-fast-forward | 先 `git pull --rebase origin main`，再 `git push` |
| 出现 LF/CRLF 警告 | Windows 正常现象，不影响上传 |
| token 泄露 | 立即到 GitHub → Settings → Developer settings 撤销 |
| 数据超过 100MB | 不要直接提交，改用 Git LFS 或只提交示例数据 |
| 邮箱不想公开 | 使用 GitHub 的 `users.noreply.github.com` 地址 |

---

## 六、现在的最小行动清单

1. 打开 <https://github.com/signup>，注册账号并验证邮箱。
2. 开启两步验证。
3. 运行 `gh auth login`，用浏览器授权。
4. 运行下面的命令，把项目推上去：

```bash
cd "C:\Users\Lenovo\Documents\New project\Three_Year_Plan_2026_2029\Energy_Data_Project"
git config user.name "你的GitHub用户名"
git config user.email "你的GitHub注册邮箱"
git commit --amend --reset-author --no-edit
gh repo create energy-data-analysis --public --source . --push
```

5. 打开 `https://github.com/你的用户名/energy-data-analysis`，确认文件都在。
