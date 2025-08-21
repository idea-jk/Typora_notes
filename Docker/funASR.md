# docker安装funASR

### 1、使用docker拉取funASR镜像

从场景上，语音识别可以分为流式语音识别和非流式语音识别。**非流式语音识别（离线识别）是指模型在用户说完一句话或一段话之后再进行识别，而流式语音识别则是指模型在用户还在说话的时候便同步进行语音识别。**流式语音识别因为其延时低的特点，在工业界中有着广泛的应用，例如听写转录等。

**支持非流式语音识别**

```shell
docker pull registry.cn-hangzhou.aliyuncs.com/funasr_repo/funasr:funasr-runtime-sdk-cpu-0.2.1
```

**支持流式语音识别**

```shell
docker pull registry.cn-hangzhou.aliyuncs.com/funasr_repo/funasr:funasr-runtime-sdk-online-cpu-0.1.1
```

### 2、启动funASR镜像

```shell
docker run -p 10095:10095 -itd --privileged=true -v /home/lukeewin/funasr/model:/workspace/models funasr:cpu-0.2.1
```

把本地的**/home/lukeewin/funasr/model**挂载到镜像中的**/workspace/models**。 funasr:cpu-0.2.1填写你自己的REPOSITORY:TAG。

### 3、服务端启动

进入容器

```shell
docker attach 容器id
```

启动服务端

注意不要用**run_server.sh**方式启动，因为该脚本中加了下载的参数，会自动联网下载，如果是内网环境下是不能启动的，所以需要到**/workspace/FunASR/funasr/runtime/websocket/build/bin**下面的**funasr-wss-server**和**funasr-wss-server-2pass**。

 **非实时语音识别 直接从sh脚本中启动**

```shell
cd FunASR/funasr/runtime
nohup bash run_server.sh \
	--vad-dir /workspace/models/damo/speech_fsmn_vad_zh-cn-16k-common-onnx \
	--model-dir /workspace/models/damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-onnx \
	--punc-dir /workspace/models/damo/punc_ct-transformer_zh-cn-common-vocab272727-onnx \
    --certfile 0 > offline-funasr.log 2>&1 &
# 如果您想关闭ssl，增加参数：--certfile 0
```

从编译好的二进制文件中启动

```shell
cd FunASR/funasr/runtime/websocket/build/bin
nohup ./funasr-wss-server \
  --vad-dir /workspace/models/damo/speech_fsmn_vad_zh-cn-16k-common-onnx \
  --model-dir /workspace/models/damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-onnx  \
  --punc-dir /workspace/models/damo/punc_ct-transformer_zh-cn-common-vocab272727-onnx > funasr.log 2>&1 & 
# 如果您想关闭ssl，增加参数：--certfile  "" --keyfile ""
# 如果您想使用时间戳或者热词模型进行部署，请设置--model-dir为对应模型：
# damo/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-onnx（时间戳）
# 或者 damo/speech_paraformer-large-contextual_asr_nat-zh-cn-16k-common-vocab8404-onnx（热词）

```

**实时语音识别**

```shell
cd FunASR/funasr/runtime/websocket/build/bin
nohup ./funasr-wss-server-2pass \
	--vad-dir /workspace/models/damo/speech_fsmn_vad_zh-cn-16k-common-onnx \
    --model-dir /workspace/models/damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-onnx \
    --online-model-dir /workspace/models/damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-online-onnx \
    --punc-dir /workspace/models/damo/punc_ct-transformer_zh-cn-common-vad_realtime-vocab272727-onnx > online_funasr.log 2>&1 &
```

**注意：**

```shell
无网环境中一定要把--download-model-dir参数去掉，否则会联网下载模型。

同时需要修改模型配置文件configuration,json把，模型的路径写成绝对路径。

上面我的挂载路径是把/home/DEV_admin/realTime_funasr/modelscope挂载到镜像里的/workspace/models，并且在modelscope下面有damo目录，damo下面存放各个模型。
```

```shell
Error when load am onnx model: Load model from /workspace/models/damo/speech_paraformer-large-contextual_asr_nat-zh-cn-16k-common-vocab8404-onnx/model_quant.onnx failed:Protobuf parsing failed
```

启动完成后可以通过ctrl+p，然后ctrl+q来保持运行并退出容器，注意不能直接使用exit命令退出。

### 4、模型下载

```python
from modelscope.hub.snapshot_download import snapshot_download  model_dir = snapshot_download('damo/speech_paraformer-large-contextual_asr_nat-zh-cn-16k-common-vocab8404-onnx', cache_dir='path/to/local/dir')
```

如果不指定保存目录，那么默认保存到~/.cache/modelscope/hub目录。 注意：一定要保持最新版本的modelscope，如果不是最新版本，那么下载的时候会报错。

```shell
pip install modelscope --upgrade
```

