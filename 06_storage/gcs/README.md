# Google Cloud Storage Integration（Google Cloud Storage 集成）

演示使用 JSON blob storage 将 Google Cloud Storage (GCS) 与 Agno agents 集成的示例。

## Setup（设置）

```shell
uv pip install google-cloud-storage
```

## Configuration（配置）

```python
from agno.agent import Agent
from agno.storage.gcs_json import GCSJsonDb

db = GCSJsonDb(
    bucket_name="your-bucket-name",
)

agent = Agent(
    db=db,
    add_history_to_context=True,
)
```

## Authentication（认证）

使用以下方法之一设置认证：

```shell
# 使用 gcloud CLI
gcloud auth application-default login

# 使用环境变量
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"
```

## Permissions（权限）

确保您的账户具有 Storage Admin 权限：

```shell
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="user:your-email@example.com" \
    --role="roles/storage.admin"
```


安装所需的 Python 包：


```bash
uv pip install google-auth google-cloud-storage openai ddgs
```


## Example Script（示例脚本）

### Debugging and Bucket Dump（调试和桶转储）

在示例脚本中，全局变量 `DEBUG_MODE` 控制是否在执行结束时打印桶内容。
在脚本中设置 `DEBUG_MODE = True` 以查看桶的内容。

```bash
gcloud init
gcloud auth application-default login
python gcs_json_storage_for_agent.py
```

## Local Testing with Fake GCS（使用 Fake GCS 进行本地测试）

如果您想在不使用真实 GCS 的情况下本地测试存储功能，可以使用 [fake-gcs-server](https://github.com/fsouza/fake-gcs-server)：

### Setup Fake GCS with Docker（使用 Docker 设置 Fake GCS）


2. **安装 Docker：**

确保您的系统上安装了 Docker。

4. **在项目根目录创建 `docker-compose.yml` 文件**，内容如下：


```yaml
version: '3.8'
services:
  fake-gcs-server:
    image: fsouza/fake-gcs-server:latest
    ports:
      - "4443:4443"
    command: ["-scheme", "http", "-port", "4443", "-public-host", "localhost"]
    volumes:
      - ./fake-gcs-data:/data
```

6. **启动 Fake GCS 服务器：**


```bash
docker-compose up -d
```

这将在 `http://localhost:4443` 上启动 fake GCS 服务器。


### Configuring the Script to Use Fake GCS（配置脚本使用 Fake GCS）


设置环境变量，使 GCS 客户端将 API 调用定向到模拟器：



```bash
export STORAGE_EMULATOR_HOST="http://localhost:4443"
python gcs_json_for_agent.py
```


使用 Fake GCS 时，不强制进行身份验证。客户端将自动检测模拟器端点。
