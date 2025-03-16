# RedditBot 🚀
**Automated, containerized and cloud-deployed Discord bot fetching reddit posts.**

---
## 🌟 Key Features
- [x] Fetches Reddit posts and presents neatly in Discord
- [x] Supports multiple sorting methods (hot, top, new, rising)
- [x] Embeds YouTube- and Reddit-hosted videos for smooth playback
- [x] Includes logging, monitoring, and automated deployments
---

## 🛠️  Workflow & Tools Used
| Method                            | Implementation |
|----------------------------------|-------------------------------------------|
| 💡 **Infrastructure as Code**       | *Azure CLI for automated container deployments* |
| 🛆 **Containerization & Orchestration** | *Dockerized and deployed to Azure Container Apps* |
| ⚙️ **CI/CD Automation**                | *GitHub Actions automatically builds and deploys images to GitHub Container Registry (GHCR)* |
| 🔒 **Secrets Management & Security**   | *Uses Azure Secrets to store API tokens* |
| 📊 **Logging**                           | *Integrated Prometheus for collecting bot metrics* |
| 🐳 **Grafana Monitoring**                | *WIP* |
| 🛡️ **Auto-Scaling**                      | *WIP* |
| 🛠️ **Automated Deployment**              | *WIP* |


---
### 🛆 Containerization & Deployment
- #####  ✅ Dockerization
  - The bot is built inside a Docker container which ensires dependency consistency across various environments:
  <details>
    <summary>Click to expand the Dockerfile</summary>

  ```dockerfile
  FROM python:3.10
  WORKDIR /app
  COPY . .
  RUN pip install -r requirements.txt
  CMD ["python", "src/bot.py"]
  ```
  </details>

- ##### ✅ CI/CD with Github Actions
  - Every time an update is pushed to **main**, Github actions:
     - [x] Builds Docker image
     - [x] Pushes it to Github Registry
     - [x] Triggers Azure deployment

 - ##### Github Actions workflow ( .github/workflows/docker-build.yml):
    <details>
      <summary>Click to expand the yml</summary>

    ```yml
      on: push
      jobs:
        build-and-push:
          runs-on: ubuntu-latest
          steps:
            - name: Checkout code
              uses: actions/checkout@v3
            - name: Log in to GHCR
              uses: docker/login-action@v2
              with:
                registry: ghcr.io
                username: ${{ github.actor }}
                password: ${{ secrets.GHCR_TOKEN }}
            - name: Build and push image
              uses: docker/build-push-action@v3
              with:
                push: true
                tags: ghcr.io/${{ github.repository_owner }}/redditbot:latest
    ```
    </details>
---

### 🌍 Cloud Deployment

- ##### ✅ The bot runs as an Azure Container App, ensuring:
  - [x] **Scalability** – Can handle increased demand
  - [x] **Security** – Uses Azure Secrets Management for API key
  - [x] **Automatic Updates** – New GitHub pushes auto-deploy
 - ##### Deployed using Azure CLI:
    <details>
      <summary>Click to expand Azure CLI</summary>

    ```bash
    az containerapp create \
      --name redditbot \
      --resource-group redditbot-group \
      --image ghcr.io/GITHUB_USERNAME/redditbot:latest \
      --secrets discord-token=discord_token \
      --env-vars DISCORD_TOKEN=secretref:discord-token \
      --registry-server ghcr.io \
      --registry-username GITHUB_USERNAME \
      --registry-password GHCR_TOKEN \
      --ingress internal
    ```
    </details>

---
### 📊🐳 Monitoring with Prometheus & Grafana
- #####  ✅ Prometheus Metrics
  - The bot tracks:
    - Messages recieved (`discord_messages_recieved`)
    - Commands used (`discord_commands_used`)
- #####  ✅ Grafana Visualization **(WIP)**
  - Dashboards track bot activity & performance **(WIP)**
  - Alert notification to signal crashes **(WIP)**

---
### 🔒 Security
  - [x] Secrets are **never** stored in code - Uses **Azure Secrets**
  - [x] **GitHub Actions** prevents unauthorized deployments
  - [x] Uses **least privilege** principle for API keys
  - [x] **Containerized** to prevent dependency conflicts

---

### 🚀 How to Run the Bot Locally

- To run with Docker
  ```bash
  docker pull ghcr.io/YOUR_GITHUB_USERNAME/redditbot:latest
  docker run -d
  -e DISCORD_TOKEN=yourtoken
  -e REDDIT_CLIENT_ID=yourid ghcr.io/YOUR_GITHUB_USERNAME/redditbot:latest
  ```
- Or manually:
  ```bash
  python -m src/app.py
  ```
---
### 🌟 Contribution
- Pull requests and suggestions are welcome, open an issue or dm for requests.

---
### 🚧 Known Bugs and Todos 😯

- ❌ ```ModuleNotFoundError: No module named 'config'```
 > **Issue**: Python cannot find the config module even though it exists.
  **Workaround:** Run Python with -m flag: `python -m src.bot`

- ❌**Grafana**
> Still working on presenting Prometheus metrics in a visual dashboard.

- ❌**AI functions**
> Subreddit trend summarizer (Using NLP to analyze trends)
 Post summarizer (Summarizes top posts using LLMs)


---

