<div id="top">

<!-- HEADER STYLE: COMPACT -->
<img src="src/frontend/static//purple.svg" width="30%" align="left" style="margin-right: 15px">

# PYGENTIC-AI
<em></em>

<!-- BADGES -->
<img src="https://img.shields.io/github/license/fsecada01/Pygentic-AI?style=plastic&logo=opensourceinitiative&logoColor=white&color=blueviolet" alt="license">
<img src="https://img.shields.io/github/last-commit/fsecada01/Pygentic-AI?style=plastic&logo=git&logoColor=white&color=blueviolet" alt="last-commit">
<img src="https://img.shields.io/github/languages/top/fsecada01/Pygentic-AI?style=plastic&color=blueviolet" alt="repo-top-language">
<img src="https://img.shields.io/github/languages/count/fsecada01/Pygentic-AI?style=plastic&color=blueviolet" alt="repo-language-count">

<em>Built with the tools and technologies:</em>

<img src="https://img.shields.io/badge/Anthropic-191919.svg?style=plastic&logo=Anthropic&logoColor=white" alt="Anthropic">
<img src="https://img.shields.io/badge/Jinja-B41717.svg?style=plastic&logo=Jinja&logoColor=white" alt="Jinja">
<img src="https://img.shields.io/badge/Redis-FF4438.svg?style=plastic&logo=Redis&logoColor=white" alt="Redis">
<img src="https://img.shields.io/badge/SQLAlchemy-D71F00.svg?style=plastic&logo=SQLAlchemy&logoColor=white" alt="SQLAlchemy">
<img src="https://img.shields.io/badge/TOML-9C4121.svg?style=plastic&logo=TOML&logoColor=white" alt="TOML">
<img src="https://img.shields.io/badge/tqdm-FFC107.svg?style=plastic&logo=tqdm&logoColor=black" alt="tqdm">
<img src="https://img.shields.io/badge/Rich-FAE742.svg?style=plastic&logo=Rich&logoColor=black" alt="Rich">
<img src="https://img.shields.io/badge/GNU%20Bash-4EAA25.svg?style=plastic&logo=GNU-Bash&logoColor=white" alt="GNU%20Bash">
<img src="https://img.shields.io/badge/Celery-37814A.svg?style=plastic&logo=Celery&logoColor=white" alt="Celery">
<br>
<img src="https://img.shields.io/badge/FastAPI-009688.svg?style=plastic&logo=FastAPI&logoColor=white" alt="FastAPI">
<img src="https://img.shields.io/badge/Docker-2496ED.svg?style=plastic&logo=Docker&logoColor=white" alt="Docker">
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=plastic&logo=Python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/GitHub%20Actions-2088FF.svg?style=plastic&logo=GitHub-Actions&logoColor=white" alt="GitHub%20Actions">
<img src="https://img.shields.io/badge/OpenAI-412991.svg?style=plastic&logo=OpenAI&logoColor=white" alt="OpenAI">
<img src="https://img.shields.io/badge/uv-DE5FE9.svg?style=plastic&logo=uv&logoColor=white" alt="uv">
<img src="https://img.shields.io/badge/Pydantic-E92063.svg?style=plastic&logo=Pydantic&logoColor=white" alt="Pydantic">
<img src="https://img.shields.io/badge/YAML-CB171E.svg?style=plastic&logo=YAML&logoColor=white" alt="YAML">

<br clear="left"/>

## ☀️ Table of Contents

