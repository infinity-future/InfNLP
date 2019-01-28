
# InfNLP

## 相关项目

### NLP后端

[HanLP](https://github.com/hankcs/HanLP)

## 私有化

### 自己运行后台的docker私有部署

如果使用私有部署，需要修改环境变量`INFNLP_ROOT`到某个地址，在结尾不要加斜杠，例如`http://localhost:5000`或者`http://yourdomain.com`

```sh
docker run -it --rm --name=infnlp -p 5000:5000 infinityfuture/infnlp:latest
```

```sh
docker run -d --name=infnlp -p 5000:5000 infinityfuture/infnlp:latest
```

### 构建后台的docker镜像

这部分只是记录，使用并不需要做这些。

HanLP相关下载，参考[HanLP](https://github.com/hankcs/HanLP)

- 下载、解压、改名、复制 `hanlp.jar` 到 `./hanlp_backend/hanlp.jar`
- 下载、解压、复制对应版本HanLP的 `data` 到 `./hanlp_backend/data`

构建docker镜像

```sh
docker build -t infinityfuture/infnlp:latest .
```