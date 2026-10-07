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
| 提交 | 已有三次提交，工作区干净 |
| `.gitignore` | 已排除 `.venv/`、`__pycache__/`、`.ipynb_checkpoints/` |
| 跟踪文件 | 25 个，不包含 `.venv` |
| 图表位置 | `output/charts/energy_trend.png`、`yoy_growth.png` |
| SSH 密钥 | 已生成 `C:\Users\Lenovo\.ssh\id_ed25519`（ed25519，无口令） |
| SSH 配置 | 已写入 `C:\Users\Lenovo\.ssh\config`，GitHub 走 `ssh.github.com:443` |
| SSH 连通性 | GitHub 与 Gitee 均已连通，等待把公钥加入账号 |

当前本地 Git 身份是临时占位：

```text
user.name  = Lenovo
user.email = lenovo@local
```

创建 GitHub 账号后，需要改成你自己的用户名和邮箱（见第二节第 4 步）。

### 当前网络检查结果（2026-10-07 实测）

| 目标 | 结果 | 说明 |
|---|---|---|
| `https://github.com`（网页） | 间歇超时 | 有时通、有时断，注册和网页操作可能失败 |
| `https://api.github.com` | 正常 | `gh` 命令行、头像、API 类操作可用 |
| `git@github.com:22` / `git@ssh.github.com:443` | 正常 | 可以用 SSH 方式推送代码 |
| `https://gitee.com`、`git@gitee.com` | 正常 | 可整条流程替代 GitHub |

结论：

1. **推代码没问题**：SSH 通道已配好，只差把公钥加入账号。
2. **网页端可能打不开**：注册、建仓库、生成 token 时如果打不开 `github.com`，换手机热点或手机浏览器试，或者等几分钟重试。
3. **`gh` 命令行可以正常登录和建仓库**：它走 `api.github.com`，不受网页端影响。
4. 如果 GitHub 网页始终进不去，就用本指南第七节的 Gitee 方案，项目内容完全一样。

本机公钥（需要复制到 GitHub / Gitee 的 SSH 公钥设置里）：

```text
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINsY/Pe4/EJ8e00gciPyp8ZrQRROJzIYS1rG4RxWwRoI lenovo-energy-2026
```

私钥 `id_ed25519` 不要发给任何人，也不要复制到聊天里。

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
& "C:\Program Files\GitHub CLI\gh.exe" auth login --hostname github.com --git-protocol ssh --web
```

依次选择：

1. **GitHub.com**
2. **SSH**（Git 操作用 SSH）
3. 终端会显示一个一次性验证码，例如 `XXXX-XXXX`
4. 打开 <https://github.com/login/device>，输入验证码并授权
   - 本机浏览器打不开时，用手机流量打开这个网址，输入同一个验证码即可。
5. 如果 `gh` 询问是否把 SSH 公钥上传到账号，选 **Yes**，并选择 `C:\Users\Lenovo\.ssh\id_ed25519.pub`。

如果 `gh` 没有自动上传公钥，就手动加：

1. GitHub → 头像 → **Settings** → **SSH and GPG keys** → **New SSH key**。
2. Title 填 `Lenovo-Windows`，Key type 选 **Authentication Key**。
3. 把上面那段 `ssh-ed25519 AAAA...` 全部粘贴进去，保存。

完成后检查：

```bash
& "C:\Program Files\GitHub CLI\gh.exe" auth status
```

看到 `Logged in to github.com` 即成功。

再验证 SSH：

```bash
ssh -T git@github.com
```

看到 `Hi 你的用户名! You've successfully authenticated...` 即成功。

**方式 B：HTTPS + Personal Access Token**