1. [☀ ️ Table of Contents](#-table-of-contents)
2. [🌞 Overview](#-overview)
3. [🔥 Features](#-features)
4. [🌅 Project Structure](#-project-structure)
    4.1. [🌄 Project Index](#-project-index)
5. [🚀 Getting Started](#-getting-started)
    5.1. [🌟 Prerequisites](#-prerequisites)
    5.2. [⚡ Installation](#-installation)
    5.3. [🔆 Usage](#-usage)
    5.4. [🌠 Testing](#-testing)
6. [🌻 Roadmap](#-roadmap)
7. [🤝 Contributing](#-contributing)
8. [📜 License](#-license)
9. [✨ Acknowledgments](#-acknowledgments)

---

## 🌞 Overview

**Pygentic-AI** is an AI-powered SWOT analysis platform that transforms any URL into actionable business intelligence. Using advanced language models (Claude, GPT-4), the system scrapes web content, analyzes it through multiple dimensions, and generates comprehensive SWOT analyses with competitive intelligence from Reddit.

### Key Capabilities
- 🔍 **Intelligent URL Analysis** - Extracts and analyzes content from any web page
- 🧠 **AI-Powered SWOT** - Generates structured SWOT analysis using Claude/GPT-4
- 💬 **Reddit Intelligence** - Gathers competitive insights from relevant subreddits
- ⚡ **Async Processing** - Celery-based task queue for long-running analysis
- ♿ **Accessible UI** - WCAG 2.1 AA compliant responsive interface
- 🎨 **Modern Frontend** - SCSS modular architecture with progressive enhancement

---

## 🔥 Features

### AI Analysis Engine
- Multi-model support (Anthropic Claude, OpenAI GPT-4o-mini)
- Tool-augmented generation with Reddit intelligence
- Structured output validation with Pydantic
- Async task processing with Celery

### User Interface
- Component-based templates with Jinjax
- HTMX for progressive enhancement
- Modular SCSS architecture (7-1 pattern)
- Full keyboard navigation and screen reader support
- Progressive loading with real-time status updates

### Infrastructure
- Docker containerization with multi-stage builds
- GitHub Actions CI/CD with Komodo deployment
- Traefik reverse proxy with Let's Encrypt
- Health checks and monitoring
- Environment-based configuration

---

## 🌅 Project Structure

```sh
└── Pygentic-AI/
    ├── .github
    │   └── workflows
    ├── bin
    │   ├── build.sh
    │   ├── linux_build.sh
    │   ├── python_build.sh
    │   └── start.sh
    ├── compose.yaml
    ├── core_requirements.in
    ├── core_requirements.txt
    ├── dev_requirements.in
    ├── dev_requirements.txt
    ├── docker
    │   ├── celery
    │   └── pygentic_ai
    ├── Dockerfile
    ├── pyproject.toml
    ├── README.md
    ├── src
    │   ├── app.py
    │   ├── backend
    │   ├── cworker.py
    │   └── frontend
    └── uv.lock
```

### 🌄 Project Index

<details open>
	<summary><b><code>PYGENTIC-AI/</code></b></summary>
	<!-- __root__ Submodule -->
	<details>
		<summary><b>__root__</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ __root__</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/compose.yaml'>compose.yaml</a></b></td>
					<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/core_requirements.in'>core_requirements.in</a></b></td>
					<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/core_requirements.txt'>core_requirements.txt</a></b></td>
					<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/dev_requirements.in'>dev_requirements.in</a></b></td>
					<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/dev_requirements.txt'>dev_requirements.txt</a></b></td>
					<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/Dockerfile'>Dockerfile</a></b></td>
					<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/pyproject.toml'>pyproject.toml</a></b></td>
					<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
				</tr>
			</table>
		</blockquote>
	</details>
	<!-- bin Submodule -->
	<details>
		<summary><b>bin</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ bin</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/bin\build.sh'>build.sh</a></b></td>
					<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/bin\linux_build.sh'>linux_build.sh</a></b></td>
					<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/bin\python_build.sh'>python_build.sh</a></b></td>
					<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/bin\start.sh'>start.sh</a></b></td>
					<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
				</tr>
			</table>
		</blockquote>
	</details>
	<!-- src Submodule -->
	<details>
		<summary><b>src</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ src</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\app.py'>app.py</a></b></td>
					<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\cworker.py'>cworker.py</a></b></td>
					<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
				</tr>
			</table>
			<!-- backend Submodule -->
			<details>
				<summary><b>backend</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ src.backend</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\logger.py'>logger.py</a></b></td>
							<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\utils.py'>utils.py</a></b></td>
							<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
						</tr>
					</table>
					<!-- core Submodule -->
					<details>
						<summary><b>core</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ src.backend.core</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\core\consts.py'>consts.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\core\core.py'>core.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\core\main.py'>main.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\core\tools.py'>tools.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\core\utils.py'>utils.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- db Submodule -->
					<details>
						<summary><b>db</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ src.backend.db</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\db\base.py'>base.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\db\consts.py'>consts.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\db\core.py'>core.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\db\db.py'>db.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\db\main.py'>main.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\db\utils.py'>utils.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- server Submodule -->
					<details>
						<summary><b>server</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ src.backend.server</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\server\consts.py'>consts.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\server\core.py'>core.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\server\main.py'>main.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\server\router.py'>router.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\server\utils.py'>utils.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- settings Submodule -->
					<details>
						<summary><b>settings</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ src.backend.settings</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\settings\backend_options.py'>backend_options.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\settings\base.py'>base.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\settings\consts.py'>consts.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\settings\core.py'>core.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\settings\dev.py'>dev.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\settings\main.py'>main.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\settings\prod.py'>prod.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\settings\utils.py'>utils.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- site Submodule -->
					<details>
						<summary><b>site</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ src.backend.site</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\site\consts.py'>consts.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\site\core.py'>core.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\site\main.py'>main.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\site\router.py'>router.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\backend\site\utils.py'>utils.py</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
							</table>
						</blockquote>
					</details>
				</blockquote>
			</details>
			<!-- frontend Submodule -->
			<details>
				<summary><b>frontend</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ src.frontend</b></code>
					<!-- templates Submodule -->
					<details>
						<summary><b>templates</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ src.frontend.templates</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\frontend\templates\home.html'>home.html</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\frontend\templates\result.html'>result.html</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\frontend\templates\status.html'>status.html</a></b></td>
									<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
								</tr>
							</table>
							<!-- components Submodule -->
							<details>
								<summary><b>components</b></summary>
								<blockquote>
									<div class='directory-path' style='padding: 8px 0; color: #666;'>
										<code><b>⦿ src.frontend.templates.components</b></code>
									<!-- forms Submodule -->
									<details>
										<summary><b>forms</b></summary>
										<blockquote>
											<div class='directory-path' style='padding: 8px 0; color: #666;'>
												<code><b>⦿ src.frontend.templates.components.forms</b></code>
											<table style='width: 100%; border-collapse: collapse;'>
											<thead>
												<tr style='background-color: #f8f9fa;'>
													<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
													<th style='text-align: left; padding: 8px;'>Summary</th>
												</tr>
											</thead>
												<tr style='border-bottom: 1px solid #eee;'>
													<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\frontend\templates\components\forms\Form.jinja'>Form.jinja</a></b></td>
													<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
												</tr>
												<tr style='border-bottom: 1px solid #eee;'>
													<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\frontend\templates\components\forms\Search.jinja'>Search.jinja</a></b></td>
													<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
												</tr>
											</table>
										</blockquote>
									</details>
									<!-- main Submodule -->
									<details>
										<summary><b>main</b></summary>
										<blockquote>
											<div class='directory-path' style='padding: 8px 0; color: #666;'>
												<code><b>⦿ src.frontend.templates.components.main</b></code>
											<table style='width: 100%; border-collapse: collapse;'>
											<thead>
												<tr style='background-color: #f8f9fa;'>
													<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
													<th style='text-align: left; padding: 8px;'>Summary</th>
												</tr>
											</thead>
												<tr style='border-bottom: 1px solid #eee;'>
													<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\frontend\templates\components\main\base.html'>base.html</a></b></td>
													<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
												</tr>
												<tr style='border-bottom: 1px solid #eee;'>
													<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\frontend\templates\components\main\Base.jinja'>Base.jinja</a></b></td>
													<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
												</tr>
												<tr style='border-bottom: 1px solid #eee;'>
													<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\frontend\templates\components\main\footer.html'>footer.html</a></b></td>
													<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
												</tr>
												<tr style='border-bottom: 1px solid #eee;'>
													<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\frontend\templates\components\main\Footer.jinja'>Footer.jinja</a></b></td>
													<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
												</tr>
												<tr style='border-bottom: 1px solid #eee;'>
													<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\frontend\templates\components\main\header.html'>header.html</a></b></td>
													<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
												</tr>
												<tr style='border-bottom: 1px solid #eee;'>
													<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\frontend\templates\components\main\Header.jinja'>Header.jinja</a></b></td>
													<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
												</tr>
												<tr style='border-bottom: 1px solid #eee;'>
													<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\frontend\templates\components\main\nav.html'>nav.html</a></b></td>
													<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
												</tr>
												<tr style='border-bottom: 1px solid #eee;'>
													<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\frontend\templates\components\main\Nav.jinja'>Nav.jinja</a></b></td>
													<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
												</tr>
												<tr style='border-bottom: 1px solid #eee;'>
													<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\frontend\templates\components\main\Scripts.jinja'>Scripts.jinja</a></b></td>
													<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
												</tr>
												<tr style='border-bottom: 1px solid #eee;'>
													<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\frontend\templates\components\main\Stylesheets.jinja'>Stylesheets.jinja</a></b></td>
													<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
												</tr>
												<tr style='border-bottom: 1px solid #eee;'>
													<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\frontend\templates\components\main\style_sheets.html'>style_sheets.html</a></b></td>
													<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
												</tr>
											</table>
										</blockquote>
									</details>
									<!-- snippets Submodule -->
									<details>
										<summary><b>snippets</b></summary>
										<blockquote>
											<div class='directory-path' style='padding: 8px 0; color: #666;'>
												<code><b>⦿ src.frontend.templates.components.snippets</b></code>
											<table style='width: 100%; border-collapse: collapse;'>
											<thead>
												<tr style='background-color: #f8f9fa;'>
													<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
													<th style='text-align: left; padding: 8px;'>Summary</th>
												</tr>
											</thead>
												<tr style='border-bottom: 1px solid #eee;'>
													<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\frontend\templates\components\snippets\Css.jinja'>Css.jinja</a></b></td>
													<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
												</tr>
												<tr style='border-bottom: 1px solid #eee;'>
													<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\frontend\templates\components\snippets\js.html'>js.html</a></b></td>
													<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
												</tr>
												<tr style='border-bottom: 1px solid #eee;'>
													<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\frontend\templates\components\snippets\Js.jinja'>Js.jinja</a></b></td>
													<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
												</tr>
												<tr style='border-bottom: 1px solid #eee;'>
													<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\frontend\templates\components\snippets\NavbarBrand.jinja'>NavbarBrand.jinja</a></b></td>
													<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
												</tr>
												<tr style='border-bottom: 1px solid #eee;'>
													<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\frontend\templates\components\snippets\NavbarMenu.jinja'>NavbarMenu.jinja</a></b></td>
													<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
												</tr>
												<tr style='border-bottom: 1px solid #eee;'>
													<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\frontend\templates\components\snippets\Result.jinja'>Result.jinja</a></b></td>
													<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
												</tr>
												<tr style='border-bottom: 1px solid #eee;'>
													<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\frontend\templates\components\snippets\ResultEntry.jinja'>ResultEntry.jinja</a></b></td>
													<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
												</tr>
												<tr style='border-bottom: 1px solid #eee;'>
													<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\frontend\templates\components\snippets\Spinner.jinja'>Spinner.jinja</a></b></td>
													<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
												</tr>
												<tr style='border-bottom: 1px solid #eee;'>
													<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/src\frontend\templates\components\snippets\StatusResult.jinja'>StatusResult.jinja</a></b></td>
													<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
												</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
						</blockquote>
					</details>
				</blockquote>
			</details>
		</blockquote>
	</details>
	<!-- .github Submodule -->
	<details>
		<summary><b>.github</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ .github</b></code>
			<!-- workflows Submodule -->
			<details>
				<summary><b>workflows</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ .github.workflows</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/.github\workflows\bandit.yml'>bandit.yml</a></b></td>
							<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/.github\workflows\docker-image.yml'>docker-image.yml</a></b></td>
							<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
						</tr>
					</table>
				</blockquote>
			</details>
		</blockquote>
	</details>
	<!-- docker Submodule -->
	<details>
		<summary><b>docker</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ docker</b></code>
			<!-- celery Submodule -->
			<details>
				<summary><b>celery</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ docker.celery</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/docker\celery\start.sh'>start.sh</a></b></td>
							<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
						</tr>
					</table>
				</blockquote>
			</details>
			<!-- pygentic_ai Submodule -->
			<details>
				<summary><b>pygentic_ai</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ docker.pygentic_ai</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/docker\pygentic_ai\build.sh'>build.sh</a></b></td>
							<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/docker\pygentic_ai\python_build.sh'>python_build.sh</a></b></td>
							<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/fsecada01/Pygentic-AI/blob/master/docker\pygentic_ai\python_start.sh'>python_start.sh</a></b></td>
							<td style='padding: 8px;'>Code>❯ REPLACE-ME</code></td>
						</tr>
					</table>
				</blockquote>
			</details>
		</blockquote>
	</details>
</details>

---

## 🚀 Getting Started

### 🌟 Prerequisites

This project requires the following dependencies:

- **Programming Language:** Python 3.13+
- **Package Manager:** [uv](https://docs.astral.sh/uv/) (recommended) or pip
- **Container Runtime:** Docker & Docker Compose
- **Task Runner:** [just](https://github.com/casey/just) (command runner)
- **Node.js:** For frontend asset compilation (npm)

### ⚡ Installation

#### Install just (Task Runner)

**macOS/Linux:**
```sh
# macOS
brew install just

# Linux
curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin
```

**Windows:**
```powershell
# Using Scoop
scoop install just

# Using Chocolatey
choco install just
```

#### Build Pygentic-AI from Source

1. **Clone the repository:**

    ```sh
    git clone https://github.com/FJS-Services-Inc/Pygentic-AI
    ```

2. **Navigate to the project directory:**

    ```sh
    cd Pygentic-AI
    ```

3. **Quick setup with justfile (recommended):**

    ```sh
    # One command setup: creates .env, installs deps, compiles SCSS
    just setup
    ```

4. **Manual installation (alternative):**

<!-- SHIELDS BADGE CURRENTLY DISABLED -->
<!-- [![docker][docker-shield]][docker-link] -->
<!-- REFERENCE LINKS -->
<!-- [docker-shield]: https://img.shields.io/badge/Docker-2CA5E0.svg?style={badge_style}&logo=docker&logoColor=white -->
<!-- [docker-link]: https://www.docker.com/ -->

**Using [docker](https://www.docker.com/):**

	```sh
	❯ docker build -t fsecada01/Pygentic-AI .
	```

<!-- SHIELDS BADGE CURRENTLY DISABLED -->
<!-- [![pip][pip-shield]][pip-link] -->
<!-- REFERENCE LINKS -->
<!-- [pip-shield]: https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white -->
<!-- [pip-link]: https://pypi.org/project/pip/ -->

**Using [pip](https://pypi.org/project/pip/):**

	```sh
	❯ pip install -r core_requirements.txt, dev_requirements.txt
	```
If this fails due to platform-specific issues, try this instead:

    ```sh
    ❯ pip install -r core_requirements.in, dev_requirements.in
    ```

<!-- SHIELDS BADGE CURRENTLY DISABLED -->
<!-- [![uv][uv-shield]][uv-link] -->
<!-- REFERENCE LINKS -->
<!-- [uv-shield]: https://img.shields.io/badge/uv-DE5FE9.svg?style=for-the-badge&logo=uv&logoColor=white -->
<!-- [uv-link]: https://docs.astral.sh/uv/ -->

**Using [uv](https://docs.astral.sh/uv/):**

	```sh
	❯ uv sync --all-extras --dev
	```

### 🔆 Usage

#### Development Mode

**Quick start (recommended):**
```sh
# Terminal 1: Start FastAPI development server
just dev

# Terminal 2: Start Celery worker
just celery

# Terminal 3: Auto-compile SCSS on changes
just scss-watch
```

**Manual start:**
```sh
# Using uv (recommended)
uv run python src/app.py              # FastAPI server
uv run python src/cworker.py          # Celery worker

# Using pip
python src/app.py
python src/cworker.py
```

#### Production Mode (Docker)

**With justfile:**
```sh
# Build and start all services
just build
just up-d

# Check status
just health
just ps

# View logs
just logs-f
```

**Manual Docker commands:**
```sh
# Build image
docker build -t s3docker.francissecada.com/pygentic_ai:latest .

# Start services
docker-compose up -d

# View logs
docker-compose logs -f
```

#### Available Commands

Run `just` to see all available commands:
```sh
just                    # List all commands
just --list             # Same as above

# Common commands
just setup             # First-time setup
just dev               # Development server
just test              # Run tests
just build [tag]       # Build Docker image
just deploy [tag]      # Deploy to production
just health            # Check service health
just clean             # Clean up containers
```

### 🌠 Testing

**Run all tests:**
```sh
just test              # Quick test run
just test-cov          # With coverage report
```

**Manual testing:**
```sh
# Using uv (recommended)
uv run pytest tests/ -v
uv run pytest tests/ --cov=src --cov-report=html

# Using pip
pytest tests/ -v
```

**Quality checks:**
```sh
just lint              # Run linters
just format            # Format code
just security          # Security scan
just check             # All checks (pre-commit)
```

---

## 🤖 Claude AI Assistance

This project includes a multi-agent orchestration system for Claude AI to assist with development.

### Setup

The project includes two key files for Claude integration:

- **`.claude/system-prompt.md`** - Multi-agent orchestration instructions (personas, MCP routing, patterns)
- **`CLAUDE.md`** - Project initialization guide (architecture, workflows, commands)

### Available Personas

Claude activates appropriate personas based on the task:

- 🏗️ **Architect** - System design, architecture decisions, scaling
- 🎨 **Frontend** - UI/UX, SCSS, accessibility, Jinjax components
- ⚙️ **Backend** - FastAPI, Celery, database, AI agents
- 🔒 **Security** - Authentication, secrets, input validation
- 🚀 **DevOps** - Docker, CI/CD, deployment, monitoring

### Usage

```sh
# View Claude context files
just start-claude      # Display orchestration context

# When using Claude
# Use /init command to load project context from CLAUDE.md
# Claude will activate appropriate personas for your task
```

### Example Workflows

**Feature Development:**
```
User: "Add user authentication"
Claude: Activates 🏗️ Architect, 🔒 Security, ⚙️ Backend, 🎨 Frontend
- Designs auth architecture
- Implements secure endpoints
- Creates login UI components
- Updates deployment configs
```

**Bug Fixing:**
```
User: "Fix SCSS compilation error"
Claude: Activates 🎨 Frontend persona
- Identifies SCSS syntax issues
- Runs just scss to verify fix
- Updates documentation if needed
```

---

## 📋 Justfile Command Reference

Quick reference for common `just` commands:

### Development
```sh
just setup              # First-time project setup
just dev                # Start FastAPI dev server
just celery             # Start Celery worker
just scss               # Compile SCSS once
just scss-watch         # Auto-compile SCSS on changes
just npm-install        # Install frontend dependencies
```

### Docker Operations
```sh
just build [tag]        # Build Docker image
just up                 # Start services
just up-d               # Start in detached mode
just down               # Stop services
just restart            # Restart services
just logs-f             # Follow all logs
just logs-web           # Follow web service logs
just logs-celery        # Follow celery logs
just health             # Check service health
just ps                 # Show container status
just stats              # Show resource usage
```

### Testing & Quality
```sh
just test               # Run test suite
just test-cov           # Run with coverage
just lint               # Run linters
just format             # Format code
just security           # Security scan
just check              # All quality checks
```

### Deployment
```sh
just deploy [tag]       # Deploy with specific tag
just deploy-dev         # Deploy dev environment
just deploy-main        # Deploy production
just pull [tag]         # Pull Docker image
```

### Database
```sh
just migrate            # Run migrations
just migration [name]   # Create migration
```

### Cleanup
```sh
just clean              # Remove containers
just clean-images       # Remove images
just clean-all          # Full cleanup
just prune              # Remove unused resources
```

### Utilities
```sh
just info               # Show environment info
just config             # Show Docker Compose config
just check-env          # Validate environment variables
just init-env           # Create .env from template
```

For a complete list: `just --list`

---

## 🌻 Roadmap

- [X] **`Task 1`**: Bootstrap a minimal application build
- [ ] **`Task 2`**: Implement DB Backend with PostgreSQL
- [ ] **`Task 3`**: Integrate user auth and group controls

---

## 🤝 Contributing

- **💬 [Join the Discussions](https://github.com/fsecada01/Pygentic-AI/discussions)**: Share your insights, provide feedback, or ask questions.
- **🐛 [Report Issues](https://github.com/fsecada01/Pygentic-AI/issues)**: Submit bugs found or log feature requests for the `Pygentic-AI` project.
- **💡 [Submit Pull Requests](https://github.com/fsecada01/Pygentic-AI/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/fsecada01/Pygentic-AI
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="left">
   <a href="https://github.com{/fsecada01/Pygentic-AI/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=fsecada01/Pygentic-AI">
   </a>
</p>
</details>

---

## 📜 License

Pygentic-ai is protected under the [LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

## ✨ Acknowledgments

- Credit `contributors`, `inspiration`, `references`, etc.

<div align="left"><a href="#top">⬆ Return</a></div>

---