提示：这条路需要能打开 `github.com` 网页端；网页打不开时优先用方式 A。

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
git remote add origin git@github.com:你的用户名/energy-data-analysis.git
git push -u origin main
```

这里故意用 SSH 地址（`git@github.com:...`）：网页端和 HTTPS 会被间歇阻断，SSH 通道更稳。已经配好 `ssh.github.com:443` 作为默认路由，不需要额外设置。

如果提示 remote 已存在：

```bash
git remote set-url origin git@github.com:你的用户名/energy-data-analysis.git
git push -u origin main
```

如果第 2 步使用 `gh repo create`，它已经自动推送，不需要再执行上面的命令。

用 `gh` 创建远程仓库并用 SSH 推送的完整命令：

```bash
cd "C:\Users\Lenovo\Documents\New project\Three_Year_Plan_2026_2029\Energy_Data_Project"
& "C:\Program Files\GitHub CLI\gh.exe" repo create energy-data-analysis --public --source . --remote origin --push
```

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
| `github.com` 网页打不开或超时 | 推代码走 SSH 不受影响；注册/建仓库改用手机流量或过几分钟重试 |
| `ssh -T git@github.com` 提示 Permission denied (publickey) | 说明还没把公钥加到账号，按方式 A 第 5 步添加 |
| `ssh -T git@github.com` 提示 Connection timed out | 运行 `ssh -G github.com`，确认输出 `hostname ssh.github.com`、`port 443` |
| `git push` 要求输入密码 | GitHub 已不接受账号密码，改用 token 或 `gh auth login` |
| 提示 remote origin already exists | 用 `git remote set-url origin ...` 改地址 |
| 推送被拒绝 non-fast-forward | 先 `git pull --rebase origin main`，再 `git push` |
| 出现 LF/CRLF 警告 | Windows 正常现象，不影响上传 |
| token 泄露 | 立即到 GitHub → Settings → Developer settings 撤销 |
| 数据超过 100MB | 不要直接提交，改用 Git LFS 或只提交示例数据 |
| 邮箱不想公开 | 使用 GitHub 的 `users.noreply.github.com` 地址 |

---

## 六、现在的最小行动清单

1. 打开 <https://github.com/signup>，注册账号并验证邮箱（打不开就用手机流量）。
2. 开启两步验证。
3. 运行：

```bash
& "C:\Program Files\GitHub CLI\gh.exe" auth login --hostname github.com --git-protocol ssh --web
```

复制终端里的一次性验证码，在 <https://github.com/login/device> 授权；询问上传 SSH 公钥时选 **Yes**。

4. 运行下面的命令，把项目推上去：

```bash
cd "C:\Users\Lenovo\Documents\New project\Three_Year_Plan_2026_2029\Energy_Data_Project"
git config user.name "你的GitHub用户名"
git config user.email "你的GitHub注册邮箱"
git commit --amend --reset-author --no-edit
& "C:\Program Files\GitHub CLI\gh.exe" repo create energy-data-analysis --public --source . --remote origin --push
```

5. 打开 `https://github.com/你的用户名/energy-data-analysis`，确认文件都在。

---

## 七、GitHub 网页始终打不开时的 Gitee 替代方案

Gitee（码云）国内可直接访问，功能和 GitHub 类似，推完仓库一样能作为竞赛、转专业、保研的技能证明材料。

### 7.1 注册与加公钥（你完成）

1. 打开 <https://gitee.com/signup>，注册并验证邮箱。
2. 开启两步验证：头像 → **账号设置** → **安全设置**。
3. 添加公钥：头像 → **账号设置** → **安全设置** → **SSH 公钥**。
4. 标题填 `Lenovo-Windows`，公钥粘贴上面那一段 `ssh-ed25519 AAAA...`，保存。
5. 在“账号设置 → 个人资料”里记下你的 **Gitee 个人空间地址**（用户名），例如 `lenovo-ujs`。

### 7.2 验证与推送（可以让我来做）

```bash
ssh -T git@gitee.com

cd "C:\Users\Lenovo\Documents\New project\Three_Year_Plan_2026_2029\Energy_Data_Project"
git config user.name "你的Gitee用户名"
git config user.email "你的注册邮箱"
git commit --amend --reset-author --no-edit
git remote add origin git@gitee.com:你的Gitee用户名/energy-data-analysis.git
git push -u origin main
```

在 Gitee 网页端先建一个空仓库 `energy-data-analysis`（不要勾选初始化 README），再执行上面的 `git remote add` 和 `git push`。

### 7.3 GitHub 与 Gitee 同时使用的注意点

1. 一套 SSH 密钥两边都能用，不需要生成两份。
2. 如果两边都要推，可以给远程仓库起不同名字：`origin`（GitHub）、`gitee`（Gitee），分别 `git push origin main`、`git push gitee main`。
3. 竞赛、保研材料里 Gitee 链接同样有效，但国外交流或申请出国时 GitHub 更通用；建议先保证 Gitee 能跑通，再做 GitHub。
